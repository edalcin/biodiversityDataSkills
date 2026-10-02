# IPT administration reference

Operator-level knowledge for installing, configuring, registering, securing, backing up and upgrading a GBIF IPT instance.
Companion files: [endpoints.md](endpoints.md) (URLs), [resources-publishing.md](resources-publishing.md) (datasets), [releases.md](releases.md) (versions), [health-checks.md](health-checks.md) (checks), [known-issues.md](known-issues.md).

Conventions: **Manual** = `https://ipt.gbif.org/manual/en/ipt/latest/<page>` (page names below, e.g. [installation](https://ipt.gbif.org/manual/en/ipt/latest/installation)). **Src** = `gbif/ipt` @ main (3.3.7-SNAPSHOT, commit 62097149). `#NNNN` = <https://github.com/gbif/ipt/issues/NNNN>. `[INFERENCE]` = not stated in source, deduced.

## Contents
1. [Requirements](#1-requirements)
2. [Installation methods](#2-installation-methods)
3. [Data directory](#3-data-directory)
4. [Initial setup wizard](#4-initial-setup-wizard)
5. [Configure IPT settings](#5-configure-ipt-settings)
6. [GBIF registration of the IPT](#6-gbif-registration-of-the-ipt)
7. [Users and roles](#7-users-and-roles)
8. [Organisations](#8-organisations)
9. [DOI accounts (DataCite)](#9-doi-accounts-datacite)
10. [Core types, extensions, vocabularies, data packages](#10-core-types-extensions-vocabularies-data-packages)
11. [Bulk publishing, background jobs](#11-bulk-publishing-background-jobs)
12. [Logging](#12-logging)
13. [Backup, move, reset](#13-backup-move-reset)
14. [Upgrading](#14-upgrading)
15. [Customization](#15-customization)
16. [Security, HTTPS, reverse proxy, outbound traffic](#16-security-https-reverse-proxy-outbound-traffic)
17. [Performance and memory](#17-performance-and-memory)
18. [Symptom to cause quick table](#18-symptom-to-cause-quick-table)
19. [Manual vs code discrepancies](#19-manual-vs-code-discrepancies)

---

## 1. Requirements
Sources: Manual [requirements](https://ipt.gbif.org/manual/en/ipt/latest/requirements), [installation](https://ipt.gbif.org/manual/en/ipt/latest/installation); Src `pom.xml`, `package/docker/Dockerfile`, `package/rpm/SPECS/ipt.spec`.

| Item | Requirement (current 3.3.x) |
|---|---|
| Java | **17** (3.3.0+ compiled for 17, `pom.xml` `java.version=17`). Older IPTs: see [releases.md](releases.md#runtime-requirements-per-version) |
| Servlet container | Servlet spec 4.0+ per manual; **Tomcat 10.1 or 11** (Jakarta Servlet 6, `jakarta.servlet-api` 6.0.0). Tomcat 8/9 **not supported since 3.3.0**. Jetty/WildFly named in manual; RPM uses `jetty-runner` |
| RAM | >= 256 MB for the app (manual); real instances need more, see [§17](#17-performance-and-memory) |
| Disk | ~250 MB app; data dir grows with data, rule of thumb **~1 KB per record** of a rich occurrence dataset; logs small |
| OS | Linux or Windows. Packages: RPM (RHEL/CentOS 8-9), APT (community, unsupported, PR [#1470](https://github.com/gbif/ipt/pull/1470)), Docker, WAR |
| Network | Stable public URL; outbound HTTPS to GBIF registry (see [§16](#16-security-https-reverse-proxy-outbound-traffic)); TLS recommended, not required |
| Browsers | MSIE unsupported since 2.5.0 ([releases.md](releases.md)) |

GBIF gives no support for OS/backup/certificate problems; "running an IPT is a commitment": back up regularly, patch quickly (Manual requirements).

## 2. Installation methods
Manual: [installation](https://ipt.gbif.org/manual/en/ipt/latest/installation), [tomcat-installation-linux](https://ipt.gbif.org/manual/en/ipt/latest/tomcat-installation-linux).

| Method | Default data dir | Port / URL | Runs as | Notes |
|---|---|---|---|---|
| **RPM** (`yum install ipt` after adding `https://packages.gbif.org/gbif.repo`) | `/var/lib/ipt` | `IPT_PORT` (default 8080), webroot `/` | system user `ipt` | systemd unit `ipt.service` runs `java -jar jetty-runner.jar --port $IPT_PORT /usr/share/java/gbif/ipt.war`; `Requires: java-headless >= 17`, `jetty-runner`. Config `/etc/sysconfig/ipt` has only `IPT_DATA_DIR`, `IPT_PORT`. `ReadWritePaths=/var/lib/ipt/`. Logs: `journalctl -u ipt` first, then `<datadir>/logs`. (Src `package/rpm/SOURCES/*`, `SPECS/ipt.spec`) |
| **WAR in Tomcat 10.1/11** | `/srv/ipt` suggested (Linux), `C:\ipt-data` (Windows) | `http://host:8080/ipt` (webapp name) | Tomcat user | Set data dir in `conf/Catalina/localhost/ipt.xml`: `<Context><Parameter name="IPT_DATA_DIR" value="/srv/ipt"/></Context>` (case-sensitive name). Multiple IPTs per server: different `*.xml`/`*.war` names **and separate data dirs** |
| **Jetty runner** | any | `--port 8080 ipt.war` | — | "very rough guide" only |
| **Docker** `gbif/ipt[:version]` | `/srv/ipt` (volume) | 8080, IPT is `ROOT` app | non-root user `tomcat` (3.3.x Dockerfile) | `docker run --detach --volume /host/data:/srv/ipt --publish 8080:8080 gbif/ipt`. Override with `-e IPT_DATA_DIR=...`. `latest` = current stable |
| **APT (Debian/Ubuntu)** | — | — | — | Community contribution, "not yet supported by the IPT developers" |

Docker image facts from Src `package/docker/Dockerfile`: base `tomcat:11.0.22-jdk17-temurin` (Manual still says "Tomcat 9 / OpenJDK 17" - stale, see [§19](#19-manual-vs-code-discrepancies)); `ENV IPT_DATA_DIR=/srv/ipt`; `VOLUME /srv/ipt`; server.xml patched `maxParameterCount` 1000 -> **10000**; `USER tomcat` (non-root since 3.3.0, [#2633](https://github.com/gbif/ipt/issues/2633)). `[INFERENCE]` a bind-mounted host data dir must be writable by the container's `tomcat` user (a system account created with `useradd -r`; uid not pinned) - otherwise "data directory is not writable" errors (see [§3](#3-data-directory)).

Linux Tomcat install: `yum install tomcat` / `apt install tomcat9`(manual text, outdated for 3.3: use a Tomcat 10.1/11 package), `systemctl enable tomcat`. After deploy the setup page appears at the URL; if not, read `catalina.out` (Manual installation).

## 3. Data directory
Manual: [installation](https://ipt.gbif.org/manual/en/ipt/latest/installation#data-directory), [initial-setup](https://ipt.gbif.org/manual/en/ipt/latest/initial-setup), [faq](https://ipt.gbif.org/manual/en/ipt/latest/faq). Src `config/IPTModule.java`, `config/DataDir.java`, `config/AppConfig.java`.

**Everything lives here**: config, users, registration, resources, logs. Losing it = losing the IPT.

**Location resolution order** (Src `IPTModule.provideDataDir`):
1. Servlet context parameter `IPT_DATA_DIR` (Tomcat `ipt.xml`).
2. OS environment variable `IPT_DATA_DIR` (Docker/RPM `EnvironmentFile`).
3. File `WEB-INF/datadir.location` inside the exploded webapp (written by the setup wizard). To change: edit/remove that file, restart.
At every startup the `tmp/` dir is emptied (`clearTmp`).

**Layout** (Src `DataDir.java`, `AppConfig.java`, `ConfigManagerImpl.java`, `*ManagerImpl`):

| Path | Content |
|---|---|
| `config/ipt.properties` | User settings (see [§5](#5-configure-ipt-settings)); `dev.*` keys are never persisted |
| `config/users.xml` | Accounts; passwords BCrypt-hashed since 2.5.6 |
| `config/registration2.xml` | IPT registration, organisations, DOI account (passwords encrypted; migrated once from legacy `registration.xml`) |
| `config/.gbifreg` | One word `PRODUCTION` or `DEVELOPMENT`: the **registry lock** (test vs production mode) - never edit |
| `config/.extensions/`, `.vocabularies/`, `.dataPackages/` | Installed extension / vocabulary / data-schema definitions (cached from rs.gbif.org) |
| `config/.uiSettings/` | `ipt-color-scheme.properties`, `logos/logo.*` (UI Management) |
| `resources/<shortname>/` | One dir per resource: `resource.xml` (config, mappings, version history), `eml.xml`, `eml-<v>.xml`, `dwca.zip`, `dwca-<v>.zip`, `<shortname>-<v>.rtf`, `publication.log`, `inferredMetadata.xml`, `sources/` (uploaded files + `<source>.log`), logo; Frictionless resources add `datapackage.json` / `metadata.yaml` |
| `logs/` | `admin.log`, `debug.log` (+ rotated `*.log.N`) |
| `tmp/` | Scratch; wiped on start |

`DataDir.isConfigured()` = directory exists and is **non-empty**. An existing dir without `config/` is rejected ("exists already and is no IPT data dir"). An empty/new dir is initialised with default `config/ipt.properties`.

Rules: absolute path only; IPT user needs read/write on it and all children (`resources/*` checked at startup and reported as startup errors); never `/tmp`; on SELinux/systemd-sandboxed hosts file ownership is not enough (e.g. `ReadWritePaths=` override, FAQ sandboxing entry). Fix recipe from FAQ: `chown -R tomcatuser:tomcatgroup <dir>`; `chmod -R 755 <dir>`. Symptom also seen as `RollingFileManager ... unable to create manager ... debug.log` ([#1726](https://github.com/gbif/ipt/issues/1726)).

Startup without a configured data dir used to crash the context ([#2968](https://github.com/gbif/ipt/issues/2968), fixed for 3.3.0): the wizard should appear instead.

## 4. Initial setup wizard
Manual: [initial-setup](https://ipt.gbif.org/manual/en/ipt/latest/initial-setup). Src `config/SetupAction.java`.

| Step | What | Gotchas |
|---|---|---|
| 0/1 Data directory | Only if not preconfigured. Existing same-version data dir can be reused, skipping steps 2-3 | Not writable -> FAQ permissions |
| 2 Administrator | Email, names, password (min 4 chars, **not recoverable**) | At least one Admin must always exist |
| 3 **IPT mode** | **Test** (`DEVELOPMENT`: UAT registry, never indexed, test DOI prefix) vs **Production** (live registry, indexed, DOIs permanent) | **Final.** Locked into `config/.gbifreg`; `AppConfig.setRegistryType` throws `DATADIR_ALREADY_REGISTERED` on change. Switching = new IPT; transfer resources via zipped resource folder ([resources-publishing.md](resources-publishing.md#create-and-import)) (FAQ) |
| 4 Public URL (+ optional institutional proxy) | Base URL auto-detected; wizard checks it is reachable | `localhost` URL = cannot register IPT, cannot associate organisation, resources not publicly accessible. Check uses HEAD since 3.3.5 ([#3092](https://github.com/gbif/ipt/issues/3092)) |
| 5 Done | Continue to Administration | Before any resource: verify settings, register IPT, add organisation |

Good order for a new production instance (Manual installation): web server + TLS first, then IPT, so the Public URL is final from the start.

## 5. Configure IPT settings
Manual: [administration#configure-ipt-settings](https://ipt.gbif.org/manual/en/ipt/latest/administration#configure-ipt-settings). Src `config/AppConfig.java`, `configDefault/ipt.properties`, `application.properties`.

| UI field | `config/ipt.properties` key | Notes |
|---|---|---|
| Public URL | `ipt.baseURL` | Colons escaped: `ipt.baseURL=http\://example.org\:7001/ipt`. UI saves only if URL answers; if the new URL is not yet live: stop IPT, edit the file, start, then **Edit GBIF registration -> update** so the registry learns the new URL ("run an update each time the public URL changes") |
| Default language | `defaultLocale` | UI languages: en, fr, es, pt, ja, zh, ru (Src `AppConfig.IPT_SUPPORTED_LANGUAGES`) |
| IPT administrator email | `admin.email` | Shown on login page; falls back to first admin's email |
| Institutional proxy URL | `proxy` | `http://proxy.example.org:8080`; tested on save against the registry URL (4 s timeout), reverted if it fails (`ConfigManagerImpl.changeProxy`) |
| SMTP host / port / user / password / STARTTLS | `mail.smtp.host`, `mail.smtp.port` (default 25), `mail.smtp.username`, `mail.smtp.password`, `mail.smtp.starttls.enable` | Added 3.3.3 ([releases.md](releases.md)). Used only for auto-publication failure mails; empty host disables |
| Google Analytics key | `analytics.key` | |
| Debugging mode | `debug=true` | Logs verbosely to `logs/debug.log`; swaps log4j2 config (`log4j2.xml` vs `log4j2-production.xml`) |
| Archival mode | `archivalMode` | **true in default new data-dir template**; absent = false. When on, every version's `dwca-<v>.zip`, `eml-<v>.xml`, `.rtf` is kept (version history downloadable). **Required to activate a DOI account.** Watch disk |
| Number of archived versions | `archivalLimit` | Keeps last N; older removed (`cleanArchiveVersions`) |
| Server location | `location.lat`, `location.lon` | Shown on GBIF map of IPTs |
| Logo redirect URL | `logoRedirectUrl` | |
| (not in UI) session timeout | `session.timeout` | See [§19](#19-manual-vs-code-discrepancies) for the unit quirk |
| (advanced) extra cores | `ipt.core_rowTypes`, `ipt.core_idTerms` | Pipe-separated, colons escaped; see [§10](#10-core-types-extensions-vocabularies-data-packages) |
| (dev, read-only) | `dev.registry.url` `https://gbrds.gbif.org`, `dev.registrydev.url` `https://gbrds.gbif-uat.org`, `dev.portal.url`, `dev.datacite.url` `https://api.datacite.org` / `dev.datacitedev.url` `https://api.test.datacite.org`, `dev.maxthreads=6` | In `application.properties`, **not overridable via `ipt.properties`** (stripped on save) |

Other Administration menu items (Manual administration; Src `struts-admin.xml` action names): **Publish all resources** (`publishAll`, [§11](#11-bulk-publishing-background-jobs)), Users (`users`), GBIF registration (`registration`), Organisations (`organisations`), Core types & extensions (`extensions`), Data packages (`dataPackages`), UI Management (`uiManagement`), View logs (`logs`/`logfile`), bulk report (`bulkReport`), `publication-report(s)` API.

## 6. GBIF registration of the IPT
Manual: [administration#configure-gbif-registration-options](https://ipt.gbif.org/manual/en/ipt/latest/administration#configure-gbif-registration-options), [faq](https://ipt.gbif.org/manual/en/ipt/latest/faq).

Prerequisites: IPT public URL reachable by GBIF, **organisation already registered in the GBIF Registry** (else Help Desk / `https://www.gbif.org/become-a-publisher`), and its **shared token** (from the organisation's registered contact).

| Mode | Registry | Portal | DOI API |
|---|---|---|---|
| Test | `https://gbrds.gbif-uat.org` | `https://www.gbif-uat.org` | `https://api.test.datacite.org` (test prefix `10.21373`) |
| Production | `https://gbrds.gbif.org` | `https://www.gbif.org` | `https://api.datacite.org` |

Steps: (1) **Validate** (checks internet, public/proxy URL, firewall, registry reachability). (2) Form: hosting **Organisation**, **Organisation's shared token**, **Alias**, **Can publish resources?**, IPT **title**, **description**, **contact name/email** (an Admin who knows the install), **IPT password** (the credential used later to edit this IPT's entry in the Registry; keep it - encrypted in `registration2.xml`). (3) Save -> Organisations page unlocks.

Afterwards:
- **Edit GBIF registration** (`updateRegistration`): re-syncs IPT + all registered resources with the Registry. Run after any public-URL change; can update title/description/contact. **Cannot change hosting organisation** - Help Desk (`helpdesk@gbif.org`), or manual edit of `config/registration2.xml` (`<registry><hostingOrganisation><key>` and `<ipt><organisationKey>`) + restart + update registration (FAQ). Network and organisation-token edit views exist (`changeTokens`, `associateWithNetwork`). Default IPT network: resources auto-join it on registration (`OverviewAction.registerResource`).
- Registered resources' metadata re-pushed on every publish and by **Publish all resources** (also calls `updateIpt`).
- Resources: see [resources-publishing.md](resources-publishing.md#registration-with-gbif).

## 7. Users and roles
Manual: [administration#configure-user-accounts](https://ipt.gbif.org/manual/en/ipt/latest/administration#configure-user-accounts). Src `model/User.java` (`Role { User, Manager, Publisher, Admin }`), `validation/UserValidator.java`.

| UI role | Code | Can |
|---|---|---|
| Admin | `Admin` | Everything; implicit manager of all resources; sees Administration menu |
| Manager **with** registration rights | `Publisher` (`hasRegistrationRights()`) | Create/edit/publish own or assigned resources **and register / update registration** with GBIF; reserve/manage DOIs |
| Manager **without** registration rights | `Manager` | Create/edit/publish resources they manage. **Cannot** register; **cannot publish** a resource that is registered or has a reserved/registered DOI (UI shows the publish button as blocked) |
| User | `User` | Log in, view only |

Rules (Manual): email = login id, immutable (to change: create new user, delete old); password >= 4 chars, unrecoverable, reset = admin generates new one (**IPT does not notify the user**; optional email-credentials link, URL-encoded password since 3.3.0 [#2981](https://github.com/gbif/ipt/issues/2981)). Cannot delete: yourself; the last Admin; the last Admin/Manager of any resource; a user who **created** a resource (downgrade to User instead). Since 2.5.6 passwords are BCrypt; **no downgrade below 2.5.6** ([releases.md](releases.md)). Lost admin password: edit `config/users.xml`, replace the Admin's `password` with the reset hash given in the [FAQ "How do I reset the admin password?"](https://ipt.gbif.org/manual/en/ipt/latest/faq), restart, log in, change immediately (the FAQ publishes a shared throw-away credential; not repeated here).

## 8. Organisations
Manual: [administration#configure-organizations](https://ipt.gbif.org/manual/en/ipt/latest/administration#configure-organizations). Src `action/admin/OrganisationsAction.java`, `validation/OrganisationSupport.java`.

Available only after IPT registration. Each organisation: GBIF key (picked from Registry list), **shared token** (validated against Registry on save), alias, **Can publish resources** (only these appear in a resource's publishing-organisation list), optional DOI account (§9). A DwC-A resource with **no publishing organisation** cannot be published (UI shows the blocked publish button), and the placeholder "No organisation" (`Constants.DEFAULT_ORG_KEY 625a5522-1886-4998-be46-52c66dd566c9`) **cannot be used to register** a resource (`OverviewAction.hasValidPublishingOrganisation`). `organisationsSynchronize` refreshes names/aliases from the Registry. Changing a resource's publishing organisation: Manual FAQ; allowed (with warning) on the overview Publication section since 3.2.0 ([#2900](https://github.com/gbif/ipt/issues/2900)), then Help Desk must update the Registry for registered datasets.

## 9. DOI accounts (DataCite)
Manual: [doi-workflow](https://ipt.gbif.org/manual/en/ipt/latest/doi-workflow), [citation](https://ipt.gbif.org/manual/en/ipt/latest/citation), [versioning](https://ipt.gbif.org/manual/en/ipt/latest/versioning), [datacite-mappings](https://ipt.gbif.org/manual/en/ipt/latest/datacite-mappings). Very few publishers use this; **by default GBIF assigns `10.15468/...` DOIs to registered datasets** and an external DOI can simply be entered as citation identifier.

Admin set-up (Src `OrganisationSupport.validate`):
1. **Archival mode must be on** (activation fails otherwise).
2. Organisation edit page: registration agency **DataCite** (only supported), account **username**, **password**, **DOI prefix/shoulder** (must start with `10.`), tick **Account activated** (only one account active at a time).
3. Mode rules: test IPT -> use test prefix `10.21373` (warning otherwise); production -> test prefix **rejected**.
4. On save the IPT proves the account by reserving then deleting a test DOI; failure -> "can't authenticate". Account must be allowed to mint under the IPT's domain (target URL) or registrations fail.
Until an account is active, DOI buttons are hidden on resources; publishing/deleting a DOI-bearing resource without an active account is blocked (`manage.overview.doi.operation.failed.noAccount`).

DOI states (`IdentifierStatus`): `UNRESERVED`, `PUBLIC_PENDING_PUBLICATION` (reserved), `PUBLIC` (registered), `UNAVAILABLE` (deactivated). Reserved + public resource -> next publish = new **major** version and DOI registered. Registered DOIs cannot be deleted; only deleting the resource deactivates (tombstone page); undelete reactivates (last published version). Resource-side detail: [resources-publishing.md](resources-publishing.md#versioning-and-dois). IPT 2.4.0 removed EZID support ([releases.md](releases.md)).

## 10. Core types, extensions, vocabularies, data packages
Manual: [administration#configure-core-types-and-extensions](https://ipt.gbif.org/manual/en/ipt/latest/administration#configure-core-types-and-extensions), [core](https://ipt.gbif.org/manual/en/ipt/latest/core), [license](https://ipt.gbif.org/manual/en/ipt/latest/license), [user-id](https://ipt.gbif.org/manual/en/ipt/latest/user-id), [database-connection](https://ipt.gbif.org/manual/en/ipt/latest/database-connection).

| Task | How / rule |
|---|---|
| Core types | Always built in: Occurrence, Taxon, Event (`AppConfig.DEFAULT_CORE_ROW_TYPES`). Add custom: `ipt.core_rowTypes=http\://rs.tdwg.org/dwc/terms/MaterialSample` + `ipt.core_idTerms=http\://rs.tdwg.org/dwc/terms/materialSampleID` (pipe-separated, equal counts, else both ignored with error "Invalid configuration"), restart, then install the extension of that rowType |
| Install extension | Administration -> Core types & extensions -> **Install** (fetched from `rs.gbif.org` via registry `/registry/extensions.json`) |
| Remove | Blocked while any resource maps it (lists the resources) |
| Update | **Update** button appears when a newer issue date exists (`ExtensionMonitor` re-checks every **24 h**). Deprecated-term mappings are removed; replaced terms auto-remapped. **Republish affected resources afterwards** |
| Synchronize vocabularies | **Synchronize** button refreshes controlled vocabularies; empty-`issued` vocabularies fixed in 2.5.0/3.0.5 ([#1619](https://github.com/gbif/ipt/issues/1619), [#2439](https://github.com/gbif/ipt/issues/2439)); "Synchronize does nothing" fixed in 3.2.0 ([#2832](https://github.com/gbif/ipt/issues/2832)) |
| Data packages (3.0+) | Administration -> Data packages. `SupportedDataPackageType`: **Camtrap DP 1.0**, **ColDP 1.1** (prod). Schemas cached in `config/.dataPackages/`; DwC-DP work in progress (milestone "DwC-DP") |
| After upgrade | "Admin should update all installed cores and extensions" (Manual release-notes) |
| New licence | Edit `WEB-INF/classes/org/gbif/metadata/eml/licenses.properties`: `license.name.<p>=...` + `license.text.<p>=...<a href="url">name</a>...`; overwritten on upgrade; datasets with non-GBIF licences cannot be registered |
| New user-id directory | `UserDirectories.properties` (same folder); key = value = URL with escaped colon in key; also overwritten on upgrade. ROR added to directories in 3.3.3 |
| New JDBC driver | Copy jar to `WEB-INF/lib`, add 4 keys to `WEB-INF/classes/jdbc.properties` (`<p>.title/.driver/.url/.limitType`, `url` placeholders `{host}` `{database}`, `limitType` = `LIMIT`/`TOP`/`ROWNUM`); exploded WAR only |

Bundled JDBC (Src `jdbc.properties`): MySQL (`com.mysql.cj.jdbc.Driver`), PostgreSQL, Sybase (jTDS), MS SQL Server (`encrypt=false` in default URL), Oracle (`jdbc:oracle:thin:@{host}:{database}`), **DuckDB** (3.3.0+, file path as `{database}`; not in manual). Manual database-connection page lists only the first five.

## 11. Bulk publishing, background jobs
Manual: [administration#publish-all-resources](https://ipt.gbif.org/manual/en/ipt/latest/administration#publish-all-resources). Src `action/admin/PublishAllResourcesAction.java`, `config/PublishingMonitor.java`, `config/ExtensionMonitor.java`.

- **Publish all resources** first calls `registryManager.updateIpt` + updates registered resources' metadata, then publishes in a mode: *all*, *selected*, *excluded*, *changed* (only if data/metadata changed). Selection/status/log UI added 3.2.0 ([#2501](https://github.com/gbif/ipt/issues/2501), [#2728](https://github.com/gbif/ipt/issues/2728)); `bulkReport` page.
- **PublishingMonitor** (thread, polls every **10 s**): publishes resources whose `nextPublished` is past; applies make-public dates; max parallel archive builds = `dev.maxthreads` (6 in `application.properties`; code fallback 3). Failure handling: retry cooldown **3 min**; after **3 failures** the resource is skipped until someone publishes it manually (counter is in memory - cleared by IPT restart or manual publish). Details: [resources-publishing.md](resources-publishing.md#auto-publication).
- **ExtensionMonitor** (24 h): flags installed extensions with newer registry versions.

## 12. Logging
Manual: [administration#view-ipt-logs](https://ipt.gbif.org/manual/en/ipt/latest/administration#view-ipt-logs). Src `config/LoggingConfiguration.java`, `LoggingConfigFactory.java`.

| File | Content | Rotation |
|---|---|---|
| `logs/admin.log` | `org.gbif` loggers at **WARN+** | new file on startup and at 10 MB (`.log.%i`) |
| `logs/debug.log` | Everything (root DEBUG, noisy libs set to ERROR) | same |
Format `LEVEL dd-MMM-yyyy HH:mm:ss [logger] - message`. Admin UI: View logs (admin.log) with link to the complete log; plain file download at `/admin/logfile.do?log=admin|debug` (see [endpoints.md](endpoints.md)). **Debug mode** setting toggles which log4j2 template is used. Per-resource: `resources/<r>/publication.log`, `resources/<r>/sources/<source>.log`. Rotation bugs: [#1659](https://github.com/gbif/ipt/issues/1659), [#2942](https://github.com/gbif/ipt/issues/2942) (fixed 3.3.0). Container/RPM first lines go to stdout/journal before the data dir logger starts.

## 13. Backup, move, reset
Manual: [installation](https://ipt.gbif.org/manual/en/ipt/latest/installation), [faq](https://ipt.gbif.org/manual/en/ipt/latest/faq), [release-notes](https://ipt.gbif.org/manual/en/ipt/latest/release-notes).

- **Backup = the data directory** (scheduled, off-host; GBIF hosting-centre criteria require it). Keep ownership/permissions when restoring. Also back up customisations that live in the webapp dir (§15).
- **Move to another server**: stop IPT, copy whole data dir preserving permissions, install IPT there, point it at the copy. Public URL change -> §5 + update registration.
- **Move one resource** between IPTs: copy `resources/<shortname>/` into the target's `resources/`, restart the target, publish there ("updates the endpoint"). Registered resources keep their Registry key but the Registry endpoint changes only after a publish/update on the new IPT. Cross-instance copy of config only: upload zipped resource folder ([resources-publishing.md](resources-publishing.md#create-and-import)).
- **Test -> production**: not possible in place; new IPT + import zipped resource folders (FAQ).
- **Disk full**: `Caused by: java.io.IOException: No space left on device` in a publication log = data-dir partition full (FAQ). Archival mode is the usual culprit.

## 14. Upgrading
Manual: [release-notes](https://ipt.gbif.org/manual/en/ipt/latest/release-notes). Version-specific notes: [releases.md](releases.md).

1. **Back up the data directory** and customisations. 2. Check [requirements](#1-requirements) (Java/Tomcat!) and OS patches. 3. By method:
 - *RPM*: `yum update ipt`; pre-release `yum install --enablerepo=gbif-testing ipt`; rollback `yum downgrade ipt-<ver>`.
 - *WAR*: replace `ipt.war` **keeping the same name** while Tomcat runs; if replaced while stopped, delete the expanded `webapps/ipt/` dir so it re-expands; if data dir is not in `ipt.xml`, open the IPT and re-enter it on the setup page; reapply custom CSS/images. Footer shows the new version (restart Tomcat if old version still shown).
 - *Docker*: pull/tag new image (`latest` = stable), same volume.
4. Post-upgrade: warnings "some resources failed to load" = old resources missing now-required metadata (republish/fix metadata); **update all cores and extensions**; republish affected resources.
Pitfalls: no downgrade past 2.5.6 (password format); 3.3.0 needs Java 17 + Tomcat 10.1/11 or the webapp will not start; 3.3.0 could not read some old `resource.xml` (`CannotResolveClassException`, resources vanish) until 3.3.1 ([#3016](https://github.com/gbif/ipt/issues/3016), [#3021](https://github.com/gbif/ipt/issues/3021)); `Struts 7.2.*` start failure fixed 3.3.4 ([#3116](https://github.com/gbif/ipt/issues/3116)).

## 15. Customization
Manual: [customization](https://ipt.gbif.org/manual/en/ipt/latest/customization). 
- **UI Management** (2.6.0+, Admin): logo + colour scheme, stored in `config/.uiSettings/` - survives upgrades (preferred).
- `custom.css` in `webapps/ipt/styles/` (servlet container only; broken in 2.5.0, [#1634](https://github.com/gbif/ipt/issues/1634)); overwritten by every upgrade -> back up and reapply. Docker/RPM: override via proxy or custom image (Dockerfile comments show `RUN curl ... images/` and `perl -pi` on `menu.ftl`).
- Custom FreeMarker templates can be loaded from the data dir (`DataDirTemplateLoader` in Src `IPTModule.provideFreemarker`, `[INFERENCE]` for exact override paths - template names under `WEB-INF/pages/`).
- Static `/media`, `/icons` can be served by the front proxy (ipt.gbif.org config).

## 16. Security, HTTPS, reverse proxy, outbound traffic
Manual: [installation#opening-the-ipt-to-the-internet](https://ipt.gbif.org/manual/en/ipt/latest/installation#opening-the-ipt-to-the-internet), [faq](https://ipt.gbif.org/manual/en/ipt/latest/faq).

- Run behind Apache HTTPD (`mod_proxy`) or nginx with TLS (LetsEncrypt). Essential header: `X-Forwarded-Proto https` (Apache `RequestHeader set X-Forwarded-Proto "https"`; nginx `proxy_set_header X-Forwarded-Proto https; proxy_set_header Host $host;`), `ProxyPreserveHost On`. Without it: mixed-content/JS over http ([#1589](https://github.com/gbif/ipt/issues/1589)), wrong MANAGE/ADMIN links ([#1878](https://github.com/gbif/ipt/issues/1878)), setup failures under HTTPS + sub-path ([#1652](https://github.com/gbif/ipt/issues/1652)). Sub-path deployments: proxy `/ipt/` to `http://localhost:8080/ipt/`.
- **Certificate chain must be complete**: GBIF's harvesters are stricter than browsers; "unable to get local issuer certificate"/"chain incomplete" -> GBIF cannot fetch DwC-A. Test with `curl https://ipt.example.org`, SSL Labs, whatsmychaincert.com (FAQ).
- Changing http -> https = change Public URL ([§5](#5-configure-ipt-settings)) + update registration.
- **Outbound** (FAQ): test mode -> `https://gbrds.gbif-uat.org`, `https://tools.gbif.org`; production -> `https://gbrds.gbif.org`; always `http://rs.gbif.org` (extensions/vocabs, plain HTTP); optional vocab sources `raw.githubusercontent.com`, `eol.org`; DataCite API if DOIs. Allow 80/443 to GBIF `130.225.43.0/24`. Pre-2.3.4 used HTTP to the registries. Optional Google Analytics.
- Hardening facts from Src: session cookie is HTTP-only (`web.xml`); CSRF token expires 15 min with page-refresh keep-alive (`AppConfig`); upload cap `struts.multipart.maxSize=10000000000` (~10 GB); passwords BCrypt; registry passwords encrypted in `registration2.xml`. Security fixes by version (Struts, Log4Shell, jQuery UI, Tomcat CVEs): [releases.md](releases.md); keep Tomcat >= 11.0.22 ([#3076](https://github.com/gbif/ipt/issues/3076)).
- Source database credentials are stored in each `resource.xml` (encrypted converter `PasswordEncrypter`); use a read-only DB account.

## 17. Performance and memory
Manual: [faq](https://ipt.gbif.org/manual/en/ipt/latest/faq#my-gbif-ipt-instance-is-slow-what-can-i-do-to-improve-performance).
- Tomcat default heap is small: with >= 4 GB RAM give the JVM ~2 GB, e.g. `export CATALINA_OPTS="-Xmx2048M"` (RPM/Jetty: add to the unit's `java` command `[INFERENCE]`).
- Large source files: upload limit 10 GB; beyond that compress (zip/gzip), use a DB source, URL source, or split files (concatenated in mapping order). No size limit for the published DwC-A.
- Parallel archive builds: `dev.maxthreads` (6). Excel files cause OOM/crashes at scale ([#1795](https://github.com/gbif/ipt/issues/1795), [#2030](https://github.com/gbif/ipt/issues/2030)) - prefer CSV/TSV or DB.
- Docker: Tomcat `maxParameterCount=10000` (many mapped fields / large form posts).
- DB sources: JDBC fetch size 10 for publishing, 5 s login timeout (`SourceManagerImpl`); slow SQL = slow publish.
- Home/manage resource tables are server-side paged since 2.7.0 (better with hundreds of resources).

## 18. Symptom to cause quick table

| Symptom | Likely cause / check |
|---|---|
| IPT shows setup wizard again after restart | data dir not found: `IPT_DATA_DIR` (context/env) or `WEB-INF/datadir.location` lost (WAR redeployed); dir empty |
| "Data directory not writable" / `RollingFileManager` error | ownership, SELinux/systemd sandbox, Windows read-only flag, Docker non-root volume |
| Startup banner "Resources directory cannot be read/written" | permissions on `resources/` or a resource subdir (`ConfigManagerImpl.checkResourcesDirAtStartup`) |
| Can't register IPT / pick organisation | Public URL is localhost/private; firewall; wrong proxy; registry unreachable; wrong shared token |
| Resources vanish after upgrade | 3.3.0 `resource.xml` parse problem (upgrade to >= 3.3.1) or missing required metadata (republish) |
| Webapp 404 / deploy fails after 3.3 upgrade | Tomcat 9 or Java < 17 |
| Auto-publication stopped | 3 failures reached ([§11](#11-bulk-publishing-background-jobs)); fix cause and publish manually; check SMTP if mails expected |
| Visibility change not visible | visibility is a *pending* change applied at next publish ([#2971](https://github.com/gbif/ipt/issues/2971)) |
| DOI buttons missing | no activated DataCite account, archival mode off, or user lacks registration rights |
| Old sources lost mappings on re-upload | number of columns changed -> IPT warns; fix mappings |

## 19. Manual vs code discrepancies
| Topic | Manual says | Code / repo says |
|---|---|---|
| Docker base image | "Tomcat 9 / OpenJDK 17" ([installation](https://ipt.gbif.org/manual/en/ipt/latest/installation)); `package/docker/README.adoc`: "Tomcat 8.5 / OpenJDK 8" | `Dockerfile`: `tomcat:11.0.22-jdk17-temurin` |
| Tomcat install hint | `apt install tomcat9` ([tomcat-installation-linux](https://ipt.gbif.org/manual/en/ipt/latest/tomcat-installation-linux)) | 3.3+ needs Tomcat 10.1/11 |
| Session timeout | template comment "(in seconds)", value `3600` | `AppConfig.getSessionTimeout()` multiplies the property by 60 (so a literal `3600` -> 216 000 s); built-in default if unset = 3600 s. `[INFERENCE]` set it in minutes |
| Required metadata | [resource-metadata](https://ipt.gbif.org/manual/en/ipt/latest/resource-metadata) lists "metadata provider(s)" as required | `EmlValidator` only validates metadata providers if present (optional since 2.7.0, [#1906](https://github.com/gbif/ipt/issues/1906)); see [resources-publishing.md](resources-publishing.md#metadata-that-blocks-publication) |
| Licences | Manual: CC0 / CC-BY / CC-BY-NC | `Constants.GBIF_SUPPORTED_LICENSES` URL set also contains ODC-By and PDDL URLs; `GBIF_SUPPORTED_LICENSES_CODES` = CC0-1.0, CC-BY-4.0, CC-BY-NC-4.0 |
| JDBC list | five systems | `jdbc.properties` also has DuckDB |
| `Publish all resources` | described as "publishes ALL" | code offers all/selected/excluded/changed modes |
