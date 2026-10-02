# IPT releases and version-aware operations

What each IPT version changed, what it needs to run, and what an operator must do when an instance is old.
Companion files: [administration.md](administration.md) (upgrade procedure), [resources-publishing.md](resources-publishing.md), [endpoints.md](endpoints.md), [known-issues.md](known-issues.md), [health-checks.md](health-checks.md).

Sources: Manual [releases](https://ipt.gbif.org/manual/en/ipt/latest/releases) and [release-notes](https://ipt.gbif.org/manual/en/ipt/latest/release-notes) (the "latest" manual is 3.3.x; older notes read from git tags `ipt-<ver>` of `docs/en/modules/ROOT/pages/{release-notes,requirements,installation}.adoc` and `pom.xml`); GitHub milestones `https://github.com/gbif/ipt/milestone/<n>` (numbers in the table); issue links `#NNNN` = <https://github.com/gbif/ipt/issues/NNNN>. `[INFERENCE]` = deduced.

## Contents
1. [Support position](#support-position)
2. [Runtime requirements per version](#runtime-requirements-per-version)
3. [One-way doors and must-know upgrade rules](#one-way-doors-and-must-know-upgrade-rules)
4. [Security-driven releases](#security-driven-releases)
5. [Version history 2.5 to 3.3](#version-history-25-to-33)
6. [Version history before 2.5](#version-history-before-25)
7. [Library baseline per version](#library-baseline-per-version)
8. [Operator playbook for an old instance](#operator-playbook-for-an-old-instance)
9. [Identifying an instance's version](#identifying-an-instances-version)

---

## Support position
- **Latest stable: 3.3.6** (Manual releases: "September 2026"; milestone 80 closed 2026-09-10). Source tree is **3.3.7-SNAPSHOT**; milestone 81 is open (4 open / 4 closed) and the Manual says "No release date has been set for the next release".
- Policy stated in the Manual: "Minor issues and security issues will be addressed in patch releases" of the current line. There is **no published end-of-life schedule** for older IPT versions; the practical rule is: only the newest release is maintained, security fixes land there, and the Manual ships a version selector (older manual versions may not be translated).
- Hard end-of-support facts that *are* documented: Tomcat 7 dropped at IPT 3.0.0, Tomcat 8 dropped (documented) at 3.2.0 and in practice unusable at 3.3.0, **Tomcat 9 and earlier unsupported from 3.3.0**, Java 8/9 dropped at 3.0.0, **Java 11 dropped at 3.3.0**, MSIE dropped at 2.5.0, EZID DOIs dropped at 2.4.0.
- Every GBIF "hosting centre" is expected to back up and patch promptly (Manual requirements/release-notes).

## Runtime requirements per version
Manual `requirements`/`installation` at each tag; `pom.xml` at each tag.

| IPT line | Java | Servlet container (documented) | Servlet API | Docker base (documented) | RPM target |
|---|---|---|---|---|---|
| 2.5.x - 2.6.x | 8 or 9 | Tomcat **7, 8 or 9** | javax 3.0.1 | Tomcat 8.5 / OpenJDK 8 / Debian | RHEL/CentOS 7 |
| 2.7.x | 8 or 9 | Tomcat **8.5 or 9** (Servlet 3.0/3.1/4.0) | javax 3.0.1 | Tomcat 8.5 / OpenJDK 8 | RHEL/CentOS 7 (8 "being developed", [#1646](https://github.com/gbif/ipt/issues/1646)) |
| 3.0.x | **11 and 17** | Tomcat **8 and 9** (min 8; "IPT 3.0.0 requires Tomcat 8 or 9. Tomcat 7 is not supported") | javax 3.0.1 | Tomcat 9 / OpenJDK 17 | RHEL/CentOS 8-9 |
| 3.1.x | 11 and 17 | Tomcat **9** (8 "minimum, likely to change") | javax 3.0.1 | Tomcat 9 / OpenJDK 17 | RHEL/CentOS 8-9 |
| 3.2.x | 11 and 17 (compiled for 11, Struts 6.8) | Tomcat **9**; "Tomcat 10 and later not supported; Tomcat 8 not supported" | javax 3.1.0 | Tomcat 9 / OpenJDK 17 | RHEL/CentOS 8-9 |
| **3.3.x** | **17** | **Tomcat 10.1 or 11** ("Tomcat 8/9 are not supported anymore") | **jakarta 6.0** | Tomcat 11 / JDK 17 Temurin (Dockerfile; Manual text still says Tomcat 9 - stale) | RHEL 8-9, `java-headless >= 17`, jetty-runner |

Notes: the 3.3.0 **git tag's own manual pages still said Tomcat 9** - the Release Notes ("IPT 3.3.0 requires Java 17 / Tomcat 10.1 or 11") are authoritative. Documented disk footprint of the app grew from ~100 MB (manual at 2.5.8 - 3.0.6) to ~250 MB (manual at 3.2.3 and later).

## One-way doors and must-know upgrade rules

| Rule | Detail / source |
|---|---|
| **Backup the data directory first**, always | Manual release-notes; needed because several upgrades are irreversible |
| **No downgrade after 2.5.6** | "changes the way user passwords are stored... not possible to downgrade" (2.5.6; BCrypt, [#1460](https://github.com/gbif/ipt/issues/1460)) |
| Use **>= 2.5.2** within 2.5.x | 2.5.0/2.5.1 had metadata editing/DB-source bugs; 2.5.1 fixed connecting to database sources |
| 2.5.0 upgraded JDBC drivers | "check your database configurations still work" (MySQL, PostgreSQL, MS SQL, Sybase, Oracle) |
| 2.5.0 data dir via container | `IPT_DATA_DIR` context parameter introduced; set once to avoid re-entering at every upgrade ([administration.md §3](administration.md#3-data-directory)) |
| 2.5.0 `custom.css` broken | [#1634](https://github.com/gbif/ipt/issues/1634); UI Management from 2.6.0 replaces it |
| Upgrade from **< 2.4** | read the old 2.4 release notes (Manual `2.4@release-notes`) first - [INFERENCE] go via 2.4.x/2.5.x rather than jump |
| 2.6.0 | home table could show no resources (quotes in resource data) - fixed in 2.6.1 ([#1835](https://github.com/gbif/ipt/issues/1835)); Docker images >= 2.6.0 crashed the JVM on some hosts - maintainer says fixed by 2.6.3, unconfirmed by reporter `[INFERENCE]` ([#1918](https://github.com/gbif/ipt/issues/1918)) |
| 2.7.0 | new server-side resource tables; upgrade straight to >= 2.7.1 (2.7.0 home-page JS bug, [#1936](https://github.com/gbif/ipt/issues/1936)) and 2.7.2 (Spanish UI could not add resources, [#1939](https://github.com/gbif/ipt/issues/1939)) |
| 3.0.0 | adds Frictionless/Camtrap DP; Tomcat 7 dropped; Java 11+; an inferred-metadata deserialization failure could stop resources from loading - fixed in 3.0.1 ([#2337](https://github.com/gbif/ipt/issues/2337), [#2338](https://github.com/gbif/ipt/issues/2338)) so go to >= 3.0.1 |
| 3.1.0 | EML 2.2.0, new rich-text metadata inputs; expect some metadata to become *Invalid* (e.g. description < 5 chars [#2541](https://github.com/gbif/ipt/issues/2541)) and "Invalid EML during publication" ([#2561](https://github.com/gbif/ipt/issues/2561)); a Camtrap resource could not update metadata after upgrade ([#2474](https://github.com/gbif/ipt/issues/2474)); upgrade problems reported for 3.1.0 -> 3.1.5 ([#2696](https://github.com/gbif/ipt/issues/2696), fixed 3.1.6) |
| 3.2.0 | Spring replaced Guice ([#2687](https://github.com/gbif/ipt/issues/2687)); Struts 6 (pom at 3.2.3); dedicated *Publishing organisation* tab in the overview ([#1987](https://github.com/gbif/ipt/issues/1987); UI note added in 3.2.3, [#2964](https://github.com/gbif/ipt/issues/2964)); inventory API v2; bulk publication; auto-publication skip options |
| **3.3.0** | needs **Java 17 + Tomcat 10.1/11**; Docker image now **non-root**; **do not stop at 3.3.0**: some old `resource.xml` failed to load ("Cannot read resource configuration", resources disappear - `CannotResolveClassException` on `filesource`/`sqlsource`) fixed in **3.3.1** ([#3016](https://github.com/gbif/ipt/issues/3016), [#3021](https://github.com/gbif/ipt/issues/3021)); jQuery UI CVEs fixed 3.3.1; Tomcat CVEs ([#3076](https://github.com/gbif/ipt/issues/3076)) fixed in milestone 3.3.3 (Dockerfile now pins Tomcat 11.0.22 `[INFERENCE]` as the fixed baseline). Run the extension/vocabulary **Update** step afterwards |
| Any upgrade | afterwards: admin updates all installed cores & extensions; managers republish resources that fail to load or validate (Manual release-notes "Post-upgrade") |

## Security-driven releases
Instances older than these have known, published vulnerabilities:

| Version (date) | Fix |
|---|---|
| 2.3.4 (Mar 2017) | Struts S2-045 (affects all <= 2.3.3) |
| 2.3.6 (Jul 2018) | jQuery |
| 2.4.0 (Jul 2019) | Jackson, Struts |
| 2.4.1 / 2.4.2 (Sep 2020) | Struts |
| 2.5.4 (Dec 2021) | Struts + **Log4Shell CVE-2021-44228** |
| 2.5.5 (Dec 2021) | further Log4j fix (CVE-2021-45105) |
| 2.5.6 (Feb 2022) | password storage hardened (irreversible) |
| 2.6.3 (Oct 2022) | "security and bug fixes" |
| 3.2.0 (Dec 2025) | Struts vulnerability ([#2622](https://github.com/gbif/ipt/issues/2622)) |
| 3.3.1 (Apr 2026) | jQuery UI 1.12.1 CVEs ([#3027](https://github.com/gbif/ipt/issues/3027)) |
| 3.3.3 (Jun 2026) | Tomcat CVEs, vulnerable Oracle JDBC avoided ([#3064](https://github.com/gbif/ipt/issues/3064)), "security improvements" |
| 3.3.4 (Jul 2026) | FreeMarker `?interpret` removed from user-controlled content ([#3118](https://github.com/gbif/ipt/issues/3118)); Struts 7.2 start-up fix |
| 3.3.5 (Sep 2026) | "security improvements": user-input escaping ([#3166](https://github.com/gbif/ipt/issues/3166)) |
| 3.3.6 (Sep 2026) | licence-related publication fix ([#3175](https://github.com/gbif/ipt/issues/3175)) |
A third-party API key exposed in 3.3.0 requests was reported ([#3077](https://github.com/gbif/ipt/issues/3077), details private, no milestone; closed 2026-06-16) - treat >= 3.3.3 as the safe floor `[INFERENCE]`.

## Version history 2.5 to 3.3
Columns: **Date** from Manual releases; **Headline** from the Manual blurb + milestone issue titles; **MS** = GitHub milestone number; **Upgrade notes** = breaking/operational.

| Version | Date | MS | Headline changes | Upgrade / breaking notes |
|---|---|---|---|---|
| **3.3.6** | Sep 2026 | 80 | Fixes licence-related publication issue (intellectual rights link stripped after filtering) | Needs Tomcat 10.1/11 + Java 17 |
| 3.3.5 | Sep 2026 | 78 | Security: escape user input; zip upload keeps `meta.xml`/`eml.xml` names; HEAD (not GET) public-URL check; "Scheduled for publishing on" label; account first/last name editable; source delimiter editable | |
| 3.3.4 | Jul 2026 | 77 | Security (FreeMarker `?interpret` removed); fix for IPT not starting after updating to Struts 7.2.*; setup wizard cannot re-run after completion | |
| 3.3.3 | Jun 2026 | 76 | ROR identifiers; email notifications for auto-publication failure (SMTP settings); cancel redirects / no immediate re-publication; Tomcat/Oracle driver security | Configure SMTP + admin email for failure mails |
| 3.3.2 | May 2026 | 75 | Bug fixes: MSSQL SSL connection, EML v1.0 parse, field delimiter shown on source page, Camtrap mapping on test IPT | |
| 3.3.1 | Apr 2026 | 74 | Fix "Cannot read resource configuration" (sqlsource/filesource), DuckDB fixes, jQuery UI update, SQL preview fixes | **Mandatory over 3.3.0** |
| **3.3.0** | Apr 2026 | 72 | Library upgrade: **Java 17**, **Tomcat 10.1/11** (Jakarta 6), **Struts 7**; **DuckDB** source; Docker non-root; RPM for Java 17; log rotation fixed; test-mode banner; "public but not republished" banner; deletion logging; warn when deleting core mapping | **Java 17 + Tomcat 10.1/11 required**; Tomcat 8/9 unsupported. Old `resource.xml` read bug -> go to 3.3.1+ |
| 3.2.3 | Mar 2026 | 73 | Bug fixes (publishing organisation tab for cloud IPTs, Camtrap mapping, citation display) | Last release for Tomcat 9 |
| 3.2.2 | Feb 2026 | 71 | Bug fixes (extension update, NPE on archive create, basisOfRecord logging) | |
| 3.2.1 | Dec 2025 | 70 | Fixes for publication ("IPT cannot publish a new version", spurious project-contact warning) | |
| **3.2.0** | Dec 2025 | 68 | 84 issues: library upgrade (Spring replaces Guice, **Struts 6**), bulk publication with selection/status, auto-publication options (skip unchanged / skip on record drop), inventory API v2, publication time & status page, change organisation with warning, vocabulary sync fix | Tomcat 8 formally dropped; Tomcat 10 still unsupported; Java 11 or 17 |
| 3.1.7 | Jun 2025 | 69 | Camtrap DP improvements (observation level, licence scope) | |
| 3.1.6 | May 2025 | 67 | Bug fixes (DataCite JAXB, MDT licence, upgrade problem) | |
| 3.1.5 | Mar 2025 | 66 | Metadata/contributor validation, re-order creators, Camtrap | |
| 3.1.4 | Feb 2025 | 65 | Metadata fixes; CC-BY-NC recognised; validation aligned with registry | |
| 3.1.3 | Jan 2025 | 64 | Camtrap DP fixes; download EML from overview | |
| 3.1.2 | Dec 2024 | 63 | **ColDP support**; source creation/upload fixes | |
| 3.1.1 | Dec 2024 | 62 | Mapping fixes for some extensions; rowType on extensions page | |
| **3.1.0** | Oct 2024 | 60 | **EML 2.2.0**; rich-text description/introduction/acknowledgements; multiple emails per contact; related projects/awards; EML validated at publish; citation format aligned with gbif.org | Metadata may now fail validation; see [#2541](https://github.com/gbif/ipt/issues/2541), [#2561](https://github.com/gbif/ipt/issues/2561) |
| 3.0.6 | Jun 2024 | 58 | Taxonomic description, registry network warnings | |
| 3.0.5 | Jun 2024 | 57 | Vocabulary update without `issued`, Camtrap registration, URL sources, deleted resources shown on home fixed | |
| 3.0.4 | May 2024 | 56 | Metadata fixes (bounding box across dateline) | |
| 3.0.3 | Apr 2024 | 55 | Metadata and DOI issuing (own DataCite DOIs) | |
| 3.0.2 | Apr 2024 | 54 | Inferred metadata, DOI, setup | |
| 3.0.1 | Feb 2024 | 52 | Inferred metadata, missing resources, Excel; deprecated auto-publication warning | |
| **3.0.0** | Feb 2024 | 38 | 141 issues: **Frictionless Data / Camtrap DP** mappings; schema management in admin; ColDP groundwork; IPT 3 UI | **Tomcat 8 or 9 only (7 dropped); Java 11+**. New `config/.dataPackages/` |
| 2.7.7 | Nov 2023 | 50 | Maps, resource visibility, **configurable default language**, delete-from-GBIF button for registered only | Last 2.x; Java 8/9 |
| 2.7.6 | Sep 2023 | 49 | Metadata inferring, vocabulary management | |
| 2.7.5 | Aug 2023 | 47 | **Default network for IPT**, org synchronisation, copy contact to creator | |
| 2.7.4 | Jul 2023 | 46 | New file uploader, new IPT setup, **compressed URL sources**, larger uploads, avoid double registration | |
| 2.7.3 | Mar 2023 | 45 | UI fixes | |
| 2.7.2 | Feb 2023 | 44 | Fix translations bug | |
| 2.7.1 | Jan 2023 | 43 | Fix resource tables, DOI management | |
| **2.7.0** | Jan 2023 | 42 | 47 issues: **server-side resource tables** (performance with many resources), faster registration/publication, drag-and-drop metadata lists, make-public-at-date, metadata providers optional, `.gz` sources | Use 2.7.1+ |
| 2.6.3 | Oct 2022 | 41 | Security + bug fixes; build number hidden for production | Docker JVM crash fixed here per maintainer reply `[INFERENCE]`, [#1918](https://github.com/gbif/ipt/issues/1918) |
| 2.6.2 | Oct 2022 | 40 | Fix user creation | |
| 2.6.1 | Sep 2022 | 39 | Fix empty resource tables | |
| **2.6.0** | Sep 2022 | 37 | **UI Management** (colours, logo), **automatic metadata inferring** (geo/taxon/temporal), auto-publishing page, source/mapping delete buttons | Home table bug -> 2.6.1 |
| 2.5.8 | May 2022 | 35 | Fix publishing resources with DOI; build in Docker; Last-Modified header | |
| 2.5.7 | Feb 2022 | 34 | Fix DB source analyse, deleting registered resource with DOI, reset password button | |
| **2.5.6** | Feb 2022 | 33 | New DwC terms (`establishmentMeans`, `degreeOfEstablishment`, `pathway`...); **new password storage**; configurable session timeout; organisation token vs IPT password UI | **No downgrade after this**; all users should upgrade |
| 2.5.5 | Dec 2021 | 32 | Further Log4j fix; `identifiedByID`/`recordedByID` display | |
| 2.5.4 | Dec 2021 | 31 | **Struts + Log4Shell fixes** | Upgrade immediately if older |
| 2.5.3 | Dec 2021 | 30 | Spanish translation, vocabularies page bugfix | Optional |
| 2.5.2 | Nov 2021 | 29 | Metadata editing / citation bugfixes, deployment & admin improvements, authentication improvements | Use instead of 2.5.0/2.5.1 |
| 2.5.1 | Sep 2021 | 28 | Fixes DB-source connection bug of 2.5.0 | Required if you use DB sources |
| **2.5.0** | Aug 2021 | 27 | 81 issues: "double login" bug fixed, new Bootstrap UI, source via URL, upload EML/CSV/Excel directly, archived-version limit & deletion, finer auto-publish dates, troubleshooting (health) page, Markdown/HTML in EML, container-provided data dir, upgraded JDBC drivers | Drops MSIE; check DB connections; docs moved to new site |

Quick map of capabilities by introduction version (for "does this feature exist on instance X?"): URL sources 2.5.0; health page 2.5.0; archive limit 2.5.0; UI Management + metadata inference 2.6.0; server-side tables 2.7.0; compressed URL sources 2.7.4; default network 2.7.5; configurable default language 2.7.7; Camtrap DP 3.0.0; ColDP 3.1.2; EML 2.2.0 3.1.0; bulk publication + inventory v2 + skip-if-unchanged 3.2.0; DuckDB + Jakarta + Java 17 3.3.0; SMTP failure mails + ROR 3.3.3.

## Version history before 2.5
Manual releases (all "Translated into 6-7 languages"; issue counts from Manual):

| Version | Date | Note |
|---|---|---|
| 2.4.2 | Sep 2020 | Struts fix; PostgreSQL large-dataset memory improvement |
| 2.4.1 | Sep 2020 | Struts vulnerability fix |
| 2.4.0 | Jul 2019 | Jackson + Struts fixes; DataCite integration updated; **EZID removed**; default Docker data dir became `/srv/ipt` (not `/usr/local/ipt`, `package/docker/README.adoc`) |
| 2.3.6 | Jul 2018 | jQuery fix; DataCite custom-DOI issue [#1411](https://github.com/gbif/ipt/issues/1411) remained |
| 2.3.5 | Oct 2017 | 27 issues (Struts S2-045 note repeated) |
| 2.3.4 | Mar 2017 | **Struts S2-045**; HTTPS registry connections |
| 2.3.3 | Dec 2016 | 90 issues; new Excel templates (occurrence, checklist, sampling-event) |
| 2.3.2 / 2.3.1 / 2.3 | Oct / Sep / Sep 2015 | 14 / 3 / 38 issues; 2.3.2 introduced CC 4.0 licences support (applying-license page) |
| 2.2.1 / 2.2 | Apr / Mar 2015 | 2.2: citation auto-generation, DOI workflow, 3 machine-readable licences, user directories |
| 2.1 | Apr 2014 | Custom cores possible, Japanese UI |
| 2.0.5 / 2.0.4 / 2.0.3 / 2.0.2 / 2.0.1 | May 2013 / Oct 2012 / Nov 2011 / Jun 2011 / Feb 2011 | 2.0.1 first IPT 2 release; Portuguese (2.0.5), Chinese (2.0.4), French+Spanish (2.0.3) translations |

## Library baseline per version
From `pom.xml` at each tag (Struts / Log4j / Servlet):

| Tag | Struts 2 | Log4j | Servlet |
|---|---|---|---|
| 2.3.6 | 2.5.14.1 | 1.2.17 | javax 3.0.1 |
| 2.4.2 | 2.5.17 | 2.13.3 | javax 3.0.1 |
| 2.5.8 | 2.5.30 | 2.17.1 | javax 3.0.1 |
| 2.6.0 | 2.5.30 | 2.17.2 | javax 3.0.1 |
| 2.7.7 | 2.5.32 | 2.22.0 | javax 3.0.1 |
| 3.0.0 | 2.5.33 | 2.22.1 | javax 3.0.1 |
| 3.1.0 | 2.5.33 | 2.24.1 | javax 3.0.1 |
| 3.2.3 | 6.8.0 | 2.25.3 | javax 3.1.0 |
| 3.3.0 | 7.1.1 | 2.25.4 | **jakarta 6.0.0** |

## Operator playbook for an old instance

| Instance runs | Risk | Do |
|---|---|---|
| **< 2.5.4** | Log4Shell / Struts remote-code-execution class vulnerabilities | Treat as exploitable: isolate from the internet, back up, upgrade (2.5.8 on Java 8, then onward) |
| **2.5.x-2.7.x** (Java 8/9, Tomcat 7-9) | No security fixes since 2023 (last 2.x = 2.7.7, Nov 2023); no EML 2.2; `[INFERENCE]` GBIF registry/DataCite API changes are not back-ported | Plan Java 11 -> 17 and Tomcat 9 -> 10.1/11 migration; stage via 3.2.3 (Tomcat 9, Java 11/17) or jump straight to 3.3.6 on a new container; back up first |
| **3.0.x-3.1.x** | Missing many publication/metadata fixes; metadata validation differences | Upgrade to 3.2.3 or 3.3.6 |
| **3.2.x** | Works on Tomcat 9/Java 11-17 but unsupported since 3.3 line | Upgrade when Tomcat 10.1/11 + Java 17 are available |
| **3.3.0** | resource-load bug, jQuery CVEs, Tomcat CVEs, API-key exposure | Upgrade to 3.3.6 immediately |
| 3.3.1-3.3.2 | Missing notification, security fixes | Upgrade to 3.3.6 |
| **>= 3.3.3** | Residual: licence/escaping fixes in 3.3.5/3.3.6 | Keep at latest patch |

Upgrade-path checklist for jumping several lines (Docker simplest): (1) copy data dir (read-only snapshot) ; (2) start the *target* release in a new container/Tomcat against the copy; (3) watch startup logs for "Cannot read resource configuration" and startup errors; (4) update cores/extensions/vocabularies; (5) open each resource with warnings, fix metadata, republish; (6) compare `/inventory/v2/dataset` before/after ([endpoints.md](endpoints.md)); (7) cut over DNS/proxy; (8) update registration (Edit GBIF registration) so the Registry sees the new state. Never run two IPTs against the same data dir.

Things that quietly change meaning across versions:
- `session.timeout`, `archivalMode` template defaults only apply to *new* data dirs ([administration.md §5](administration.md#5-configure-ipt-settings)).
- Version numbering of data packages is integer-only (3.0+); DwC-A versions stay `major.minor`.
- Auto-publication failure counter is in-memory (restart resets it); visibility of exceeded-failure resources on the overview page improved in 3.3.7 (milestone 81, [#3194](https://github.com/gbif/ipt/issues/3194), bulk publish of such resources [#3191](https://github.com/gbif/ipt/issues/3191)) - unreleased at the time of writing.
- Docker: data dir `/srv/ipt` since 2.4.0; image user non-root since 3.3.0.
- Registry hostnames moved from `gbrds.gbif.org` (HTTP) to HTTPS in 2.3.4.

## Identifying an instance's version
- Footer of every page: `x.y.z` (formerly `x.y.z-r<git7>`; build number hidden for production instances since 2.6.3, [#1857](https://github.com/gbif/ipt/issues/1857)); logged-in users see detail on the Health/troubleshooting page (`/health.do`, see [endpoints.md](endpoints.md)).
- `dev.version` = `${project.version}-r${buildNumber}` in `application.properties`; `AppConfig.getShortVersion()` strips the `-r…` build suffix.
- Docker: image tag; RPM: `rpm -q ipt`; WAR: file name / `WEB-INF/classes/application.properties`.
- Cross-check with GBIF: the Registry lists installations; the footer-to-release mapping above gives Java/Tomcat floor.
