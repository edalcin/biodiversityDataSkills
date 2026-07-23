# Grist FAQ

Source: [support.getgrist.com/FAQ](https://support.getgrist.com/FAQ/)

## Accounts

**Multiple team sites on one login?** Yes — create more from the personal
site's top-left site switcher → "+ Create new team site". You can also add a
second Grist login as a member of a team site you own (user menu → "Manage
Users" while viewing that team site).

**Multiple login accounts in one browser?** Yes — user menu → "Add Account";
switch between all accounts/teams from the same menu.

**Update profile settings?** User menu → "Profile Settings" — name, theme
(light/dark), language, API key management.

**Change account email?** Not directly. Instead transfer ownership of
documents/team sites between two accounts you own (see below) — an
effective email change. Multiple accounts can be added and switched between
via "Add Account".

**Delete account?** Profile Settings → Privacy & Data → "Delete Account"
(permanent). To delete a *team site* instead, see Billing Account.

## Plans

**Why multiple sites?** Every user gets a free **personal site**
(`docs.getgrist.com`, named `@you`); each doc there allows up to 2 free
guests. Docs others share with you appear under `@TheirName` workspaces.
Team sites are separate, paid-per-member spaces.

**Manage/transfer team site ownership?** User menu → "Manage Team" → add a
second Owner (and ideally also add them as Billing Manager under "Billing
Account"). To fully transfer: the new owner then removes the original owner
from both pages. Personal accounts cannot have a second owner or be
transferred.

**Edit team name/subdomain?** From the Billing Account page (user menu).

## Documents and data

**Move documents between sites?** Share icon → "Duplicate Document" → pick
target site. This copies (doesn't move) — delete the original if desired.

**Row limit?** Rule of thumb: comfortable **under 100,000 rows**; actual
limit depends on column count and cell size — roughly a **20 MB CSV-equivalent**
ceiling (e.g. 200k rows × 12 numeric columns hits it). Attachments count
separately, capped with data at **1 GB per document**.

**Non-English characters?** Supported in column **labels** and cell values,
but **not in column IDs** (the Python identifier used in formulas) — those
get approximated with English characters on import; rename the label
afterward if needed. Edit label vs. ID separately via the column menu's link
icon.

**Sum/aggregate a column?** Grist is a database, not a spreadsheet — rows
are records, not summable ranges. Use a **summary table**: Add New → Add
Page/Widget to Page → click the Σ icon next to the source table. See
[FORMULAS_AND_FUNCTIONS.md#summary-tables](FORMULAS_AND_FUNCTIONS.md#summary-tables-group-by)
for grouping by month/store/etc.

## Sharing

**Team member vs. guest?** Team members belong to a paid-per-seat team site
(`your-team.getgrist.com`); default access to all its documents (narrowable
per doc/workspace). Guests are invited to individual documents only, don't
count toward plan seats — every document (including on personal sites)
allows up to 2 free guests.

**Share outside the team?** Four mechanisms: (1) 2 free guests per doc, (2)
public **link sharing** (viewer or editor role, anyone with the link — use
cautiously with sensitive data), (3) **restricted view-only links** via
[link keys](ACCESS_RULES.md#link-keys) in access rules for a narrower slice,
(4) **view-only iframe embed** — see [INTEGRATIONS.md#embedding-iframe](INTEGRATIONS.md#embedding-iframe).

**"Too many pending invites" error?** Rate-limited invites to emails without
an existing Grist account. Wait 24h, or wait for invitees to register first.
Enterprise/self-hosted may have a different limit.

## Grist and your website/app

**Embed Grist in a website?** Yes, view-only iframe with public link
sharing on — see [INTEGRATIONS.md#embedding-iframe](INTEGRATIONS.md#embedding-iframe).

**Use Grist as a web app backend?** **Not currently supported.** No
appropriate browser-safe auth method exists yet — an API key embedded in
client-side code would be exposed to any page viewer. Feature request
territory; discuss on the [community forum](https://community.getgrist.com/).
