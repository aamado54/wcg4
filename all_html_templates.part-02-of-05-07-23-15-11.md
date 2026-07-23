# CONCATENATED .HTML FILES

PART_NUMBER=2
TOTAL_PARTS=5

DOCUMENT_MODE=LITERAL_CODE_ARCHIVE
PARSING_PRIORITY=PATH_LITERAL->CONTENT_NUMBERED_BEGIN->CONTENT_BASE64_BEGIN->CONTENT_BEGIN
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
RECORD_SEPARATOR=BEGIN_LITERAL_FILE_RECORD|END_LITERAL_FILE_RECORD
RECORD_BOUNDARY=========== RECORD_BOUNDARY ==========
CONTENT_POLICY=PRESERVE_EXACT_TEXT_WITH_METADATA_AND_NUMBERED_FALLBACK
READING_HINT=Prefer PATH_LITERAL first for file identity. Prefer CONTENT_NUMBERED_BEGIN for faithful line-by-line reading. Use CONTENT_BASE64_BEGIN for exact reconstruction when available. Use CONTENT_BEGIN only as a convenience view. If CONTENT_BEGIN looks compacted, flattened, or visually altered, do not use it to infer exact identifiers, variable names, paths, punctuation grouping, or spacing.
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgc/admin/_styles.html
PATH_JSON="templates/pgc/admin/_styles.html"
FILENAME=_styles.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=609
SIZE_BYTES_UTF8=14965
CONTENT_SHA256=13f1d6cf10ba29acb79af6bfa8450fa211c7afc4363a0ad9522c9ab8c6d1a5a5
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~html
<style>
    .adm {
        --adm-primary: #0f3d56;
        --adm-accent: #0f766e;
        --adm-card: #ffffff;
        --adm-border: #d9e2ec;
        --adm-muted: #64748b;
        --adm-bg-soft: #f8fafc;
    }

    .adm-header {
        background: var(--adm-card);
        border: 1px solid var(--adm-border);
        border-radius: 12px;
        padding: 22px 26px;
        margin-bottom: 18px;
    }

    .adm-header-top {
        display: flex;
        flex-wrap: wrap;
        align-items: flex-start;
        justify-content: space-between;
        gap: 18px;
    }

    .adm-period-label {
        font-size: 1.85rem;
        font-weight: 700;
        color: var(--adm-primary);
        margin: 6px 0 4px;
        letter-spacing: -0.02em;
    }

    .adm-period-status {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 600;
    }

    .adm-period-status.incomplete { background: #fef3c7; color: #92400e; }
    .adm-period-status.in_review { background: #e0f2fe; color: #0369a1; }
    .adm-period-status.ready { background: #d1fae5; color: #065f46; }
    .adm-period-status.closed { background: #e2e8f0; color: #334155; }

    .adm-nav {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 18px;
    }

    .adm-nav a {
        padding: 8px 14px;
        border-radius: 8px;
        text-decoration: none;
        font-size: 0.9rem;
        font-weight: 600;
        color: var(--adm-primary);
        border: 1px solid var(--adm-border);
        background: white;
    }

    .adm-nav a.active {
        background: var(--adm-primary);
        color: white;
        border-color: var(--adm-primary);
    }

    .adm-btn {
        padding: 9px 15px;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 600;
        cursor: pointer;
        text-decoration: none;
        border: none;
        display: inline-block;
    }

    .adm-btn-primary { background: var(--adm-accent); color: white; }
    .adm-btn-secondary { background: white; color: var(--adm-primary); border: 1px solid var(--adm-border); }
    .adm-btn-ghost { background: transparent; color: var(--adm-muted); border: 1px solid var(--adm-border); }
    .adm-btn-discard {
        background: #fff7ed;
        color: #9a3412;
        border: 1px solid #fdba74;
    }
    .adm-upload-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        align-items: center;
    }

    .adm-period-select {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        align-items: end;
    }

    .adm-period-select select, .adm-period-select input {
        padding: 8px 10px;
        border: 1px solid var(--adm-border);
        border-radius: 6px;
    }

    .adm-layout {
        display: grid;
        grid-template-columns: 1fr 320px;
        gap: 18px;
        align-items: start;
    }

    @media (max-width: 960px) {
        .adm-layout { grid-template-columns: 1fr; }
    }

    .adm-route {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
        gap: 12px;
        margin-bottom: 18px;
    }

    .adm-block-card {
        background: var(--adm-card);
        border: 2px solid var(--adm-border);
        border-radius: 12px;
        padding: 16px;
        text-decoration: none;
        color: inherit;
        display: block;
        transition: border-color 0.15s, box-shadow 0.15s;
    }

    .adm-block-card:hover {
        border-color: #94a3b8;
        box-shadow: 0 4px 14px rgba(15, 61, 86, 0.07);
    }

    .adm-block-card.active {
        border-color: var(--adm-primary);
        box-shadow: 0 4px 16px rgba(15, 61, 86, 0.1);
    }

    .adm-block-step {
        font-size: 0.72rem;
        font-weight: 700;
        color: var(--adm-muted);
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .adm-block-title {
        font-size: 1rem;
        font-weight: 700;
        margin: 5px 0 7px;
        color: var(--adm-primary);
    }

    .adm-badge {
        display: inline-block;
        padding: 3px 9px;
        border-radius: 999px;
        font-size: 0.76rem;
        font-weight: 600;
    }

    .adm-badge.pending { background: #f1f5f9; color: #94a3b8; }
    .adm-badge.loaded { background: #d1fae5; color: #0f766e; }
    .adm-badge.observed { background: #fef3c7; color: #b45309; }
    .adm-badge.reviewed { background: #dbeafe; color: #1d4ed8; }
    .adm-badge.closed { background: #e2e8f0; color: #475569; }

    .adm-block-meta {
        font-size: 0.8rem;
        color: var(--adm-muted);
        margin-top: 8px;
        line-height: 1.4;
    }

    .adm-panel {
        background: var(--adm-card);
        border: 1px solid var(--adm-border);
        border-radius: 12px;
        padding: 22px;
        margin-bottom: 16px;
    }

    .adm-panel h3 {
        margin: 0 0 5px;
        color: var(--adm-primary);
        font-size: 1.15rem;
    }

    .adm-panel .subtitle {
        color: var(--adm-muted);
        margin: 0 0 18px;
        font-size: 0.9rem;
    }

    .adm-checklist {
        list-style: none;
        padding: 0;
        margin: 0 0 18px;
    }

    .adm-checklist li {
        padding: 7px 0;
        border-bottom: 1px solid #edf2f7;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .adm-checklist li::before { content: "○"; color: #94a3b8; font-weight: 700; }
    .adm-checklist li.done::before { content: "✓"; color: #0f766e; }

    .adm-side-card {
        background: var(--adm-card);
        border: 1px solid var(--adm-border);
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 14px;
    }

    .adm-side-card h4 {
        margin: 0 0 12px;
        font-size: 0.92rem;
        color: var(--adm-primary);
    }

    .adm-stat-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }

    .adm-stat {
        background: var(--adm-bg-soft);
        border-radius: 8px;
        padding: 10px;
        text-align: center;
    }

    .adm-stat .value { font-size: 1.3rem; font-weight: 700; color: var(--adm-primary); }
    .adm-stat .label { font-size: 0.75rem; color: var(--adm-muted); margin-top: 2px; }

    .adm-reminder {
        font-size: 0.86rem;
        color: #475569;
        padding: 7px 0;
        border-bottom: 1px solid #edf2f7;
        line-height: 1.45;
    }

    .adm-reminder:last-child { border-bottom: none; }

    .adm-upload-row {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
        padding: 9px 0;
        border-bottom: 1px solid #edf2f7;
        font-size: 0.88rem;
    }

    .adm-log-item {
        font-size: 0.84rem;
        padding: 7px 0;
        border-bottom: 1px solid #edf2f7;
        color: #475569;
    }

    .adm-tabs {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 18px;
    }

    .adm-tabs a {
        padding: 8px 14px;
        border-radius: 8px;
        text-decoration: none;
        font-size: 0.88rem;
        font-weight: 600;
        color: var(--adm-primary);
        border: 1px solid var(--adm-border);
        background: white;
    }

    .adm-tabs a.active {
        background: var(--adm-accent);
        color: white;
        border-color: var(--adm-accent);
    }

    .adm-edit-grid {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.88rem;
    }

    .adm-edit-grid th, .adm-edit-grid td {
        padding: 8px 10px;
        border-bottom: 1px solid #edf2f7;
        text-align: center;
    }

    .adm-edit-grid th {
        background: var(--adm-bg-soft);
        color: var(--adm-primary);
        font-weight: 600;
    }

    .adm-edit-grid th:first-child, .adm-edit-grid td:first-child {
        text-align: left;
        font-weight: 600;
    }

    .adm-edit-grid input[type="text"],
    .adm-edit-grid input[type="number"],
    .adm-edit-grid select,
    .adm-edit-grid textarea {
        width: 100%;
        max-width: 140px;
        padding: 6px 8px;
        border: 1px solid var(--adm-border);
        border-radius: 6px;
        font-size: 0.88rem;
    }

    .adm-edit-grid textarea { max-width: 100%; min-height: 60px; }

    .adm-form-footer {
        margin-top: 18px;
        padding-top: 16px;
        border-top: 1px solid #edf2f7;
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        align-items: end;
    }

    .adm-form-footer label { font-size: 0.85rem; }
    .adm-form-footer input[type="text"] {
        min-width: 220px;
        padding: 8px 10px;
        border: 1px solid var(--adm-border);
        border-radius: 6px;
    }

    .adm-scroll { overflow-x: auto; }

    .adm-browse-grid td input[type="text"],
    .adm-browse-grid td input[type="number"],
    .adm-browse-grid td select {
        min-width: 0;
        width: 100%;
        max-width: 180px;
    }

    .adm-browse-new td {
        background: #f0fdf9;
    }

    .adm-une-legend {
        display: flex;
        flex-wrap: wrap;
        gap: 10px 16px;
        margin: 0 0 14px;
        font-size: 0.88rem;
        color: var(--adm-muted);
    }

    .adm-une-legend-item strong {
        color: var(--adm-primary);
        margin-right: 4px;
    }

    .adm-une-grid td:last-child {
        min-width: 420px;
    }

    .adm-une-pick {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
    }

    .adm-une-opt {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 6px 9px;
        border: 1px solid var(--adm-border);
        border-radius: 8px;
        background: #fff;
        cursor: pointer;
        font-size: 0.8rem;
        user-select: none;
    }

    .adm-une-opt input {
        margin: 0;
    }

    .adm-une-opt .adm-une-short {
        font-weight: 700;
        color: var(--adm-primary);
        font-variant-numeric: tabular-nums;
    }

    .adm-une-opt .adm-une-name {
        color: var(--adm-muted);
    }

    .adm-une-opt.is-current {
        border-color: #99f6e4;
        background: #f0fdfa;
    }

    .adm-une-opt:has(input:checked) {
        border-color: var(--adm-accent);
        background: #ccfbf1;
        box-shadow: inset 0 0 0 1px var(--adm-accent);
    }

    .adm-une-opt:has(input:checked) .adm-une-name {
        color: #115e59;
        font-weight: 600;
    }

    .adm-period-hint {
        margin: 8px 0 0;
        font-size: 0.86rem;
    }

    .adm-banner {
        padding: 12px 14px;
        border-radius: 8px;
        margin: 0 0 14px;
        font-size: 0.9rem;
        border: 1px solid var(--adm-border);
    }
    .adm-banner-warn { background: #fffbeb; border-color: #f0c36d; color: #92400e; }
    .adm-banner-info { background: #f0fdfa; border-color: #99f6e4; color: #115e59; }

    .adm-currency-tag {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        color: #0f766e;
        background: #ccfbf1;
        padding: 2px 6px;
        border-radius: 4px;
    }

    .adm-ingresos-cell {
        background: #f8fffd;
        min-width: 160px;
        vertical-align: top;
    }
    .adm-ingresos-stack input[type="text"] {
        width: 100%;
        max-width: 160px;
    }

    .adm-route-hint {
        margin: 0 0 14px;
        padding: 10px 14px;
        background: #f8fafc;
        border: 1px solid var(--adm-border);
        border-radius: 8px;
        font-size: 0.88rem;
        color: #334155;
    }
    .adm-currency-toggle {
        display: flex;
        gap: 10px;
        margin-bottom: 6px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .adm-currency-toggle label {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        cursor: pointer;
    }

    .adm-year-ingresos th,
    .adm-year-ingresos td {
        min-width: 110px;
    }
    .adm-year-ingresos input[type="text"] {
        width: 100%;
        max-width: 140px;
        padding: 6px 8px;
    }
    .adm-currency-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        align-items: center;
        padding: 10px 12px;
        background: #f8fafc;
        border: 1px solid var(--adm-border);
        border-radius: 8px;
        font-size: 0.9rem;
    }

    /* Colorblind-friendly: hue + dark border + symbol (not color alone) */
    .adm-nav-recalc {
        margin-left: auto;
        display: flex;
        align-items: center;
    }
    .adm-recalc-form { margin: 0; }
    .adm-recalc-btn {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 14px;
        border-radius: 8px;
        border: 2px solid;
        font-weight: 700;
        font-size: 0.88rem;
        cursor: pointer;
        line-height: 1.2;
        transition: transform 0.08s ease, box-shadow 0.12s ease, filter 0.12s ease, opacity 0.12s ease;
        user-select: none;
    }
    .adm-recalc-btn:active:not(:disabled) {
        transform: scale(0.96);
        box-shadow: inset 0 2px 6px rgba(0,0,0,0.18);
    }
    .adm-recalc-btn:focus-visible {
        outline: 3px solid #38bdf8;
        outline-offset: 2px;
    }
    .adm-recalc-btn.is-pending {
        background: #F3E8B8; /* pastel yellow */
        border-color: #8A7340; /* brown edge */
        color: #3D3420;
    }
    .adm-recalc-btn.is-pending:hover:not(:disabled) {
        background: #EDE0A0;
    }
    .adm-recalc-btn.is-ready {
        background: #C9DFD0; /* pastel green */
        border-color: #2F6B4F; /* dark green edge */
        color: #1A3D2E;
    }
    .adm-recalc-btn.is-ready:hover:not(:disabled) {
        background: #B7D4C2;
    }
    .adm-recalc-btn.is-working {
        cursor: wait;
        opacity: 0.92;
        filter: saturate(0.85);
        box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.25);
    }
    .adm-recalc-btn.is-working .adm-recalc-symbol {
        display: none;
    }
    .adm-recalc-spinner {
        display: none;
        width: 14px;
        height: 14px;
        border: 2px solid currentColor;
        border-right-color: transparent;
        border-radius: 50%;
        animation: adm-recalc-spin 0.7s linear infinite;
        flex-shrink: 0;
    }
    .adm-recalc-btn.is-working .adm-recalc-spinner {
        display: inline-block;
    }
    @keyframes adm-recalc-spin {
        to { transform: rotate(360deg); }
    }
    .adm-recalc-symbol {
        font-size: 1.05rem;
        font-weight: 800;
    }
    .adm-recalc-count { font-weight: 800; }
    .adm-recalc-details {
        margin: 8px 0 12px;
        padding: 8px 12px;
        background: #F7F1D8;
        border: 1px dashed #8A7340;
        border-radius: 8px;
        font-size: 0.85rem;
        color: #3D3420;
    }
    .adm-recalc-details ul {
        margin: 8px 0 0;
        padding-left: 18px;
    }
</style>

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|<style>
00002|    .adm {
00003|        --adm-primary: #0f3d56;
00004|        --adm-accent: #0f766e;
00005|        --adm-card: #ffffff;
00006|        --adm-border: #d9e2ec;
00007|        --adm-muted: #64748b;
00008|        --adm-bg-soft: #f8fafc;
00009|    }
00010|
00011|    .adm-header {
00012|        background: var(--adm-card);
00013|        border: 1px solid var(--adm-border);
00014|        border-radius: 12px;
00015|        padding: 22px 26px;
00016|        margin-bottom: 18px;
00017|    }
00018|
00019|    .adm-header-top {
00020|        display: flex;
00021|        flex-wrap: wrap;
00022|        align-items: flex-start;
00023|        justify-content: space-between;
00024|        gap: 18px;
00025|    }
00026|
00027|    .adm-period-label {
00028|        font-size: 1.85rem;
00029|        font-weight: 700;
00030|        color: var(--adm-primary);
00031|        margin: 6px 0 4px;
00032|        letter-spacing: -0.02em;
00033|    }
00034|
00035|    .adm-period-status {
00036|        display: inline-block;
00037|        padding: 5px 12px;
00038|        border-radius: 999px;
00039|        font-size: 0.82rem;
00040|        font-weight: 600;
00041|    }
00042|
00043|    .adm-period-status.incomplete { background: #fef3c7; color: #92400e; }
00044|    .adm-period-status.in_review { background: #e0f2fe; color: #0369a1; }
00045|    .adm-period-status.ready { background: #d1fae5; color: #065f46; }
00046|    .adm-period-status.closed { background: #e2e8f0; color: #334155; }
00047|
00048|    .adm-nav {
00049|        display: flex;
00050|        flex-wrap: wrap;
00051|        gap: 8px;
00052|        margin-bottom: 18px;
00053|    }
00054|
00055|    .adm-nav a {
00056|        padding: 8px 14px;
00057|        border-radius: 8px;
00058|        text-decoration: none;
00059|        font-size: 0.9rem;
00060|        font-weight: 600;
00061|        color: var(--adm-primary);
00062|        border: 1px solid var(--adm-border);
00063|        background: white;
00064|    }
00065|
00066|    .adm-nav a.active {
00067|        background: var(--adm-primary);
00068|        color: white;
00069|        border-color: var(--adm-primary);
00070|    }
00071|
00072|    .adm-btn {
00073|        padding: 9px 15px;
00074|        border-radius: 8px;
00075|        font-size: 0.9rem;
00076|        font-weight: 600;
00077|        cursor: pointer;
00078|        text-decoration: none;
00079|        border: none;
00080|        display: inline-block;
00081|    }
00082|
00083|    .adm-btn-primary { background: var(--adm-accent); color: white; }
00084|    .adm-btn-secondary { background: white; color: var(--adm-primary); border: 1px solid var(--adm-border); }
00085|    .adm-btn-ghost { background: transparent; color: var(--adm-muted); border: 1px solid var(--adm-border); }
00086|    .adm-btn-discard {
00087|        background: #fff7ed;
00088|        color: #9a3412;
00089|        border: 1px solid #fdba74;
00090|    }
00091|    .adm-upload-actions {
00092|        display: flex;
00093|        flex-wrap: wrap;
00094|        gap: 8px;
00095|        align-items: center;
00096|    }
00097|
00098|    .adm-period-select {
00099|        display: flex;
00100|        gap: 10px;
00101|        flex-wrap: wrap;
00102|        align-items: end;
00103|    }
00104|
00105|    .adm-period-select select, .adm-period-select input {
00106|        padding: 8px 10px;
00107|        border: 1px solid var(--adm-border);
00108|        border-radius: 6px;
00109|    }
00110|
00111|    .adm-layout {
00112|        display: grid;
00113|        grid-template-columns: 1fr 320px;
00114|        gap: 18px;
00115|        align-items: start;
00116|    }
00117|
00118|    @media (max-width: 960px) {
00119|        .adm-layout { grid-template-columns: 1fr; }
00120|    }
00121|
00122|    .adm-route {
00123|        display: grid;
00124|        grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
00125|        gap: 12px;
00126|        margin-bottom: 18px;
00127|    }
00128|
00129|    .adm-block-card {
00130|        background: var(--adm-card);
00131|        border: 2px solid var(--adm-border);
00132|        border-radius: 12px;
00133|        padding: 16px;
00134|        text-decoration: none;
00135|        color: inherit;
00136|        display: block;
00137|        transition: border-color 0.15s, box-shadow 0.15s;
00138|    }
00139|
00140|    .adm-block-card:hover {
00141|        border-color: #94a3b8;
00142|        box-shadow: 0 4px 14px rgba(15, 61, 86, 0.07);
00143|    }
00144|
00145|    .adm-block-card.active {
00146|        border-color: var(--adm-primary);
00147|        box-shadow: 0 4px 16px rgba(15, 61, 86, 0.1);
00148|    }
00149|
00150|    .adm-block-step {
00151|        font-size: 0.72rem;
00152|        font-weight: 700;
00153|        color: var(--adm-muted);
00154|        text-transform: uppercase;
00155|        letter-spacing: 0.04em;
00156|    }
00157|
00158|    .adm-block-title {
00159|        font-size: 1rem;
00160|        font-weight: 700;
00161|        margin: 5px 0 7px;
00162|        color: var(--adm-primary);
00163|    }
00164|
00165|    .adm-badge {
00166|        display: inline-block;
00167|        padding: 3px 9px;
00168|        border-radius: 999px;
00169|        font-size: 0.76rem;
00170|        font-weight: 600;
00171|    }
00172|
00173|    .adm-badge.pending { background: #f1f5f9; color: #94a3b8; }
00174|    .adm-badge.loaded { background: #d1fae5; color: #0f766e; }
00175|    .adm-badge.observed { background: #fef3c7; color: #b45309; }
00176|    .adm-badge.reviewed { background: #dbeafe; color: #1d4ed8; }
00177|    .adm-badge.closed { background: #e2e8f0; color: #475569; }
00178|
00179|    .adm-block-meta {
00180|        font-size: 0.8rem;
00181|        color: var(--adm-muted);
00182|        margin-top: 8px;
00183|        line-height: 1.4;
00184|    }
00185|
00186|    .adm-panel {
00187|        background: var(--adm-card);
00188|        border: 1px solid var(--adm-border);
00189|        border-radius: 12px;
00190|        padding: 22px;
00191|        margin-bottom: 16px;
00192|    }
00193|
00194|    .adm-panel h3 {
00195|        margin: 0 0 5px;
00196|        color: var(--adm-primary);
00197|        font-size: 1.15rem;
00198|    }
00199|
00200|    .adm-panel .subtitle {
00201|        color: var(--adm-muted);
00202|        margin: 0 0 18px;
00203|        font-size: 0.9rem;
00204|    }
00205|
00206|    .adm-checklist {
00207|        list-style: none;
00208|        padding: 0;
00209|        margin: 0 0 18px;
00210|    }
00211|
00212|    .adm-checklist li {
00213|        padding: 7px 0;
00214|        border-bottom: 1px solid #edf2f7;
00215|        font-size: 0.9rem;
00216|        display: flex;
00217|        align-items: center;
00218|        gap: 8px;
00219|    }
00220|
00221|    .adm-checklist li::before { content: "○"; color: #94a3b8; font-weight: 700; }
00222|    .adm-checklist li.done::before { content: "✓"; color: #0f766e; }
00223|
00224|    .adm-side-card {
00225|        background: var(--adm-card);
00226|        border: 1px solid var(--adm-border);
00227|        border-radius: 12px;
00228|        padding: 18px;
00229|        margin-bottom: 14px;
00230|    }
00231|
00232|    .adm-side-card h4 {
00233|        margin: 0 0 12px;
00234|        font-size: 0.92rem;
00235|        color: var(--adm-primary);
00236|    }
00237|
00238|    .adm-stat-grid {
00239|        display: grid;
00240|        grid-template-columns: 1fr 1fr;
00241|        gap: 8px;
00242|    }
00243|
00244|    .adm-stat {
00245|        background: var(--adm-bg-soft);
00246|        border-radius: 8px;
00247|        padding: 10px;
00248|        text-align: center;
00249|    }
00250|
00251|    .adm-stat .value { font-size: 1.3rem; font-weight: 700; color: var(--adm-primary); }
00252|    .adm-stat .label { font-size: 0.75rem; color: var(--adm-muted); margin-top: 2px; }
00253|
00254|    .adm-reminder {
00255|        font-size: 0.86rem;
00256|        color: #475569;
00257|        padding: 7px 0;
00258|        border-bottom: 1px solid #edf2f7;
00259|        line-height: 1.45;
00260|    }
00261|
00262|    .adm-reminder:last-child { border-bottom: none; }
00263|
00264|    .adm-upload-row {
00265|        display: flex;
00266|        flex-wrap: wrap;
00267|        align-items: center;
00268|        justify-content: space-between;
00269|        gap: 8px;
00270|        padding: 9px 0;
00271|        border-bottom: 1px solid #edf2f7;
00272|        font-size: 0.88rem;
00273|    }
00274|
00275|    .adm-log-item {
00276|        font-size: 0.84rem;
00277|        padding: 7px 0;
00278|        border-bottom: 1px solid #edf2f7;
00279|        color: #475569;
00280|    }
00281|
00282|    .adm-tabs {
00283|        display: flex;
00284|        flex-wrap: wrap;
00285|        gap: 6px;
00286|        margin-bottom: 18px;
00287|    }
00288|
00289|    .adm-tabs a {
00290|        padding: 8px 14px;
00291|        border-radius: 8px;
00292|        text-decoration: none;
00293|        font-size: 0.88rem;
00294|        font-weight: 600;
00295|        color: var(--adm-primary);
00296|        border: 1px solid var(--adm-border);
00297|        background: white;
00298|    }
00299|
00300|    .adm-tabs a.active {
00301|        background: var(--adm-accent);
00302|        color: white;
00303|        border-color: var(--adm-accent);
00304|    }
00305|
00306|    .adm-edit-grid {
00307|        width: 100%;
00308|        border-collapse: collapse;
00309|        font-size: 0.88rem;
00310|    }
00311|
00312|    .adm-edit-grid th, .adm-edit-grid td {
00313|        padding: 8px 10px;
00314|        border-bottom: 1px solid #edf2f7;
00315|        text-align: center;
00316|    }
00317|
00318|    .adm-edit-grid th {
00319|        background: var(--adm-bg-soft);
00320|        color: var(--adm-primary);
00321|        font-weight: 600;
00322|    }
00323|
00324|    .adm-edit-grid th:first-child, .adm-edit-grid td:first-child {
00325|        text-align: left;
00326|        font-weight: 600;
00327|    }
00328|
00329|    .adm-edit-grid input[type="text"],
00330|    .adm-edit-grid input[type="number"],
00331|    .adm-edit-grid select,
00332|    .adm-edit-grid textarea {
00333|        width: 100%;
00334|        max-width: 140px;
00335|        padding: 6px 8px;
00336|        border: 1px solid var(--adm-border);
00337|        border-radius: 6px;
00338|        font-size: 0.88rem;
00339|    }
00340|
00341|    .adm-edit-grid textarea { max-width: 100%; min-height: 60px; }
00342|
00343|    .adm-form-footer {
00344|        margin-top: 18px;
00345|        padding-top: 16px;
00346|        border-top: 1px solid #edf2f7;
00347|        display: flex;
00348|        flex-wrap: wrap;
00349|        gap: 12px;
00350|        align-items: end;
00351|    }
00352|
00353|    .adm-form-footer label { font-size: 0.85rem; }
00354|    .adm-form-footer input[type="text"] {
00355|        min-width: 220px;
00356|        padding: 8px 10px;
00357|        border: 1px solid var(--adm-border);
00358|        border-radius: 6px;
00359|    }
00360|
00361|    .adm-scroll { overflow-x: auto; }
00362|
00363|    .adm-browse-grid td input[type="text"],
00364|    .adm-browse-grid td input[type="number"],
00365|    .adm-browse-grid td select {
00366|        min-width: 0;
00367|        width: 100%;
00368|        max-width: 180px;
00369|    }
00370|
00371|    .adm-browse-new td {
00372|        background: #f0fdf9;
00373|    }
00374|
00375|    .adm-une-legend {
00376|        display: flex;
00377|        flex-wrap: wrap;
00378|        gap: 10px 16px;
00379|        margin: 0 0 14px;
00380|        font-size: 0.88rem;
00381|        color: var(--adm-muted);
00382|    }
00383|
00384|    .adm-une-legend-item strong {
00385|        color: var(--adm-primary);
00386|        margin-right: 4px;
00387|    }
00388|
00389|    .adm-une-grid td:last-child {
00390|        min-width: 420px;
00391|    }
00392|
00393|    .adm-une-pick {
00394|        display: flex;
00395|        flex-wrap: wrap;
00396|        gap: 6px;
00397|    }
00398|
00399|    .adm-une-opt {
00400|        display: inline-flex;
00401|        align-items: center;
00402|        gap: 5px;
00403|        padding: 6px 9px;
00404|        border: 1px solid var(--adm-border);
00405|        border-radius: 8px;
00406|        background: #fff;
00407|        cursor: pointer;
00408|        font-size: 0.8rem;
00409|        user-select: none;
00410|    }
00411|
00412|    .adm-une-opt input {
00413|        margin: 0;
00414|    }
00415|
00416|    .adm-une-opt .adm-une-short {
00417|        font-weight: 700;
00418|        color: var(--adm-primary);
00419|        font-variant-numeric: tabular-nums;
00420|    }
00421|
00422|    .adm-une-opt .adm-une-name {
00423|        color: var(--adm-muted);
00424|    }
00425|
00426|    .adm-une-opt.is-current {
00427|        border-color: #99f6e4;
00428|        background: #f0fdfa;
00429|    }
00430|
00431|    .adm-une-opt:has(input:checked) {
00432|        border-color: var(--adm-accent);
00433|        background: #ccfbf1;
00434|        box-shadow: inset 0 0 0 1px var(--adm-accent);
00435|    }
00436|
00437|    .adm-une-opt:has(input:checked) .adm-une-name {
00438|        color: #115e59;
00439|        font-weight: 600;
00440|    }
00441|
00442|    .adm-period-hint {
00443|        margin: 8px 0 0;
00444|        font-size: 0.86rem;
00445|    }
00446|
00447|    .adm-banner {
00448|        padding: 12px 14px;
00449|        border-radius: 8px;
00450|        margin: 0 0 14px;
00451|        font-size: 0.9rem;
00452|        border: 1px solid var(--adm-border);
00453|    }
00454|    .adm-banner-warn { background: #fffbeb; border-color: #f0c36d; color: #92400e; }
00455|    .adm-banner-info { background: #f0fdfa; border-color: #99f6e4; color: #115e59; }
00456|
00457|    .adm-currency-tag {
00458|        display: inline-block;
00459|        font-size: 0.72rem;
00460|        font-weight: 700;
00461|        color: #0f766e;
00462|        background: #ccfbf1;
00463|        padding: 2px 6px;
00464|        border-radius: 4px;
00465|    }
00466|
00467|    .adm-ingresos-cell {
00468|        background: #f8fffd;
00469|        min-width: 160px;
00470|        vertical-align: top;
00471|    }
00472|    .adm-ingresos-stack input[type="text"] {
00473|        width: 100%;
00474|        max-width: 160px;
00475|    }
00476|
00477|    .adm-route-hint {
00478|        margin: 0 0 14px;
00479|        padding: 10px 14px;
00480|        background: #f8fafc;
00481|        border: 1px solid var(--adm-border);
00482|        border-radius: 8px;
00483|        font-size: 0.88rem;
00484|        color: #334155;
00485|    }
00486|    .adm-currency-toggle {
00487|        display: flex;
00488|        gap: 10px;
00489|        margin-bottom: 6px;
00490|        font-size: 0.82rem;
00491|        font-weight: 600;
00492|    }
00493|    .adm-currency-toggle label {
00494|        display: inline-flex;
00495|        align-items: center;
00496|        gap: 4px;
00497|        cursor: pointer;
00498|    }
00499|
00500|    .adm-year-ingresos th,
00501|    .adm-year-ingresos td {
00502|        min-width: 110px;
00503|    }
00504|    .adm-year-ingresos input[type="text"] {
00505|        width: 100%;
00506|        max-width: 140px;
00507|        padding: 6px 8px;
00508|    }
00509|    .adm-currency-bar {
00510|        display: flex;
00511|        flex-wrap: wrap;
00512|        gap: 12px;
00513|        align-items: center;
00514|        padding: 10px 12px;
00515|        background: #f8fafc;
00516|        border: 1px solid var(--adm-border);
00517|        border-radius: 8px;
00518|        font-size: 0.9rem;
00519|    }
00520|
00521|    /* Colorblind-friendly: hue + dark border + symbol (not color alone) */
00522|    .adm-nav-recalc {
00523|        margin-left: auto;
00524|        display: flex;
00525|        align-items: center;
00526|    }
00527|    .adm-recalc-form { margin: 0; }
00528|    .adm-recalc-btn {
00529|        display: inline-flex;
00530|        align-items: center;
00531|        gap: 8px;
00532|        padding: 8px 14px;
00533|        border-radius: 8px;
00534|        border: 2px solid;
00535|        font-weight: 700;
00536|        font-size: 0.88rem;
00537|        cursor: pointer;
00538|        line-height: 1.2;
00539|        transition: transform 0.08s ease, box-shadow 0.12s ease, filter 0.12s ease, opacity 0.12s ease;
00540|        user-select: none;
00541|    }
00542|    .adm-recalc-btn:active:not(:disabled) {
00543|        transform: scale(0.96);
00544|        box-shadow: inset 0 2px 6px rgba(0,0,0,0.18);
00545|    }
00546|    .adm-recalc-btn:focus-visible {
00547|        outline: 3px solid #38bdf8;
00548|        outline-offset: 2px;
00549|    }
00550|    .adm-recalc-btn.is-pending {
00551|        background: #F3E8B8; /* pastel yellow */
00552|        border-color: #8A7340; /* brown edge */
00553|        color: #3D3420;
00554|    }
00555|    .adm-recalc-btn.is-pending:hover:not(:disabled) {
00556|        background: #EDE0A0;
00557|    }
00558|    .adm-recalc-btn.is-ready {
00559|        background: #C9DFD0; /* pastel green */
00560|        border-color: #2F6B4F; /* dark green edge */
00561|        color: #1A3D2E;
00562|    }
00563|    .adm-recalc-btn.is-ready:hover:not(:disabled) {
00564|        background: #B7D4C2;
00565|    }
00566|    .adm-recalc-btn.is-working {
00567|        cursor: wait;
00568|        opacity: 0.92;
00569|        filter: saturate(0.85);
00570|        box-shadow: 0 0 0 3px rgba(15, 118, 110, 0.25);
00571|    }
00572|    .adm-recalc-btn.is-working .adm-recalc-symbol {
00573|        display: none;
00574|    }
00575|    .adm-recalc-spinner {
00576|        display: none;
00577|        width: 14px;
00578|        height: 14px;
00579|        border: 2px solid currentColor;
00580|        border-right-color: transparent;
00581|        border-radius: 50%;
00582|        animation: adm-recalc-spin 0.7s linear infinite;
00583|        flex-shrink: 0;
00584|    }
00585|    .adm-recalc-btn.is-working .adm-recalc-spinner {
00586|        display: inline-block;
00587|    }
00588|    @keyframes adm-recalc-spin {
00589|        to { transform: rotate(360deg); }
00590|    }
00591|    .adm-recalc-symbol {
00592|        font-size: 1.05rem;
00593|        font-weight: 800;
00594|    }
00595|    .adm-recalc-count { font-weight: 800; }
00596|    .adm-recalc-details {
00597|        margin: 8px 0 12px;
00598|        padding: 8px 12px;
00599|        background: #F7F1D8;
00600|        border: 1px dashed #8A7340;
00601|        border-radius: 8px;
00602|        font-size: 0.85rem;
00603|        color: #3D3420;
00604|    }
00605|    .adm-recalc-details ul {
00606|        margin: 8px 0 0;
00607|        padding-left: 18px;
00608|    }
00609|</style>

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
PHN0eWxlPgogICAgLmFkbSB7CiAgICAgICAgLS1hZG0tcHJpbWFyeTogIzBmM2Q1NjsKICAgICAgICAtLWFkbS1hY2NlbnQ6ICMwZjc2NmU7CiAgICAgICAgLS1hZG0tY2FyZDogI2ZmZmZmZjsKICAgICAgICAtLWFkbS1ib3JkZXI6ICNkOWUyZWM7CiAgICAgICAgLS1hZG0tbXV0ZWQ6ICM2NDc0OGI7CiAgICAgICAgLS1hZG0tYmctc29mdDogI2Y4ZmFmYzsKICAgIH0KCiAgICAuYWRtLWhlYWRlciB7CiAgICAgICAgYmFja2dyb3VuZDogdmFyKC0tYWRtLWNhcmQpOwogICAgICAgIGJvcmRlcjogMXB4IHNvbGlkIHZhcigtLWFkbS1ib3JkZXIpOwogICAgICAgIGJvcmRlci1yYWRpdXM6IDEycHg7CiAgICAgICAgcGFkZGluZzogMjJweCAyNnB4OwogICAgICAgIG1hcmdpbi1ib3R0b206IDE4cHg7CiAgICB9CgogICAgLmFkbS1oZWFkZXItdG9wIHsKICAgICAgICBkaXNwbGF5OiBmbGV4OwogICAgICAgIGZsZXgtd3JhcDogd3JhcDsKICAgICAgICBhbGlnbi1pdGVtczogZmxleC1zdGFydDsKICAgICAgICBqdXN0aWZ5LWNvbnRlbnQ6IHNwYWNlLWJldHdlZW47CiAgICAgICAgZ2FwOiAxOHB4OwogICAgfQoKICAgIC5hZG0tcGVyaW9kLWxhYmVsIHsKICAgICAgICBmb250LXNpemU6IDEuODVyZW07CiAgICAgICAgZm9udC13ZWlnaHQ6IDcwMDsKICAgICAgICBjb2xvcjogdmFyKC0tYWRtLXByaW1hcnkpOwogICAgICAgIG1hcmdpbjogNnB4IDAgNHB4OwogICAgICAgIGxldHRlci1zcGFjaW5nOiAtMC4wMmVtOwogICAgfQoKICAgIC5hZG0tcGVyaW9kLXN0YXR1cyB7CiAgICAgICAgZGlzcGxheTogaW5saW5lLWJsb2NrOwogICAgICAgIHBhZGRpbmc6IDVweCAxMnB4OwogICAgICAgIGJvcmRlci1yYWRpdXM6IDk5OXB4OwogICAgICAgIGZvbnQtc2l6ZTogMC44MnJlbTsKICAgICAgICBmb250LXdlaWdodDogNjAwOwogICAgfQoKICAgIC5hZG0tcGVyaW9kLXN0YXR1cy5pbmNvbXBsZXRlIHsgYmFja2dyb3VuZDogI2ZlZjNjNzsgY29sb3I6ICM5MjQwMGU7IH0KICAgIC5hZG0tcGVyaW9kLXN0YXR1cy5pbl9yZXZpZXcgeyBiYWNrZ3JvdW5kOiAjZTBmMmZlOyBjb2xvcjogIzAzNjlhMTsgfQogICAgLmFkbS1wZXJpb2Qtc3RhdHVzLnJlYWR5IHsgYmFja2dyb3VuZDogI2QxZmFlNTsgY29sb3I6ICMwNjVmNDY7IH0KICAgIC5hZG0tcGVyaW9kLXN0YXR1cy5jbG9zZWQgeyBiYWNrZ3JvdW5kOiAjZTJlOGYwOyBjb2xvcjogIzMzNDE1NTsgfQoKICAgIC5hZG0tbmF2IHsKICAgICAgICBkaXNwbGF5OiBmbGV4OwogICAgICAgIGZsZXgtd3JhcDogd3JhcDsKICAgICAgICBnYXA6IDhweDsKICAgICAgICBtYXJnaW4tYm90dG9tOiAxOHB4OwogICAgfQoKICAgIC5hZG0tbmF2IGEgewogICAgICAgIHBhZGRpbmc6IDhweCAxNHB4OwogICAgICAgIGJvcmRlci1yYWRpdXM6IDhweDsKICAgICAgICB0ZXh0LWRlY29yYXRpb246IG5vbmU7CiAgICAgICAgZm9udC1zaXplOiAwLjlyZW07CiAgICAgICAgZm9udC13ZWlnaHQ6IDYwMDsKICAgICAgICBjb2xvcjogdmFyKC0tYWRtLXByaW1hcnkpOwogICAgICAgIGJvcmRlcjogMXB4IHNvbGlkIHZhcigtLWFkbS1ib3JkZXIpOwogICAgICAgIGJhY2tncm91bmQ6IHdoaXRlOwogICAgfQoKICAgIC5hZG0tbmF2IGEuYWN0aXZlIHsKICAgICAgICBiYWNrZ3JvdW5kOiB2YXIoLS1hZG0tcHJpbWFyeSk7CiAgICAgICAgY29sb3I6IHdoaXRlOwogICAgICAgIGJvcmRlci1jb2xvcjogdmFyKC0tYWRtLXByaW1hcnkpOwogICAgfQoKICAgIC5hZG0tYnRuIHsKICAgICAgICBwYWRkaW5nOiA5cHggMTVweDsKICAgICAgICBib3JkZXItcmFkaXVzOiA4cHg7CiAgICAgICAgZm9udC1zaXplOiAwLjlyZW07CiAgICAgICAgZm9udC13ZWlnaHQ6IDYwMDsKICAgICAgICBjdXJzb3I6IHBvaW50ZXI7CiAgICAgICAgdGV4dC1kZWNvcmF0aW9uOiBub25lOwogICAgICAgIGJvcmRlcjogbm9uZTsKICAgICAgICBkaXNwbGF5OiBpbmxpbmUtYmxvY2s7CiAgICB9CgogICAgLmFkbS1idG4tcHJpbWFyeSB7IGJhY2tncm91bmQ6IHZhcigtLWFkbS1hY2NlbnQpOyBjb2xvcjogd2hpdGU7IH0KICAgIC5hZG0tYnRuLXNlY29uZGFyeSB7IGJhY2tncm91bmQ6IHdoaXRlOyBjb2xvcjogdmFyKC0tYWRtLXByaW1hcnkpOyBib3JkZXI6IDFweCBzb2xpZCB2YXIoLS1hZG0tYm9yZGVyKTsgfQogICAgLmFkbS1idG4tZ2hvc3QgeyBiYWNrZ3JvdW5kOiB0cmFuc3BhcmVudDsgY29sb3I6IHZhcigtLWFkbS1tdXRlZCk7IGJvcmRlcjogMXB4IHNvbGlkIHZhcigtLWFkbS1ib3JkZXIpOyB9CiAgICAuYWRtLWJ0bi1kaXNjYXJkIHsKICAgICAgICBiYWNrZ3JvdW5kOiAjZmZmN2VkOwogICAgICAgIGNvbG9yOiAjOWEzNDEyOwogICAgICAgIGJvcmRlcjogMXB4IHNvbGlkICNmZGJhNzQ7CiAgICB9CiAgICAuYWRtLXVwbG9hZC1hY3Rpb25zIHsKICAgICAgICBkaXNwbGF5OiBmbGV4OwogICAgICAgIGZsZXgtd3JhcDogd3JhcDsKICAgICAgICBnYXA6IDhweDsKICAgICAgICBhbGlnbi1pdGVtczogY2VudGVyOwogICAgfQoKICAgIC5hZG0tcGVyaW9kLXNlbGVjdCB7CiAgICAgICAgZGlzcGxheTogZmxleDsKICAgICAgICBnYXA6IDEwcHg7CiAgICAgICAgZmxleC13cmFwOiB3cmFwOwogICAgICAgIGFsaWduLWl0ZW1zOiBlbmQ7CiAgICB9CgogICAgLmFkbS1wZXJpb2Qtc2VsZWN0IHNlbGVjdCwgLmFkbS1wZXJpb2Qtc2VsZWN0IGlucHV0IHsKICAgICAgICBwYWRkaW5nOiA4cHggMTBweDsKICAgICAgICBib3JkZXI6IDFweCBzb2xpZCB2YXIoLS1hZG0tYm9yZGVyKTsKICAgICAgICBib3JkZXItcmFkaXVzOiA2cHg7CiAgICB9CgogICAgLmFkbS1sYXlvdXQgewogICAgICAgIGRpc3BsYXk6IGdyaWQ7CiAgICAgICAgZ3JpZC10ZW1wbGF0ZS1jb2x1bW5zOiAxZnIgMzIwcHg7CiAgICAgICAgZ2FwOiAxOHB4OwogICAgICAgIGFsaWduLWl0ZW1zOiBzdGFydDsKICAgIH0KCiAgICBAbWVkaWEgKG1heC13aWR0aDogOTYwcHgpIHsKICAgICAgICAuYWRtLWxheW91dCB7IGdyaWQtdGVtcGxhdGUtY29sdW1uczogMWZyOyB9CiAgICB9CgogICAgLmFkbS1yb3V0ZSB7CiAgICAgICAgZGlzcGxheTogZ3JpZDsKICAgICAgICBncmlkLXRlbXBsYXRlLWNvbHVtbnM6IHJlcGVhdChhdXRvLWZpbGwsIG1pbm1heCgxOTBweCwgMWZyKSk7CiAgICAgICAgZ2FwOiAxMnB4OwogICAgICAgIG1hcmdpbi1ib3R0b206IDE4cHg7CiAgICB9CgogICAgLmFkbS1ibG9jay1jYXJkIHsKICAgICAgICBiYWNrZ3JvdW5kOiB2YXIoLS1hZG0tY2FyZCk7CiAgICAgICAgYm9yZGVyOiAycHggc29saWQgdmFyKC0tYWRtLWJvcmRlcik7CiAgICAgICAgYm9yZGVyLXJhZGl1czogMTJweDsKICAgICAgICBwYWRkaW5nOiAxNnB4OwogICAgICAgIHRleHQtZGVjb3JhdGlvbjogbm9uZTsKICAgICAgICBjb2xvcjogaW5oZXJpdDsKICAgICAgICBkaXNwbGF5OiBibG9jazsKICAgICAgICB0cmFuc2l0aW9uOiBib3JkZXItY29sb3IgMC4xNXMsIGJveC1zaGFkb3cgMC4xNXM7CiAgICB9CgogICAgLmFkbS1ibG9jay1jYXJkOmhvdmVyIHsKICAgICAgICBib3JkZXItY29sb3I6ICM5NGEzYjg7CiAgICAgICAgYm94LXNoYWRvdzogMCA0cHggMTRweCByZ2JhKDE1LCA2MSwgODYsIDAuMDcpOwogICAgfQoKICAgIC5hZG0tYmxvY2stY2FyZC5hY3RpdmUgewogICAgICAgIGJvcmRlci1jb2xvcjogdmFyKC0tYWRtLXByaW1hcnkpOwogICAgICAgIGJveC1zaGFkb3c6IDAgNHB4IDE2cHggcmdiYSgxNSwgNjEsIDg2LCAwLjEpOwogICAgfQoKICAgIC5hZG0tYmxvY2stc3RlcCB7CiAgICAgICAgZm9udC1zaXplOiAwLjcycmVtOwogICAgICAgIGZvbnQtd2VpZ2h0OiA3MDA7CiAgICAgICAgY29sb3I6IHZhcigtLWFkbS1tdXRlZCk7CiAgICAgICAgdGV4dC10cmFuc2Zvcm06IHVwcGVyY2FzZTsKICAgICAgICBsZXR0ZXItc3BhY2luZzogMC4wNGVtOwogICAgfQoKICAgIC5hZG0tYmxvY2stdGl0bGUgewogICAgICAgIGZvbnQtc2l6ZTogMXJlbTsKICAgICAgICBmb250LXdlaWdodDogNzAwOwogICAgICAgIG1hcmdpbjogNXB4IDAgN3B4OwogICAgICAgIGNvbG9yOiB2YXIoLS1hZG0tcHJpbWFyeSk7CiAgICB9CgogICAgLmFkbS1iYWRnZSB7CiAgICAgICAgZGlzcGxheTogaW5saW5lLWJsb2NrOwogICAgICAgIHBhZGRpbmc6IDNweCA5cHg7CiAgICAgICAgYm9yZGVyLXJhZGl1czogOTk5cHg7CiAgICAgICAgZm9udC1zaXplOiAwLjc2cmVtOwogICAgICAgIGZvbnQtd2VpZ2h0OiA2MDA7CiAgICB9CgogICAgLmFkbS1iYWRnZS5wZW5kaW5nIHsgYmFja2dyb3VuZDogI2YxZjVmOTsgY29sb3I6ICM5NGEzYjg7IH0KICAgIC5hZG0tYmFkZ2UubG9hZGVkIHsgYmFja2dyb3VuZDogI2QxZmFlNTsgY29sb3I6ICMwZjc2NmU7IH0KICAgIC5hZG0tYmFkZ2Uub2JzZXJ2ZWQgeyBiYWNrZ3JvdW5kOiAjZmVmM2M3OyBjb2xvcjogI2I0NTMwOTsgfQogICAgLmFkbS1iYWRnZS5yZXZpZXdlZCB7IGJhY2tncm91bmQ6ICNkYmVhZmU7IGNvbG9yOiAjMWQ0ZWQ4OyB9CiAgICAuYWRtLWJhZGdlLmNsb3NlZCB7IGJhY2tncm91bmQ6ICNlMmU4ZjA7IGNvbG9yOiAjNDc1NTY5OyB9CgogICAgLmFkbS1ibG9jay1tZXRhIHsKICAgICAgICBmb250LXNpemU6IDAuOHJlbTsKICAgICAgICBjb2xvcjogdmFyKC0tYWRtLW11dGVkKTsKICAgICAgICBtYXJnaW4tdG9wOiA4cHg7CiAgICAgICAgbGluZS1oZWlnaHQ6IDEuNDsKICAgIH0KCiAgICAuYWRtLXBhbmVsIHsKICAgICAgICBiYWNrZ3JvdW5kOiB2YXIoLS1hZG0tY2FyZCk7CiAgICAgICAgYm9yZGVyOiAxcHggc29saWQgdmFyKC0tYWRtLWJvcmRlcik7CiAgICAgICAgYm9yZGVyLXJhZGl1czogMTJweDsKICAgICAgICBwYWRkaW5nOiAyMnB4OwogICAgICAgIG1hcmdpbi1ib3R0b206IDE2cHg7CiAgICB9CgogICAgLmFkbS1wYW5lbCBoMyB7CiAgICAgICAgbWFyZ2luOiAwIDAgNXB4OwogICAgICAgIGNvbG9yOiB2YXIoLS1hZG0tcHJpbWFyeSk7CiAgICAgICAgZm9udC1zaXplOiAxLjE1cmVtOwogICAgfQoKICAgIC5hZG0tcGFuZWwgLnN1YnRpdGxlIHsKICAgICAgICBjb2xvcjogdmFyKC0tYWRtLW11dGVkKTsKICAgICAgICBtYXJnaW46IDAgMCAxOHB4OwogICAgICAgIGZvbnQtc2l6ZTogMC45cmVtOwogICAgfQoKICAgIC5hZG0tY2hlY2tsaXN0IHsKICAgICAgICBsaXN0LXN0eWxlOiBub25lOwogICAgICAgIHBhZGRpbmc6IDA7CiAgICAgICAgbWFyZ2luOiAwIDAgMThweDsKICAgIH0KCiAgICAuYWRtLWNoZWNrbGlzdCBsaSB7CiAgICAgICAgcGFkZGluZzogN3B4IDA7CiAgICAgICAgYm9yZGVyLWJvdHRvbTogMXB4IHNvbGlkICNlZGYyZjc7CiAgICAgICAgZm9udC1zaXplOiAwLjlyZW07CiAgICAgICAgZGlzcGxheTogZmxleDsKICAgICAgICBhbGlnbi1pdGVtczogY2VudGVyOwogICAgICAgIGdhcDogOHB4OwogICAgfQoKICAgIC5hZG0tY2hlY2tsaXN0IGxpOjpiZWZvcmUgeyBjb250ZW50OiAi4peLIjsgY29sb3I6ICM5NGEzYjg7IGZvbnQtd2VpZ2h0OiA3MDA7IH0KICAgIC5hZG0tY2hlY2tsaXN0IGxpLmRvbmU6OmJlZm9yZSB7IGNvbnRlbnQ6ICLinJMiOyBjb2xvcjogIzBmNzY2ZTsgfQoKICAgIC5hZG0tc2lkZS1jYXJkIHsKICAgICAgICBiYWNrZ3JvdW5kOiB2YXIoLS1hZG0tY2FyZCk7CiAgICAgICAgYm9yZGVyOiAxcHggc29saWQgdmFyKC0tYWRtLWJvcmRlcik7CiAgICAgICAgYm9yZGVyLXJhZGl1czogMTJweDsKICAgICAgICBwYWRkaW5nOiAxOHB4OwogICAgICAgIG1hcmdpbi1ib3R0b206IDE0cHg7CiAgICB9CgogICAgLmFkbS1zaWRlLWNhcmQgaDQgewogICAgICAgIG1hcmdpbjogMCAwIDEycHg7CiAgICAgICAgZm9udC1zaXplOiAwLjkycmVtOwogICAgICAgIGNvbG9yOiB2YXIoLS1hZG0tcHJpbWFyeSk7CiAgICB9CgogICAgLmFkbS1zdGF0LWdyaWQgewogICAgICAgIGRpc3BsYXk6IGdyaWQ7CiAgICAgICAgZ3JpZC10ZW1wbGF0ZS1jb2x1bW5zOiAxZnIgMWZyOwogICAgICAgIGdhcDogOHB4OwogICAgfQoKICAgIC5hZG0tc3RhdCB7CiAgICAgICAgYmFja2dyb3VuZDogdmFyKC0tYWRtLWJnLXNvZnQpOwogICAgICAgIGJvcmRlci1yYWRpdXM6IDhweDsKICAgICAgICBwYWRkaW5nOiAxMHB4OwogICAgICAgIHRleHQtYWxpZ246IGNlbnRlcjsKICAgIH0KCiAgICAuYWRtLXN0YXQgLnZhbHVlIHsgZm9udC1zaXplOiAxLjNyZW07IGZvbnQtd2VpZ2h0OiA3MDA7IGNvbG9yOiB2YXIoLS1hZG0tcHJpbWFyeSk7IH0KICAgIC5hZG0tc3RhdCAubGFiZWwgeyBmb250LXNpemU6IDAuNzVyZW07IGNvbG9yOiB2YXIoLS1hZG0tbXV0ZWQpOyBtYXJnaW4tdG9wOiAycHg7IH0KCiAgICAuYWRtLXJlbWluZGVyIHsKICAgICAgICBmb250LXNpemU6IDAuODZyZW07CiAgICAgICAgY29sb3I6ICM0NzU1Njk7CiAgICAgICAgcGFkZGluZzogN3B4IDA7CiAgICAgICAgYm9yZGVyLWJvdHRvbTogMXB4IHNvbGlkICNlZGYyZjc7CiAgICAgICAgbGluZS1oZWlnaHQ6IDEuNDU7CiAgICB9CgogICAgLmFkbS1yZW1pbmRlcjpsYXN0LWNoaWxkIHsgYm9yZGVyLWJvdHRvbTogbm9uZTsgfQoKICAgIC5hZG0tdXBsb2FkLXJvdyB7CiAgICAgICAgZGlzcGxheTogZmxleDsKICAgICAgICBmbGV4LXdyYXA6IHdyYXA7CiAgICAgICAgYWxpZ24taXRlbXM6IGNlbnRlcjsKICAgICAgICBqdXN0aWZ5LWNvbnRlbnQ6IHNwYWNlLWJldHdlZW47CiAgICAgICAgZ2FwOiA4cHg7CiAgICAgICAgcGFkZGluZzogOXB4IDA7CiAgICAgICAgYm9yZGVyLWJvdHRvbTogMXB4IHNvbGlkICNlZGYyZjc7CiAgICAgICAgZm9udC1zaXplOiAwLjg4cmVtOwogICAgfQoKICAgIC5hZG0tbG9nLWl0ZW0gewogICAgICAgIGZvbnQtc2l6ZTogMC44NHJlbTsKICAgICAgICBwYWRkaW5nOiA3cHggMDsKICAgICAgICBib3JkZXItYm90dG9tOiAxcHggc29saWQgI2VkZjJmNzsKICAgICAgICBjb2xvcjogIzQ3NTU2OTsKICAgIH0KCiAgICAuYWRtLXRhYnMgewogICAgICAgIGRpc3BsYXk6IGZsZXg7CiAgICAgICAgZmxleC13cmFwOiB3cmFwOwogICAgICAgIGdhcDogNnB4OwogICAgICAgIG1hcmdpbi1ib3R0b206IDE4cHg7CiAgICB9CgogICAgLmFkbS10YWJzIGEgewogICAgICAgIHBhZGRpbmc6IDhweCAxNHB4OwogICAgICAgIGJvcmRlci1yYWRpdXM6IDhweDsKICAgICAgICB0ZXh0LWRlY29yYXRpb246IG5vbmU7CiAgICAgICAgZm9udC1zaXplOiAwLjg4cmVtOwogICAgICAgIGZvbnQtd2VpZ2h0OiA2MDA7CiAgICAgICAgY29sb3I6IHZhcigtLWFkbS1wcmltYXJ5KTsKICAgICAgICBib3JkZXI6IDFweCBzb2xpZCB2YXIoLS1hZG0tYm9yZGVyKTsKICAgICAgICBiYWNrZ3JvdW5kOiB3aGl0ZTsKICAgIH0KCiAgICAuYWRtLXRhYnMgYS5hY3RpdmUgewogICAgICAgIGJhY2tncm91bmQ6IHZhcigtLWFkbS1hY2NlbnQpOwogICAgICAgIGNvbG9yOiB3aGl0ZTsKICAgICAgICBib3JkZXItY29sb3I6IHZhcigtLWFkbS1hY2NlbnQpOwogICAgfQoKICAgIC5hZG0tZWRpdC1ncmlkIHsKICAgICAgICB3aWR0aDogMTAwJTsKICAgICAgICBib3JkZXItY29sbGFwc2U6IGNvbGxhcHNlOwogICAgICAgIGZvbnQtc2l6ZTogMC44OHJlbTsKICAgIH0KCiAgICAuYWRtLWVkaXQtZ3JpZCB0aCwgLmFkbS1lZGl0LWdyaWQgdGQgewogICAgICAgIHBhZGRpbmc6IDhweCAxMHB4OwogICAgICAgIGJvcmRlci1ib3R0b206IDFweCBzb2xpZCAjZWRmMmY3OwogICAgICAgIHRleHQtYWxpZ246IGNlbnRlcjsKICAgIH0KCiAgICAuYWRtLWVkaXQtZ3JpZCB0aCB7CiAgICAgICAgYmFja2dyb3VuZDogdmFyKC0tYWRtLWJnLXNvZnQpOwogICAgICAgIGNvbG9yOiB2YXIoLS1hZG0tcHJpbWFyeSk7CiAgICAgICAgZm9udC13ZWlnaHQ6IDYwMDsKICAgIH0KCiAgICAuYWRtLWVkaXQtZ3JpZCB0aDpmaXJzdC1jaGlsZCwgLmFkbS1lZGl0LWdyaWQgdGQ6Zmlyc3QtY2hpbGQgewogICAgICAgIHRleHQtYWxpZ246IGxlZnQ7CiAgICAgICAgZm9udC13ZWlnaHQ6IDYwMDsKICAgIH0KCiAgICAuYWRtLWVkaXQtZ3JpZCBpbnB1dFt0eXBlPSJ0ZXh0Il0sCiAgICAuYWRtLWVkaXQtZ3JpZCBpbnB1dFt0eXBlPSJudW1iZXIiXSwKICAgIC5hZG0tZWRpdC1ncmlkIHNlbGVjdCwKICAgIC5hZG0tZWRpdC1ncmlkIHRleHRhcmVhIHsKICAgICAgICB3aWR0aDogMTAwJTsKICAgICAgICBtYXgtd2lkdGg6IDE0MHB4OwogICAgICAgIHBhZGRpbmc6IDZweCA4cHg7CiAgICAgICAgYm9yZGVyOiAxcHggc29saWQgdmFyKC0tYWRtLWJvcmRlcik7CiAgICAgICAgYm9yZGVyLXJhZGl1czogNnB4OwogICAgICAgIGZvbnQtc2l6ZTogMC44OHJlbTsKICAgIH0KCiAgICAuYWRtLWVkaXQtZ3JpZCB0ZXh0YXJlYSB7IG1heC13aWR0aDogMTAwJTsgbWluLWhlaWdodDogNjBweDsgfQoKICAgIC5hZG0tZm9ybS1mb290ZXIgewogICAgICAgIG1hcmdpbi10b3A6IDE4cHg7CiAgICAgICAgcGFkZGluZy10b3A6IDE2cHg7CiAgICAgICAgYm9yZGVyLXRvcDogMXB4IHNvbGlkICNlZGYyZjc7CiAgICAgICAgZGlzcGxheTogZmxleDsKICAgICAgICBmbGV4LXdyYXA6IHdyYXA7CiAgICAgICAgZ2FwOiAxMnB4OwogICAgICAgIGFsaWduLWl0ZW1zOiBlbmQ7CiAgICB9CgogICAgLmFkbS1mb3JtLWZvb3RlciBsYWJlbCB7IGZvbnQtc2l6ZTogMC44NXJlbTsgfQogICAgLmFkbS1mb3JtLWZvb3RlciBpbnB1dFt0eXBlPSJ0ZXh0Il0gewogICAgICAgIG1pbi13aWR0aDogMjIwcHg7CiAgICAgICAgcGFkZGluZzogOHB4IDEwcHg7CiAgICAgICAgYm9yZGVyOiAxcHggc29saWQgdmFyKC0tYWRtLWJvcmRlcik7CiAgICAgICAgYm9yZGVyLXJhZGl1czogNnB4OwogICAgfQoKICAgIC5hZG0tc2Nyb2xsIHsgb3ZlcmZsb3cteDogYXV0bzsgfQoKICAgIC5hZG0tYnJvd3NlLWdyaWQgdGQgaW5wdXRbdHlwZT0idGV4dCJdLAogICAgLmFkbS1icm93c2UtZ3JpZCB0ZCBpbnB1dFt0eXBlPSJudW1iZXIiXSwKICAgIC5hZG0tYnJvd3NlLWdyaWQgdGQgc2VsZWN0IHsKICAgICAgICBtaW4td2lkdGg6IDA7CiAgICAgICAgd2lkdGg6IDEwMCU7CiAgICAgICAgbWF4LXdpZHRoOiAxODBweDsKICAgIH0KCiAgICAuYWRtLWJyb3dzZS1uZXcgdGQgewogICAgICAgIGJhY2tncm91bmQ6ICNmMGZkZjk7CiAgICB9CgogICAgLmFkbS11bmUtbGVnZW5kIHsKICAgICAgICBkaXNwbGF5OiBmbGV4OwogICAgICAgIGZsZXgtd3JhcDogd3JhcDsKICAgICAgICBnYXA6IDEwcHggMTZweDsKICAgICAgICBtYXJnaW46IDAgMCAxNHB4OwogICAgICAgIGZvbnQtc2l6ZTogMC44OHJlbTsKICAgICAgICBjb2xvcjogdmFyKC0tYWRtLW11dGVkKTsKICAgIH0KCiAgICAuYWRtLXVuZS1sZWdlbmQtaXRlbSBzdHJvbmcgewogICAgICAgIGNvbG9yOiB2YXIoLS1hZG0tcHJpbWFyeSk7CiAgICAgICAgbWFyZ2luLXJpZ2h0OiA0cHg7CiAgICB9CgogICAgLmFkbS11bmUtZ3JpZCB0ZDpsYXN0LWNoaWxkIHsKICAgICAgICBtaW4td2lkdGg6IDQyMHB4OwogICAgfQoKICAgIC5hZG0tdW5lLXBpY2sgewogICAgICAgIGRpc3BsYXk6IGZsZXg7CiAgICAgICAgZmxleC13cmFwOiB3cmFwOwogICAgICAgIGdhcDogNnB4OwogICAgfQoKICAgIC5hZG0tdW5lLW9wdCB7CiAgICAgICAgZGlzcGxheTogaW5saW5lLWZsZXg7CiAgICAgICAgYWxpZ24taXRlbXM6IGNlbnRlcjsKICAgICAgICBnYXA6IDVweDsKICAgICAgICBwYWRkaW5nOiA2cHggOXB4OwogICAgICAgIGJvcmRlcjogMXB4IHNvbGlkIHZhcigtLWFkbS1ib3JkZXIpOwogICAgICAgIGJvcmRlci1yYWRpdXM6IDhweDsKICAgICAgICBiYWNrZ3JvdW5kOiAjZmZmOwogICAgICAgIGN1cnNvcjogcG9pbnRlcjsKICAgICAgICBmb250LXNpemU6IDAuOHJlbTsKICAgICAgICB1c2VyLXNlbGVjdDogbm9uZTsKICAgIH0KCiAgICAuYWRtLXVuZS1vcHQgaW5wdXQgewogICAgICAgIG1hcmdpbjogMDsKICAgIH0KCiAgICAuYWRtLXVuZS1vcHQgLmFkbS11bmUtc2hvcnQgewogICAgICAgIGZvbnQtd2VpZ2h0OiA3MDA7CiAgICAgICAgY29sb3I6IHZhcigtLWFkbS1wcmltYXJ5KTsKICAgICAgICBmb250LXZhcmlhbnQtbnVtZXJpYzogdGFidWxhci1udW1zOwogICAgfQoKICAgIC5hZG0tdW5lLW9wdCAuYWRtLXVuZS1uYW1lIHsKICAgICAgICBjb2xvcjogdmFyKC0tYWRtLW11dGVkKTsKICAgIH0KCiAgICAuYWRtLXVuZS1vcHQuaXMtY3VycmVudCB7CiAgICAgICAgYm9yZGVyLWNvbG9yOiAjOTlmNmU0OwogICAgICAgIGJhY2tncm91bmQ6ICNmMGZkZmE7CiAgICB9CgogICAgLmFkbS11bmUtb3B0OmhhcyhpbnB1dDpjaGVja2VkKSB7CiAgICAgICAgYm9yZGVyLWNvbG9yOiB2YXIoLS1hZG0tYWNjZW50KTsKICAgICAgICBiYWNrZ3JvdW5kOiAjY2NmYmYxOwogICAgICAgIGJveC1zaGFkb3c6IGluc2V0IDAgMCAwIDFweCB2YXIoLS1hZG0tYWNjZW50KTsKICAgIH0KCiAgICAuYWRtLXVuZS1vcHQ6aGFzKGlucHV0OmNoZWNrZWQpIC5hZG0tdW5lLW5hbWUgewogICAgICAgIGNvbG9yOiAjMTE1ZTU5OwogICAgICAgIGZvbnQtd2VpZ2h0OiA2MDA7CiAgICB9CgogICAgLmFkbS1wZXJpb2QtaGludCB7CiAgICAgICAgbWFyZ2luOiA4cHggMCAwOwogICAgICAgIGZvbnQtc2l6ZTogMC44NnJlbTsKICAgIH0KCiAgICAuYWRtLWJhbm5lciB7CiAgICAgICAgcGFkZGluZzogMTJweCAxNHB4OwogICAgICAgIGJvcmRlci1yYWRpdXM6IDhweDsKICAgICAgICBtYXJnaW46IDAgMCAxNHB4OwogICAgICAgIGZvbnQtc2l6ZTogMC45cmVtOwogICAgICAgIGJvcmRlcjogMXB4IHNvbGlkIHZhcigtLWFkbS1ib3JkZXIpOwogICAgfQogICAgLmFkbS1iYW5uZXItd2FybiB7IGJhY2tncm91bmQ6ICNmZmZiZWI7IGJvcmRlci1jb2xvcjogI2YwYzM2ZDsgY29sb3I6ICM5MjQwMGU7IH0KICAgIC5hZG0tYmFubmVyLWluZm8geyBiYWNrZ3JvdW5kOiAjZjBmZGZhOyBib3JkZXItY29sb3I6ICM5OWY2ZTQ7IGNvbG9yOiAjMTE1ZTU5OyB9CgogICAgLmFkbS1jdXJyZW5jeS10YWcgewogICAgICAgIGRpc3BsYXk6IGlubGluZS1ibG9jazsKICAgICAgICBmb250LXNpemU6IDAuNzJyZW07CiAgICAgICAgZm9udC13ZWlnaHQ6IDcwMDsKICAgICAgICBjb2xvcjogIzBmNzY2ZTsKICAgICAgICBiYWNrZ3JvdW5kOiAjY2NmYmYxOwogICAgICAgIHBhZGRpbmc6IDJweCA2cHg7CiAgICAgICAgYm9yZGVyLXJhZGl1czogNHB4OwogICAgfQoKICAgIC5hZG0taW5ncmVzb3MtY2VsbCB7CiAgICAgICAgYmFja2dyb3VuZDogI2Y4ZmZmZDsKICAgICAgICBtaW4td2lkdGg6IDE2MHB4OwogICAgICAgIHZlcnRpY2FsLWFsaWduOiB0b3A7CiAgICB9CiAgICAuYWRtLWluZ3Jlc29zLXN0YWNrIGlucHV0W3R5cGU9InRleHQiXSB7CiAgICAgICAgd2lkdGg6IDEwMCU7CiAgICAgICAgbWF4LXdpZHRoOiAxNjBweDsKICAgIH0KCiAgICAuYWRtLXJvdXRlLWhpbnQgewogICAgICAgIG1hcmdpbjogMCAwIDE0cHg7CiAgICAgICAgcGFkZGluZzogMTBweCAxNHB4OwogICAgICAgIGJhY2tncm91bmQ6ICNmOGZhZmM7CiAgICAgICAgYm9yZGVyOiAxcHggc29saWQgdmFyKC0tYWRtLWJvcmRlcik7CiAgICAgICAgYm9yZGVyLXJhZGl1czogOHB4OwogICAgICAgIGZvbnQtc2l6ZTogMC44OHJlbTsKICAgICAgICBjb2xvcjogIzMzNDE1NTsKICAgIH0KICAgIC5hZG0tY3VycmVuY3ktdG9nZ2xlIHsKICAgICAgICBkaXNwbGF5OiBmbGV4OwogICAgICAgIGdhcDogMTBweDsKICAgICAgICBtYXJnaW4tYm90dG9tOiA2cHg7CiAgICAgICAgZm9udC1zaXplOiAwLjgycmVtOwogICAgICAgIGZvbnQtd2VpZ2h0OiA2MDA7CiAgICB9CiAgICAuYWRtLWN1cnJlbmN5LXRvZ2dsZSBsYWJlbCB7CiAgICAgICAgZGlzcGxheTogaW5saW5lLWZsZXg7CiAgICAgICAgYWxpZ24taXRlbXM6IGNlbnRlcjsKICAgICAgICBnYXA6IDRweDsKICAgICAgICBjdXJzb3I6IHBvaW50ZXI7CiAgICB9CgogICAgLmFkbS15ZWFyLWluZ3Jlc29zIHRoLAogICAgLmFkbS15ZWFyLWluZ3Jlc29zIHRkIHsKICAgICAgICBtaW4td2lkdGg6IDExMHB4OwogICAgfQogICAgLmFkbS15ZWFyLWluZ3Jlc29zIGlucHV0W3R5cGU9InRleHQiXSB7CiAgICAgICAgd2lkdGg6IDEwMCU7CiAgICAgICAgbWF4LXdpZHRoOiAxNDBweDsKICAgICAgICBwYWRkaW5nOiA2cHggOHB4OwogICAgfQogICAgLmFkbS1jdXJyZW5jeS1iYXIgewogICAgICAgIGRpc3BsYXk6IGZsZXg7CiAgICAgICAgZmxleC13cmFwOiB3cmFwOwogICAgICAgIGdhcDogMTJweDsKICAgICAgICBhbGlnbi1pdGVtczogY2VudGVyOwogICAgICAgIHBhZGRpbmc6IDEwcHggMTJweDsKICAgICAgICBiYWNrZ3JvdW5kOiAjZjhmYWZjOwogICAgICAgIGJvcmRlcjogMXB4IHNvbGlkIHZhcigtLWFkbS1ib3JkZXIpOwogICAgICAgIGJvcmRlci1yYWRpdXM6IDhweDsKICAgICAgICBmb250LXNpemU6IDAuOXJlbTsKICAgIH0KCiAgICAvKiBDb2xvcmJsaW5kLWZyaWVuZGx5OiBodWUgKyBkYXJrIGJvcmRlciArIHN5bWJvbCAobm90IGNvbG9yIGFsb25lKSAqLwogICAgLmFkbS1uYXYtcmVjYWxjIHsKICAgICAgICBtYXJnaW4tbGVmdDogYXV0bzsKICAgICAgICBkaXNwbGF5OiBmbGV4OwogICAgICAgIGFsaWduLWl0ZW1zOiBjZW50ZXI7CiAgICB9CiAgICAuYWRtLXJlY2FsYy1mb3JtIHsgbWFyZ2luOiAwOyB9CiAgICAuYWRtLXJlY2FsYy1idG4gewogICAgICAgIGRpc3BsYXk6IGlubGluZS1mbGV4OwogICAgICAgIGFsaWduLWl0ZW1zOiBjZW50ZXI7CiAgICAgICAgZ2FwOiA4cHg7CiAgICAgICAgcGFkZGluZzogOHB4IDE0cHg7CiAgICAgICAgYm9yZGVyLXJhZGl1czogOHB4OwogICAgICAgIGJvcmRlcjogMnB4IHNvbGlkOwogICAgICAgIGZvbnQtd2VpZ2h0OiA3MDA7CiAgICAgICAgZm9udC1zaXplOiAwLjg4cmVtOwogICAgICAgIGN1cnNvcjogcG9pbnRlcjsKICAgICAgICBsaW5lLWhlaWdodDogMS4yOwogICAgICAgIHRyYW5zaXRpb246IHRyYW5zZm9ybSAwLjA4cyBlYXNlLCBib3gtc2hhZG93IDAuMTJzIGVhc2UsIGZpbHRlciAwLjEycyBlYXNlLCBvcGFjaXR5IDAuMTJzIGVhc2U7CiAgICAgICAgdXNlci1zZWxlY3Q6IG5vbmU7CiAgICB9CiAgICAuYWRtLXJlY2FsYy1idG46YWN0aXZlOm5vdCg6ZGlzYWJsZWQpIHsKICAgICAgICB0cmFuc2Zvcm06IHNjYWxlKDAuOTYpOwogICAgICAgIGJveC1zaGFkb3c6IGluc2V0IDAgMnB4IDZweCByZ2JhKDAsMCwwLDAuMTgpOwogICAgfQogICAgLmFkbS1yZWNhbGMtYnRuOmZvY3VzLXZpc2libGUgewogICAgICAgIG91dGxpbmU6IDNweCBzb2xpZCAjMzhiZGY4OwogICAgICAgIG91dGxpbmUtb2Zmc2V0OiAycHg7CiAgICB9CiAgICAuYWRtLXJlY2FsYy1idG4uaXMtcGVuZGluZyB7CiAgICAgICAgYmFja2dyb3VuZDogI0YzRThCODsgLyogcGFzdGVsIHllbGxvdyAqLwogICAgICAgIGJvcmRlci1jb2xvcjogIzhBNzM0MDsgLyogYnJvd24gZWRnZSAqLwogICAgICAgIGNvbG9yOiAjM0QzNDIwOwogICAgfQogICAgLmFkbS1yZWNhbGMtYnRuLmlzLXBlbmRpbmc6aG92ZXI6bm90KDpkaXNhYmxlZCkgewogICAgICAgIGJhY2tncm91bmQ6ICNFREUwQTA7CiAgICB9CiAgICAuYWRtLXJlY2FsYy1idG4uaXMtcmVhZHkgewogICAgICAgIGJhY2tncm91bmQ6ICNDOURGRDA7IC8qIHBhc3RlbCBncmVlbiAqLwogICAgICAgIGJvcmRlci1jb2xvcjogIzJGNkI0RjsgLyogZGFyayBncmVlbiBlZGdlICovCiAgICAgICAgY29sb3I6ICMxQTNEMkU7CiAgICB9CiAgICAuYWRtLXJlY2FsYy1idG4uaXMtcmVhZHk6aG92ZXI6bm90KDpkaXNhYmxlZCkgewogICAgICAgIGJhY2tncm91bmQ6ICNCN0Q0QzI7CiAgICB9CiAgICAuYWRtLXJlY2FsYy1idG4uaXMtd29ya2luZyB7CiAgICAgICAgY3Vyc29yOiB3YWl0OwogICAgICAgIG9wYWNpdHk6IDAuOTI7CiAgICAgICAgZmlsdGVyOiBzYXR1cmF0ZSgwLjg1KTsKICAgICAgICBib3gtc2hhZG93OiAwIDAgMCAzcHggcmdiYSgxNSwgMTE4LCAxMTAsIDAuMjUpOwogICAgfQogICAgLmFkbS1yZWNhbGMtYnRuLmlzLXdvcmtpbmcgLmFkbS1yZWNhbGMtc3ltYm9sIHsKICAgICAgICBkaXNwbGF5OiBub25lOwogICAgfQogICAgLmFkbS1yZWNhbGMtc3Bpbm5lciB7CiAgICAgICAgZGlzcGxheTogbm9uZTsKICAgICAgICB3aWR0aDogMTRweDsKICAgICAgICBoZWlnaHQ6IDE0cHg7CiAgICAgICAgYm9yZGVyOiAycHggc29saWQgY3VycmVudENvbG9yOwogICAgICAgIGJvcmRlci1yaWdodC1jb2xvcjogdHJhbnNwYXJlbnQ7CiAgICAgICAgYm9yZGVyLXJhZGl1czogNTAlOwogICAgICAgIGFuaW1hdGlvbjogYWRtLXJlY2FsYy1zcGluIDAuN3MgbGluZWFyIGluZmluaXRlOwogICAgICAgIGZsZXgtc2hyaW5rOiAwOwogICAgfQogICAgLmFkbS1yZWNhbGMtYnRuLmlzLXdvcmtpbmcgLmFkbS1yZWNhbGMtc3Bpbm5lciB7CiAgICAgICAgZGlzcGxheTogaW5saW5lLWJsb2NrOwogICAgfQogICAgQGtleWZyYW1lcyBhZG0tcmVjYWxjLXNwaW4gewogICAgICAgIHRvIHsgdHJhbnNmb3JtOiByb3RhdGUoMzYwZGVnKTsgfQogICAgfQogICAgLmFkbS1yZWNhbGMtc3ltYm9sIHsKICAgICAgICBmb250LXNpemU6IDEuMDVyZW07CiAgICAgICAgZm9udC13ZWlnaHQ6IDgwMDsKICAgIH0KICAgIC5hZG0tcmVjYWxjLWNvdW50IHsgZm9udC13ZWlnaHQ6IDgwMDsgfQogICAgLmFkbS1yZWNhbGMtZGV0YWlscyB7CiAgICAgICAgbWFyZ2luOiA4cHggMCAxMnB4OwogICAgICAgIHBhZGRpbmc6IDhweCAxMnB4OwogICAgICAgIGJhY2tncm91bmQ6ICNGN0YxRDg7CiAgICAgICAgYm9yZGVyOiAxcHggZGFzaGVkICM4QTczNDA7CiAgICAgICAgYm9yZGVyLXJhZGl1czogOHB4OwogICAgICAgIGZvbnQtc2l6ZTogMC44NXJlbTsKICAgICAgICBjb2xvcjogIzNEMzQyMDsKICAgIH0KICAgIC5hZG0tcmVjYWxjLWRldGFpbHMgdWwgewogICAgICAgIG1hcmdpbjogOHB4IDAgMDsKICAgICAgICBwYWRkaW5nLWxlZnQ6IDE4cHg7CiAgICB9Cjwvc3R5bGU+Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgc/admin_ingresos_year.html
PATH_JSON="templates/pgc/admin_ingresos_year.html"
FILENAME=admin_ingresos_year.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=134
SIZE_BYTES_UTF8=6751
CONTENT_SHA256=05fdcab72ca2d34a7bb5d17a6d994ef0900ebf1e602c5371757e5b52cb7a052b
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~html
{% extends "base.html" %}
{% load l10n %}

{% block title %}Ingresos anuales {{ year }}{% endblock %}

{% block content %}
{% include "pgc/admin/_styles.html" %}

<div class="adm">
    {% include "pgc/admin/_nav.html" with adm_nav_active="ingresos_year" %}

    <div class="adm-header">
        <div class="adm-header-top">
            <div>
                <p class="muted" style="margin:0;">Captura de ingresos reales · año completo</p>
                <div class="adm-period-label">{{ year }}</div>
                {% if not plan %}<p class="muted" style="color:#b45309;">No hay plan PGC para este año.</p>{% endif %}
            </div>
            {% include "pgc/admin/_period_select.html" %}
        </div>
    </div>

    <div class="adm-panel">
        <h3 style="margin-top:0;">Ingresos por UNE · enero a diciembre</h3>
        <p class="subtitle">
            Columnas = las 4 UNEs. Filas = 12 meses fijos.
            Elija moneda de captura (<strong>Q</strong> o <strong>$</strong>); lo guardado canónico es siempre <strong>USD</strong>.
            La 5.ª columna es el tipo de cambio del mes (1 USD = X GTQ), editable.
        </p>

        <form method="get" class="adm-currency-bar" style="margin-bottom:14px;">
            <input type="hidden" name="year" value="{{ year }}">
            <input type="hidden" name="month_from" value="{{ month_from }}">
            <input type="hidden" name="month_to" value="{{ month_to }}">
            <input type="hidden" name="month" value="{{ month }}">
            <label style="font-weight:600;">Moneda de captura:</label>
            <label>
                <input type="radio" name="curr" value="GTQ" {% if capture_currency == "GTQ" %}checked{% endif %}
                       onchange="this.form.submit()"> Q (GTQ)
            </label>
            <label>
                <input type="radio" name="curr" value="USD" {% if capture_currency == "USD" %}checked{% endif %}
                       onchange="this.form.submit()"> $ (USD)
            </label>
            <span class="muted" style="margin-left:8px;">
                {% if capture_currency == "GTQ" %}
                Conversión: <code>GTQ ÷ TC del mes → USD</code>
                {% else %}
                Se guarda directo en USD (sin TC).
                {% endif %}
            </span>
        </form>

        {% if capture_currency == "GTQ" and missing_fx_months %}
        <div class="adm-banner adm-banner-warn">
            Falta TC en: {% for m in missing_fx_months %}<code style="margin-right:6px;">{{ m }}</code>{% endfor %}
            Complete la columna TC antes de capturar ingresos en Q en esos meses (o capture en $).
        </div>
        {% endif %}

        <form method="post">
            {% csrf_token %}
            <input type="hidden" name="action" value="save_ingresos_year">
            <input type="hidden" name="year" value="{{ year }}">
            <input type="hidden" name="month" value="{{ month }}">
            <input type="hidden" name="month_from" value="{{ month_from }}">
            <input type="hidden" name="month_to" value="{{ month_to }}">
            <input type="hidden" name="capture_currency" value="{{ capture_currency }}">

            <div class="adm-scroll">
                <table class="adm-edit-grid adm-year-ingresos">
                    <thead>
                        <tr>
                            <th>Mes</th>
                            {% for une in unes %}
                            <th>
                                {{ une.name_es }}<br>
                                <span class="adm-currency-tag">
                                    {% if capture_currency == "GTQ" %}captura Q → USD{% else %}captura $ (USD){% endif %}
                                </span>
                            </th>
                            {% endfor %}
                            <th>
                                TC<br>
                                <span class="adm-currency-tag">1 USD = … GTQ</span>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in month_rows %}
                        <tr>
                            <td style="text-align:left; white-space:nowrap;">
                                <strong>{{ row.label }}</strong>
                                <span class="muted"> {{ year }}-{{ row.month|stringformat:"02d" }}</span>
                            </td>
                            {% for cell in row.cells %}
                            <td class="adm-ingresos-cell">
                                <input type="text"
                                       inputmode="decimal"
                                       name="ing_{{ row.month }}_{{ cell.une.id }}"
                                       value="{% if cell.value is not None %}{{ cell.value|unlocalize }}{% endif %}"
                                       placeholder="{% if capture_currency == 'USD' %}${% else %}Q{% endif %}"
                                       {% if cell.input_disabled %}title="Sin TC guardado aún: complete la columna TC en este mismo envío, o capture en $"{% endif %}>
                                {% if cell.measured_usd_display %}
                                <div class="muted" style="font-size:0.72rem; margin-top:3px;">
                                    USD: {{ cell.measured_usd_display }}
                                    {% if cell.conversion_status == "STALE_FX" %}
                                    · <span style="color:#b45309;">TC viejo</span>
                                    {% endif %}
                                </div>
                                {% endif %}
                            </td>
                            {% endfor %}
                            <td>
                                <input type="text"
                                       inputmode="decimal"
                                       name="fx_{{ row.month }}"
                                       value="{% if row.fx_value is not None %}{{ row.fx_value|unlocalize }}{% endif %}"
                                       placeholder="ej. 7.85"
                                       style="width:90px;">
                                {% if not row.has_fx %}
                                <div class="muted" style="font-size:0.72rem; color:#b45309;">sin TC</div>
                                {% endif %}
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>

            {% include "pgc/admin/_save_footer.html" with reason_required=True %}
    </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base.html" %}
00002|{% load l10n %}
00003|
00004|{% block title %}Ingresos anuales {{ year }}{% endblock %}
00005|
00006|{% block content %}
00007|{% include "pgc/admin/_styles.html" %}
00008|
00009|<div class="adm">
00010|    {% include "pgc/admin/_nav.html" with adm_nav_active="ingresos_year" %}
00011|
00012|    <div class="adm-header">
00013|        <div class="adm-header-top">
00014|            <div>
00015|                <p class="muted" style="margin:0;">Captura de ingresos reales · año completo</p>
00016|                <div class="adm-period-label">{{ year }}</div>
00017|                {% if not plan %}<p class="muted" style="color:#b45309;">No hay plan PGC para este año.</p>{% endif %}
00018|            </div>
00019|            {% include "pgc/admin/_period_select.html" %}
00020|        </div>
00021|    </div>
00022|
00023|    <div class="adm-panel">
00024|        <h3 style="margin-top:0;">Ingresos por UNE · enero a diciembre</h3>
00025|        <p class="subtitle">
00026|            Columnas = las 4 UNEs. Filas = 12 meses fijos.
00027|            Elija moneda de captura (<strong>Q</strong> o <strong>$</strong>); lo guardado canónico es siempre <strong>USD</strong>.
00028|            La 5.ª columna es el tipo de cambio del mes (1 USD = X GTQ), editable.
00029|        </p>
00030|
00031|        <form method="get" class="adm-currency-bar" style="margin-bottom:14px;">
00032|            <input type="hidden" name="year" value="{{ year }}">
00033|            <input type="hidden" name="month_from" value="{{ month_from }}">
00034|            <input type="hidden" name="month_to" value="{{ month_to }}">
00035|            <input type="hidden" name="month" value="{{ month }}">
00036|            <label style="font-weight:600;">Moneda de captura:</label>
00037|            <label>
00038|                <input type="radio" name="curr" value="GTQ" {% if capture_currency == "GTQ" %}checked{% endif %}
00039|                       onchange="this.form.submit()"> Q (GTQ)
00040|            </label>
00041|            <label>
00042|                <input type="radio" name="curr" value="USD" {% if capture_currency == "USD" %}checked{% endif %}
00043|                       onchange="this.form.submit()"> $ (USD)
00044|            </label>
00045|            <span class="muted" style="margin-left:8px;">
00046|                {% if capture_currency == "GTQ" %}
00047|                Conversión: <code>GTQ ÷ TC del mes → USD</code>
00048|                {% else %}
00049|                Se guarda directo en USD (sin TC).
00050|                {% endif %}
00051|            </span>
00052|        </form>
00053|
00054|        {% if capture_currency == "GTQ" and missing_fx_months %}
00055|        <div class="adm-banner adm-banner-warn">
00056|            Falta TC en: {% for m in missing_fx_months %}<code style="margin-right:6px;">{{ m }}</code>{% endfor %}
00057|            Complete la columna TC antes de capturar ingresos en Q en esos meses (o capture en $).
00058|        </div>
00059|        {% endif %}
00060|
00061|        <form method="post">
00062|            {% csrf_token %}
00063|            <input type="hidden" name="action" value="save_ingresos_year">
00064|            <input type="hidden" name="year" value="{{ year }}">
00065|            <input type="hidden" name="month" value="{{ month }}">
00066|            <input type="hidden" name="month_from" value="{{ month_from }}">
00067|            <input type="hidden" name="month_to" value="{{ month_to }}">
00068|            <input type="hidden" name="capture_currency" value="{{ capture_currency }}">
00069|
00070|            <div class="adm-scroll">
00071|                <table class="adm-edit-grid adm-year-ingresos">
00072|                    <thead>
00073|                        <tr>
00074|                            <th>Mes</th>
00075|                            {% for une in unes %}
00076|                            <th>
00077|                                {{ une.name_es }}<br>
00078|                                <span class="adm-currency-tag">
00079|                                    {% if capture_currency == "GTQ" %}captura Q → USD{% else %}captura $ (USD){% endif %}
00080|                                </span>
00081|                            </th>
00082|                            {% endfor %}
00083|                            <th>
00084|                                TC<br>
00085|                                <span class="adm-currency-tag">1 USD = … GTQ</span>
00086|                            </th>
00087|                        </tr>
00088|                    </thead>
00089|                    <tbody>
00090|                        {% for row in month_rows %}
00091|                        <tr>
00092|                            <td style="text-align:left; white-space:nowrap;">
00093|                                <strong>{{ row.label }}</strong>
00094|                                <span class="muted"> {{ year }}-{{ row.month|stringformat:"02d" }}</span>
00095|                            </td>
00096|                            {% for cell in row.cells %}
00097|                            <td class="adm-ingresos-cell">
00098|                                <input type="text"
00099|                                       inputmode="decimal"
00100|                                       name="ing_{{ row.month }}_{{ cell.une.id }}"
00101|                                       value="{% if cell.value is not None %}{{ cell.value|unlocalize }}{% endif %}"
00102|                                       placeholder="{% if capture_currency == 'USD' %}${% else %}Q{% endif %}"
00103|                                       {% if cell.input_disabled %}title="Sin TC guardado aún: complete la columna TC en este mismo envío, o capture en $"{% endif %}>
00104|                                {% if cell.measured_usd_display %}
00105|                                <div class="muted" style="font-size:0.72rem; margin-top:3px;">
00106|                                    USD: {{ cell.measured_usd_display }}
00107|                                    {% if cell.conversion_status == "STALE_FX" %}
00108|                                    · <span style="color:#b45309;">TC viejo</span>
00109|                                    {% endif %}
00110|                                </div>
00111|                                {% endif %}
00112|                            </td>
00113|                            {% endfor %}
00114|                            <td>
00115|                                <input type="text"
00116|                                       inputmode="decimal"
00117|                                       name="fx_{{ row.month }}"
00118|                                       value="{% if row.fx_value is not None %}{{ row.fx_value|unlocalize }}{% endif %}"
00119|                                       placeholder="ej. 7.85"
00120|                                       style="width:90px;">
00121|                                {% if not row.has_fx %}
00122|                                <div class="muted" style="font-size:0.72rem; color:#b45309;">sin TC</div>
00123|                                {% endif %}
00124|                            </td>
00125|                        </tr>
00126|                        {% endfor %}
00127|                    </tbody>
00128|                </table>
00129|            </div>
00130|
00131|            {% include "pgc/admin/_save_footer.html" with reason_required=True %}
00132|    </div>
00133|</div>
00134|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZS5odG1sIiAlfQp7JSBsb2FkIGwxMG4gJX0KCnslIGJsb2NrIHRpdGxlICV9SW5ncmVzb3MgYW51YWxlcyB7eyB5ZWFyIH19eyUgZW5kYmxvY2sgJX0KCnslIGJsb2NrIGNvbnRlbnQgJX0KeyUgaW5jbHVkZSAicGdjL2FkbWluL19zdHlsZXMuaHRtbCIgJX0KCjxkaXYgY2xhc3M9ImFkbSI+CiAgICB7JSBpbmNsdWRlICJwZ2MvYWRtaW4vX25hdi5odG1sIiB3aXRoIGFkbV9uYXZfYWN0aXZlPSJpbmdyZXNvc195ZWFyIiAlfQoKICAgIDxkaXYgY2xhc3M9ImFkbS1oZWFkZXIiPgogICAgICAgIDxkaXYgY2xhc3M9ImFkbS1oZWFkZXItdG9wIj4KICAgICAgICAgICAgPGRpdj4KICAgICAgICAgICAgICAgIDxwIGNsYXNzPSJtdXRlZCIgc3R5bGU9Im1hcmdpbjowOyI+Q2FwdHVyYSBkZSBpbmdyZXNvcyByZWFsZXMgwrcgYcOxbyBjb21wbGV0bzwvcD4KICAgICAgICAgICAgICAgIDxkaXYgY2xhc3M9ImFkbS1wZXJpb2QtbGFiZWwiPnt7IHllYXIgfX08L2Rpdj4KICAgICAgICAgICAgICAgIHslIGlmIG5vdCBwbGFuICV9PHAgY2xhc3M9Im11dGVkIiBzdHlsZT0iY29sb3I6I2I0NTMwOTsiPk5vIGhheSBwbGFuIFBHQyBwYXJhIGVzdGUgYcOxby48L3A+eyUgZW5kaWYgJX0KICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICAgIHslIGluY2x1ZGUgInBnYy9hZG1pbi9fcGVyaW9kX3NlbGVjdC5odG1sIiAlfQogICAgICAgIDwvZGl2PgogICAgPC9kaXY+CgogICAgPGRpdiBjbGFzcz0iYWRtLXBhbmVsIj4KICAgICAgICA8aDMgc3R5bGU9Im1hcmdpbi10b3A6MDsiPkluZ3Jlc29zIHBvciBVTkUgwrcgZW5lcm8gYSBkaWNpZW1icmU8L2gzPgogICAgICAgIDxwIGNsYXNzPSJzdWJ0aXRsZSI+CiAgICAgICAgICAgIENvbHVtbmFzID0gbGFzIDQgVU5Fcy4gRmlsYXMgPSAxMiBtZXNlcyBmaWpvcy4KICAgICAgICAgICAgRWxpamEgbW9uZWRhIGRlIGNhcHR1cmEgKDxzdHJvbmc+UTwvc3Ryb25nPiBvIDxzdHJvbmc+JDwvc3Ryb25nPik7IGxvIGd1YXJkYWRvIGNhbsOzbmljbyBlcyBzaWVtcHJlIDxzdHJvbmc+VVNEPC9zdHJvbmc+LgogICAgICAgICAgICBMYSA1LsKqIGNvbHVtbmEgZXMgZWwgdGlwbyBkZSBjYW1iaW8gZGVsIG1lcyAoMSBVU0QgPSBYIEdUUSksIGVkaXRhYmxlLgogICAgICAgIDwvcD4KCiAgICAgICAgPGZvcm0gbWV0aG9kPSJnZXQiIGNsYXNzPSJhZG0tY3VycmVuY3ktYmFyIiBzdHlsZT0ibWFyZ2luLWJvdHRvbToxNHB4OyI+CiAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9InllYXIiIHZhbHVlPSJ7eyB5ZWFyIH19Ij4KICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ibW9udGhfZnJvbSIgdmFsdWU9Int7IG1vbnRoX2Zyb20gfX0iPgogICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aF90byIgdmFsdWU9Int7IG1vbnRoX3RvIH19Ij4KICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ibW9udGgiIHZhbHVlPSJ7eyBtb250aCB9fSI+CiAgICAgICAgICAgIDxsYWJlbCBzdHlsZT0iZm9udC13ZWlnaHQ6NjAwOyI+TW9uZWRhIGRlIGNhcHR1cmE6PC9sYWJlbD4KICAgICAgICAgICAgPGxhYmVsPgogICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9InJhZGlvIiBuYW1lPSJjdXJyIiB2YWx1ZT0iR1RRIiB7JSBpZiBjYXB0dXJlX2N1cnJlbmN5ID09ICJHVFEiICV9Y2hlY2tlZHslIGVuZGlmICV9CiAgICAgICAgICAgICAgICAgICAgICAgb25jaGFuZ2U9InRoaXMuZm9ybS5zdWJtaXQoKSI+IFEgKEdUUSkKICAgICAgICAgICAgPC9sYWJlbD4KICAgICAgICAgICAgPGxhYmVsPgogICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9InJhZGlvIiBuYW1lPSJjdXJyIiB2YWx1ZT0iVVNEIiB7JSBpZiBjYXB0dXJlX2N1cnJlbmN5ID09ICJVU0QiICV9Y2hlY2tlZHslIGVuZGlmICV9CiAgICAgICAgICAgICAgICAgICAgICAgb25jaGFuZ2U9InRoaXMuZm9ybS5zdWJtaXQoKSI+ICQgKFVTRCkKICAgICAgICAgICAgPC9sYWJlbD4KICAgICAgICAgICAgPHNwYW4gY2xhc3M9Im11dGVkIiBzdHlsZT0ibWFyZ2luLWxlZnQ6OHB4OyI+CiAgICAgICAgICAgICAgICB7JSBpZiBjYXB0dXJlX2N1cnJlbmN5ID09ICJHVFEiICV9CiAgICAgICAgICAgICAgICBDb252ZXJzacOzbjogPGNvZGU+R1RRIMO3IFRDIGRlbCBtZXMg4oaSIFVTRDwvY29kZT4KICAgICAgICAgICAgICAgIHslIGVsc2UgJX0KICAgICAgICAgICAgICAgIFNlIGd1YXJkYSBkaXJlY3RvIGVuIFVTRCAoc2luIFRDKS4KICAgICAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgIDwvc3Bhbj4KICAgICAgICA8L2Zvcm0+CgogICAgICAgIHslIGlmIGNhcHR1cmVfY3VycmVuY3kgPT0gIkdUUSIgYW5kIG1pc3NpbmdfZnhfbW9udGhzICV9CiAgICAgICAgPGRpdiBjbGFzcz0iYWRtLWJhbm5lciBhZG0tYmFubmVyLXdhcm4iPgogICAgICAgICAgICBGYWx0YSBUQyBlbjogeyUgZm9yIG0gaW4gbWlzc2luZ19meF9tb250aHMgJX08Y29kZSBzdHlsZT0ibWFyZ2luLXJpZ2h0OjZweDsiPnt7IG0gfX08L2NvZGU+eyUgZW5kZm9yICV9CiAgICAgICAgICAgIENvbXBsZXRlIGxhIGNvbHVtbmEgVEMgYW50ZXMgZGUgY2FwdHVyYXIgaW5ncmVzb3MgZW4gUSBlbiBlc29zIG1lc2VzIChvIGNhcHR1cmUgZW4gJCkuCiAgICAgICAgPC9kaXY+CiAgICAgICAgeyUgZW5kaWYgJX0KCiAgICAgICAgPGZvcm0gbWV0aG9kPSJwb3N0Ij4KICAgICAgICAgICAgeyUgY3NyZl90b2tlbiAlfQogICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJhY3Rpb24iIHZhbHVlPSJzYXZlX2luZ3Jlc29zX3llYXIiPgogICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJ5ZWFyIiB2YWx1ZT0ie3sgeWVhciB9fSI+CiAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9Im1vbnRoIiB2YWx1ZT0ie3sgbW9udGggfX0iPgogICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aF9mcm9tIiB2YWx1ZT0ie3sgbW9udGhfZnJvbSB9fSI+CiAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9Im1vbnRoX3RvIiB2YWx1ZT0ie3sgbW9udGhfdG8gfX0iPgogICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJjYXB0dXJlX2N1cnJlbmN5IiB2YWx1ZT0ie3sgY2FwdHVyZV9jdXJyZW5jeSB9fSI+CgogICAgICAgICAgICA8ZGl2IGNsYXNzPSJhZG0tc2Nyb2xsIj4KICAgICAgICAgICAgICAgIDx0YWJsZSBjbGFzcz0iYWRtLWVkaXQtZ3JpZCBhZG0teWVhci1pbmdyZXNvcyI+CiAgICAgICAgICAgICAgICAgICAgPHRoZWFkPgogICAgICAgICAgICAgICAgICAgICAgICA8dHI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGg+TWVzPC90aD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGZvciB1bmUgaW4gdW5lcyAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRoPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHt7IHVuZS5uYW1lX2VzIH19PGJyPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJhZG0tY3VycmVuY3ktdGFnIj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgaWYgY2FwdHVyZV9jdXJyZW5jeSA9PSAiR1RRIiAlfWNhcHR1cmEgUSDihpIgVVNEeyUgZWxzZSAlfWNhcHR1cmEgJCAoVVNEKXslIGVuZGlmICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC9zcGFuPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90aD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRoPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIFRDPGJyPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJhZG0tY3VycmVuY3ktdGFnIj4xIFVTRCA9IOKApiBHVFE8L3NwYW4+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RoPgogICAgICAgICAgICAgICAgICAgICAgICA8L3RyPgogICAgICAgICAgICAgICAgICAgIDwvdGhlYWQ+CiAgICAgICAgICAgICAgICAgICAgPHRib2R5PgogICAgICAgICAgICAgICAgICAgICAgICB7JSBmb3Igcm93IGluIG1vbnRoX3Jvd3MgJX0KICAgICAgICAgICAgICAgICAgICAgICAgPHRyPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkIHN0eWxlPSJ0ZXh0LWFsaWduOmxlZnQ7IHdoaXRlLXNwYWNlOm5vd3JhcDsiPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxzdHJvbmc+e3sgcm93LmxhYmVsIH19PC9zdHJvbmc+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHNwYW4gY2xhc3M9Im11dGVkIj4ge3sgeWVhciB9fS17eyByb3cubW9udGh8c3RyaW5nZm9ybWF0OiIwMmQiIH19PC9zcGFuPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGZvciBjZWxsIGluIHJvdy5jZWxscyAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkIGNsYXNzPSJhZG0taW5ncmVzb3MtY2VsbCI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9InRleHQiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlucHV0bW9kZT0iZGVjaW1hbCIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgbmFtZT0iaW5nX3t7IHJvdy5tb250aCB9fV97eyBjZWxsLnVuZS5pZCB9fSIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdmFsdWU9InslIGlmIGNlbGwudmFsdWUgaXMgbm90IE5vbmUgJX17eyBjZWxsLnZhbHVlfHVubG9jYWxpemUgfX17JSBlbmRpZiAlfSIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgcGxhY2Vob2xkZXI9InslIGlmIGNhcHR1cmVfY3VycmVuY3kgPT0gJ1VTRCcgJX0keyUgZWxzZSAlfVF7JSBlbmRpZiAlfSIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgaWYgY2VsbC5pbnB1dF9kaXNhYmxlZCAlfXRpdGxlPSJTaW4gVEMgZ3VhcmRhZG8gYcO6bjogY29tcGxldGUgbGEgY29sdW1uYSBUQyBlbiBlc3RlIG1pc21vIGVudsOtbywgbyBjYXB0dXJlIGVuICQieyUgZW5kaWYgJX0+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgaWYgY2VsbC5tZWFzdXJlZF91c2RfZGlzcGxheSAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxkaXYgY2xhc3M9Im11dGVkIiBzdHlsZT0iZm9udC1zaXplOjAuNzJyZW07IG1hcmdpbi10b3A6M3B4OyI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIFVTRDoge3sgY2VsbC5tZWFzdXJlZF91c2RfZGlzcGxheSB9fQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiBjZWxsLmNvbnZlcnNpb25fc3RhdHVzID09ICJTVEFMRV9GWCIgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgwrcgPHNwYW4gc3R5bGU9ImNvbG9yOiNiNDUzMDk7Ij5UQyB2aWVqbzwvc3Bhbj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L2Rpdj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJ0ZXh0IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBpbnB1dG1vZGU9ImRlY2ltYWwiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIG5hbWU9ImZ4X3t7IHJvdy5tb250aCB9fSIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdmFsdWU9InslIGlmIHJvdy5meF92YWx1ZSBpcyBub3QgTm9uZSAlfXt7IHJvdy5meF92YWx1ZXx1bmxvY2FsaXplIH19eyUgZW5kaWYgJX0iCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHBsYWNlaG9sZGVyPSJlai4gNy44NSIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgc3R5bGU9IndpZHRoOjkwcHg7Ij4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiBub3Qgcm93Lmhhc19meCAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxkaXYgY2xhc3M9Im11dGVkIiBzdHlsZT0iZm9udC1zaXplOjAuNzJyZW07IGNvbG9yOiNiNDUzMDk7Ij5zaW4gVEM8L2Rpdj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgPC90cj4KICAgICAgICAgICAgICAgICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgICAgICAgICAgICAgPC90Ym9keT4KICAgICAgICAgICAgICAgIDwvdGFibGU+CiAgICAgICAgICAgIDwvZGl2PgoKICAgICAgICAgICAgeyUgaW5jbHVkZSAicGdjL2FkbWluL19zYXZlX2Zvb3Rlci5odG1sIiB3aXRoIHJlYXNvbl9yZXF1aXJlZD1UcnVlICV9CiAgICA8L2Rpdj4KPC9kaXY+CnslIGVuZGJsb2NrICV9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgc/admin_manual_edit.html
PATH_JSON="templates/pgc/admin_manual_edit.html"
FILENAME=admin_manual_edit.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=491
SIZE_BYTES_UTF8=29531
CONTENT_SHA256=705c9f6acb45f1774e5ede2c574d6842fafcaa7ae3accd701bbb8dca7e4ff170
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~html
{% extends "base.html" %}
{% load l10n %}

{% block title %}Edición manual — {{ label }}{% endblock %}

{% block content %}
{% include "pgc/admin/_styles.html" %}

<div class="adm">
    {% include "pgc/admin/_nav.html" with adm_nav_active="manual" %}

    <div class="adm-header">
        <div class="adm-header-top">
            <div>
                <p class="muted" style="margin:0;">Edición manual del período</p>
                <div class="adm-period-label">{{ label }}</div>
                {% if not plan %}<p class="muted" style="color:#b45309;">No hay plan PGC para este año.</p>{% endif %}
            </div>
            {% include "pgc/admin/_period_select.html" %}
        </div>
    </div>

    <div class="adm-route-hint">
        <strong>Ruta sugerida:</strong>
        Tipos de cambio → Metas (USD) → Resultados (ingresos Q o $ → se guardan en USD).
        Metas/resultados usan el mes foco <code>{{ focus_label }}</code>; el TC usa el rango completo.
    </div>

    <div class="adm-tabs">
        {% for tab_id, tab_label in tabs %}
        <a href="?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}&tab={{ tab_id }}"
           class="{% if tab == tab_id %}active{% endif %}">{{ tab_label }}</a>
        {% endfor %}
    </div>

    <div class="adm-layout">
        <div>
            <div class="adm-panel">
                {% if tab == "targets" %}
                <h3>Metas mensuales · {{ focus_label }}</h3>
                <p class="subtitle">
                    Metas de <strong>Ingresos en USD ($)</strong>. Las demás métricas son cantidades / cumplimiento, no moneda.
                    Deje vacío para no modificar.
                </p>
                <form method="post">
                    {% csrf_token %}
                    <input type="hidden" name="action" value="save_targets">
                    <input type="hidden" name="year" value="{{ year }}">
                    <input type="hidden" name="month" value="{{ month }}">
                    <input type="hidden" name="month_from" value="{{ month_from }}">
                    <input type="hidden" name="month_to" value="{{ month_to }}">
                    <input type="hidden" name="tab" value="{{ tab }}">
                    <div class="adm-scroll">
                        <table class="adm-edit-grid">
                            <thead>
                                <tr>
                                    <th>UNE</th>
                                    {% for metric in metrics %}
                                    <th>
                                        {% if metric.code == "INGRESOS" %}
                                        {{ metric.name }}<br><span class="adm-currency-tag">USD ($)</span>
                                        {% else %}
                                        {{ metric.name }}
                                        {% endif %}
                                    </th>
                                    {% endfor %}
                                </tr>
                            </thead>
                            <tbody>
                                {% for row in target_rows %}
                                <tr>
                                    <td>{{ row.une.name_es }}</td>
                                    {% for cell in row.cells %}
                                    <td>
                                        <input type="number" step="0.01"
                                               name="target_{{ row.une.id }}_{{ cell.metric.id }}"
                                               value="{% if cell.value is not None %}{{ cell.value|unlocalize }}{% endif %}">
                                    </td>
                                    {% endfor %}
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    {% include "pgc/admin/_save_footer.html" with reason_required=False %}

                {% elif tab == "results" %}
                <h3>Resultados mensuales · {{ focus_label }}</h3>
                <p class="subtitle">
                    <strong>Ingresos</strong>: elija <strong>Q</strong> o <strong>$</strong> por UNE.
                    Si captura en Q, se convierte a USD con el TC del mes y se guarda el USD canónico.
                    Si captura en $, se guarda directo en USD (sin TC). Las demás métricas no son moneda.
                </p>

                {% if not has_fx %}
                <div class="adm-banner adm-banner-warn">
                    <strong>Falta tipo de cambio para {{ focus_label }}.</strong>
                    Sin TC no se pueden guardar ingresos en quetzales (Q). Sí se puede capturar en dólares ($).
                    <a href="?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}&tab=fx"
                       class="adm-btn adm-btn-secondary" style="margin-left:8px;">Ir a tipos de cambio</a>
                </div>
                {% else %}
                <div class="adm-banner adm-banner-info">
                    TC del período {{ focus_label }}: <strong>1 USD = {{ fx_rate }} GTQ</strong>.
                    Conversión: <code>GTQ ÷ TC → USD</code>.
                </div>
                {% endif %}

                {% if stale_ingresos_count %}
                <div class="adm-banner adm-banner-warn">
                    <strong>{{ stale_ingresos_count }} ingreso(s) con TC desactualizado (STALE).</strong>
                    El tipo de cambio cambió después de la captura en Q.
                    <form method="post" style="display:inline; margin-left:8px;">
                        {% csrf_token %}
                        <input type="hidden" name="action" value="recalc_stale_ingresos">
                        <input type="hidden" name="year" value="{{ year }}">
                        <input type="hidden" name="month" value="{{ month }}">
                        <input type="hidden" name="month_from" value="{{ month_from }}">
                        <input type="hidden" name="month_to" value="{{ month_to }}">
                        <input type="hidden" name="tab" value="{{ tab }}">
                        <input type="hidden" name="reason" value="Recálculo STALE desde resultados">
                        <button type="submit" class="adm-btn adm-btn-primary">Recalcular USD desde GTQ</button>
                    </form>
                </div>
                {% endif %}

                <form method="post">
                    {% csrf_token %}
                    <input type="hidden" name="action" value="save_results">
                    <input type="hidden" name="year" value="{{ year }}">
                    <input type="hidden" name="month" value="{{ month }}">
                    <input type="hidden" name="month_from" value="{{ month_from }}">
                    <input type="hidden" name="month_to" value="{{ month_to }}">
                    <input type="hidden" name="tab" value="{{ tab }}">
                    <div class="adm-scroll">
                        <table class="adm-edit-grid">
                            <thead>
                                <tr>
                                    <th>UNE</th>
                                    {% for metric in metrics %}
                                    <th>
                                        {% if metric.code == "INGRESOS" %}
                                        {{ metric.name }} (guardado USD)<br>
                                        <span class="adm-currency-tag">captura Q o $</span>
                                        {% else %}
                                        {{ metric.name }}
                                        {% endif %}
                                    </th>
                                    {% endfor %}
                                </tr>
                            </thead>
                            <tbody>
                                {% for row in result_rows %}
                                <tr>
                                    <td>{{ row.une.name_es }}</td>
                                    {% for cell in row.cells %}
                                    <td class="{% if cell.is_ingresos %}adm-ingresos-cell{% endif %}">
                                        {% if cell.is_ingresos %}
                                        <div class="adm-ingresos-stack">
                                            <div class="adm-currency-toggle">
                                                <label>
                                                    <input type="radio"
                                                           name="ingresos_curr_{{ row.une.id }}"
                                                           value="GTQ"
                                                           {% if cell.input_currency == "GTQ" %}checked{% endif %}
                                                           onchange="admToggleIngresos(this)">
                                                    Q
                                                </label>
                                                <label>
                                                    <input type="radio"
                                                           name="ingresos_curr_{{ row.une.id }}"
                                                           value="USD"
                                                           {% if cell.input_currency == "USD" %}checked{% endif %}
                                                           onchange="admToggleIngresos(this)">
                                                    $
                                                </label>
                                            </div>
                                            <label class="muted adm-ingresos-label" style="font-size:0.75rem;">
                                                {% if cell.input_currency == "USD" %}Ingreso (USD $){% else %}Ingreso (GTQ Q){% endif %}
                                            </label>
                                            <input type="text"
                                                   class="adm-ingresos-input"
                                                   inputmode="decimal"
                                                   name="result_{{ row.une.id }}_{{ cell.metric.id }}"
                                                   value="{% if cell.value is not None %}{{ cell.value|unlocalize }}{% endif %}"
                                                   data-needs-fx="{% if not has_fx %}1{% else %}0{% endif %}"
                                                   placeholder="{% if cell.input_currency == 'USD' %}USD{% else %}GTQ{% endif %}"
                                                   {% if cell.input_disabled %}title="Sin TC guardado aún: complete el TC en este mismo envío, o capture en $"{% endif %}>
                                            <div class="muted" style="font-size:0.78rem; margin-top:4px;">
                                                {% if cell.measured_usd_display %}
                                                Guardado canónico: <strong>{{ cell.measured_usd_display }} USD</strong>
                                                {% else %}
                                                Guardado canónico USD: —
                                                {% endif %}
                                                {% if cell.fx_used %}<br>FX usado: {{ cell.fx_used }}{% endif %}
                                                {% if cell.conversion_status == "STALE_FX" %}
                                                <br><span style="color:#b45309;font-weight:600;">TC desactualizado</span>
                                                {% elif cell.conversion_status == "CONVERTED" %}
                                                <br><span style="color:#065f46;">Convertido Q→$</span>
                                                {% elif cell.conversion_status == "NATIVE_USD" %}
                                                <br><span style="color:#065f46;">USD nativo</span>
                                                {% endif %}
                                            </div>
                                        </div>
                                        {% else %}
                                        <input type="number" step="0.01"
                                               name="result_{{ row.une.id }}_{{ cell.metric.id }}"
                                               value="{% if cell.value is not None %}{{ cell.value|unlocalize }}{% endif %}">
                                        {% endif %}
                                    </td>
                                    {% endfor %}
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    {% include "pgc/admin/_save_footer.html" with reason_required=True %}

                {% elif tab == "requirements" %}
                <h3>Respuesta a requerimientos</h3>
                <p class="subtitle">Cumplimiento manual por UNE. Si hay incidencia, indique nota o motivo.</p>
                <form method="post">
                    {% csrf_token %}
                    <input type="hidden" name="action" value="save_requirements">
                    <input type="hidden" name="year" value="{{ year }}">
                    <input type="hidden" name="month" value="{{ month }}">
                    <input type="hidden" name="month_from" value="{{ month_from }}">
                    <input type="hidden" name="month_to" value="{{ month_to }}">
                    <input type="hidden" name="tab" value="{{ tab }}">
                    <table class="adm-edit-grid">
                        <thead>
                            <tr><th>UNE</th><th>Cumple</th><th>Nota de incidencia</th></tr>
                        </thead>
                        <tbody>
                            {% for item in requirements %}
                            <tr>
                                <td>{{ item.une.name_es }}</td>
                                <td>
                                    <input type="checkbox" name="req_compliant_{{ item.une.id }}" value="1"
                                           {% if not item.obj or item.obj.is_compliant %}checked{% endif %}>
                                </td>
                                <td>
                                    <input type="text" name="req_note_{{ item.une.id }}"
                                           value="{% if item.obj %}{{ item.obj.incident_note }}{% endif %}"
                                           style="max-width:280px;">
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    {% include "pgc/admin/_save_footer.html" with reason_required=False %}

                {% elif tab == "fx" %}
                <h3>Tipos de cambio · {{ label }}</h3>
                <p class="subtitle">
                    1 USD = X GTQ. Si el rango es varios meses, edite <strong>todos</strong> aquí.
                    Si cambia un TC ya usado por ingresos capturados en Q, esos se marcan STALE (no se recalculan solos).
                </p>
                {% if missing_fx_months %}
                <div class="adm-banner adm-banner-warn">
                    Falta TC en: {% for m in missing_fx_months %}<code style="margin-right:6px;">{{ m }}</code>{% endfor %}
                </div>
                {% endif %}
                <form method="post">
                    {% csrf_token %}
                    <input type="hidden" name="action" value="save_fx">
                    <input type="hidden" name="year" value="{{ year }}">
                    <input type="hidden" name="month" value="{{ month }}">
                    <input type="hidden" name="month_from" value="{{ month_from }}">
                    <input type="hidden" name="month_to" value="{{ month_to }}">
                    <input type="hidden" name="tab" value="{{ tab }}">
                    <div class="adm-scroll">
                        <table class="adm-edit-grid" style="max-width:420px;">
                            <thead>
                                <tr>
                                    <th>Mes</th>
                                    <th>1 USD = … GTQ</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for row in fx_rows %}
                                <tr {% if row.is_focus %}style="background:#f0f9ff;"{% endif %}>
                                    <td style="text-align:left;">
                                        {{ row.label }}
                                        {% if row.missing %}<span class="muted"> (sin TC)</span>{% endif %}
                                        {% if row.is_focus %}<span class="muted"> · foco</span>{% endif %}
                                    </td>
                                    <td>
                                        <input type="text"
                                               name="fx_value_{{ row.month }}"
                                               inputmode="decimal"
                                               style="padding:8px; width:160px;"
                                               value="{% if row.value is not None %}{{ row.value|unlocalize }}{% endif %}"
                                               placeholder="ej. 7.85">
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    {% include "pgc/admin/_save_footer.html" with reason_required=False %}

                {% elif tab == "aliases" %}
                <h3>Alias de UNE</h3>
                <p class="subtitle">Normalice valores crudos detectados en importaciones.
                    Si el valor crudo menciona <strong>Investment</strong>, siempre es <strong>Inversiones</strong>.</p>
                {% if pending_aliases %}
                <p><strong>Valores pendientes en este período:</strong>
                    {% for raw in pending_aliases %}<code style="margin-right:6px;">{{ raw }}</code>{% endfor %}
                </p>
                {% endif %}
                <form method="post" style="margin-bottom:20px;">
                    {% csrf_token %}
                    <input type="hidden" name="action" value="save_alias">
                    <input type="hidden" name="year" value="{{ year }}">
                    <input type="hidden" name="month" value="{{ month }}">
                    <input type="hidden" name="month_from" value="{{ month_from }}">
                    <input type="hidden" name="month_to" value="{{ month_to }}">
                    <input type="hidden" name="tab" value="{{ tab }}">
                    <div style="display:flex; flex-wrap:wrap; gap:12px; align-items:end;">
                        <div>
                            <label>Valor crudo</label><br>
                            <input type="text" name="alias_raw" list="pending-alias-list" style="padding:8px; min-width:200px;">
                            <datalist id="pending-alias-list">
                                {% for raw in pending_aliases %}<option value="{{ raw }}">{% endfor %}
                            </datalist>
                        </div>
                        <div>
                            <label>UNE destino</label><br>
                            <select name="alias_une">
                                {% for une in unes %}<option value="{{ une.id }}">{{ une.name_es }}</option>{% endfor %}
                            </select>
                        </div>
                    </div>
                    {% include "pgc/admin/_save_footer.html" with reason_required=False %}

                <h4 style="font-size:0.92rem;">Alias activos — edite UNE y guarde</h4>
                <form method="post">
                    {% csrf_token %}
                    <input type="hidden" name="action" value="save_aliases_bulk">
                    <input type="hidden" name="year" value="{{ year }}">
                    <input type="hidden" name="month" value="{{ month }}">
                    <input type="hidden" name="month_from" value="{{ month_from }}">
                    <input type="hidden" name="month_to" value="{{ month_to }}">
                    <input type="hidden" name="tab" value="{{ tab }}">
                    <div class="adm-scroll" style="max-height:360px;">
                        <table class="adm-edit-grid">
                            <thead><tr><th>Valor crudo</th><th>UNE</th></tr></thead>
                            <tbody>
                                {% for alias in aliases %}
                                <tr>
                                    <td style="text-align:left;">{{ alias.raw_value }}</td>
                                    <td>
                                        <select name="alias_{{ alias.id }}_une">
                                            {% for une in unes %}
                                            <option value="{{ une.id }}" {% if alias.une_id == une.id %}selected{% endif %}>
                                                {{ une.name_es }}
                                            </option>
                                            {% endfor %}
                                        </select>
                                    </td>
                                </tr>
                                {% empty %}
                                <tr><td colspan="2" class="muted">Sin aliases activos.</td></tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    {% include "pgc/admin/_save_footer.html" with reason_required=False %}

                {% elif tab == "imports" %}
                <h3>Registros importados</h3>
                <p class="subtitle">Corrija filas con observaciones o UNE no resueltas.</p>
                <form method="post">
                    {% csrf_token %}
                    <input type="hidden" name="action" value="save_imports">
                    <input type="hidden" name="year" value="{{ year }}">
                    <input type="hidden" name="month" value="{{ month }}">
                    <input type="hidden" name="month_from" value="{{ month_from }}">
                    <input type="hidden" name="month_to" value="{{ month_to }}">
                    <input type="hidden" name="tab" value="{{ tab }}">

                    <h4 style="font-size:0.92rem; margin-top:0;">Clientes nuevos</h4>
                    {% if new_client_rows %}
                    <div class="adm-scroll">
                        <table class="adm-edit-grid">
                            <thead>
                                <tr><th>Mes</th><th>Cliente</th><th>UNE</th><th>¿Cuenta?</th><th>Observaciones</th></tr>
                            </thead>
                            <tbody>
                                {% for row in new_client_rows %}
                                <tr>
                                    <td class="muted">{{ row.month|stringformat:"02d" }}</td>
                                    <td>{{ row.client_name|default:row.operation_code }}</td>
                                    <td>{{ row.une.name_es }}</td>
                                    <td>
                                        <input type="checkbox" name="nc_{{ row.id }}_counts_as_new" value="1"
                                               {% if row.counts_as_new %}checked{% endif %}>
                                    </td>
                                    <td>
                                        <input type="text" name="nc_{{ row.id }}_observations" value="{{ row.observations }}" style="max-width:200px;">
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    {% else %}
                    <p class="muted">Sin filas de clientes nuevos para este período.</p>
                    {% endif %}

                    <h4 style="font-size:0.92rem; margin-top:20px;">Venta cruzada</h4>
                    {% if cross_sale_rows %}
                    <div class="adm-scroll">
                        <table class="adm-edit-grid">
                            <thead>
                                <tr><th>Cliente</th><th>Origen</th><th>Destino</th><th>Raw origen</th><th>Raw destino</th></tr>
                            </thead>
                            <tbody>
                                {% for row in cross_sale_rows %}
                                <tr>
                                    <td>{{ row.client_name|default:row.operation_code }}</td>
                                    <td>
                                        <select name="cs_{{ row.id }}_orig">
                                            <option value="">—</option>
                                            {% for une in unes %}
                                            <option value="{{ une.id }}" {% if row.une_origin_id == une.id %}selected{% endif %}>{{ une.code }}</option>
                                            {% endfor %}
                                        </select>
                                    </td>
                                    <td>
                                        <select name="cs_{{ row.id }}_dest">
                                            <option value="">—</option>
                                            {% for une in unes %}
                                            <option value="{{ une.id }}" {% if row.une_destination_id == une.id %}selected{% endif %}>{{ une.code }}</option>
                                            {% endfor %}
                                        </select>
                                    </td>
                                    <td class="muted">{{ row.raw_une_origin }}</td>
                                    <td class="muted">{{ row.raw_une_destination }}</td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                    {% else %}
                    <p class="muted">Sin filas de venta cruzada para este período.</p>
                    {% endif %}
                    {% include "pgc/admin/_save_footer.html" with reason_required=False %}

                {% elif tab == "notes" %}
                <h3>Notas del período</h3>
                <p class="subtitle">Observaciones administrativas visibles para el equipo operativo.</p>
                <form method="post">
                    {% csrf_token %}
                    <input type="hidden" name="action" value="save_notes">
                    <input type="hidden" name="year" value="{{ year }}">
                    <input type="hidden" name="month" value="{{ month }}">
                    <input type="hidden" name="month_from" value="{{ month_from }}">
                    <input type="hidden" name="month_to" value="{{ month_to }}">
                    <input type="hidden" name="tab" value="{{ tab }}">
                    <textarea name="period_note" rows="6" style="width:100%; padding:12px; border:1px solid #d9e2ec; border-radius:8px;">{{ period_note }}</textarea>
                    {% include "pgc/admin/_save_footer.html" with reason_required=False %}
                {% endif %}
            </div>
        </div>

        <div>
            <div class="adm-side-card">
                <h4>Guía rápida</h4>
                <div class="adm-reminder"><strong>1.</strong> Tipos de cambio del rango (si captura ingresos en Q).</div>
                <div class="adm-reminder"><strong>2.</strong> Metas de ingresos siempre en <strong>USD ($)</strong>.</div>
                <div class="adm-reminder"><strong>3.</strong> Resultados → Ingresos: Q o $; lo guardado es siempre USD.</div>
                <div class="adm-reminder">Campos vacíos no sobrescriben. Resultados requieren motivo.</div>
            </div>
            <div class="adm-side-card">
                <h4>Cambios recientes</h4>
                {% for edit in recent_edits %}
                <div class="adm-log-item">
                    <strong>{{ edit.get_entity_type_display }}</strong> · {{ edit.field_name }}<br>
                    {{ edit.old_value|default:"—" }} → {{ edit.new_value|default:"—" }}
                    <br><span class="muted">{{ edit.created_at|date:"d/m/Y H:i" }}{% if edit.edited_by %} · {{ edit.edited_by.username }}{% endif %}</span>
                </div>
                {% empty %}
                <p class="muted">Sin ediciones manuales en este período.</p>
                {% endfor %}
            </div>
        </div>
    </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base.html" %}
00002|{% load l10n %}
00003|
00004|{% block title %}Edición manual — {{ label }}{% endblock %}
00005|
00006|{% block content %}
00007|{% include "pgc/admin/_styles.html" %}
00008|
00009|<div class="adm">
00010|    {% include "pgc/admin/_nav.html" with adm_nav_active="manual" %}
00011|
00012|    <div class="adm-header">
00013|        <div class="adm-header-top">
00014|            <div>
00015|                <p class="muted" style="margin:0;">Edición manual del período</p>
00016|                <div class="adm-period-label">{{ label }}</div>
00017|                {% if not plan %}<p class="muted" style="color:#b45309;">No hay plan PGC para este año.</p>{% endif %}
00018|            </div>
00019|            {% include "pgc/admin/_period_select.html" %}
00020|        </div>
00021|    </div>
00022|
00023|    <div class="adm-route-hint">
00024|        <strong>Ruta sugerida:</strong>
00025|        Tipos de cambio → Metas (USD) → Resultados (ingresos Q o $ → se guardan en USD).
00026|        Metas/resultados usan el mes foco <code>{{ focus_label }}</code>; el TC usa el rango completo.
00027|    </div>
00028|
00029|    <div class="adm-tabs">
00030|        {% for tab_id, tab_label in tabs %}
00031|        <a href="?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}&tab={{ tab_id }}"
00032|           class="{% if tab == tab_id %}active{% endif %}">{{ tab_label }}</a>
00033|        {% endfor %}
00034|    </div>
00035|
00036|    <div class="adm-layout">
00037|        <div>
00038|            <div class="adm-panel">
00039|                {% if tab == "targets" %}
00040|                <h3>Metas mensuales · {{ focus_label }}</h3>
00041|                <p class="subtitle">
00042|                    Metas de <strong>Ingresos en USD ($)</strong>. Las demás métricas son cantidades / cumplimiento, no moneda.
00043|                    Deje vacío para no modificar.
00044|                </p>
00045|                <form method="post">
00046|                    {% csrf_token %}
00047|                    <input type="hidden" name="action" value="save_targets">
00048|                    <input type="hidden" name="year" value="{{ year }}">
00049|                    <input type="hidden" name="month" value="{{ month }}">
00050|                    <input type="hidden" name="month_from" value="{{ month_from }}">
00051|                    <input type="hidden" name="month_to" value="{{ month_to }}">
00052|                    <input type="hidden" name="tab" value="{{ tab }}">
00053|                    <div class="adm-scroll">
00054|                        <table class="adm-edit-grid">
00055|                            <thead>
00056|                                <tr>
00057|                                    <th>UNE</th>
00058|                                    {% for metric in metrics %}
00059|                                    <th>
00060|                                        {% if metric.code == "INGRESOS" %}
00061|                                        {{ metric.name }}<br><span class="adm-currency-tag">USD ($)</span>
00062|                                        {% else %}
00063|                                        {{ metric.name }}
00064|                                        {% endif %}
00065|                                    </th>
00066|                                    {% endfor %}
00067|                                </tr>
00068|                            </thead>
00069|                            <tbody>
00070|                                {% for row in target_rows %}
00071|                                <tr>
00072|                                    <td>{{ row.une.name_es }}</td>
00073|                                    {% for cell in row.cells %}
00074|                                    <td>
00075|                                        <input type="number" step="0.01"
00076|                                               name="target_{{ row.une.id }}_{{ cell.metric.id }}"
00077|                                               value="{% if cell.value is not None %}{{ cell.value|unlocalize }}{% endif %}">
00078|                                    </td>
00079|                                    {% endfor %}
00080|                                </tr>
00081|                                {% endfor %}
00082|                            </tbody>
00083|                        </table>
00084|                    </div>
00085|                    {% include "pgc/admin/_save_footer.html" with reason_required=False %}
00086|
00087|                {% elif tab == "results" %}
00088|                <h3>Resultados mensuales · {{ focus_label }}</h3>
00089|                <p class="subtitle">
00090|                    <strong>Ingresos</strong>: elija <strong>Q</strong> o <strong>$</strong> por UNE.
00091|                    Si captura en Q, se convierte a USD con el TC del mes y se guarda el USD canónico.
00092|                    Si captura en $, se guarda directo en USD (sin TC). Las demás métricas no son moneda.
00093|                </p>
00094|
00095|                {% if not has_fx %}
00096|                <div class="adm-banner adm-banner-warn">
00097|                    <strong>Falta tipo de cambio para {{ focus_label }}.</strong>
00098|                    Sin TC no se pueden guardar ingresos en quetzales (Q). Sí se puede capturar en dólares ($).
00099|                    <a href="?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}&tab=fx"
00100|                       class="adm-btn adm-btn-secondary" style="margin-left:8px;">Ir a tipos de cambio</a>
00101|                </div>
00102|                {% else %}
00103|                <div class="adm-banner adm-banner-info">
00104|                    TC del período {{ focus_label }}: <strong>1 USD = {{ fx_rate }} GTQ</strong>.
00105|                    Conversión: <code>GTQ ÷ TC → USD</code>.
00106|                </div>
00107|                {% endif %}
00108|
00109|                {% if stale_ingresos_count %}
00110|                <div class="adm-banner adm-banner-warn">
00111|                    <strong>{{ stale_ingresos_count }} ingreso(s) con TC desactualizado (STALE).</strong>
00112|                    El tipo de cambio cambió después de la captura en Q.
00113|                    <form method="post" style="display:inline; margin-left:8px;">
00114|                        {% csrf_token %}
00115|                        <input type="hidden" name="action" value="recalc_stale_ingresos">
00116|                        <input type="hidden" name="year" value="{{ year }}">
00117|                        <input type="hidden" name="month" value="{{ month }}">
00118|                        <input type="hidden" name="month_from" value="{{ month_from }}">
00119|                        <input type="hidden" name="month_to" value="{{ month_to }}">
00120|                        <input type="hidden" name="tab" value="{{ tab }}">
00121|                        <input type="hidden" name="reason" value="Recálculo STALE desde resultados">
00122|                        <button type="submit" class="adm-btn adm-btn-primary">Recalcular USD desde GTQ</button>
00123|                    </form>
00124|                </div>
00125|                {% endif %}
00126|
00127|                <form method="post">
00128|                    {% csrf_token %}
00129|                    <input type="hidden" name="action" value="save_results">
00130|                    <input type="hidden" name="year" value="{{ year }}">
00131|                    <input type="hidden" name="month" value="{{ month }}">
00132|                    <input type="hidden" name="month_from" value="{{ month_from }}">
00133|                    <input type="hidden" name="month_to" value="{{ month_to }}">
00134|                    <input type="hidden" name="tab" value="{{ tab }}">
00135|                    <div class="adm-scroll">
00136|                        <table class="adm-edit-grid">
00137|                            <thead>
00138|                                <tr>
00139|                                    <th>UNE</th>
00140|                                    {% for metric in metrics %}
00141|                                    <th>
00142|                                        {% if metric.code == "INGRESOS" %}
00143|                                        {{ metric.name }} (guardado USD)<br>
00144|                                        <span class="adm-currency-tag">captura Q o $</span>
00145|                                        {% else %}
00146|                                        {{ metric.name }}
00147|                                        {% endif %}
00148|                                    </th>
00149|                                    {% endfor %}
00150|                                </tr>
00151|                            </thead>
00152|                            <tbody>
00153|                                {% for row in result_rows %}
00154|                                <tr>
00155|                                    <td>{{ row.une.name_es }}</td>
00156|                                    {% for cell in row.cells %}
00157|                                    <td class="{% if cell.is_ingresos %}adm-ingresos-cell{% endif %}">
00158|                                        {% if cell.is_ingresos %}
00159|                                        <div class="adm-ingresos-stack">
00160|                                            <div class="adm-currency-toggle">
00161|                                                <label>
00162|                                                    <input type="radio"
00163|                                                           name="ingresos_curr_{{ row.une.id }}"
00164|                                                           value="GTQ"
00165|                                                           {% if cell.input_currency == "GTQ" %}checked{% endif %}
00166|                                                           onchange="admToggleIngresos(this)">
00167|                                                    Q
00168|                                                </label>
00169|                                                <label>
00170|                                                    <input type="radio"
00171|                                                           name="ingresos_curr_{{ row.une.id }}"
00172|                                                           value="USD"
00173|                                                           {% if cell.input_currency == "USD" %}checked{% endif %}
00174|                                                           onchange="admToggleIngresos(this)">
00175|                                                    $
00176|                                                </label>
00177|                                            </div>
00178|                                            <label class="muted adm-ingresos-label" style="font-size:0.75rem;">
00179|                                                {% if cell.input_currency == "USD" %}Ingreso (USD $){% else %}Ingreso (GTQ Q){% endif %}
00180|                                            </label>
00181|                                            <input type="text"
00182|                                                   class="adm-ingresos-input"
00183|                                                   inputmode="decimal"
00184|                                                   name="result_{{ row.une.id }}_{{ cell.metric.id }}"
00185|                                                   value="{% if cell.value is not None %}{{ cell.value|unlocalize }}{% endif %}"
00186|                                                   data-needs-fx="{% if not has_fx %}1{% else %}0{% endif %}"
00187|                                                   placeholder="{% if cell.input_currency == 'USD' %}USD{% else %}GTQ{% endif %}"
00188|                                                   {% if cell.input_disabled %}title="Sin TC guardado aún: complete el TC en este mismo envío, o capture en $"{% endif %}>
00189|                                            <div class="muted" style="font-size:0.78rem; margin-top:4px;">
00190|                                                {% if cell.measured_usd_display %}
00191|                                                Guardado canónico: <strong>{{ cell.measured_usd_display }} USD</strong>
00192|                                                {% else %}
00193|                                                Guardado canónico USD: —
00194|                                                {% endif %}
00195|                                                {% if cell.fx_used %}<br>FX usado: {{ cell.fx_used }}{% endif %}
00196|                                                {% if cell.conversion_status == "STALE_FX" %}
00197|                                                <br><span style="color:#b45309;font-weight:600;">TC desactualizado</span>
00198|                                                {% elif cell.conversion_status == "CONVERTED" %}
00199|                                                <br><span style="color:#065f46;">Convertido Q→$</span>
00200|                                                {% elif cell.conversion_status == "NATIVE_USD" %}
00201|                                                <br><span style="color:#065f46;">USD nativo</span>
00202|                                                {% endif %}
00203|                                            </div>
00204|                                        </div>
00205|                                        {% else %}
00206|                                        <input type="number" step="0.01"
00207|                                               name="result_{{ row.une.id }}_{{ cell.metric.id }}"
00208|                                               value="{% if cell.value is not None %}{{ cell.value|unlocalize }}{% endif %}">
00209|                                        {% endif %}
00210|                                    </td>
00211|                                    {% endfor %}
00212|                                </tr>
00213|                                {% endfor %}
00214|                            </tbody>
00215|                        </table>
00216|                    </div>
00217|                    {% include "pgc/admin/_save_footer.html" with reason_required=True %}
00218|
00219|                {% elif tab == "requirements" %}
00220|                <h3>Respuesta a requerimientos</h3>
00221|                <p class="subtitle">Cumplimiento manual por UNE. Si hay incidencia, indique nota o motivo.</p>
00222|                <form method="post">
00223|                    {% csrf_token %}
00224|                    <input type="hidden" name="action" value="save_requirements">
00225|                    <input type="hidden" name="year" value="{{ year }}">
00226|                    <input type="hidden" name="month" value="{{ month }}">
00227|                    <input type="hidden" name="month_from" value="{{ month_from }}">
00228|                    <input type="hidden" name="month_to" value="{{ month_to }}">
00229|                    <input type="hidden" name="tab" value="{{ tab }}">
00230|                    <table class="adm-edit-grid">
00231|                        <thead>
00232|                            <tr><th>UNE</th><th>Cumple</th><th>Nota de incidencia</th></tr>
00233|                        </thead>
00234|                        <tbody>
00235|                            {% for item in requirements %}
00236|                            <tr>
00237|                                <td>{{ item.une.name_es }}</td>
00238|                                <td>
00239|                                    <input type="checkbox" name="req_compliant_{{ item.une.id }}" value="1"
00240|                                           {% if not item.obj or item.obj.is_compliant %}checked{% endif %}>
00241|                                </td>
00242|                                <td>
00243|                                    <input type="text" name="req_note_{{ item.une.id }}"
00244|                                           value="{% if item.obj %}{{ item.obj.incident_note }}{% endif %}"
00245|                                           style="max-width:280px;">
00246|                                </td>
00247|                            </tr>
00248|                            {% endfor %}
00249|                        </tbody>
00250|                    </table>
00251|                    {% include "pgc/admin/_save_footer.html" with reason_required=False %}
00252|
00253|                {% elif tab == "fx" %}
00254|                <h3>Tipos de cambio · {{ label }}</h3>
00255|                <p class="subtitle">
00256|                    1 USD = X GTQ. Si el rango es varios meses, edite <strong>todos</strong> aquí.
00257|                    Si cambia un TC ya usado por ingresos capturados en Q, esos se marcan STALE (no se recalculan solos).
00258|                </p>
00259|                {% if missing_fx_months %}
00260|                <div class="adm-banner adm-banner-warn">
00261|                    Falta TC en: {% for m in missing_fx_months %}<code style="margin-right:6px;">{{ m }}</code>{% endfor %}
00262|                </div>
00263|                {% endif %}
00264|                <form method="post">
00265|                    {% csrf_token %}
00266|                    <input type="hidden" name="action" value="save_fx">
00267|                    <input type="hidden" name="year" value="{{ year }}">
00268|                    <input type="hidden" name="month" value="{{ month }}">
00269|                    <input type="hidden" name="month_from" value="{{ month_from }}">
00270|                    <input type="hidden" name="month_to" value="{{ month_to }}">
00271|                    <input type="hidden" name="tab" value="{{ tab }}">
00272|                    <div class="adm-scroll">
00273|                        <table class="adm-edit-grid" style="max-width:420px;">
00274|                            <thead>
00275|                                <tr>
00276|                                    <th>Mes</th>
00277|                                    <th>1 USD = … GTQ</th>
00278|                                </tr>
00279|                            </thead>
00280|                            <tbody>
00281|                                {% for row in fx_rows %}
00282|                                <tr {% if row.is_focus %}style="background:#f0f9ff;"{% endif %}>
00283|                                    <td style="text-align:left;">
00284|                                        {{ row.label }}
00285|                                        {% if row.missing %}<span class="muted"> (sin TC)</span>{% endif %}
00286|                                        {% if row.is_focus %}<span class="muted"> · foco</span>{% endif %}
00287|                                    </td>
00288|                                    <td>
00289|                                        <input type="text"
00290|                                               name="fx_value_{{ row.month }}"
00291|                                               inputmode="decimal"
00292|                                               style="padding:8px; width:160px;"
00293|                                               value="{% if row.value is not None %}{{ row.value|unlocalize }}{% endif %}"
00294|                                               placeholder="ej. 7.85">
00295|                                    </td>
00296|                                </tr>
00297|                                {% endfor %}
00298|                            </tbody>
00299|                        </table>
00300|                    </div>
00301|                    {% include "pgc/admin/_save_footer.html" with reason_required=False %}
00302|
00303|                {% elif tab == "aliases" %}
00304|                <h3>Alias de UNE</h3>
00305|                <p class="subtitle">Normalice valores crudos detectados en importaciones.
00306|                    Si el valor crudo menciona <strong>Investment</strong>, siempre es <strong>Inversiones</strong>.</p>
00307|                {% if pending_aliases %}
00308|                <p><strong>Valores pendientes en este período:</strong>
00309|                    {% for raw in pending_aliases %}<code style="margin-right:6px;">{{ raw }}</code>{% endfor %}
00310|                </p>
00311|                {% endif %}
00312|                <form method="post" style="margin-bottom:20px;">
00313|                    {% csrf_token %}
00314|                    <input type="hidden" name="action" value="save_alias">
00315|                    <input type="hidden" name="year" value="{{ year }}">
00316|                    <input type="hidden" name="month" value="{{ month }}">
00317|                    <input type="hidden" name="month_from" value="{{ month_from }}">
00318|                    <input type="hidden" name="month_to" value="{{ month_to }}">
00319|                    <input type="hidden" name="tab" value="{{ tab }}">
00320|                    <div style="display:flex; flex-wrap:wrap; gap:12px; align-items:end;">
00321|                        <div>
00322|                            <label>Valor crudo</label><br>
00323|                            <input type="text" name="alias_raw" list="pending-alias-list" style="padding:8px; min-width:200px;">
00324|                            <datalist id="pending-alias-list">
00325|                                {% for raw in pending_aliases %}<option value="{{ raw }}">{% endfor %}
00326|                            </datalist>
00327|                        </div>
00328|                        <div>
00329|                            <label>UNE destino</label><br>
00330|                            <select name="alias_une">
00331|                                {% for une in unes %}<option value="{{ une.id }}">{{ une.name_es }}</option>{% endfor %}
00332|                            </select>
00333|                        </div>
00334|                    </div>
00335|                    {% include "pgc/admin/_save_footer.html" with reason_required=False %}
00336|
00337|                <h4 style="font-size:0.92rem;">Alias activos — edite UNE y guarde</h4>
00338|                <form method="post">
00339|                    {% csrf_token %}
00340|                    <input type="hidden" name="action" value="save_aliases_bulk">
00341|                    <input type="hidden" name="year" value="{{ year }}">
00342|                    <input type="hidden" name="month" value="{{ month }}">
00343|                    <input type="hidden" name="month_from" value="{{ month_from }}">
00344|                    <input type="hidden" name="month_to" value="{{ month_to }}">
00345|                    <input type="hidden" name="tab" value="{{ tab }}">
00346|                    <div class="adm-scroll" style="max-height:360px;">
00347|                        <table class="adm-edit-grid">
00348|                            <thead><tr><th>Valor crudo</th><th>UNE</th></tr></thead>
00349|                            <tbody>
00350|                                {% for alias in aliases %}
00351|                                <tr>
00352|                                    <td style="text-align:left;">{{ alias.raw_value }}</td>
00353|                                    <td>
00354|                                        <select name="alias_{{ alias.id }}_une">
00355|                                            {% for une in unes %}
00356|                                            <option value="{{ une.id }}" {% if alias.une_id == une.id %}selected{% endif %}>
00357|                                                {{ une.name_es }}
00358|                                            </option>
00359|                                            {% endfor %}
00360|                                        </select>
00361|                                    </td>
00362|                                </tr>
00363|                                {% empty %}
00364|                                <tr><td colspan="2" class="muted">Sin aliases activos.</td></tr>
00365|                                {% endfor %}
00366|                            </tbody>
00367|                        </table>
00368|                    </div>
00369|                    {% include "pgc/admin/_save_footer.html" with reason_required=False %}
00370|
00371|                {% elif tab == "imports" %}
00372|                <h3>Registros importados</h3>
00373|                <p class="subtitle">Corrija filas con observaciones o UNE no resueltas.</p>
00374|                <form method="post">
00375|                    {% csrf_token %}
00376|                    <input type="hidden" name="action" value="save_imports">
00377|                    <input type="hidden" name="year" value="{{ year }}">
00378|                    <input type="hidden" name="month" value="{{ month }}">
00379|                    <input type="hidden" name="month_from" value="{{ month_from }}">
00380|                    <input type="hidden" name="month_to" value="{{ month_to }}">
00381|                    <input type="hidden" name="tab" value="{{ tab }}">
00382|
00383|                    <h4 style="font-size:0.92rem; margin-top:0;">Clientes nuevos</h4>
00384|                    {% if new_client_rows %}
00385|                    <div class="adm-scroll">
00386|                        <table class="adm-edit-grid">
00387|                            <thead>
00388|                                <tr><th>Mes</th><th>Cliente</th><th>UNE</th><th>¿Cuenta?</th><th>Observaciones</th></tr>
00389|                            </thead>
00390|                            <tbody>
00391|                                {% for row in new_client_rows %}
00392|                                <tr>
00393|                                    <td class="muted">{{ row.month|stringformat:"02d" }}</td>
00394|                                    <td>{{ row.client_name|default:row.operation_code }}</td>
00395|                                    <td>{{ row.une.name_es }}</td>
00396|                                    <td>
00397|                                        <input type="checkbox" name="nc_{{ row.id }}_counts_as_new" value="1"
00398|                                               {% if row.counts_as_new %}checked{% endif %}>
00399|                                    </td>
00400|                                    <td>
00401|                                        <input type="text" name="nc_{{ row.id }}_observations" value="{{ row.observations }}" style="max-width:200px;">
00402|                                    </td>
00403|                                </tr>
00404|                                {% endfor %}
00405|                            </tbody>
00406|                        </table>
00407|                    </div>
00408|                    {% else %}
00409|                    <p class="muted">Sin filas de clientes nuevos para este período.</p>
00410|                    {% endif %}
00411|
00412|                    <h4 style="font-size:0.92rem; margin-top:20px;">Venta cruzada</h4>
00413|                    {% if cross_sale_rows %}
00414|                    <div class="adm-scroll">
00415|                        <table class="adm-edit-grid">
00416|                            <thead>
00417|                                <tr><th>Cliente</th><th>Origen</th><th>Destino</th><th>Raw origen</th><th>Raw destino</th></tr>
00418|                            </thead>
00419|                            <tbody>
00420|                                {% for row in cross_sale_rows %}
00421|                                <tr>
00422|                                    <td>{{ row.client_name|default:row.operation_code }}</td>
00423|                                    <td>
00424|                                        <select name="cs_{{ row.id }}_orig">
00425|                                            <option value="">—</option>
00426|                                            {% for une in unes %}
00427|                                            <option value="{{ une.id }}" {% if row.une_origin_id == une.id %}selected{% endif %}>{{ une.code }}</option>
00428|                                            {% endfor %}
00429|                                        </select>
00430|                                    </td>
00431|                                    <td>
00432|                                        <select name="cs_{{ row.id }}_dest">
00433|                                            <option value="">—</option>
00434|                                            {% for une in unes %}
00435|                                            <option value="{{ une.id }}" {% if row.une_destination_id == une.id %}selected{% endif %}>{{ une.code }}</option>
00436|                                            {% endfor %}
00437|                                        </select>
00438|                                    </td>
00439|                                    <td class="muted">{{ row.raw_une_origin }}</td>
00440|                                    <td class="muted">{{ row.raw_une_destination }}</td>
00441|                                </tr>
00442|                                {% endfor %}
00443|                            </tbody>
00444|                        </table>
00445|                    </div>
00446|                    {% else %}
00447|                    <p class="muted">Sin filas de venta cruzada para este período.</p>
00448|                    {% endif %}
00449|                    {% include "pgc/admin/_save_footer.html" with reason_required=False %}
00450|
00451|                {% elif tab == "notes" %}
00452|                <h3>Notas del período</h3>
00453|                <p class="subtitle">Observaciones administrativas visibles para el equipo operativo.</p>
00454|                <form method="post">
00455|                    {% csrf_token %}
00456|                    <input type="hidden" name="action" value="save_notes">
00457|                    <input type="hidden" name="year" value="{{ year }}">
00458|                    <input type="hidden" name="month" value="{{ month }}">
00459|                    <input type="hidden" name="month_from" value="{{ month_from }}">
00460|                    <input type="hidden" name="month_to" value="{{ month_to }}">
00461|                    <input type="hidden" name="tab" value="{{ tab }}">
00462|                    <textarea name="period_note" rows="6" style="width:100%; padding:12px; border:1px solid #d9e2ec; border-radius:8px;">{{ period_note }}</textarea>
00463|                    {% include "pgc/admin/_save_footer.html" with reason_required=False %}
00464|                {% endif %}
00465|            </div>
00466|        </div>
00467|
00468|        <div>
00469|            <div class="adm-side-card">
00470|                <h4>Guía rápida</h4>
00471|                <div class="adm-reminder"><strong>1.</strong> Tipos de cambio del rango (si captura ingresos en Q).</div>
00472|                <div class="adm-reminder"><strong>2.</strong> Metas de ingresos siempre en <strong>USD ($)</strong>.</div>
00473|                <div class="adm-reminder"><strong>3.</strong> Resultados → Ingresos: Q o $; lo guardado es siempre USD.</div>
00474|                <div class="adm-reminder">Campos vacíos no sobrescriben. Resultados requieren motivo.</div>
00475|            </div>
00476|            <div class="adm-side-card">
00477|                <h4>Cambios recientes</h4>
00478|                {% for edit in recent_edits %}
00479|                <div class="adm-log-item">
00480|                    <strong>{{ edit.get_entity_type_display }}</strong> · {{ edit.field_name }}<br>
00481|                    {{ edit.old_value|default:"—" }} → {{ edit.new_value|default:"—" }}
00482|                    <br><span class="muted">{{ edit.created_at|date:"d/m/Y H:i" }}{% if edit.edited_by %} · {{ edit.edited_by.username }}{% endif %}</span>
00483|                </div>
00484|                {% empty %}
00485|                <p class="muted">Sin ediciones manuales en este período.</p>
00486|                {% endfor %}
00487|            </div>
00488|        </div>
00489|    </div>
00490|</div>
00491|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZS5odG1sIiAlfQp7JSBsb2FkIGwxMG4gJX0KCnslIGJsb2NrIHRpdGxlICV9RWRpY2nDs24gbWFudWFsIOKAlCB7eyBsYWJlbCB9fXslIGVuZGJsb2NrICV9Cgp7JSBibG9jayBjb250ZW50ICV9CnslIGluY2x1ZGUgInBnYy9hZG1pbi9fc3R5bGVzLmh0bWwiICV9Cgo8ZGl2IGNsYXNzPSJhZG0iPgogICAgeyUgaW5jbHVkZSAicGdjL2FkbWluL19uYXYuaHRtbCIgd2l0aCBhZG1fbmF2X2FjdGl2ZT0ibWFudWFsIiAlfQoKICAgIDxkaXYgY2xhc3M9ImFkbS1oZWFkZXIiPgogICAgICAgIDxkaXYgY2xhc3M9ImFkbS1oZWFkZXItdG9wIj4KICAgICAgICAgICAgPGRpdj4KICAgICAgICAgICAgICAgIDxwIGNsYXNzPSJtdXRlZCIgc3R5bGU9Im1hcmdpbjowOyI+RWRpY2nDs24gbWFudWFsIGRlbCBwZXLDrW9kbzwvcD4KICAgICAgICAgICAgICAgIDxkaXYgY2xhc3M9ImFkbS1wZXJpb2QtbGFiZWwiPnt7IGxhYmVsIH19PC9kaXY+CiAgICAgICAgICAgICAgICB7JSBpZiBub3QgcGxhbiAlfTxwIGNsYXNzPSJtdXRlZCIgc3R5bGU9ImNvbG9yOiNiNDUzMDk7Ij5ObyBoYXkgcGxhbiBQR0MgcGFyYSBlc3RlIGHDsW8uPC9wPnslIGVuZGlmICV9CiAgICAgICAgICAgIDwvZGl2PgogICAgICAgICAgICB7JSBpbmNsdWRlICJwZ2MvYWRtaW4vX3BlcmlvZF9zZWxlY3QuaHRtbCIgJX0KICAgICAgICA8L2Rpdj4KICAgIDwvZGl2PgoKICAgIDxkaXYgY2xhc3M9ImFkbS1yb3V0ZS1oaW50Ij4KICAgICAgICA8c3Ryb25nPlJ1dGEgc3VnZXJpZGE6PC9zdHJvbmc+CiAgICAgICAgVGlwb3MgZGUgY2FtYmlvIOKGkiBNZXRhcyAoVVNEKSDihpIgUmVzdWx0YWRvcyAoaW5ncmVzb3MgUSBvICQg4oaSIHNlIGd1YXJkYW4gZW4gVVNEKS4KICAgICAgICBNZXRhcy9yZXN1bHRhZG9zIHVzYW4gZWwgbWVzIGZvY28gPGNvZGU+e3sgZm9jdXNfbGFiZWwgfX08L2NvZGU+OyBlbCBUQyB1c2EgZWwgcmFuZ28gY29tcGxldG8uCiAgICA8L2Rpdj4KCiAgICA8ZGl2IGNsYXNzPSJhZG0tdGFicyI+CiAgICAgICAgeyUgZm9yIHRhYl9pZCwgdGFiX2xhYmVsIGluIHRhYnMgJX0KICAgICAgICA8YSBocmVmPSI/eWVhcj17eyB5ZWFyIH19Jm1vbnRoX2Zyb209e3sgbW9udGhfZnJvbSB9fSZtb250aF90bz17eyBtb250aF90byB9fSZtb250aD17eyBtb250aCB9fSZ0YWI9e3sgdGFiX2lkIH19IgogICAgICAgICAgIGNsYXNzPSJ7JSBpZiB0YWIgPT0gdGFiX2lkICV9YWN0aXZleyUgZW5kaWYgJX0iPnt7IHRhYl9sYWJlbCB9fTwvYT4KICAgICAgICB7JSBlbmRmb3IgJX0KICAgIDwvZGl2PgoKICAgIDxkaXYgY2xhc3M9ImFkbS1sYXlvdXQiPgogICAgICAgIDxkaXY+CiAgICAgICAgICAgIDxkaXYgY2xhc3M9ImFkbS1wYW5lbCI+CiAgICAgICAgICAgICAgICB7JSBpZiB0YWIgPT0gInRhcmdldHMiICV9CiAgICAgICAgICAgICAgICA8aDM+TWV0YXMgbWVuc3VhbGVzIMK3IHt7IGZvY3VzX2xhYmVsIH19PC9oMz4KICAgICAgICAgICAgICAgIDxwIGNsYXNzPSJzdWJ0aXRsZSI+CiAgICAgICAgICAgICAgICAgICAgTWV0YXMgZGUgPHN0cm9uZz5JbmdyZXNvcyBlbiBVU0QgKCQpPC9zdHJvbmc+LiBMYXMgZGVtw6FzIG3DqXRyaWNhcyBzb24gY2FudGlkYWRlcyAvIGN1bXBsaW1pZW50bywgbm8gbW9uZWRhLgogICAgICAgICAgICAgICAgICAgIERlamUgdmFjw61vIHBhcmEgbm8gbW9kaWZpY2FyLgogICAgICAgICAgICAgICAgPC9wPgogICAgICAgICAgICAgICAgPGZvcm0gbWV0aG9kPSJwb3N0Ij4KICAgICAgICAgICAgICAgICAgICB7JSBjc3JmX3Rva2VuICV9CiAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0iYWN0aW9uIiB2YWx1ZT0ic2F2ZV90YXJnZXRzIj4KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJ5ZWFyIiB2YWx1ZT0ie3sgeWVhciB9fSI+CiAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ibW9udGgiIHZhbHVlPSJ7eyBtb250aCB9fSI+CiAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ibW9udGhfZnJvbSIgdmFsdWU9Int7IG1vbnRoX2Zyb20gfX0iPgogICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9Im1vbnRoX3RvIiB2YWx1ZT0ie3sgbW9udGhfdG8gfX0iPgogICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9InRhYiIgdmFsdWU9Int7IHRhYiB9fSI+CiAgICAgICAgICAgICAgICAgICAgPGRpdiBjbGFzcz0iYWRtLXNjcm9sbCI+CiAgICAgICAgICAgICAgICAgICAgICAgIDx0YWJsZSBjbGFzcz0iYWRtLWVkaXQtZ3JpZCI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGhlYWQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRyPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGg+VU5FPC90aD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZm9yIG1ldHJpYyBpbiBtZXRyaWNzICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0aD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGlmIG1ldHJpYy5jb2RlID09ICJJTkdSRVNPUyIgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHt7IG1ldHJpYy5uYW1lIH19PGJyPjxzcGFuIGNsYXNzPSJhZG0tY3VycmVuY3ktdGFnIj5VU0QgKCQpPC9zcGFuPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAge3sgbWV0cmljLm5hbWUgfX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGg+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdHI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RoZWFkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRib2R5PgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGZvciByb3cgaW4gdGFyZ2V0X3Jvd3MgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dHI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD57eyByb3cudW5lLm5hbWVfZXMgfX08L3RkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBmb3IgY2VsbCBpbiByb3cuY2VsbHMgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9Im51bWJlciIgc3RlcD0iMC4wMSIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBuYW1lPSJ0YXJnZXRfe3sgcm93LnVuZS5pZCB9fV97eyBjZWxsLm1ldHJpYy5pZCB9fSIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB2YWx1ZT0ieyUgaWYgY2VsbC52YWx1ZSBpcyBub3QgTm9uZSAlfXt7IGNlbGwudmFsdWV8dW5sb2NhbGl6ZSB9fXslIGVuZGlmICV9Ij4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90cj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGJvZHk+CiAgICAgICAgICAgICAgICAgICAgICAgIDwvdGFibGU+CiAgICAgICAgICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICAgICAgICAgICAgeyUgaW5jbHVkZSAicGdjL2FkbWluL19zYXZlX2Zvb3Rlci5odG1sIiB3aXRoIHJlYXNvbl9yZXF1aXJlZD1GYWxzZSAlfQoKICAgICAgICAgICAgICAgIHslIGVsaWYgdGFiID09ICJyZXN1bHRzIiAlfQogICAgICAgICAgICAgICAgPGgzPlJlc3VsdGFkb3MgbWVuc3VhbGVzIMK3IHt7IGZvY3VzX2xhYmVsIH19PC9oMz4KICAgICAgICAgICAgICAgIDxwIGNsYXNzPSJzdWJ0aXRsZSI+CiAgICAgICAgICAgICAgICAgICAgPHN0cm9uZz5JbmdyZXNvczwvc3Ryb25nPjogZWxpamEgPHN0cm9uZz5RPC9zdHJvbmc+IG8gPHN0cm9uZz4kPC9zdHJvbmc+IHBvciBVTkUuCiAgICAgICAgICAgICAgICAgICAgU2kgY2FwdHVyYSBlbiBRLCBzZSBjb252aWVydGUgYSBVU0QgY29uIGVsIFRDIGRlbCBtZXMgeSBzZSBndWFyZGEgZWwgVVNEIGNhbsOzbmljby4KICAgICAgICAgICAgICAgICAgICBTaSBjYXB0dXJhIGVuICQsIHNlIGd1YXJkYSBkaXJlY3RvIGVuIFVTRCAoc2luIFRDKS4gTGFzIGRlbcOhcyBtw6l0cmljYXMgbm8gc29uIG1vbmVkYS4KICAgICAgICAgICAgICAgIDwvcD4KCiAgICAgICAgICAgICAgICB7JSBpZiBub3QgaGFzX2Z4ICV9CiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJhZG0tYmFubmVyIGFkbS1iYW5uZXItd2FybiI+CiAgICAgICAgICAgICAgICAgICAgPHN0cm9uZz5GYWx0YSB0aXBvIGRlIGNhbWJpbyBwYXJhIHt7IGZvY3VzX2xhYmVsIH19Ljwvc3Ryb25nPgogICAgICAgICAgICAgICAgICAgIFNpbiBUQyBubyBzZSBwdWVkZW4gZ3VhcmRhciBpbmdyZXNvcyBlbiBxdWV0emFsZXMgKFEpLiBTw60gc2UgcHVlZGUgY2FwdHVyYXIgZW4gZMOzbGFyZXMgKCQpLgogICAgICAgICAgICAgICAgICAgIDxhIGhyZWY9Ij95ZWFyPXt7IHllYXIgfX0mbW9udGhfZnJvbT17eyBtb250aF9mcm9tIH19Jm1vbnRoX3RvPXt7IG1vbnRoX3RvIH19Jm1vbnRoPXt7IG1vbnRoIH19JnRhYj1meCIKICAgICAgICAgICAgICAgICAgICAgICBjbGFzcz0iYWRtLWJ0biBhZG0tYnRuLXNlY29uZGFyeSIgc3R5bGU9Im1hcmdpbi1sZWZ0OjhweDsiPklyIGEgdGlwb3MgZGUgY2FtYmlvPC9hPgogICAgICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICAgICAgICB7JSBlbHNlICV9CiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJhZG0tYmFubmVyIGFkbS1iYW5uZXItaW5mbyI+CiAgICAgICAgICAgICAgICAgICAgVEMgZGVsIHBlcsOtb2RvIHt7IGZvY3VzX2xhYmVsIH19OiA8c3Ryb25nPjEgVVNEID0ge3sgZnhfcmF0ZSB9fSBHVFE8L3N0cm9uZz4uCiAgICAgICAgICAgICAgICAgICAgQ29udmVyc2nDs246IDxjb2RlPkdUUSDDtyBUQyDihpIgVVNEPC9jb2RlPi4KICAgICAgICAgICAgICAgIDwvZGl2PgogICAgICAgICAgICAgICAgeyUgZW5kaWYgJX0KCiAgICAgICAgICAgICAgICB7JSBpZiBzdGFsZV9pbmdyZXNvc19jb3VudCAlfQogICAgICAgICAgICAgICAgPGRpdiBjbGFzcz0iYWRtLWJhbm5lciBhZG0tYmFubmVyLXdhcm4iPgogICAgICAgICAgICAgICAgICAgIDxzdHJvbmc+e3sgc3RhbGVfaW5ncmVzb3NfY291bnQgfX0gaW5ncmVzbyhzKSBjb24gVEMgZGVzYWN0dWFsaXphZG8gKFNUQUxFKS48L3N0cm9uZz4KICAgICAgICAgICAgICAgICAgICBFbCB0aXBvIGRlIGNhbWJpbyBjYW1iacOzIGRlc3B1w6lzIGRlIGxhIGNhcHR1cmEgZW4gUS4KICAgICAgICAgICAgICAgICAgICA8Zm9ybSBtZXRob2Q9InBvc3QiIHN0eWxlPSJkaXNwbGF5OmlubGluZTsgbWFyZ2luLWxlZnQ6OHB4OyI+CiAgICAgICAgICAgICAgICAgICAgICAgIHslIGNzcmZfdG9rZW4gJX0KICAgICAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0iYWN0aW9uIiB2YWx1ZT0icmVjYWxjX3N0YWxlX2luZ3Jlc29zIj4KICAgICAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ieWVhciIgdmFsdWU9Int7IHllYXIgfX0iPgogICAgICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aCIgdmFsdWU9Int7IG1vbnRoIH19Ij4KICAgICAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ibW9udGhfZnJvbSIgdmFsdWU9Int7IG1vbnRoX2Zyb20gfX0iPgogICAgICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aF90byIgdmFsdWU9Int7IG1vbnRoX3RvIH19Ij4KICAgICAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0idGFiIiB2YWx1ZT0ie3sgdGFiIH19Ij4KICAgICAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0icmVhc29uIiB2YWx1ZT0iUmVjw6FsY3VsbyBTVEFMRSBkZXNkZSByZXN1bHRhZG9zIj4KICAgICAgICAgICAgICAgICAgICAgICAgPGJ1dHRvbiB0eXBlPSJzdWJtaXQiIGNsYXNzPSJhZG0tYnRuIGFkbS1idG4tcHJpbWFyeSI+UmVjYWxjdWxhciBVU0QgZGVzZGUgR1RRPC9idXR0b24+CiAgICAgICAgICAgICAgICAgICAgPC9mb3JtPgogICAgICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICAgICAgICB7JSBlbmRpZiAlfQoKICAgICAgICAgICAgICAgIDxmb3JtIG1ldGhvZD0icG9zdCI+CiAgICAgICAgICAgICAgICAgICAgeyUgY3NyZl90b2tlbiAlfQogICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9ImFjdGlvbiIgdmFsdWU9InNhdmVfcmVzdWx0cyI+CiAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ieWVhciIgdmFsdWU9Int7IHllYXIgfX0iPgogICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9Im1vbnRoIiB2YWx1ZT0ie3sgbW9udGggfX0iPgogICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9Im1vbnRoX2Zyb20iIHZhbHVlPSJ7eyBtb250aF9mcm9tIH19Ij4KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aF90byIgdmFsdWU9Int7IG1vbnRoX3RvIH19Ij4KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJ0YWIiIHZhbHVlPSJ7eyB0YWIgfX0iPgogICAgICAgICAgICAgICAgICAgIDxkaXYgY2xhc3M9ImFkbS1zY3JvbGwiPgogICAgICAgICAgICAgICAgICAgICAgICA8dGFibGUgY2xhc3M9ImFkbS1lZGl0LWdyaWQiPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRoZWFkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0cj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRoPlVORTwvdGg+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGZvciBtZXRyaWMgaW4gbWV0cmljcyAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGg+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiBtZXRyaWMuY29kZSA9PSAiSU5HUkVTT1MiICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7eyBtZXRyaWMubmFtZSB9fSAoZ3VhcmRhZG8gVVNEKTxicj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJhZG0tY3VycmVuY3ktdGFnIj5jYXB0dXJhIFEgbyAkPC9zcGFuPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAge3sgbWV0cmljLm5hbWUgfX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGg+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdHI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RoZWFkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRib2R5PgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGZvciByb3cgaW4gcmVzdWx0X3Jvd3MgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dHI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD57eyByb3cudW5lLm5hbWVfZXMgfX08L3RkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBmb3IgY2VsbCBpbiByb3cuY2VsbHMgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkIGNsYXNzPSJ7JSBpZiBjZWxsLmlzX2luZ3Jlc29zICV9YWRtLWluZ3Jlc29zLWNlbGx7JSBlbmRpZiAlfSI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiBjZWxsLmlzX2luZ3Jlc29zICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJhZG0taW5ncmVzb3Mtc3RhY2siPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxkaXYgY2xhc3M9ImFkbS1jdXJyZW5jeS10b2dnbGUiPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8bGFiZWw+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0icmFkaW8iCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgbmFtZT0iaW5ncmVzb3NfY3Vycl97eyByb3cudW5lLmlkIH19IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlPSJHVFEiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgaWYgY2VsbC5pbnB1dF9jdXJyZW5jeSA9PSAiR1RRIiAlfWNoZWNrZWR7JSBlbmRpZiAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIG9uY2hhbmdlPSJhZG1Ub2dnbGVJbmdyZXNvcyh0aGlzKSI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBRCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvbGFiZWw+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxsYWJlbD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJyYWRpbyIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBuYW1lPSJpbmdyZXNvc19jdXJyX3t7IHJvdy51bmUuaWQgfX0iCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdmFsdWU9IlVTRCIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiBjZWxsLmlucHV0X2N1cnJlbmN5ID09ICJVU0QiICV9Y2hlY2tlZHslIGVuZGlmICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgb25jaGFuZ2U9ImFkbVRvZ2dsZUluZ3Jlc29zKHRoaXMpIj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICQKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC9sYWJlbD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L2Rpdj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8bGFiZWwgY2xhc3M9Im11dGVkIGFkbS1pbmdyZXNvcy1sYWJlbCIgc3R5bGU9ImZvbnQtc2l6ZTowLjc1cmVtOyI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGlmIGNlbGwuaW5wdXRfY3VycmVuY3kgPT0gIlVTRCIgJX1JbmdyZXNvIChVU0QgJCl7JSBlbHNlICV9SW5ncmVzbyAoR1RRIFEpeyUgZW5kaWYgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L2xhYmVsPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJ0ZXh0IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBjbGFzcz0iYWRtLWluZ3Jlc29zLWlucHV0IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBpbnB1dG1vZGU9ImRlY2ltYWwiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIG5hbWU9InJlc3VsdF97eyByb3cudW5lLmlkIH19X3t7IGNlbGwubWV0cmljLmlkIH19IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB2YWx1ZT0ieyUgaWYgY2VsbC52YWx1ZSBpcyBub3QgTm9uZSAlfXt7IGNlbGwudmFsdWV8dW5sb2NhbGl6ZSB9fXslIGVuZGlmICV9IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBkYXRhLW5lZWRzLWZ4PSJ7JSBpZiBub3QgaGFzX2Z4ICV9MXslIGVsc2UgJX0weyUgZW5kaWYgJX0iCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHBsYWNlaG9sZGVyPSJ7JSBpZiBjZWxsLmlucHV0X2N1cnJlbmN5ID09ICdVU0QnICV9VVNEeyUgZWxzZSAlfUdUUXslIGVuZGlmICV9IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiBjZWxsLmlucHV0X2Rpc2FibGVkICV9dGl0bGU9IlNpbiBUQyBndWFyZGFkbyBhw7puOiBjb21wbGV0ZSBlbCBUQyBlbiBlc3RlIG1pc21vIGVudsOtbywgbyBjYXB0dXJlIGVuICQieyUgZW5kaWYgJX0+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPGRpdiBjbGFzcz0ibXV0ZWQiIHN0eWxlPSJmb250LXNpemU6MC43OHJlbTsgbWFyZ2luLXRvcDo0cHg7Ij4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgaWYgY2VsbC5tZWFzdXJlZF91c2RfZGlzcGxheSAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBHdWFyZGFkbyBjYW7Ds25pY286IDxzdHJvbmc+e3sgY2VsbC5tZWFzdXJlZF91c2RfZGlzcGxheSB9fSBVU0Q8L3N0cm9uZz4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBHdWFyZGFkbyBjYW7Ds25pY28gVVNEOiDigJQKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgaWYgY2VsbC5meF91c2VkICV9PGJyPkZYIHVzYWRvOiB7eyBjZWxsLmZ4X3VzZWQgfX17JSBlbmRpZiAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiBjZWxsLmNvbnZlcnNpb25fc3RhdHVzID09ICJTVEFMRV9GWCIgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPGJyPjxzcGFuIHN0eWxlPSJjb2xvcjojYjQ1MzA5O2ZvbnQtd2VpZ2h0OjYwMDsiPlRDIGRlc2FjdHVhbGl6YWRvPC9zcGFuPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbGlmIGNlbGwuY29udmVyc2lvbl9zdGF0dXMgPT0gIkNPTlZFUlRFRCIgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPGJyPjxzcGFuIHN0eWxlPSJjb2xvcjojMDY1ZjQ2OyI+Q29udmVydGlkbyBR4oaSJDwvc3Bhbj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZWxpZiBjZWxsLmNvbnZlcnNpb25fc3RhdHVzID09ICJOQVRJVkVfVVNEIiAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8YnI+PHNwYW4gc3R5bGU9ImNvbG9yOiMwNjVmNDY7Ij5VU0QgbmF0aXZvPC9zcGFuPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvZGl2PgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbHNlICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0ibnVtYmVyIiBzdGVwPSIwLjAxIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIG5hbWU9InJlc3VsdF97eyByb3cudW5lLmlkIH19X3t7IGNlbGwubWV0cmljLmlkIH19IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlPSJ7JSBpZiBjZWxsLnZhbHVlIGlzIG5vdCBOb25lICV9e3sgY2VsbC52YWx1ZXx1bmxvY2FsaXplIH19eyUgZW5kaWYgJX0iPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90cj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGJvZHk+CiAgICAgICAgICAgICAgICAgICAgICAgIDwvdGFibGU+CiAgICAgICAgICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICAgICAgICAgICAgeyUgaW5jbHVkZSAicGdjL2FkbWluL19zYXZlX2Zvb3Rlci5odG1sIiB3aXRoIHJlYXNvbl9yZXF1aXJlZD1UcnVlICV9CgogICAgICAgICAgICAgICAgeyUgZWxpZiB0YWIgPT0gInJlcXVpcmVtZW50cyIgJX0KICAgICAgICAgICAgICAgIDxoMz5SZXNwdWVzdGEgYSByZXF1ZXJpbWllbnRvczwvaDM+CiAgICAgICAgICAgICAgICA8cCBjbGFzcz0ic3VidGl0bGUiPkN1bXBsaW1pZW50byBtYW51YWwgcG9yIFVORS4gU2kgaGF5IGluY2lkZW5jaWEsIGluZGlxdWUgbm90YSBvIG1vdGl2by48L3A+CiAgICAgICAgICAgICAgICA8Zm9ybSBtZXRob2Q9InBvc3QiPgogICAgICAgICAgICAgICAgICAgIHslIGNzcmZfdG9rZW4gJX0KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJhY3Rpb24iIHZhbHVlPSJzYXZlX3JlcXVpcmVtZW50cyI+CiAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ieWVhciIgdmFsdWU9Int7IHllYXIgfX0iPgogICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9Im1vbnRoIiB2YWx1ZT0ie3sgbW9udGggfX0iPgogICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9Im1vbnRoX2Zyb20iIHZhbHVlPSJ7eyBtb250aF9mcm9tIH19Ij4KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aF90byIgdmFsdWU9Int7IG1vbnRoX3RvIH19Ij4KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJ0YWIiIHZhbHVlPSJ7eyB0YWIgfX0iPgogICAgICAgICAgICAgICAgICAgIDx0YWJsZSBjbGFzcz0iYWRtLWVkaXQtZ3JpZCI+CiAgICAgICAgICAgICAgICAgICAgICAgIDx0aGVhZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0cj48dGg+VU5FPC90aD48dGg+Q3VtcGxlPC90aD48dGg+Tm90YSBkZSBpbmNpZGVuY2lhPC90aD48L3RyPgogICAgICAgICAgICAgICAgICAgICAgICA8L3RoZWFkPgogICAgICAgICAgICAgICAgICAgICAgICA8dGJvZHk+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBmb3IgaXRlbSBpbiByZXF1aXJlbWVudHMgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0cj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGQ+e3sgaXRlbS51bmUubmFtZV9lcyB9fTwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iY2hlY2tib3giIG5hbWU9InJlcV9jb21wbGlhbnRfe3sgaXRlbS51bmUuaWQgfX0iIHZhbHVlPSIxIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgaWYgbm90IGl0ZW0ub2JqIG9yIGl0ZW0ub2JqLmlzX2NvbXBsaWFudCAlfWNoZWNrZWR7JSBlbmRpZiAlfT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9InRleHQiIG5hbWU9InJlcV9ub3RlX3t7IGl0ZW0udW5lLmlkIH19IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdmFsdWU9InslIGlmIGl0ZW0ub2JqICV9e3sgaXRlbS5vYmouaW5jaWRlbnRfbm90ZSB9fXslIGVuZGlmICV9IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgc3R5bGU9Im1heC13aWR0aDoyODBweDsiPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RyPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgICAgICAgICAgICAgICAgIDwvdGJvZHk+CiAgICAgICAgICAgICAgICAgICAgPC90YWJsZT4KICAgICAgICAgICAgICAgICAgICB7JSBpbmNsdWRlICJwZ2MvYWRtaW4vX3NhdmVfZm9vdGVyLmh0bWwiIHdpdGggcmVhc29uX3JlcXVpcmVkPUZhbHNlICV9CgogICAgICAgICAgICAgICAgeyUgZWxpZiB0YWIgPT0gImZ4IiAlfQogICAgICAgICAgICAgICAgPGgzPlRpcG9zIGRlIGNhbWJpbyDCtyB7eyBsYWJlbCB9fTwvaDM+CiAgICAgICAgICAgICAgICA8cCBjbGFzcz0ic3VidGl0bGUiPgogICAgICAgICAgICAgICAgICAgIDEgVVNEID0gWCBHVFEuIFNpIGVsIHJhbmdvIGVzIHZhcmlvcyBtZXNlcywgZWRpdGUgPHN0cm9uZz50b2Rvczwvc3Ryb25nPiBhcXXDrS4KICAgICAgICAgICAgICAgICAgICBTaSBjYW1iaWEgdW4gVEMgeWEgdXNhZG8gcG9yIGluZ3Jlc29zIGNhcHR1cmFkb3MgZW4gUSwgZXNvcyBzZSBtYXJjYW4gU1RBTEUgKG5vIHNlIHJlY2FsY3VsYW4gc29sb3MpLgogICAgICAgICAgICAgICAgPC9wPgogICAgICAgICAgICAgICAgeyUgaWYgbWlzc2luZ19meF9tb250aHMgJX0KICAgICAgICAgICAgICAgIDxkaXYgY2xhc3M9ImFkbS1iYW5uZXIgYWRtLWJhbm5lci13YXJuIj4KICAgICAgICAgICAgICAgICAgICBGYWx0YSBUQyBlbjogeyUgZm9yIG0gaW4gbWlzc2luZ19meF9tb250aHMgJX08Y29kZSBzdHlsZT0ibWFyZ2luLXJpZ2h0OjZweDsiPnt7IG0gfX08L2NvZGU+eyUgZW5kZm9yICV9CiAgICAgICAgICAgICAgICA8L2Rpdj4KICAgICAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgICAgICA8Zm9ybSBtZXRob2Q9InBvc3QiPgogICAgICAgICAgICAgICAgICAgIHslIGNzcmZfdG9rZW4gJX0KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJhY3Rpb24iIHZhbHVlPSJzYXZlX2Z4Ij4KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJ5ZWFyIiB2YWx1ZT0ie3sgeWVhciB9fSI+CiAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ibW9udGgiIHZhbHVlPSJ7eyBtb250aCB9fSI+CiAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ibW9udGhfZnJvbSIgdmFsdWU9Int7IG1vbnRoX2Zyb20gfX0iPgogICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9Im1vbnRoX3RvIiB2YWx1ZT0ie3sgbW9udGhfdG8gfX0iPgogICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9InRhYiIgdmFsdWU9Int7IHRhYiB9fSI+CiAgICAgICAgICAgICAgICAgICAgPGRpdiBjbGFzcz0iYWRtLXNjcm9sbCI+CiAgICAgICAgICAgICAgICAgICAgICAgIDx0YWJsZSBjbGFzcz0iYWRtLWVkaXQtZ3JpZCIgc3R5bGU9Im1heC13aWR0aDo0MjBweDsiPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRoZWFkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0cj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRoPk1lczwvdGg+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0aD4xIFVTRCA9IOKApiBHVFE8L3RoPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdHI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RoZWFkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRib2R5PgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGZvciByb3cgaW4gZnhfcm93cyAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ciB7JSBpZiByb3cuaXNfZm9jdXMgJX1zdHlsZT0iYmFja2dyb3VuZDojZjBmOWZmOyJ7JSBlbmRpZiAlfT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkIHN0eWxlPSJ0ZXh0LWFsaWduOmxlZnQ7Ij4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHt7IHJvdy5sYWJlbCB9fQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgaWYgcm93Lm1pc3NpbmcgJX08c3BhbiBjbGFzcz0ibXV0ZWQiPiAoc2luIFRDKTwvc3Bhbj57JSBlbmRpZiAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgaWYgcm93LmlzX2ZvY3VzICV9PHNwYW4gY2xhc3M9Im11dGVkIj4gwrcgZm9jbzwvc3Bhbj57JSBlbmRpZiAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0idGV4dCIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBuYW1lPSJmeF92YWx1ZV97eyByb3cubW9udGggfX0iCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgaW5wdXRtb2RlPSJkZWNpbWFsIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHN0eWxlPSJwYWRkaW5nOjhweDsgd2lkdGg6MTYwcHg7IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlPSJ7JSBpZiByb3cudmFsdWUgaXMgbm90IE5vbmUgJX17eyByb3cudmFsdWV8dW5sb2NhbGl6ZSB9fXslIGVuZGlmICV9IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHBsYWNlaG9sZGVyPSJlai4gNy44NSI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90cj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGJvZHk+CiAgICAgICAgICAgICAgICAgICAgICAgIDwvdGFibGU+CiAgICAgICAgICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICAgICAgICAgICAgeyUgaW5jbHVkZSAicGdjL2FkbWluL19zYXZlX2Zvb3Rlci5odG1sIiB3aXRoIHJlYXNvbl9yZXF1aXJlZD1GYWxzZSAlfQoKICAgICAgICAgICAgICAgIHslIGVsaWYgdGFiID09ICJhbGlhc2VzIiAlfQogICAgICAgICAgICAgICAgPGgzPkFsaWFzIGRlIFVORTwvaDM+CiAgICAgICAgICAgICAgICA8cCBjbGFzcz0ic3VidGl0bGUiPk5vcm1hbGljZSB2YWxvcmVzIGNydWRvcyBkZXRlY3RhZG9zIGVuIGltcG9ydGFjaW9uZXMuCiAgICAgICAgICAgICAgICAgICAgU2kgZWwgdmFsb3IgY3J1ZG8gbWVuY2lvbmEgPHN0cm9uZz5JbnZlc3RtZW50PC9zdHJvbmc+LCBzaWVtcHJlIGVzIDxzdHJvbmc+SW52ZXJzaW9uZXM8L3N0cm9uZz4uPC9wPgogICAgICAgICAgICAgICAgeyUgaWYgcGVuZGluZ19hbGlhc2VzICV9CiAgICAgICAgICAgICAgICA8cD48c3Ryb25nPlZhbG9yZXMgcGVuZGllbnRlcyBlbiBlc3RlIHBlcsOtb2RvOjwvc3Ryb25nPgogICAgICAgICAgICAgICAgICAgIHslIGZvciByYXcgaW4gcGVuZGluZ19hbGlhc2VzICV9PGNvZGUgc3R5bGU9Im1hcmdpbi1yaWdodDo2cHg7Ij57eyByYXcgfX08L2NvZGU+eyUgZW5kZm9yICV9CiAgICAgICAgICAgICAgICA8L3A+CiAgICAgICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgICAgICAgPGZvcm0gbWV0aG9kPSJwb3N0IiBzdHlsZT0ibWFyZ2luLWJvdHRvbToyMHB4OyI+CiAgICAgICAgICAgICAgICAgICAgeyUgY3NyZl90b2tlbiAlfQogICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9ImFjdGlvbiIgdmFsdWU9InNhdmVfYWxpYXMiPgogICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9InllYXIiIHZhbHVlPSJ7eyB5ZWFyIH19Ij4KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aCIgdmFsdWU9Int7IG1vbnRoIH19Ij4KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aF9mcm9tIiB2YWx1ZT0ie3sgbW9udGhfZnJvbSB9fSI+CiAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ibW9udGhfdG8iIHZhbHVlPSJ7eyBtb250aF90byB9fSI+CiAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0idGFiIiB2YWx1ZT0ie3sgdGFiIH19Ij4KICAgICAgICAgICAgICAgICAgICA8ZGl2IHN0eWxlPSJkaXNwbGF5OmZsZXg7IGZsZXgtd3JhcDp3cmFwOyBnYXA6MTJweDsgYWxpZ24taXRlbXM6ZW5kOyI+CiAgICAgICAgICAgICAgICAgICAgICAgIDxkaXY+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8bGFiZWw+VmFsb3IgY3J1ZG88L2xhYmVsPjxicj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJ0ZXh0IiBuYW1lPSJhbGlhc19yYXciIGxpc3Q9InBlbmRpbmctYWxpYXMtbGlzdCIgc3R5bGU9InBhZGRpbmc6OHB4OyBtaW4td2lkdGg6MjAwcHg7Ij4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxkYXRhbGlzdCBpZD0icGVuZGluZy1hbGlhcy1saXN0Ij4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBmb3IgcmF3IGluIHBlbmRpbmdfYWxpYXNlcyAlfTxvcHRpb24gdmFsdWU9Int7IHJhdyB9fSI+eyUgZW5kZm9yICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L2RhdGFsaXN0PgogICAgICAgICAgICAgICAgICAgICAgICA8L2Rpdj4KICAgICAgICAgICAgICAgICAgICAgICAgPGRpdj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxsYWJlbD5VTkUgZGVzdGlubzwvbGFiZWw+PGJyPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHNlbGVjdCBuYW1lPSJhbGlhc191bmUiPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGZvciB1bmUgaW4gdW5lcyAlfTxvcHRpb24gdmFsdWU9Int7IHVuZS5pZCB9fSI+e3sgdW5lLm5hbWVfZXMgfX08L29wdGlvbj57JSBlbmRmb3IgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvc2VsZWN0PgogICAgICAgICAgICAgICAgICAgICAgICA8L2Rpdj4KICAgICAgICAgICAgICAgICAgICA8L2Rpdj4KICAgICAgICAgICAgICAgICAgICB7JSBpbmNsdWRlICJwZ2MvYWRtaW4vX3NhdmVfZm9vdGVyLmh0bWwiIHdpdGggcmVhc29uX3JlcXVpcmVkPUZhbHNlICV9CgogICAgICAgICAgICAgICAgPGg0IHN0eWxlPSJmb250LXNpemU6MC45MnJlbTsiPkFsaWFzIGFjdGl2b3Mg4oCUIGVkaXRlIFVORSB5IGd1YXJkZTwvaDQ+CiAgICAgICAgICAgICAgICA8Zm9ybSBtZXRob2Q9InBvc3QiPgogICAgICAgICAgICAgICAgICAgIHslIGNzcmZfdG9rZW4gJX0KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJhY3Rpb24iIHZhbHVlPSJzYXZlX2FsaWFzZXNfYnVsayI+CiAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ieWVhciIgdmFsdWU9Int7IHllYXIgfX0iPgogICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9Im1vbnRoIiB2YWx1ZT0ie3sgbW9udGggfX0iPgogICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9Im1vbnRoX2Zyb20iIHZhbHVlPSJ7eyBtb250aF9mcm9tIH19Ij4KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aF90byIgdmFsdWU9Int7IG1vbnRoX3RvIH19Ij4KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJ0YWIiIHZhbHVlPSJ7eyB0YWIgfX0iPgogICAgICAgICAgICAgICAgICAgIDxkaXYgY2xhc3M9ImFkbS1zY3JvbGwiIHN0eWxlPSJtYXgtaGVpZ2h0OjM2MHB4OyI+CiAgICAgICAgICAgICAgICAgICAgICAgIDx0YWJsZSBjbGFzcz0iYWRtLWVkaXQtZ3JpZCI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGhlYWQ+PHRyPjx0aD5WYWxvciBjcnVkbzwvdGg+PHRoPlVORTwvdGg+PC90cj48L3RoZWFkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRib2R5PgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGZvciBhbGlhcyBpbiBhbGlhc2VzICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRyPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGQgc3R5bGU9InRleHQtYWxpZ246bGVmdDsiPnt7IGFsaWFzLnJhd192YWx1ZSB9fTwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxzZWxlY3QgbmFtZT0iYWxpYXNfe3sgYWxpYXMuaWQgfX1fdW5lIj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBmb3IgdW5lIGluIHVuZXMgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8b3B0aW9uIHZhbHVlPSJ7eyB1bmUuaWQgfX0iIHslIGlmIGFsaWFzLnVuZV9pZCA9PSB1bmUuaWQgJX1zZWxlY3RlZHslIGVuZGlmICV9PgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7eyB1bmUubmFtZV9lcyB9fQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvb3B0aW9uPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC9zZWxlY3Q+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90cj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbXB0eSAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0cj48dGQgY29sc3Bhbj0iMiIgY2xhc3M9Im11dGVkIj5TaW4gYWxpYXNlcyBhY3Rpdm9zLjwvdGQ+PC90cj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGJvZHk+CiAgICAgICAgICAgICAgICAgICAgICAgIDwvdGFibGU+CiAgICAgICAgICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICAgICAgICAgICAgeyUgaW5jbHVkZSAicGdjL2FkbWluL19zYXZlX2Zvb3Rlci5odG1sIiB3aXRoIHJlYXNvbl9yZXF1aXJlZD1GYWxzZSAlfQoKICAgICAgICAgICAgICAgIHslIGVsaWYgdGFiID09ICJpbXBvcnRzIiAlfQogICAgICAgICAgICAgICAgPGgzPlJlZ2lzdHJvcyBpbXBvcnRhZG9zPC9oMz4KICAgICAgICAgICAgICAgIDxwIGNsYXNzPSJzdWJ0aXRsZSI+Q29ycmlqYSBmaWxhcyBjb24gb2JzZXJ2YWNpb25lcyBvIFVORSBubyByZXN1ZWx0YXMuPC9wPgogICAgICAgICAgICAgICAgPGZvcm0gbWV0aG9kPSJwb3N0Ij4KICAgICAgICAgICAgICAgICAgICB7JSBjc3JmX3Rva2VuICV9CiAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0iYWN0aW9uIiB2YWx1ZT0ic2F2ZV9pbXBvcnRzIj4KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJ5ZWFyIiB2YWx1ZT0ie3sgeWVhciB9fSI+CiAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ibW9udGgiIHZhbHVlPSJ7eyBtb250aCB9fSI+CiAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ibW9udGhfZnJvbSIgdmFsdWU9Int7IG1vbnRoX2Zyb20gfX0iPgogICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9Im1vbnRoX3RvIiB2YWx1ZT0ie3sgbW9udGhfdG8gfX0iPgogICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9InRhYiIgdmFsdWU9Int7IHRhYiB9fSI+CgogICAgICAgICAgICAgICAgICAgIDxoNCBzdHlsZT0iZm9udC1zaXplOjAuOTJyZW07IG1hcmdpbi10b3A6MDsiPkNsaWVudGVzIG51ZXZvczwvaDQ+CiAgICAgICAgICAgICAgICAgICAgeyUgaWYgbmV3X2NsaWVudF9yb3dzICV9CiAgICAgICAgICAgICAgICAgICAgPGRpdiBjbGFzcz0iYWRtLXNjcm9sbCI+CiAgICAgICAgICAgICAgICAgICAgICAgIDx0YWJsZSBjbGFzcz0iYWRtLWVkaXQtZ3JpZCI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGhlYWQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRyPjx0aD5NZXM8L3RoPjx0aD5DbGllbnRlPC90aD48dGg+VU5FPC90aD48dGg+wr9DdWVudGE/PC90aD48dGg+T2JzZXJ2YWNpb25lczwvdGg+PC90cj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGhlYWQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGJvZHk+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZm9yIHJvdyBpbiBuZXdfY2xpZW50X3Jvd3MgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dHI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZCBjbGFzcz0ibXV0ZWQiPnt7IHJvdy5tb250aHxzdHJpbmdmb3JtYXQ6IjAyZCIgfX08L3RkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGQ+e3sgcm93LmNsaWVudF9uYW1lfGRlZmF1bHQ6cm93Lm9wZXJhdGlvbl9jb2RlIH19PC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkPnt7IHJvdy51bmUubmFtZV9lcyB9fTwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJjaGVja2JveCIgbmFtZT0ibmNfe3sgcm93LmlkIH19X2NvdW50c19hc19uZXciIHZhbHVlPSIxIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGlmIHJvdy5jb3VudHNfYXNfbmV3ICV9Y2hlY2tlZHslIGVuZGlmICV9PgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0idGV4dCIgbmFtZT0ibmNfe3sgcm93LmlkIH19X29ic2VydmF0aW9ucyIgdmFsdWU9Int7IHJvdy5vYnNlcnZhdGlvbnMgfX0iIHN0eWxlPSJtYXgtd2lkdGg6MjAwcHg7Ij4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RyPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90Ym9keT4KICAgICAgICAgICAgICAgICAgICAgICAgPC90YWJsZT4KICAgICAgICAgICAgICAgICAgICA8L2Rpdj4KICAgICAgICAgICAgICAgICAgICB7JSBlbHNlICV9CiAgICAgICAgICAgICAgICAgICAgPHAgY2xhc3M9Im11dGVkIj5TaW4gZmlsYXMgZGUgY2xpZW50ZXMgbnVldm9zIHBhcmEgZXN0ZSBwZXLDrW9kby48L3A+CiAgICAgICAgICAgICAgICAgICAgeyUgZW5kaWYgJX0KCiAgICAgICAgICAgICAgICAgICAgPGg0IHN0eWxlPSJmb250LXNpemU6MC45MnJlbTsgbWFyZ2luLXRvcDoyMHB4OyI+VmVudGEgY3J1emFkYTwvaDQ+CiAgICAgICAgICAgICAgICAgICAgeyUgaWYgY3Jvc3Nfc2FsZV9yb3dzICV9CiAgICAgICAgICAgICAgICAgICAgPGRpdiBjbGFzcz0iYWRtLXNjcm9sbCI+CiAgICAgICAgICAgICAgICAgICAgICAgIDx0YWJsZSBjbGFzcz0iYWRtLWVkaXQtZ3JpZCI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGhlYWQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRyPjx0aD5DbGllbnRlPC90aD48dGg+T3JpZ2VuPC90aD48dGg+RGVzdGlubzwvdGg+PHRoPlJhdyBvcmlnZW48L3RoPjx0aD5SYXcgZGVzdGlubzwvdGg+PC90cj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGhlYWQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGJvZHk+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZm9yIHJvdyBpbiBjcm9zc19zYWxlX3Jvd3MgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dHI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD57eyByb3cuY2xpZW50X25hbWV8ZGVmYXVsdDpyb3cub3BlcmF0aW9uX2NvZGUgfX08L3RkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8c2VsZWN0IG5hbWU9ImNzX3t7IHJvdy5pZCB9fV9vcmlnIj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8b3B0aW9uIHZhbHVlPSIiPuKAlDwvb3B0aW9uPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGZvciB1bmUgaW4gdW5lcyAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9Int7IHVuZS5pZCB9fSIgeyUgaWYgcm93LnVuZV9vcmlnaW5faWQgPT0gdW5lLmlkICV9c2VsZWN0ZWR7JSBlbmRpZiAlfT57eyB1bmUuY29kZSB9fTwvb3B0aW9uPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC9zZWxlY3Q+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxzZWxlY3QgbmFtZT0iY3Nfe3sgcm93LmlkIH19X2Rlc3QiPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9IiI+4oCUPC9vcHRpb24+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZm9yIHVuZSBpbiB1bmVzICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPG9wdGlvbiB2YWx1ZT0ie3sgdW5lLmlkIH19IiB7JSBpZiByb3cudW5lX2Rlc3RpbmF0aW9uX2lkID09IHVuZS5pZCAlfXNlbGVjdGVkeyUgZW5kaWYgJX0+e3sgdW5lLmNvZGUgfX08L29wdGlvbj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvc2VsZWN0PgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGQgY2xhc3M9Im11dGVkIj57eyByb3cucmF3X3VuZV9vcmlnaW4gfX08L3RkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGQgY2xhc3M9Im11dGVkIj57eyByb3cucmF3X3VuZV9kZXN0aW5hdGlvbiB9fTwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90cj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGJvZHk+CiAgICAgICAgICAgICAgICAgICAgICAgIDwvdGFibGU+CiAgICAgICAgICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICAgICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgICAgICAgICAgIDxwIGNsYXNzPSJtdXRlZCI+U2luIGZpbGFzIGRlIHZlbnRhIGNydXphZGEgcGFyYSBlc3RlIHBlcsOtb2RvLjwvcD4KICAgICAgICAgICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgICAgICAgICAgIHslIGluY2x1ZGUgInBnYy9hZG1pbi9fc2F2ZV9mb290ZXIuaHRtbCIgd2l0aCByZWFzb25fcmVxdWlyZWQ9RmFsc2UgJX0KCiAgICAgICAgICAgICAgICB7JSBlbGlmIHRhYiA9PSAibm90ZXMiICV9CiAgICAgICAgICAgICAgICA8aDM+Tm90YXMgZGVsIHBlcsOtb2RvPC9oMz4KICAgICAgICAgICAgICAgIDxwIGNsYXNzPSJzdWJ0aXRsZSI+T2JzZXJ2YWNpb25lcyBhZG1pbmlzdHJhdGl2YXMgdmlzaWJsZXMgcGFyYSBlbCBlcXVpcG8gb3BlcmF0aXZvLjwvcD4KICAgICAgICAgICAgICAgIDxmb3JtIG1ldGhvZD0icG9zdCI+CiAgICAgICAgICAgICAgICAgICAgeyUgY3NyZl90b2tlbiAlfQogICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9ImFjdGlvbiIgdmFsdWU9InNhdmVfbm90ZXMiPgogICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9InllYXIiIHZhbHVlPSJ7eyB5ZWFyIH19Ij4KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aCIgdmFsdWU9Int7IG1vbnRoIH19Ij4KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aF9mcm9tIiB2YWx1ZT0ie3sgbW9udGhfZnJvbSB9fSI+CiAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ibW9udGhfdG8iIHZhbHVlPSJ7eyBtb250aF90byB9fSI+CiAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0idGFiIiB2YWx1ZT0ie3sgdGFiIH19Ij4KICAgICAgICAgICAgICAgICAgICA8dGV4dGFyZWEgbmFtZT0icGVyaW9kX25vdGUiIHJvd3M9IjYiIHN0eWxlPSJ3aWR0aDoxMDAlOyBwYWRkaW5nOjEycHg7IGJvcmRlcjoxcHggc29saWQgI2Q5ZTJlYzsgYm9yZGVyLXJhZGl1czo4cHg7Ij57eyBwZXJpb2Rfbm90ZSB9fTwvdGV4dGFyZWE+CiAgICAgICAgICAgICAgICAgICAgeyUgaW5jbHVkZSAicGdjL2FkbWluL19zYXZlX2Zvb3Rlci5odG1sIiB3aXRoIHJlYXNvbl9yZXF1aXJlZD1GYWxzZSAlfQogICAgICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgPC9kaXY+CgogICAgICAgIDxkaXY+CiAgICAgICAgICAgIDxkaXYgY2xhc3M9ImFkbS1zaWRlLWNhcmQiPgogICAgICAgICAgICAgICAgPGg0Pkd1w61hIHLDoXBpZGE8L2g0PgogICAgICAgICAgICAgICAgPGRpdiBjbGFzcz0iYWRtLXJlbWluZGVyIj48c3Ryb25nPjEuPC9zdHJvbmc+IFRpcG9zIGRlIGNhbWJpbyBkZWwgcmFuZ28gKHNpIGNhcHR1cmEgaW5ncmVzb3MgZW4gUSkuPC9kaXY+CiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJhZG0tcmVtaW5kZXIiPjxzdHJvbmc+Mi48L3N0cm9uZz4gTWV0YXMgZGUgaW5ncmVzb3Mgc2llbXByZSBlbiA8c3Ryb25nPlVTRCAoJCk8L3N0cm9uZz4uPC9kaXY+CiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJhZG0tcmVtaW5kZXIiPjxzdHJvbmc+My48L3N0cm9uZz4gUmVzdWx0YWRvcyDihpIgSW5ncmVzb3M6IFEgbyAkOyBsbyBndWFyZGFkbyBlcyBzaWVtcHJlIFVTRC48L2Rpdj4KICAgICAgICAgICAgICAgIDxkaXYgY2xhc3M9ImFkbS1yZW1pbmRlciI+Q2FtcG9zIHZhY8Otb3Mgbm8gc29icmVzY3JpYmVuLiBSZXN1bHRhZG9zIHJlcXVpZXJlbiBtb3Rpdm8uPC9kaXY+CiAgICAgICAgICAgIDwvZGl2PgogICAgICAgICAgICA8ZGl2IGNsYXNzPSJhZG0tc2lkZS1jYXJkIj4KICAgICAgICAgICAgICAgIDxoND5DYW1iaW9zIHJlY2llbnRlczwvaDQ+CiAgICAgICAgICAgICAgICB7JSBmb3IgZWRpdCBpbiByZWNlbnRfZWRpdHMgJX0KICAgICAgICAgICAgICAgIDxkaXYgY2xhc3M9ImFkbS1sb2ctaXRlbSI+CiAgICAgICAgICAgICAgICAgICAgPHN0cm9uZz57eyBlZGl0LmdldF9lbnRpdHlfdHlwZV9kaXNwbGF5IH19PC9zdHJvbmc+IMK3IHt7IGVkaXQuZmllbGRfbmFtZSB9fTxicj4KICAgICAgICAgICAgICAgICAgICB7eyBlZGl0Lm9sZF92YWx1ZXxkZWZhdWx0OiLigJQiIH19IOKGkiB7eyBlZGl0Lm5ld192YWx1ZXxkZWZhdWx0OiLigJQiIH19CiAgICAgICAgICAgICAgICAgICAgPGJyPjxzcGFuIGNsYXNzPSJtdXRlZCI+e3sgZWRpdC5jcmVhdGVkX2F0fGRhdGU6ImQvbS9ZIEg6aSIgfX17JSBpZiBlZGl0LmVkaXRlZF9ieSAlfSDCtyB7eyBlZGl0LmVkaXRlZF9ieS51c2VybmFtZSB9fXslIGVuZGlmICV9PC9zcGFuPgogICAgICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICAgICAgICB7JSBlbXB0eSAlfQogICAgICAgICAgICAgICAgPHAgY2xhc3M9Im11dGVkIj5TaW4gZWRpY2lvbmVzIG1hbnVhbGVzIGVuIGVzdGUgcGVyw61vZG8uPC9wPgogICAgICAgICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgICAgIDwvZGl2PgogICAgICAgIDwvZGl2PgogICAgPC9kaXY+CjwvZGl2Pgp7JSBlbmRibG9jayAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgc/admin_monthly.html
PATH_JSON="templates/pgc/admin_monthly.html"
FILENAME=admin_monthly.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=228
SIZE_BYTES_UTF8=13152
CONTENT_SHA256=e212fe789b64736e0111f45219556174c93f4aadbe4bae562a4938154a9ae3c3
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~html
{% extends "base.html" %}
{% load l10n %}

{% block title %}Administración mensual{% endblock %}

{% block content %}
{% include "pgc/admin/_styles.html" %}

<div class="adm">
    {% include "pgc/admin/_nav.html" with adm_nav_active="monthly" show_django_admin=True %}

    <div class="adm-header">
        <div class="adm-header-top">
            <div>
                <p class="muted" style="margin:0;">Panel de operaciones</p>
                <div class="adm-period-label">{{ snapshot.label }}</div>
                <span class="adm-period-status {{ snapshot.period_status }}">{{ snapshot.period_status_label }}</span>
            </div>
            <div style="display:flex; flex-wrap:wrap; gap:10px; align-items:end;">
                {% include "pgc/admin/_period_select.html" %}
            </div>
        </div>
    </div>

    <div class="adm-route">
        {% for block in snapshot.blocks %}
        <a href="?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}&block={{ block.id }}"
           class="adm-block-card {% if block.id == selected_block %}active{% endif %}">
            <div class="adm-block-step">Paso {{ block.step }}</div>
            <div class="adm-block-title">{{ block.label }}</div>
            <span class="adm-badge {{ block.status }}">{{ block.status_label }}</span>
            <div class="adm-block-meta">
                {{ block.summary }}
                {% if block.last_action_at %}
                <br>{{ block.last_action_at|date:"d/m/Y H:i" }}{% if block.last_action_by %} · {{ block.last_action_by }}{% endif %}
                {% endif %}
            </div>
        </a>
        {% endfor %}
    </div>

    <div class="adm-layout">
        <div>
            <div class="adm-panel">
                <h3>{{ block_detail.label }}</h3>
                <p class="subtitle">{{ block_detail.short }}</p>

                <ul class="adm-checklist">
                    {% for item in block_detail.checklist %}
                    <li class="{% if item.done %}done{% endif %}">{{ item.label }}</li>
                    {% endfor %}
                </ul>

                {% if selected_block == "targets" %}
                <p class="muted">Ajuste metas del plan en la pantalla de edición manual.</p>
                <a href="{% url 'pgc:admin_manual_edit' %}?year={{ year }}&month={{ month }}&tab=targets"
                   class="adm-btn adm-btn-primary">Editar metas del período</a>

                {% elif selected_block == "manual_requirements" %}
                <p class="muted">Registre cumplimiento de respuesta a requerimientos por UNE.</p>
                <a href="{% url 'pgc:admin_manual_edit' %}?year={{ year }}&month={{ month }}&tab=requirements"
                   class="adm-btn adm-btn-primary">Editar requerimientos</a>

                {% elif selected_block == "review" %}
                <p class="muted">Revise el tablero después de cargar y recalcular.</p>
                <a href="{% url 'pgc:dashboard' %}?year={{ year }}&month={{ month }}" class="adm-btn adm-btn-primary">Abrir tablero</a>
                <a href="{% url 'pgc:admin_ingresos_year' %}?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}"
                   class="adm-btn adm-btn-secondary">Captura ingresos (año)</a>
                <a href="{% url 'pgc:ingresos' %}?year={{ year }}&month={{ month }}" class="adm-btn adm-btn-secondary">Ingresos vs meta</a>

                {% else %}
                <form method="post" enctype="multipart/form-data" style="margin-bottom:16px;">
                    {% csrf_token %}
                    <input type="hidden" name="action" value="upload">
                    <input type="hidden" name="block" value="{{ selected_block }}">
                    <input type="hidden" name="year" value="{{ year }}">
                    <input type="hidden" name="month" value="{{ month }}">
                    <input type="hidden" name="month_from" value="{{ month_from }}">
                    <input type="hidden" name="month_to" value="{{ month_to }}">
                    <div style="margin-bottom:10px;">{{ upload_form.stored_file }}</div>
                    <button type="submit" class="adm-btn adm-btn-primary">Subir archivo</button>
                </form>

                {% if block_detail.uploads %}
                <h4 style="margin:0 0 8px; font-size:0.92rem;">Archivos del período</h4>
                {% for u in block_detail.uploads %}
                <div class="adm-upload-row">
                    <div>
                        <strong>{{ u.filename }}</strong><br>
                        <span class="muted">{{ u.status_display }} · {{ u.created_at|date:"d/m/Y H:i" }}{% if u.user %} · {{ u.user }}{% endif %}</span>
                    </div>
                    <div class="adm-upload-actions">
                        <form method="post" class="adm-process-form">
                            {% csrf_token %}
                            <input type="hidden" name="action" value="process">
                            <input type="hidden" name="block" value="{{ selected_block }}">
                            <input type="hidden" name="file_id" value="{{ u.id }}">
                            <input type="hidden" name="year" value="{{ year }}">
                            <input type="hidden" name="month" value="{{ month }}">
                            <input type="hidden" name="month_from" value="{{ month_from }}">
                            <input type="hidden" name="month_to" value="{{ month_to }}">
                            {% if u.status == "PARSED_OK" %}
                            <button type="button" class="adm-btn adm-btn-ghost" disabled title="Ya procesado">Procesado</button>
                            {% else %}
                            <button type="submit" class="adm-btn adm-btn-secondary adm-process-btn">Procesar</button>
                            {% endif %}
                        </form>
                        {% if u.can_discard %}
                        <form method="post" class="adm-discard-form"
                              onsubmit="return confirm('¿Quitar de la cola «{{ u.filename|escapejs }}»? Solo elimina el archivo pendiente; no toca datos ya procesados.');">
                            {% csrf_token %}
                            <input type="hidden" name="action" value="discard_pending">
                            <input type="hidden" name="block" value="{{ selected_block }}">
                            <input type="hidden" name="file_id" value="{{ u.id }}">
                            <input type="hidden" name="year" value="{{ year }}">
                            <input type="hidden" name="month" value="{{ month }}">
                            <input type="hidden" name="month_from" value="{{ month_from }}">
                            <input type="hidden" name="month_to" value="{{ month_to }}">
                            <button type="submit" class="adm-btn adm-btn-discard">Quitar de la cola</button>
                        </form>
                        {% endif %}
                    </div>
                </div>
                {% endfor %}
                {% endif %}

                {% if selected_block == "new_clients" and block_detail.stats.duplicate_rows %}
                <div style="margin-top:16px; padding:12px 14px; border:1px solid #f0c36d; border-radius:8px; background:#fff9eb;">
                    <strong>Duplicados detectados:</strong>
                    {{ block_detail.stats.duplicate_rows }} registro(s) repetido(s) en el detalle de clientes.
                    <form method="post" style="margin-top:10px;" class="adm-dedup-form"
                          onsubmit="return confirm('¿Eliminar {{ block_detail.stats.duplicate_rows }} registro(s) duplicado(s)? Se conservará una copia de cada cliente.');">
                        {% csrf_token %}
                        <input type="hidden" name="action" value="dedup_new_clients">
                        <input type="hidden" name="year" value="{{ year }}">
                        <input type="hidden" name="month" value="{{ month }}">
                    <input type="hidden" name="month_from" value="{{ month_from }}">
                    <input type="hidden" name="month_to" value="{{ month_to }}">
                        <button type="submit" class="adm-btn adm-btn-primary">Eliminar duplicados</button>
                    </form>
                </div>
                {% endif %}

                {% if selected_block == "financial" %}
                <p class="muted" style="margin-top:12px;">
                    Confirme el <a href="{% url 'pgc:admin_manual_edit' %}?year={{ year }}&month={{ month }}&tab=fx">tipo de cambio</a> antes de importar WC*.
                </p>
                {% elif selected_block == "new_clients" %}
                <p class="muted" style="margin-top:12px;">
                    Edite filas en
                    <a href="{% url 'pgc:admin_new_clients_browse' %}?year={{ year }}&month={{ month }}">Clientes (browse)</a>,
                    reasigne UNE en
                    <a href="{% url 'pgc:admin_new_clients_une' %}?year={{ year }}&month={{ month }}">Clientes (UNE)</a>,
                    o use
                    <a href="{% url 'pgc:admin_manual_edit' %}?year={{ year }}&month={{ month }}&tab=imports">registros importados</a>
                    /
                    <a href="{% url 'pgc:admin_manual_edit' %}?year={{ year }}&month={{ month }}&tab=aliases">alias UNE</a>.
                </p>
                {% elif selected_block == "cross_sale" %}
                <p class="muted" style="margin-top:12px;">
                    Corrija filas en <a href="{% url 'pgc:admin_manual_edit' %}?year={{ year }}&month={{ month }}&tab=imports">registros importados</a>
                    o <a href="{% url 'pgc:admin_manual_edit' %}?year={{ year }}&month={{ month }}&tab=aliases">alias UNE</a>.
                </p>
                {% endif %}
                {% endif %}
            </div>
        </div>

        <div>
            <div class="adm-side-card">
                <h4>Resumen del período</h4>
                <div class="adm-stat-grid">
                    <div class="adm-stat"><div class="value">{{ snapshot.summary.files_loaded }}</div><div class="label">Archivos</div></div>
                    <div class="adm-stat"><div class="value">{{ snapshot.summary.valid_rows }}</div><div class="label">Filas válidas</div></div>
                    <div class="adm-stat"><div class="value">{{ snapshot.summary.rows_with_observations }}</div><div class="label">Observaciones</div></div>
                    <div class="adm-stat"><div class="value">{{ snapshot.summary.pending_aliases }}</div><div class="label">Alias pendientes</div></div>
                </div>
                {% if snapshot.summary.last_score_update %}
                <p class="muted" style="margin:12px 0 0; font-size:0.82rem;">Último score: {{ snapshot.summary.last_score_update|date:"d/m/Y H:i" }}</p>
                {% endif %}
            </div>

            <div class="adm-side-card">
                <h4>Recordatorios</h4>
                <div class="adm-reminder">Verifique el período activo antes de subir archivos.</div>
                <div class="adm-reminder">Confirme que el archivo corresponde al bloque seleccionado.</div>
                <div class="adm-reminder">Revise alias UNE nuevos antes de confiar en el score.</div>
                <div class="adm-reminder">Tras cargar datos, use el botón de recálculo (amarillo si hay pendientes).</div>
            </div>

            <div class="adm-side-card">
                <h4>Bitácora reciente</h4>
                {% for entry in recent_log %}
                <div class="adm-log-item">
                    <strong>{{ entry.title }}</strong><br>{{ entry.detail }}
                    <br><span class="muted">{{ entry.at|date:"d/m/Y H:i" }}{% if entry.user %} · {{ entry.user }}{% endif %}</span>
                </div>
                {% empty %}
                <p class="muted">Sin actividad.</p>
                {% endfor %}
                <a href="{% url 'pgc:admin_monthly_log' %}?year={{ year }}&month={{ month }}"
                   class="adm-btn adm-btn-ghost" style="margin-top:10px; width:100%; text-align:center;">Ver bitácora completa</a>
            </div>
        </div>
    </div>
</div>

<script>
document.querySelectorAll(".adm-process-form, .adm-dedup-form").forEach(function (form) {
    form.addEventListener("submit", function () {
        var btn = form.querySelector('button[type="submit"]');
        if (btn && !btn.disabled) {
            btn.disabled = true;
            btn.textContent = "Procesando…";
        }
    });
});
document.querySelectorAll(".adm-discard-form").forEach(function (form) {
    form.addEventListener("submit", function () {
        var btn = form.querySelector('button[type="submit"]');
        if (btn && !btn.disabled) {
            btn.disabled = true;
            btn.textContent = "Quitando…";
        }
    });
});
</script>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base.html" %}
00002|{% load l10n %}
00003|
00004|{% block title %}Administración mensual{% endblock %}
00005|
00006|{% block content %}
00007|{% include "pgc/admin/_styles.html" %}
00008|
00009|<div class="adm">
00010|    {% include "pgc/admin/_nav.html" with adm_nav_active="monthly" show_django_admin=True %}
00011|
00012|    <div class="adm-header">
00013|        <div class="adm-header-top">
00014|            <div>
00015|                <p class="muted" style="margin:0;">Panel de operaciones</p>
00016|                <div class="adm-period-label">{{ snapshot.label }}</div>
00017|                <span class="adm-period-status {{ snapshot.period_status }}">{{ snapshot.period_status_label }}</span>
00018|            </div>
00019|            <div style="display:flex; flex-wrap:wrap; gap:10px; align-items:end;">
00020|                {% include "pgc/admin/_period_select.html" %}
00021|            </div>
00022|        </div>
00023|    </div>
00024|
00025|    <div class="adm-route">
00026|        {% for block in snapshot.blocks %}
00027|        <a href="?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}&block={{ block.id }}"
00028|           class="adm-block-card {% if block.id == selected_block %}active{% endif %}">
00029|            <div class="adm-block-step">Paso {{ block.step }}</div>
00030|            <div class="adm-block-title">{{ block.label }}</div>
00031|            <span class="adm-badge {{ block.status }}">{{ block.status_label }}</span>
00032|            <div class="adm-block-meta">
00033|                {{ block.summary }}
00034|                {% if block.last_action_at %}
00035|                <br>{{ block.last_action_at|date:"d/m/Y H:i" }}{% if block.last_action_by %} · {{ block.last_action_by }}{% endif %}
00036|                {% endif %}
00037|            </div>
00038|        </a>
00039|        {% endfor %}
00040|    </div>
00041|
00042|    <div class="adm-layout">
00043|        <div>
00044|            <div class="adm-panel">
00045|                <h3>{{ block_detail.label }}</h3>
00046|                <p class="subtitle">{{ block_detail.short }}</p>
00047|
00048|                <ul class="adm-checklist">
00049|                    {% for item in block_detail.checklist %}
00050|                    <li class="{% if item.done %}done{% endif %}">{{ item.label }}</li>
00051|                    {% endfor %}
00052|                </ul>
00053|
00054|                {% if selected_block == "targets" %}
00055|                <p class="muted">Ajuste metas del plan en la pantalla de edición manual.</p>
00056|                <a href="{% url 'pgc:admin_manual_edit' %}?year={{ year }}&month={{ month }}&tab=targets"
00057|                   class="adm-btn adm-btn-primary">Editar metas del período</a>
00058|
00059|                {% elif selected_block == "manual_requirements" %}
00060|                <p class="muted">Registre cumplimiento de respuesta a requerimientos por UNE.</p>
00061|                <a href="{% url 'pgc:admin_manual_edit' %}?year={{ year }}&month={{ month }}&tab=requirements"
00062|                   class="adm-btn adm-btn-primary">Editar requerimientos</a>
00063|
00064|                {% elif selected_block == "review" %}
00065|                <p class="muted">Revise el tablero después de cargar y recalcular.</p>
00066|                <a href="{% url 'pgc:dashboard' %}?year={{ year }}&month={{ month }}" class="adm-btn adm-btn-primary">Abrir tablero</a>
00067|                <a href="{% url 'pgc:admin_ingresos_year' %}?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}"
00068|                   class="adm-btn adm-btn-secondary">Captura ingresos (año)</a>
00069|                <a href="{% url 'pgc:ingresos' %}?year={{ year }}&month={{ month }}" class="adm-btn adm-btn-secondary">Ingresos vs meta</a>
00070|
00071|                {% else %}
00072|                <form method="post" enctype="multipart/form-data" style="margin-bottom:16px;">
00073|                    {% csrf_token %}
00074|                    <input type="hidden" name="action" value="upload">
00075|                    <input type="hidden" name="block" value="{{ selected_block }}">
00076|                    <input type="hidden" name="year" value="{{ year }}">
00077|                    <input type="hidden" name="month" value="{{ month }}">
00078|                    <input type="hidden" name="month_from" value="{{ month_from }}">
00079|                    <input type="hidden" name="month_to" value="{{ month_to }}">
00080|                    <div style="margin-bottom:10px;">{{ upload_form.stored_file }}</div>
00081|                    <button type="submit" class="adm-btn adm-btn-primary">Subir archivo</button>
00082|                </form>
00083|
00084|                {% if block_detail.uploads %}
00085|                <h4 style="margin:0 0 8px; font-size:0.92rem;">Archivos del período</h4>
00086|                {% for u in block_detail.uploads %}
00087|                <div class="adm-upload-row">
00088|                    <div>
00089|                        <strong>{{ u.filename }}</strong><br>
00090|                        <span class="muted">{{ u.status_display }} · {{ u.created_at|date:"d/m/Y H:i" }}{% if u.user %} · {{ u.user }}{% endif %}</span>
00091|                    </div>
00092|                    <div class="adm-upload-actions">
00093|                        <form method="post" class="adm-process-form">
00094|                            {% csrf_token %}
00095|                            <input type="hidden" name="action" value="process">
00096|                            <input type="hidden" name="block" value="{{ selected_block }}">
00097|                            <input type="hidden" name="file_id" value="{{ u.id }}">
00098|                            <input type="hidden" name="year" value="{{ year }}">
00099|                            <input type="hidden" name="month" value="{{ month }}">
00100|                            <input type="hidden" name="month_from" value="{{ month_from }}">
00101|                            <input type="hidden" name="month_to" value="{{ month_to }}">
00102|                            {% if u.status == "PARSED_OK" %}
00103|                            <button type="button" class="adm-btn adm-btn-ghost" disabled title="Ya procesado">Procesado</button>
00104|                            {% else %}
00105|                            <button type="submit" class="adm-btn adm-btn-secondary adm-process-btn">Procesar</button>
00106|                            {% endif %}
00107|                        </form>
00108|                        {% if u.can_discard %}
00109|                        <form method="post" class="adm-discard-form"
00110|                              onsubmit="return confirm('¿Quitar de la cola «{{ u.filename|escapejs }}»? Solo elimina el archivo pendiente; no toca datos ya procesados.');">
00111|                            {% csrf_token %}
00112|                            <input type="hidden" name="action" value="discard_pending">
00113|                            <input type="hidden" name="block" value="{{ selected_block }}">
00114|                            <input type="hidden" name="file_id" value="{{ u.id }}">
00115|                            <input type="hidden" name="year" value="{{ year }}">
00116|                            <input type="hidden" name="month" value="{{ month }}">
00117|                            <input type="hidden" name="month_from" value="{{ month_from }}">
00118|                            <input type="hidden" name="month_to" value="{{ month_to }}">
00119|                            <button type="submit" class="adm-btn adm-btn-discard">Quitar de la cola</button>
00120|                        </form>
00121|                        {% endif %}
00122|                    </div>
00123|                </div>
00124|                {% endfor %}
00125|                {% endif %}
00126|
00127|                {% if selected_block == "new_clients" and block_detail.stats.duplicate_rows %}
00128|                <div style="margin-top:16px; padding:12px 14px; border:1px solid #f0c36d; border-radius:8px; background:#fff9eb;">
00129|                    <strong>Duplicados detectados:</strong>
00130|                    {{ block_detail.stats.duplicate_rows }} registro(s) repetido(s) en el detalle de clientes.
00131|                    <form method="post" style="margin-top:10px;" class="adm-dedup-form"
00132|                          onsubmit="return confirm('¿Eliminar {{ block_detail.stats.duplicate_rows }} registro(s) duplicado(s)? Se conservará una copia de cada cliente.');">
00133|                        {% csrf_token %}
00134|                        <input type="hidden" name="action" value="dedup_new_clients">
00135|                        <input type="hidden" name="year" value="{{ year }}">
00136|                        <input type="hidden" name="month" value="{{ month }}">
00137|                    <input type="hidden" name="month_from" value="{{ month_from }}">
00138|                    <input type="hidden" name="month_to" value="{{ month_to }}">
00139|                        <button type="submit" class="adm-btn adm-btn-primary">Eliminar duplicados</button>
00140|                    </form>
00141|                </div>
00142|                {% endif %}
00143|
00144|                {% if selected_block == "financial" %}
00145|                <p class="muted" style="margin-top:12px;">
00146|                    Confirme el <a href="{% url 'pgc:admin_manual_edit' %}?year={{ year }}&month={{ month }}&tab=fx">tipo de cambio</a> antes de importar WC*.
00147|                </p>
00148|                {% elif selected_block == "new_clients" %}
00149|                <p class="muted" style="margin-top:12px;">
00150|                    Edite filas en
00151|                    <a href="{% url 'pgc:admin_new_clients_browse' %}?year={{ year }}&month={{ month }}">Clientes (browse)</a>,
00152|                    reasigne UNE en
00153|                    <a href="{% url 'pgc:admin_new_clients_une' %}?year={{ year }}&month={{ month }}">Clientes (UNE)</a>,
00154|                    o use
00155|                    <a href="{% url 'pgc:admin_manual_edit' %}?year={{ year }}&month={{ month }}&tab=imports">registros importados</a>
00156|                    /
00157|                    <a href="{% url 'pgc:admin_manual_edit' %}?year={{ year }}&month={{ month }}&tab=aliases">alias UNE</a>.
00158|                </p>
00159|                {% elif selected_block == "cross_sale" %}
00160|                <p class="muted" style="margin-top:12px;">
00161|                    Corrija filas en <a href="{% url 'pgc:admin_manual_edit' %}?year={{ year }}&month={{ month }}&tab=imports">registros importados</a>
00162|                    o <a href="{% url 'pgc:admin_manual_edit' %}?year={{ year }}&month={{ month }}&tab=aliases">alias UNE</a>.
00163|                </p>
00164|                {% endif %}
00165|                {% endif %}
00166|            </div>
00167|        </div>
00168|
00169|        <div>
00170|            <div class="adm-side-card">
00171|                <h4>Resumen del período</h4>
00172|                <div class="adm-stat-grid">
00173|                    <div class="adm-stat"><div class="value">{{ snapshot.summary.files_loaded }}</div><div class="label">Archivos</div></div>
00174|                    <div class="adm-stat"><div class="value">{{ snapshot.summary.valid_rows }}</div><div class="label">Filas válidas</div></div>
00175|                    <div class="adm-stat"><div class="value">{{ snapshot.summary.rows_with_observations }}</div><div class="label">Observaciones</div></div>
00176|                    <div class="adm-stat"><div class="value">{{ snapshot.summary.pending_aliases }}</div><div class="label">Alias pendientes</div></div>
00177|                </div>
00178|                {% if snapshot.summary.last_score_update %}
00179|                <p class="muted" style="margin:12px 0 0; font-size:0.82rem;">Último score: {{ snapshot.summary.last_score_update|date:"d/m/Y H:i" }}</p>
00180|                {% endif %}
00181|            </div>
00182|
00183|            <div class="adm-side-card">
00184|                <h4>Recordatorios</h4>
00185|                <div class="adm-reminder">Verifique el período activo antes de subir archivos.</div>
00186|                <div class="adm-reminder">Confirme que el archivo corresponde al bloque seleccionado.</div>
00187|                <div class="adm-reminder">Revise alias UNE nuevos antes de confiar en el score.</div>
00188|                <div class="adm-reminder">Tras cargar datos, use el botón de recálculo (amarillo si hay pendientes).</div>
00189|            </div>
00190|
00191|            <div class="adm-side-card">
00192|                <h4>Bitácora reciente</h4>
00193|                {% for entry in recent_log %}
00194|                <div class="adm-log-item">
00195|                    <strong>{{ entry.title }}</strong><br>{{ entry.detail }}
00196|                    <br><span class="muted">{{ entry.at|date:"d/m/Y H:i" }}{% if entry.user %} · {{ entry.user }}{% endif %}</span>
00197|                </div>
00198|                {% empty %}
00199|                <p class="muted">Sin actividad.</p>
00200|                {% endfor %}
00201|                <a href="{% url 'pgc:admin_monthly_log' %}?year={{ year }}&month={{ month }}"
00202|                   class="adm-btn adm-btn-ghost" style="margin-top:10px; width:100%; text-align:center;">Ver bitácora completa</a>
00203|            </div>
00204|        </div>
00205|    </div>
00206|</div>
00207|
00208|<script>
00209|document.querySelectorAll(".adm-process-form, .adm-dedup-form").forEach(function (form) {
00210|    form.addEventListener("submit", function () {
00211|        var btn = form.querySelector('button[type="submit"]');
00212|        if (btn && !btn.disabled) {
00213|            btn.disabled = true;
00214|            btn.textContent = "Procesando…";
00215|        }
00216|    });
00217|});
00218|document.querySelectorAll(".adm-discard-form").forEach(function (form) {
00219|    form.addEventListener("submit", function () {
00220|        var btn = form.querySelector('button[type="submit"]');
00221|        if (btn && !btn.disabled) {
00222|            btn.disabled = true;
00223|            btn.textContent = "Quitando…";
00224|        }
00225|    });
00226|});
00227|</script>
00228|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZS5odG1sIiAlfQp7JSBsb2FkIGwxMG4gJX0KCnslIGJsb2NrIHRpdGxlICV9QWRtaW5pc3RyYWNpw7NuIG1lbnN1YWx7JSBlbmRibG9jayAlfQoKeyUgYmxvY2sgY29udGVudCAlfQp7JSBpbmNsdWRlICJwZ2MvYWRtaW4vX3N0eWxlcy5odG1sIiAlfQoKPGRpdiBjbGFzcz0iYWRtIj4KICAgIHslIGluY2x1ZGUgInBnYy9hZG1pbi9fbmF2Lmh0bWwiIHdpdGggYWRtX25hdl9hY3RpdmU9Im1vbnRobHkiIHNob3dfZGphbmdvX2FkbWluPVRydWUgJX0KCiAgICA8ZGl2IGNsYXNzPSJhZG0taGVhZGVyIj4KICAgICAgICA8ZGl2IGNsYXNzPSJhZG0taGVhZGVyLXRvcCI+CiAgICAgICAgICAgIDxkaXY+CiAgICAgICAgICAgICAgICA8cCBjbGFzcz0ibXV0ZWQiIHN0eWxlPSJtYXJnaW46MDsiPlBhbmVsIGRlIG9wZXJhY2lvbmVzPC9wPgogICAgICAgICAgICAgICAgPGRpdiBjbGFzcz0iYWRtLXBlcmlvZC1sYWJlbCI+e3sgc25hcHNob3QubGFiZWwgfX08L2Rpdj4KICAgICAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJhZG0tcGVyaW9kLXN0YXR1cyB7eyBzbmFwc2hvdC5wZXJpb2Rfc3RhdHVzIH19Ij57eyBzbmFwc2hvdC5wZXJpb2Rfc3RhdHVzX2xhYmVsIH19PC9zcGFuPgogICAgICAgICAgICA8L2Rpdj4KICAgICAgICAgICAgPGRpdiBzdHlsZT0iZGlzcGxheTpmbGV4OyBmbGV4LXdyYXA6d3JhcDsgZ2FwOjEwcHg7IGFsaWduLWl0ZW1zOmVuZDsiPgogICAgICAgICAgICAgICAgeyUgaW5jbHVkZSAicGdjL2FkbWluL19wZXJpb2Rfc2VsZWN0Lmh0bWwiICV9CiAgICAgICAgICAgIDwvZGl2PgogICAgICAgIDwvZGl2PgogICAgPC9kaXY+CgogICAgPGRpdiBjbGFzcz0iYWRtLXJvdXRlIj4KICAgICAgICB7JSBmb3IgYmxvY2sgaW4gc25hcHNob3QuYmxvY2tzICV9CiAgICAgICAgPGEgaHJlZj0iP3llYXI9e3sgeWVhciB9fSZtb250aF9mcm9tPXt7IG1vbnRoX2Zyb20gfX0mbW9udGhfdG89e3sgbW9udGhfdG8gfX0mbW9udGg9e3sgbW9udGggfX0mYmxvY2s9e3sgYmxvY2suaWQgfX0iCiAgICAgICAgICAgY2xhc3M9ImFkbS1ibG9jay1jYXJkIHslIGlmIGJsb2NrLmlkID09IHNlbGVjdGVkX2Jsb2NrICV9YWN0aXZleyUgZW5kaWYgJX0iPgogICAgICAgICAgICA8ZGl2IGNsYXNzPSJhZG0tYmxvY2stc3RlcCI+UGFzbyB7eyBibG9jay5zdGVwIH19PC9kaXY+CiAgICAgICAgICAgIDxkaXYgY2xhc3M9ImFkbS1ibG9jay10aXRsZSI+e3sgYmxvY2subGFiZWwgfX08L2Rpdj4KICAgICAgICAgICAgPHNwYW4gY2xhc3M9ImFkbS1iYWRnZSB7eyBibG9jay5zdGF0dXMgfX0iPnt7IGJsb2NrLnN0YXR1c19sYWJlbCB9fTwvc3Bhbj4KICAgICAgICAgICAgPGRpdiBjbGFzcz0iYWRtLWJsb2NrLW1ldGEiPgogICAgICAgICAgICAgICAge3sgYmxvY2suc3VtbWFyeSB9fQogICAgICAgICAgICAgICAgeyUgaWYgYmxvY2subGFzdF9hY3Rpb25fYXQgJX0KICAgICAgICAgICAgICAgIDxicj57eyBibG9jay5sYXN0X2FjdGlvbl9hdHxkYXRlOiJkL20vWSBIOmkiIH19eyUgaWYgYmxvY2subGFzdF9hY3Rpb25fYnkgJX0gwrcge3sgYmxvY2subGFzdF9hY3Rpb25fYnkgfX17JSBlbmRpZiAlfQogICAgICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgPC9hPgogICAgICAgIHslIGVuZGZvciAlfQogICAgPC9kaXY+CgogICAgPGRpdiBjbGFzcz0iYWRtLWxheW91dCI+CiAgICAgICAgPGRpdj4KICAgICAgICAgICAgPGRpdiBjbGFzcz0iYWRtLXBhbmVsIj4KICAgICAgICAgICAgICAgIDxoMz57eyBibG9ja19kZXRhaWwubGFiZWwgfX08L2gzPgogICAgICAgICAgICAgICAgPHAgY2xhc3M9InN1YnRpdGxlIj57eyBibG9ja19kZXRhaWwuc2hvcnQgfX08L3A+CgogICAgICAgICAgICAgICAgPHVsIGNsYXNzPSJhZG0tY2hlY2tsaXN0Ij4KICAgICAgICAgICAgICAgICAgICB7JSBmb3IgaXRlbSBpbiBibG9ja19kZXRhaWwuY2hlY2tsaXN0ICV9CiAgICAgICAgICAgICAgICAgICAgPGxpIGNsYXNzPSJ7JSBpZiBpdGVtLmRvbmUgJX1kb25leyUgZW5kaWYgJX0iPnt7IGl0ZW0ubGFiZWwgfX08L2xpPgogICAgICAgICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICAgICAgPC91bD4KCiAgICAgICAgICAgICAgICB7JSBpZiBzZWxlY3RlZF9ibG9jayA9PSAidGFyZ2V0cyIgJX0KICAgICAgICAgICAgICAgIDxwIGNsYXNzPSJtdXRlZCI+QWp1c3RlIG1ldGFzIGRlbCBwbGFuIGVuIGxhIHBhbnRhbGxhIGRlIGVkaWNpw7NuIG1hbnVhbC48L3A+CiAgICAgICAgICAgICAgICA8YSBocmVmPSJ7JSB1cmwgJ3BnYzphZG1pbl9tYW51YWxfZWRpdCcgJX0/eWVhcj17eyB5ZWFyIH19Jm1vbnRoPXt7IG1vbnRoIH19JnRhYj10YXJnZXRzIgogICAgICAgICAgICAgICAgICAgY2xhc3M9ImFkbS1idG4gYWRtLWJ0bi1wcmltYXJ5Ij5FZGl0YXIgbWV0YXMgZGVsIHBlcsOtb2RvPC9hPgoKICAgICAgICAgICAgICAgIHslIGVsaWYgc2VsZWN0ZWRfYmxvY2sgPT0gIm1hbnVhbF9yZXF1aXJlbWVudHMiICV9CiAgICAgICAgICAgICAgICA8cCBjbGFzcz0ibXV0ZWQiPlJlZ2lzdHJlIGN1bXBsaW1pZW50byBkZSByZXNwdWVzdGEgYSByZXF1ZXJpbWllbnRvcyBwb3IgVU5FLjwvcD4KICAgICAgICAgICAgICAgIDxhIGhyZWY9InslIHVybCAncGdjOmFkbWluX21hbnVhbF9lZGl0JyAlfT95ZWFyPXt7IHllYXIgfX0mbW9udGg9e3sgbW9udGggfX0mdGFiPXJlcXVpcmVtZW50cyIKICAgICAgICAgICAgICAgICAgIGNsYXNzPSJhZG0tYnRuIGFkbS1idG4tcHJpbWFyeSI+RWRpdGFyIHJlcXVlcmltaWVudG9zPC9hPgoKICAgICAgICAgICAgICAgIHslIGVsaWYgc2VsZWN0ZWRfYmxvY2sgPT0gInJldmlldyIgJX0KICAgICAgICAgICAgICAgIDxwIGNsYXNzPSJtdXRlZCI+UmV2aXNlIGVsIHRhYmxlcm8gZGVzcHXDqXMgZGUgY2FyZ2FyIHkgcmVjYWxjdWxhci48L3A+CiAgICAgICAgICAgICAgICA8YSBocmVmPSJ7JSB1cmwgJ3BnYzpkYXNoYm9hcmQnICV9P3llYXI9e3sgeWVhciB9fSZtb250aD17eyBtb250aCB9fSIgY2xhc3M9ImFkbS1idG4gYWRtLWJ0bi1wcmltYXJ5Ij5BYnJpciB0YWJsZXJvPC9hPgogICAgICAgICAgICAgICAgPGEgaHJlZj0ieyUgdXJsICdwZ2M6YWRtaW5faW5ncmVzb3NfeWVhcicgJX0/eWVhcj17eyB5ZWFyIH19Jm1vbnRoX2Zyb209e3sgbW9udGhfZnJvbSB9fSZtb250aF90bz17eyBtb250aF90byB9fSZtb250aD17eyBtb250aCB9fSIKICAgICAgICAgICAgICAgICAgIGNsYXNzPSJhZG0tYnRuIGFkbS1idG4tc2Vjb25kYXJ5Ij5DYXB0dXJhIGluZ3Jlc29zIChhw7FvKTwvYT4KICAgICAgICAgICAgICAgIDxhIGhyZWY9InslIHVybCAncGdjOmluZ3Jlc29zJyAlfT95ZWFyPXt7IHllYXIgfX0mbW9udGg9e3sgbW9udGggfX0iIGNsYXNzPSJhZG0tYnRuIGFkbS1idG4tc2Vjb25kYXJ5Ij5JbmdyZXNvcyB2cyBtZXRhPC9hPgoKICAgICAgICAgICAgICAgIHslIGVsc2UgJX0KICAgICAgICAgICAgICAgIDxmb3JtIG1ldGhvZD0icG9zdCIgZW5jdHlwZT0ibXVsdGlwYXJ0L2Zvcm0tZGF0YSIgc3R5bGU9Im1hcmdpbi1ib3R0b206MTZweDsiPgogICAgICAgICAgICAgICAgICAgIHslIGNzcmZfdG9rZW4gJX0KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJhY3Rpb24iIHZhbHVlPSJ1cGxvYWQiPgogICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9ImJsb2NrIiB2YWx1ZT0ie3sgc2VsZWN0ZWRfYmxvY2sgfX0iPgogICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9InllYXIiIHZhbHVlPSJ7eyB5ZWFyIH19Ij4KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aCIgdmFsdWU9Int7IG1vbnRoIH19Ij4KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aF9mcm9tIiB2YWx1ZT0ie3sgbW9udGhfZnJvbSB9fSI+CiAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ibW9udGhfdG8iIHZhbHVlPSJ7eyBtb250aF90byB9fSI+CiAgICAgICAgICAgICAgICAgICAgPGRpdiBzdHlsZT0ibWFyZ2luLWJvdHRvbToxMHB4OyI+e3sgdXBsb2FkX2Zvcm0uc3RvcmVkX2ZpbGUgfX08L2Rpdj4KICAgICAgICAgICAgICAgICAgICA8YnV0dG9uIHR5cGU9InN1Ym1pdCIgY2xhc3M9ImFkbS1idG4gYWRtLWJ0bi1wcmltYXJ5Ij5TdWJpciBhcmNoaXZvPC9idXR0b24+CiAgICAgICAgICAgICAgICA8L2Zvcm0+CgogICAgICAgICAgICAgICAgeyUgaWYgYmxvY2tfZGV0YWlsLnVwbG9hZHMgJX0KICAgICAgICAgICAgICAgIDxoNCBzdHlsZT0ibWFyZ2luOjAgMCA4cHg7IGZvbnQtc2l6ZTowLjkycmVtOyI+QXJjaGl2b3MgZGVsIHBlcsOtb2RvPC9oND4KICAgICAgICAgICAgICAgIHslIGZvciB1IGluIGJsb2NrX2RldGFpbC51cGxvYWRzICV9CiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJhZG0tdXBsb2FkLXJvdyI+CiAgICAgICAgICAgICAgICAgICAgPGRpdj4KICAgICAgICAgICAgICAgICAgICAgICAgPHN0cm9uZz57eyB1LmZpbGVuYW1lIH19PC9zdHJvbmc+PGJyPgogICAgICAgICAgICAgICAgICAgICAgICA8c3BhbiBjbGFzcz0ibXV0ZWQiPnt7IHUuc3RhdHVzX2Rpc3BsYXkgfX0gwrcge3sgdS5jcmVhdGVkX2F0fGRhdGU6ImQvbS9ZIEg6aSIgfX17JSBpZiB1LnVzZXIgJX0gwrcge3sgdS51c2VyIH19eyUgZW5kaWYgJX08L3NwYW4+CiAgICAgICAgICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICAgICAgICAgICAgPGRpdiBjbGFzcz0iYWRtLXVwbG9hZC1hY3Rpb25zIj4KICAgICAgICAgICAgICAgICAgICAgICAgPGZvcm0gbWV0aG9kPSJwb3N0IiBjbGFzcz0iYWRtLXByb2Nlc3MtZm9ybSI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBjc3JmX3Rva2VuICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJhY3Rpb24iIHZhbHVlPSJwcm9jZXNzIj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9ImJsb2NrIiB2YWx1ZT0ie3sgc2VsZWN0ZWRfYmxvY2sgfX0iPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0iZmlsZV9pZCIgdmFsdWU9Int7IHUuaWQgfX0iPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ieWVhciIgdmFsdWU9Int7IHllYXIgfX0iPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ibW9udGgiIHZhbHVlPSJ7eyBtb250aCB9fSI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aF9mcm9tIiB2YWx1ZT0ie3sgbW9udGhfZnJvbSB9fSI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aF90byIgdmFsdWU9Int7IG1vbnRoX3RvIH19Ij4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGlmIHUuc3RhdHVzID09ICJQQVJTRURfT0siICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8YnV0dG9uIHR5cGU9ImJ1dHRvbiIgY2xhc3M9ImFkbS1idG4gYWRtLWJ0bi1naG9zdCIgZGlzYWJsZWQgdGl0bGU9IllhIHByb2Nlc2FkbyI+UHJvY2VzYWRvPC9idXR0b24+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbHNlICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8YnV0dG9uIHR5cGU9InN1Ym1pdCIgY2xhc3M9ImFkbS1idG4gYWRtLWJ0bi1zZWNvbmRhcnkgYWRtLXByb2Nlc3MtYnRuIj5Qcm9jZXNhcjwvYnV0dG9uPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgICAgICAgICAgICAgICAgPC9mb3JtPgogICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiB1LmNhbl9kaXNjYXJkICV9CiAgICAgICAgICAgICAgICAgICAgICAgIDxmb3JtIG1ldGhvZD0icG9zdCIgY2xhc3M9ImFkbS1kaXNjYXJkLWZvcm0iCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIG9uc3VibWl0PSJyZXR1cm4gY29uZmlybSgnwr9RdWl0YXIgZGUgbGEgY29sYSDCq3t7IHUuZmlsZW5hbWV8ZXNjYXBlanMgfX3Cuz8gU29sbyBlbGltaW5hIGVsIGFyY2hpdm8gcGVuZGllbnRlOyBubyB0b2NhIGRhdG9zIHlhIHByb2Nlc2Fkb3MuJyk7Ij4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGNzcmZfdG9rZW4gJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9ImFjdGlvbiIgdmFsdWU9ImRpc2NhcmRfcGVuZGluZyI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJibG9jayIgdmFsdWU9Int7IHNlbGVjdGVkX2Jsb2NrIH19Ij4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9ImZpbGVfaWQiIHZhbHVlPSJ7eyB1LmlkIH19Ij4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9InllYXIiIHZhbHVlPSJ7eyB5ZWFyIH19Ij4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9Im1vbnRoIiB2YWx1ZT0ie3sgbW9udGggfX0iPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ibW9udGhfZnJvbSIgdmFsdWU9Int7IG1vbnRoX2Zyb20gfX0iPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ibW9udGhfdG8iIHZhbHVlPSJ7eyBtb250aF90byB9fSI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8YnV0dG9uIHR5cGU9InN1Ym1pdCIgY2xhc3M9ImFkbS1idG4gYWRtLWJ0bi1kaXNjYXJkIj5RdWl0YXIgZGUgbGEgY29sYTwvYnV0dG9uPgogICAgICAgICAgICAgICAgICAgICAgICA8L2Zvcm0+CiAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICAgICAgICA8L2Rpdj4KICAgICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICAgICAgeyUgZW5kaWYgJX0KCiAgICAgICAgICAgICAgICB7JSBpZiBzZWxlY3RlZF9ibG9jayA9PSAibmV3X2NsaWVudHMiIGFuZCBibG9ja19kZXRhaWwuc3RhdHMuZHVwbGljYXRlX3Jvd3MgJX0KICAgICAgICAgICAgICAgIDxkaXYgc3R5bGU9Im1hcmdpbi10b3A6MTZweDsgcGFkZGluZzoxMnB4IDE0cHg7IGJvcmRlcjoxcHggc29saWQgI2YwYzM2ZDsgYm9yZGVyLXJhZGl1czo4cHg7IGJhY2tncm91bmQ6I2ZmZjllYjsiPgogICAgICAgICAgICAgICAgICAgIDxzdHJvbmc+RHVwbGljYWRvcyBkZXRlY3RhZG9zOjwvc3Ryb25nPgogICAgICAgICAgICAgICAgICAgIHt7IGJsb2NrX2RldGFpbC5zdGF0cy5kdXBsaWNhdGVfcm93cyB9fSByZWdpc3RybyhzKSByZXBldGlkbyhzKSBlbiBlbCBkZXRhbGxlIGRlIGNsaWVudGVzLgogICAgICAgICAgICAgICAgICAgIDxmb3JtIG1ldGhvZD0icG9zdCIgc3R5bGU9Im1hcmdpbi10b3A6MTBweDsiIGNsYXNzPSJhZG0tZGVkdXAtZm9ybSIKICAgICAgICAgICAgICAgICAgICAgICAgICBvbnN1Ym1pdD0icmV0dXJuIGNvbmZpcm0oJ8K/RWxpbWluYXIge3sgYmxvY2tfZGV0YWlsLnN0YXRzLmR1cGxpY2F0ZV9yb3dzIH19IHJlZ2lzdHJvKHMpIGR1cGxpY2FkbyhzKT8gU2UgY29uc2VydmFyw6EgdW5hIGNvcGlhIGRlIGNhZGEgY2xpZW50ZS4nKTsiPgogICAgICAgICAgICAgICAgICAgICAgICB7JSBjc3JmX3Rva2VuICV9CiAgICAgICAgICAgICAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9ImFjdGlvbiIgdmFsdWU9ImRlZHVwX25ld19jbGllbnRzIj4KICAgICAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ieWVhciIgdmFsdWU9Int7IHllYXIgfX0iPgogICAgICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aCIgdmFsdWU9Int7IG1vbnRoIH19Ij4KICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aF9mcm9tIiB2YWx1ZT0ie3sgbW9udGhfZnJvbSB9fSI+CiAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ibW9udGhfdG8iIHZhbHVlPSJ7eyBtb250aF90byB9fSI+CiAgICAgICAgICAgICAgICAgICAgICAgIDxidXR0b24gdHlwZT0ic3VibWl0IiBjbGFzcz0iYWRtLWJ0biBhZG0tYnRuLXByaW1hcnkiPkVsaW1pbmFyIGR1cGxpY2Fkb3M8L2J1dHRvbj4KICAgICAgICAgICAgICAgICAgICA8L2Zvcm0+CiAgICAgICAgICAgICAgICA8L2Rpdj4KICAgICAgICAgICAgICAgIHslIGVuZGlmICV9CgogICAgICAgICAgICAgICAgeyUgaWYgc2VsZWN0ZWRfYmxvY2sgPT0gImZpbmFuY2lhbCIgJX0KICAgICAgICAgICAgICAgIDxwIGNsYXNzPSJtdXRlZCIgc3R5bGU9Im1hcmdpbi10b3A6MTJweDsiPgogICAgICAgICAgICAgICAgICAgIENvbmZpcm1lIGVsIDxhIGhyZWY9InslIHVybCAncGdjOmFkbWluX21hbnVhbF9lZGl0JyAlfT95ZWFyPXt7IHllYXIgfX0mbW9udGg9e3sgbW9udGggfX0mdGFiPWZ4Ij50aXBvIGRlIGNhbWJpbzwvYT4gYW50ZXMgZGUgaW1wb3J0YXIgV0MqLgogICAgICAgICAgICAgICAgPC9wPgogICAgICAgICAgICAgICAgeyUgZWxpZiBzZWxlY3RlZF9ibG9jayA9PSAibmV3X2NsaWVudHMiICV9CiAgICAgICAgICAgICAgICA8cCBjbGFzcz0ibXV0ZWQiIHN0eWxlPSJtYXJnaW4tdG9wOjEycHg7Ij4KICAgICAgICAgICAgICAgICAgICBFZGl0ZSBmaWxhcyBlbgogICAgICAgICAgICAgICAgICAgIDxhIGhyZWY9InslIHVybCAncGdjOmFkbWluX25ld19jbGllbnRzX2Jyb3dzZScgJX0/eWVhcj17eyB5ZWFyIH19Jm1vbnRoPXt7IG1vbnRoIH19Ij5DbGllbnRlcyAoYnJvd3NlKTwvYT4sCiAgICAgICAgICAgICAgICAgICAgcmVhc2lnbmUgVU5FIGVuCiAgICAgICAgICAgICAgICAgICAgPGEgaHJlZj0ieyUgdXJsICdwZ2M6YWRtaW5fbmV3X2NsaWVudHNfdW5lJyAlfT95ZWFyPXt7IHllYXIgfX0mbW9udGg9e3sgbW9udGggfX0iPkNsaWVudGVzIChVTkUpPC9hPiwKICAgICAgICAgICAgICAgICAgICBvIHVzZQogICAgICAgICAgICAgICAgICAgIDxhIGhyZWY9InslIHVybCAncGdjOmFkbWluX21hbnVhbF9lZGl0JyAlfT95ZWFyPXt7IHllYXIgfX0mbW9udGg9e3sgbW9udGggfX0mdGFiPWltcG9ydHMiPnJlZ2lzdHJvcyBpbXBvcnRhZG9zPC9hPgogICAgICAgICAgICAgICAgICAgIC8KICAgICAgICAgICAgICAgICAgICA8YSBocmVmPSJ7JSB1cmwgJ3BnYzphZG1pbl9tYW51YWxfZWRpdCcgJX0/eWVhcj17eyB5ZWFyIH19Jm1vbnRoPXt7IG1vbnRoIH19JnRhYj1hbGlhc2VzIj5hbGlhcyBVTkU8L2E+LgogICAgICAgICAgICAgICAgPC9wPgogICAgICAgICAgICAgICAgeyUgZWxpZiBzZWxlY3RlZF9ibG9jayA9PSAiY3Jvc3Nfc2FsZSIgJX0KICAgICAgICAgICAgICAgIDxwIGNsYXNzPSJtdXRlZCIgc3R5bGU9Im1hcmdpbi10b3A6MTJweDsiPgogICAgICAgICAgICAgICAgICAgIENvcnJpamEgZmlsYXMgZW4gPGEgaHJlZj0ieyUgdXJsICdwZ2M6YWRtaW5fbWFudWFsX2VkaXQnICV9P3llYXI9e3sgeWVhciB9fSZtb250aD17eyBtb250aCB9fSZ0YWI9aW1wb3J0cyI+cmVnaXN0cm9zIGltcG9ydGFkb3M8L2E+CiAgICAgICAgICAgICAgICAgICAgbyA8YSBocmVmPSJ7JSB1cmwgJ3BnYzphZG1pbl9tYW51YWxfZWRpdCcgJX0/eWVhcj17eyB5ZWFyIH19Jm1vbnRoPXt7IG1vbnRoIH19JnRhYj1hbGlhc2VzIj5hbGlhcyBVTkU8L2E+LgogICAgICAgICAgICAgICAgPC9wPgogICAgICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgIDwvZGl2PgogICAgICAgIDwvZGl2PgoKICAgICAgICA8ZGl2PgogICAgICAgICAgICA8ZGl2IGNsYXNzPSJhZG0tc2lkZS1jYXJkIj4KICAgICAgICAgICAgICAgIDxoND5SZXN1bWVuIGRlbCBwZXLDrW9kbzwvaDQ+CiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJhZG0tc3RhdC1ncmlkIj4KICAgICAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJhZG0tc3RhdCI+PGRpdiBjbGFzcz0idmFsdWUiPnt7IHNuYXBzaG90LnN1bW1hcnkuZmlsZXNfbG9hZGVkIH19PC9kaXY+PGRpdiBjbGFzcz0ibGFiZWwiPkFyY2hpdm9zPC9kaXY+PC9kaXY+CiAgICAgICAgICAgICAgICAgICAgPGRpdiBjbGFzcz0iYWRtLXN0YXQiPjxkaXYgY2xhc3M9InZhbHVlIj57eyBzbmFwc2hvdC5zdW1tYXJ5LnZhbGlkX3Jvd3MgfX08L2Rpdj48ZGl2IGNsYXNzPSJsYWJlbCI+RmlsYXMgdsOhbGlkYXM8L2Rpdj48L2Rpdj4KICAgICAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJhZG0tc3RhdCI+PGRpdiBjbGFzcz0idmFsdWUiPnt7IHNuYXBzaG90LnN1bW1hcnkucm93c193aXRoX29ic2VydmF0aW9ucyB9fTwvZGl2PjxkaXYgY2xhc3M9ImxhYmVsIj5PYnNlcnZhY2lvbmVzPC9kaXY+PC9kaXY+CiAgICAgICAgICAgICAgICAgICAgPGRpdiBjbGFzcz0iYWRtLXN0YXQiPjxkaXYgY2xhc3M9InZhbHVlIj57eyBzbmFwc2hvdC5zdW1tYXJ5LnBlbmRpbmdfYWxpYXNlcyB9fTwvZGl2PjxkaXYgY2xhc3M9ImxhYmVsIj5BbGlhcyBwZW5kaWVudGVzPC9kaXY+PC9kaXY+CiAgICAgICAgICAgICAgICA8L2Rpdj4KICAgICAgICAgICAgICAgIHslIGlmIHNuYXBzaG90LnN1bW1hcnkubGFzdF9zY29yZV91cGRhdGUgJX0KICAgICAgICAgICAgICAgIDxwIGNsYXNzPSJtdXRlZCIgc3R5bGU9Im1hcmdpbjoxMnB4IDAgMDsgZm9udC1zaXplOjAuODJyZW07Ij7Dmmx0aW1vIHNjb3JlOiB7eyBzbmFwc2hvdC5zdW1tYXJ5Lmxhc3Rfc2NvcmVfdXBkYXRlfGRhdGU6ImQvbS9ZIEg6aSIgfX08L3A+CiAgICAgICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgICA8L2Rpdj4KCiAgICAgICAgICAgIDxkaXYgY2xhc3M9ImFkbS1zaWRlLWNhcmQiPgogICAgICAgICAgICAgICAgPGg0PlJlY29yZGF0b3Jpb3M8L2g0PgogICAgICAgICAgICAgICAgPGRpdiBjbGFzcz0iYWRtLXJlbWluZGVyIj5WZXJpZmlxdWUgZWwgcGVyw61vZG8gYWN0aXZvIGFudGVzIGRlIHN1YmlyIGFyY2hpdm9zLjwvZGl2PgogICAgICAgICAgICAgICAgPGRpdiBjbGFzcz0iYWRtLXJlbWluZGVyIj5Db25maXJtZSBxdWUgZWwgYXJjaGl2byBjb3JyZXNwb25kZSBhbCBibG9xdWUgc2VsZWNjaW9uYWRvLjwvZGl2PgogICAgICAgICAgICAgICAgPGRpdiBjbGFzcz0iYWRtLXJlbWluZGVyIj5SZXZpc2UgYWxpYXMgVU5FIG51ZXZvcyBhbnRlcyBkZSBjb25maWFyIGVuIGVsIHNjb3JlLjwvZGl2PgogICAgICAgICAgICAgICAgPGRpdiBjbGFzcz0iYWRtLXJlbWluZGVyIj5UcmFzIGNhcmdhciBkYXRvcywgdXNlIGVsIGJvdMOzbiBkZSByZWPDoWxjdWxvIChhbWFyaWxsbyBzaSBoYXkgcGVuZGllbnRlcykuPC9kaXY+CiAgICAgICAgICAgIDwvZGl2PgoKICAgICAgICAgICAgPGRpdiBjbGFzcz0iYWRtLXNpZGUtY2FyZCI+CiAgICAgICAgICAgICAgICA8aDQ+Qml0w6Fjb3JhIHJlY2llbnRlPC9oND4KICAgICAgICAgICAgICAgIHslIGZvciBlbnRyeSBpbiByZWNlbnRfbG9nICV9CiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJhZG0tbG9nLWl0ZW0iPgogICAgICAgICAgICAgICAgICAgIDxzdHJvbmc+e3sgZW50cnkudGl0bGUgfX08L3N0cm9uZz48YnI+e3sgZW50cnkuZGV0YWlsIH19CiAgICAgICAgICAgICAgICAgICAgPGJyPjxzcGFuIGNsYXNzPSJtdXRlZCI+e3sgZW50cnkuYXR8ZGF0ZToiZC9tL1kgSDppIiB9fXslIGlmIGVudHJ5LnVzZXIgJX0gwrcge3sgZW50cnkudXNlciB9fXslIGVuZGlmICV9PC9zcGFuPgogICAgICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICAgICAgICB7JSBlbXB0eSAlfQogICAgICAgICAgICAgICAgPHAgY2xhc3M9Im11dGVkIj5TaW4gYWN0aXZpZGFkLjwvcD4KICAgICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICAgICAgPGEgaHJlZj0ieyUgdXJsICdwZ2M6YWRtaW5fbW9udGhseV9sb2cnICV9P3llYXI9e3sgeWVhciB9fSZtb250aD17eyBtb250aCB9fSIKICAgICAgICAgICAgICAgICAgIGNsYXNzPSJhZG0tYnRuIGFkbS1idG4tZ2hvc3QiIHN0eWxlPSJtYXJnaW4tdG9wOjEwcHg7IHdpZHRoOjEwMCU7IHRleHQtYWxpZ246Y2VudGVyOyI+VmVyIGJpdMOhY29yYSBjb21wbGV0YTwvYT4KICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgPC9kaXY+CiAgICA8L2Rpdj4KPC9kaXY+Cgo8c2NyaXB0Pgpkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCIuYWRtLXByb2Nlc3MtZm9ybSwgLmFkbS1kZWR1cC1mb3JtIikuZm9yRWFjaChmdW5jdGlvbiAoZm9ybSkgewogICAgZm9ybS5hZGRFdmVudExpc3RlbmVyKCJzdWJtaXQiLCBmdW5jdGlvbiAoKSB7CiAgICAgICAgdmFyIGJ0biA9IGZvcm0ucXVlcnlTZWxlY3RvcignYnV0dG9uW3R5cGU9InN1Ym1pdCJdJyk7CiAgICAgICAgaWYgKGJ0biAmJiAhYnRuLmRpc2FibGVkKSB7CiAgICAgICAgICAgIGJ0bi5kaXNhYmxlZCA9IHRydWU7CiAgICAgICAgICAgIGJ0bi50ZXh0Q29udGVudCA9ICJQcm9jZXNhbmRv4oCmIjsKICAgICAgICB9CiAgICB9KTsKfSk7CmRvY3VtZW50LnF1ZXJ5U2VsZWN0b3JBbGwoIi5hZG0tZGlzY2FyZC1mb3JtIikuZm9yRWFjaChmdW5jdGlvbiAoZm9ybSkgewogICAgZm9ybS5hZGRFdmVudExpc3RlbmVyKCJzdWJtaXQiLCBmdW5jdGlvbiAoKSB7CiAgICAgICAgdmFyIGJ0biA9IGZvcm0ucXVlcnlTZWxlY3RvcignYnV0dG9uW3R5cGU9InN1Ym1pdCJdJyk7CiAgICAgICAgaWYgKGJ0biAmJiAhYnRuLmRpc2FibGVkKSB7CiAgICAgICAgICAgIGJ0bi5kaXNhYmxlZCA9IHRydWU7CiAgICAgICAgICAgIGJ0bi50ZXh0Q29udGVudCA9ICJRdWl0YW5kb+KApiI7CiAgICAgICAgfQogICAgfSk7Cn0pOwo8L3NjcmlwdD4KeyUgZW5kYmxvY2sgJX0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgc/admin_monthly_log.html
PATH_JSON="templates/pgc/admin_monthly_log.html"
FILENAME=admin_monthly_log.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=56
SIZE_BYTES_UTF8=2395
CONTENT_SHA256=2e54a00cba6aad7d9ffb517b956a90f528230714d3a213dd2328bcc2e6c77da9
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~html
{% extends "base.html" %}

{% block title %}Bitácora — {{ period_label }}{% endblock %}

{% block content %}
{% include "pgc/admin/_styles.html" %}

<div class="adm">
    {% include "pgc/admin/_nav.html" with adm_nav_active="log" %}

    <div class="adm-header">
        <div class="adm-header-top">
            <div>
                <h2 style="margin:0; color:#0f3d56;">Bitácora del período</h2>
                <div class="adm-period-label" style="font-size:1.4rem;">{{ period_label }}</div>
                <span class="adm-period-status {{ snapshot.period_status }}">{{ snapshot.period_status_label }}</span>
            </div>
            <div style="display:flex; flex-wrap:wrap; gap:10px; align-items:end;">
                {% include "pgc/admin/_period_select.html" %}
                <a href="{% url 'pgc:admin_monthly' %}?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}" class="adm-btn adm-btn-secondary">Volver al tablero</a>
            </div>
        </div>
    </div>

    <div class="adm-panel adm-scroll">
        <table class="adm-edit-grid" style="text-align:left;">
            <thead>
                <tr>
                    <th style="text-align:left;">Fecha</th>
                    <th>Nivel</th>
                    <th style="text-align:left;">Evento</th>
                    <th style="text-align:left;">Detalle</th>
                    <th>Usuario</th>
                </tr>
            </thead>
            <tbody>
                {% for entry in entries %}
                <tr>
                    <td style="text-align:left;">{{ entry.at|date:"d/m/Y H:i" }}</td>
                    <td>
                        <span class="adm-badge {% if entry.level == 'ERROR' %}observed{% elif entry.kind == 'manual_edit' %}reviewed{% else %}loaded{% endif %}">
                            {{ entry.level }}
                        </span>
                    </td>
                    <td style="text-align:left;">{{ entry.title }}</td>
                    <td style="text-align:left;">{{ entry.detail }}</td>
                    <td>{% if entry.user %}{{ entry.user }}{% else %}—{% endif %}</td>
                </tr>
                {% empty %}
                <tr><td colspan="5">No hay registros para este período.</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base.html" %}
00002|
00003|{% block title %}Bitácora — {{ period_label }}{% endblock %}
00004|
00005|{% block content %}
00006|{% include "pgc/admin/_styles.html" %}
00007|
00008|<div class="adm">
00009|    {% include "pgc/admin/_nav.html" with adm_nav_active="log" %}
00010|
00011|    <div class="adm-header">
00012|        <div class="adm-header-top">
00013|            <div>
00014|                <h2 style="margin:0; color:#0f3d56;">Bitácora del período</h2>
00015|                <div class="adm-period-label" style="font-size:1.4rem;">{{ period_label }}</div>
00016|                <span class="adm-period-status {{ snapshot.period_status }}">{{ snapshot.period_status_label }}</span>
00017|            </div>
00018|            <div style="display:flex; flex-wrap:wrap; gap:10px; align-items:end;">
00019|                {% include "pgc/admin/_period_select.html" %}
00020|                <a href="{% url 'pgc:admin_monthly' %}?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}" class="adm-btn adm-btn-secondary">Volver al tablero</a>
00021|            </div>
00022|        </div>
00023|    </div>
00024|
00025|    <div class="adm-panel adm-scroll">
00026|        <table class="adm-edit-grid" style="text-align:left;">
00027|            <thead>
00028|                <tr>
00029|                    <th style="text-align:left;">Fecha</th>
00030|                    <th>Nivel</th>
00031|                    <th style="text-align:left;">Evento</th>
00032|                    <th style="text-align:left;">Detalle</th>
00033|                    <th>Usuario</th>
00034|                </tr>
00035|            </thead>
00036|            <tbody>
00037|                {% for entry in entries %}
00038|                <tr>
00039|                    <td style="text-align:left;">{{ entry.at|date:"d/m/Y H:i" }}</td>
00040|                    <td>
00041|                        <span class="adm-badge {% if entry.level == 'ERROR' %}observed{% elif entry.kind == 'manual_edit' %}reviewed{% else %}loaded{% endif %}">
00042|                            {{ entry.level }}
00043|                        </span>
00044|                    </td>
00045|                    <td style="text-align:left;">{{ entry.title }}</td>
00046|                    <td style="text-align:left;">{{ entry.detail }}</td>
00047|                    <td>{% if entry.user %}{{ entry.user }}{% else %}—{% endif %}</td>
00048|                </tr>
00049|                {% empty %}
00050|                <tr><td colspan="5">No hay registros para este período.</td></tr>
00051|                {% endfor %}
00052|            </tbody>
00053|        </table>
00054|    </div>
00055|</div>
00056|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZS5odG1sIiAlfQoKeyUgYmxvY2sgdGl0bGUgJX1CaXTDoWNvcmEg4oCUIHt7IHBlcmlvZF9sYWJlbCB9fXslIGVuZGJsb2NrICV9Cgp7JSBibG9jayBjb250ZW50ICV9CnslIGluY2x1ZGUgInBnYy9hZG1pbi9fc3R5bGVzLmh0bWwiICV9Cgo8ZGl2IGNsYXNzPSJhZG0iPgogICAgeyUgaW5jbHVkZSAicGdjL2FkbWluL19uYXYuaHRtbCIgd2l0aCBhZG1fbmF2X2FjdGl2ZT0ibG9nIiAlfQoKICAgIDxkaXYgY2xhc3M9ImFkbS1oZWFkZXIiPgogICAgICAgIDxkaXYgY2xhc3M9ImFkbS1oZWFkZXItdG9wIj4KICAgICAgICAgICAgPGRpdj4KICAgICAgICAgICAgICAgIDxoMiBzdHlsZT0ibWFyZ2luOjA7IGNvbG9yOiMwZjNkNTY7Ij5CaXTDoWNvcmEgZGVsIHBlcsOtb2RvPC9oMj4KICAgICAgICAgICAgICAgIDxkaXYgY2xhc3M9ImFkbS1wZXJpb2QtbGFiZWwiIHN0eWxlPSJmb250LXNpemU6MS40cmVtOyI+e3sgcGVyaW9kX2xhYmVsIH19PC9kaXY+CiAgICAgICAgICAgICAgICA8c3BhbiBjbGFzcz0iYWRtLXBlcmlvZC1zdGF0dXMge3sgc25hcHNob3QucGVyaW9kX3N0YXR1cyB9fSI+e3sgc25hcHNob3QucGVyaW9kX3N0YXR1c19sYWJlbCB9fTwvc3Bhbj4KICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICAgIDxkaXYgc3R5bGU9ImRpc3BsYXk6ZmxleDsgZmxleC13cmFwOndyYXA7IGdhcDoxMHB4OyBhbGlnbi1pdGVtczplbmQ7Ij4KICAgICAgICAgICAgICAgIHslIGluY2x1ZGUgInBnYy9hZG1pbi9fcGVyaW9kX3NlbGVjdC5odG1sIiAlfQogICAgICAgICAgICAgICAgPGEgaHJlZj0ieyUgdXJsICdwZ2M6YWRtaW5fbW9udGhseScgJX0/eWVhcj17eyB5ZWFyIH19Jm1vbnRoX2Zyb209e3sgbW9udGhfZnJvbSB9fSZtb250aF90bz17eyBtb250aF90byB9fSZtb250aD17eyBtb250aCB9fSIgY2xhc3M9ImFkbS1idG4gYWRtLWJ0bi1zZWNvbmRhcnkiPlZvbHZlciBhbCB0YWJsZXJvPC9hPgogICAgICAgICAgICA8L2Rpdj4KICAgICAgICA8L2Rpdj4KICAgIDwvZGl2PgoKICAgIDxkaXYgY2xhc3M9ImFkbS1wYW5lbCBhZG0tc2Nyb2xsIj4KICAgICAgICA8dGFibGUgY2xhc3M9ImFkbS1lZGl0LWdyaWQiIHN0eWxlPSJ0ZXh0LWFsaWduOmxlZnQ7Ij4KICAgICAgICAgICAgPHRoZWFkPgogICAgICAgICAgICAgICAgPHRyPgogICAgICAgICAgICAgICAgICAgIDx0aCBzdHlsZT0idGV4dC1hbGlnbjpsZWZ0OyI+RmVjaGE8L3RoPgogICAgICAgICAgICAgICAgICAgIDx0aD5OaXZlbDwvdGg+CiAgICAgICAgICAgICAgICAgICAgPHRoIHN0eWxlPSJ0ZXh0LWFsaWduOmxlZnQ7Ij5FdmVudG88L3RoPgogICAgICAgICAgICAgICAgICAgIDx0aCBzdHlsZT0idGV4dC1hbGlnbjpsZWZ0OyI+RGV0YWxsZTwvdGg+CiAgICAgICAgICAgICAgICAgICAgPHRoPlVzdWFyaW88L3RoPgogICAgICAgICAgICAgICAgPC90cj4KICAgICAgICAgICAgPC90aGVhZD4KICAgICAgICAgICAgPHRib2R5PgogICAgICAgICAgICAgICAgeyUgZm9yIGVudHJ5IGluIGVudHJpZXMgJX0KICAgICAgICAgICAgICAgIDx0cj4KICAgICAgICAgICAgICAgICAgICA8dGQgc3R5bGU9InRleHQtYWxpZ246bGVmdDsiPnt7IGVudHJ5LmF0fGRhdGU6ImQvbS9ZIEg6aSIgfX08L3RkPgogICAgICAgICAgICAgICAgICAgIDx0ZD4KICAgICAgICAgICAgICAgICAgICAgICAgPHNwYW4gY2xhc3M9ImFkbS1iYWRnZSB7JSBpZiBlbnRyeS5sZXZlbCA9PSAnRVJST1InICV9b2JzZXJ2ZWR7JSBlbGlmIGVudHJ5LmtpbmQgPT0gJ21hbnVhbF9lZGl0JyAlfXJldmlld2VkeyUgZWxzZSAlfWxvYWRlZHslIGVuZGlmICV9Ij4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHt7IGVudHJ5LmxldmVsIH19CiAgICAgICAgICAgICAgICAgICAgICAgIDwvc3Bhbj4KICAgICAgICAgICAgICAgICAgICA8L3RkPgogICAgICAgICAgICAgICAgICAgIDx0ZCBzdHlsZT0idGV4dC1hbGlnbjpsZWZ0OyI+e3sgZW50cnkudGl0bGUgfX08L3RkPgogICAgICAgICAgICAgICAgICAgIDx0ZCBzdHlsZT0idGV4dC1hbGlnbjpsZWZ0OyI+e3sgZW50cnkuZGV0YWlsIH19PC90ZD4KICAgICAgICAgICAgICAgICAgICA8dGQ+eyUgaWYgZW50cnkudXNlciAlfXt7IGVudHJ5LnVzZXIgfX17JSBlbHNlICV94oCUeyUgZW5kaWYgJX08L3RkPgogICAgICAgICAgICAgICAgPC90cj4KICAgICAgICAgICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgICAgICAgICA8dHI+PHRkIGNvbHNwYW49IjUiPk5vIGhheSByZWdpc3Ryb3MgcGFyYSBlc3RlIHBlcsOtb2RvLjwvdGQ+PC90cj4KICAgICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICA8L3Rib2R5PgogICAgICAgIDwvdGFibGU+CiAgICA8L2Rpdj4KPC9kaXY+CnslIGVuZGJsb2NrICV9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgc/admin_new_clients_browse.html
PATH_JSON="templates/pgc/admin_new_clients_browse.html"
FILENAME=admin_new_clients_browse.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=142
SIZE_BYTES_UTF8=8360
CONTENT_SHA256=4b986619fb266a6ba8b7e6cc07bd383a7fc468913562a5b2ce7dc3c2c6b968e2
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~html
{% extends "base.html" %}
{% load l10n %}

{% block title %}Clientes nuevos — browse {{ label }}{% endblock %}

{% block content %}
{% include "pgc/admin/_styles.html" %}

<div class="adm">
    {% include "pgc/admin/_nav.html" with adm_nav_active="clients_browse" %}

    <div class="adm-header">
        <div class="adm-header-top">
            <div>
                <p class="muted" style="margin:0;">Editor de registros · clientes nuevos</p>
                <div class="adm-period-label">{{ label }}</div>
                <p class="muted" style="margin:0;">{{ row_count }} registro(s)
                    {% if not header %}<span style="color:#b45309;"> · sin encabezado aún (se crea al agregar el primero)</span>{% endif %}
                </p>
            </div>
            {% include "pgc/admin/_period_select.html" %}
        </div>
    </div>

    <div class="adm-panel">
        <h3 style="margin-top:0;">Browse · editar / eliminar / agregar</h3>
        <p class="subtitle">Edite celdas, marque Eliminar, o complete la fila nueva al final. Guarde al terminar.</p>

        <form method="post">
            {% csrf_token %}
            <input type="hidden" name="year" value="{{ year }}">
            <input type="hidden" name="month" value="{{ month }}">
            <input type="hidden" name="month_from" value="{{ month_from }}">
            <input type="hidden" name="month_to" value="{{ month_to }}">

            <div class="adm-scroll">
                <table class="adm-edit-grid adm-browse-grid">
                    <thead>
                        <tr>
                            <th>Eliminar</th>
                            <th>Id</th>
                            <th>Mes</th>
                            <th>UNE</th>
                            <th>Cliente</th>
                            <th>NIT</th>
                            <th>Operación</th>
                            <th>Contratos</th>
                            <th>¿Nuevo?</th>
                            <th>Moneda</th>
                            <th>Monto</th>
                            <th>UNE raw</th>
                            <th>Observación</th>
                            <th>Fila origen</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in rows %}
                        <tr>
                            <td>
                                <input type="checkbox" name="delete_ids" value="{{ row.id }}" title="Eliminar este registro">
                            </td>
                            <td class="muted">{{ row.id }}</td>
                            <td class="muted">{{ row.month|stringformat:"02d" }}</td>
                            <td>
                                <select name="row_{{ row.id }}_une" required>
                                    {% for une in unes %}
                                    <option value="{{ une.id }}" {% if row.une_id == une.id %}selected{% endif %}>
                                        {{ une.short }} {{ une.name_es }}
                                    </option>
                                    {% endfor %}
                                </select>
                            </td>
                            <td><input type="text" name="row_{{ row.id }}_client_name" value="{{ row.client_name }}"></td>
                            <td><input type="text" name="row_{{ row.id }}_nit" value="{{ row.nit }}" style="max-width:110px;"></td>
                            <td><input type="text" name="row_{{ row.id }}_operation_code" value="{{ row.operation_code }}" style="max-width:120px;"></td>
                            <td><input type="number" name="row_{{ row.id }}_previous_contracts" value="{{ row.previous_contracts }}" style="max-width:70px;"></td>
                            <td style="text-align:center;">
                                <input type="checkbox" name="row_{{ row.id }}_counts_as_new" value="1" {% if row.counts_as_new %}checked{% endif %}>
                            </td>
                            <td>
                                <select name="row_{{ row.id }}_currency">
                                    <option value="">—</option>
                                    {% for cur in currencies %}
                                    <option value="{{ cur.id }}" {% if row.currency_id == cur.id %}selected{% endif %}>{{ cur.code }}{% if cur.symbol %} ({{ cur.symbol }}){% endif %}</option>
                                    {% endfor %}
                                </select>
                            </td>
                            <td><input type="text" name="row_{{ row.id }}_amount" value="{% if row.amount != None %}{{ row.amount }}{% endif %}" style="max-width:110px;"></td>
                            <td><input type="text" name="row_{{ row.id }}_raw_une_value" value="{{ row.raw_une_value }}" style="max-width:100px;"></td>
                            <td><input type="text" name="row_{{ row.id }}_observations" value="{{ row.observations }}"></td>
                            <td><input type="number" name="row_{{ row.id }}_source_row_number" value="{% if row.source_row_number != None %}{{ row.source_row_number }}{% endif %}" style="max-width:70px;"></td>
                        </tr>
                        {% empty %}
                        <tr><td colspan="14" class="muted">Sin registros en este período.</td></tr>
                        {% endfor %}

                        <tr class="adm-browse-new">
                            <td class="muted">Nuevo</td>
                            <td class="muted">—</td>
                            <td>
                                <select name="new_month">
                                    {% for m in month_choices %}
                                    {% if m >= month_from and m <= month_to %}
                                    <option value="{{ m }}" {% if m == month %}selected{% endif %}>{{ m|stringformat:"02d" }}</option>
                                    {% endif %}
                                    {% endfor %}
                                </select>
                            </td>
                            <td>
                                <select name="new_une">
                                    <option value="">— UNE —</option>
                                    {% for une in unes %}
                                    <option value="{{ une.id }}">{{ une.short }} {{ une.name_es }}</option>
                                    {% endfor %}
                                </select>
                            </td>
                            <td><input type="text" name="new_client_name" placeholder="Cliente"></td>
                            <td><input type="text" name="new_nit" placeholder="NIT" style="max-width:110px;"></td>
                            <td><input type="text" name="new_operation_code" placeholder="Operación" style="max-width:120px;"></td>
                            <td><input type="number" name="new_previous_contracts" value="0" style="max-width:70px;"></td>
                            <td style="text-align:center;"><input type="checkbox" name="new_counts_as_new" value="1"></td>
                            <td>
                                <select name="new_currency">
                                    <option value="">—</option>
                                    {% for cur in currencies %}
                                    <option value="{{ cur.id }}">{{ cur.code }}{% if cur.symbol %} ({{ cur.symbol }}){% endif %}</option>
                                    {% endfor %}
                                </select>
                            </td>
                            <td><input type="text" name="new_amount" placeholder="Monto" style="max-width:110px;"></td>
                            <td><input type="text" name="new_raw_une_value" style="max-width:100px;"></td>
                            <td><input type="text" name="new_observations"></td>
                            <td><input type="number" name="new_source_row_number" style="max-width:70px;"></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            {% include "pgc/admin/_save_footer.html" with reason_required=False %}
    </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base.html" %}
00002|{% load l10n %}
00003|
00004|{% block title %}Clientes nuevos — browse {{ label }}{% endblock %}
00005|
00006|{% block content %}
00007|{% include "pgc/admin/_styles.html" %}
00008|
00009|<div class="adm">
00010|    {% include "pgc/admin/_nav.html" with adm_nav_active="clients_browse" %}
00011|
00012|    <div class="adm-header">
00013|        <div class="adm-header-top">
00014|            <div>
00015|                <p class="muted" style="margin:0;">Editor de registros · clientes nuevos</p>
00016|                <div class="adm-period-label">{{ label }}</div>
00017|                <p class="muted" style="margin:0;">{{ row_count }} registro(s)
00018|                    {% if not header %}<span style="color:#b45309;"> · sin encabezado aún (se crea al agregar el primero)</span>{% endif %}
00019|                </p>
00020|            </div>
00021|            {% include "pgc/admin/_period_select.html" %}
00022|        </div>
00023|    </div>
00024|
00025|    <div class="adm-panel">
00026|        <h3 style="margin-top:0;">Browse · editar / eliminar / agregar</h3>
00027|        <p class="subtitle">Edite celdas, marque Eliminar, o complete la fila nueva al final. Guarde al terminar.</p>
00028|
00029|        <form method="post">
00030|            {% csrf_token %}
00031|            <input type="hidden" name="year" value="{{ year }}">
00032|            <input type="hidden" name="month" value="{{ month }}">
00033|            <input type="hidden" name="month_from" value="{{ month_from }}">
00034|            <input type="hidden" name="month_to" value="{{ month_to }}">
00035|
00036|            <div class="adm-scroll">
00037|                <table class="adm-edit-grid adm-browse-grid">
00038|                    <thead>
00039|                        <tr>
00040|                            <th>Eliminar</th>
00041|                            <th>Id</th>
00042|                            <th>Mes</th>
00043|                            <th>UNE</th>
00044|                            <th>Cliente</th>
00045|                            <th>NIT</th>
00046|                            <th>Operación</th>
00047|                            <th>Contratos</th>
00048|                            <th>¿Nuevo?</th>
00049|                            <th>Moneda</th>
00050|                            <th>Monto</th>
00051|                            <th>UNE raw</th>
00052|                            <th>Observación</th>
00053|                            <th>Fila origen</th>
00054|                        </tr>
00055|                    </thead>
00056|                    <tbody>
00057|                        {% for row in rows %}
00058|                        <tr>
00059|                            <td>
00060|                                <input type="checkbox" name="delete_ids" value="{{ row.id }}" title="Eliminar este registro">
00061|                            </td>
00062|                            <td class="muted">{{ row.id }}</td>
00063|                            <td class="muted">{{ row.month|stringformat:"02d" }}</td>
00064|                            <td>
00065|                                <select name="row_{{ row.id }}_une" required>
00066|                                    {% for une in unes %}
00067|                                    <option value="{{ une.id }}" {% if row.une_id == une.id %}selected{% endif %}>
00068|                                        {{ une.short }} {{ une.name_es }}
00069|                                    </option>
00070|                                    {% endfor %}
00071|                                </select>
00072|                            </td>
00073|                            <td><input type="text" name="row_{{ row.id }}_client_name" value="{{ row.client_name }}"></td>
00074|                            <td><input type="text" name="row_{{ row.id }}_nit" value="{{ row.nit }}" style="max-width:110px;"></td>
00075|                            <td><input type="text" name="row_{{ row.id }}_operation_code" value="{{ row.operation_code }}" style="max-width:120px;"></td>
00076|                            <td><input type="number" name="row_{{ row.id }}_previous_contracts" value="{{ row.previous_contracts }}" style="max-width:70px;"></td>
00077|                            <td style="text-align:center;">
00078|                                <input type="checkbox" name="row_{{ row.id }}_counts_as_new" value="1" {% if row.counts_as_new %}checked{% endif %}>
00079|                            </td>
00080|                            <td>
00081|                                <select name="row_{{ row.id }}_currency">
00082|                                    <option value="">—</option>
00083|                                    {% for cur in currencies %}
00084|                                    <option value="{{ cur.id }}" {% if row.currency_id == cur.id %}selected{% endif %}>{{ cur.code }}{% if cur.symbol %} ({{ cur.symbol }}){% endif %}</option>
00085|                                    {% endfor %}
00086|                                </select>
00087|                            </td>
00088|                            <td><input type="text" name="row_{{ row.id }}_amount" value="{% if row.amount != None %}{{ row.amount }}{% endif %}" style="max-width:110px;"></td>
00089|                            <td><input type="text" name="row_{{ row.id }}_raw_une_value" value="{{ row.raw_une_value }}" style="max-width:100px;"></td>
00090|                            <td><input type="text" name="row_{{ row.id }}_observations" value="{{ row.observations }}"></td>
00091|                            <td><input type="number" name="row_{{ row.id }}_source_row_number" value="{% if row.source_row_number != None %}{{ row.source_row_number }}{% endif %}" style="max-width:70px;"></td>
00092|                        </tr>
00093|                        {% empty %}
00094|                        <tr><td colspan="14" class="muted">Sin registros en este período.</td></tr>
00095|                        {% endfor %}
00096|
00097|                        <tr class="adm-browse-new">
00098|                            <td class="muted">Nuevo</td>
00099|                            <td class="muted">—</td>
00100|                            <td>
00101|                                <select name="new_month">
00102|                                    {% for m in month_choices %}
00103|                                    {% if m >= month_from and m <= month_to %}
00104|                                    <option value="{{ m }}" {% if m == month %}selected{% endif %}>{{ m|stringformat:"02d" }}</option>
00105|                                    {% endif %}
00106|                                    {% endfor %}
00107|                                </select>
00108|                            </td>
00109|                            <td>
00110|                                <select name="new_une">
00111|                                    <option value="">— UNE —</option>
00112|                                    {% for une in unes %}
00113|                                    <option value="{{ une.id }}">{{ une.short }} {{ une.name_es }}</option>
00114|                                    {% endfor %}
00115|                                </select>
00116|                            </td>
00117|                            <td><input type="text" name="new_client_name" placeholder="Cliente"></td>
00118|                            <td><input type="text" name="new_nit" placeholder="NIT" style="max-width:110px;"></td>
00119|                            <td><input type="text" name="new_operation_code" placeholder="Operación" style="max-width:120px;"></td>
00120|                            <td><input type="number" name="new_previous_contracts" value="0" style="max-width:70px;"></td>
00121|                            <td style="text-align:center;"><input type="checkbox" name="new_counts_as_new" value="1"></td>
00122|                            <td>
00123|                                <select name="new_currency">
00124|                                    <option value="">—</option>
00125|                                    {% for cur in currencies %}
00126|                                    <option value="{{ cur.id }}">{{ cur.code }}{% if cur.symbol %} ({{ cur.symbol }}){% endif %}</option>
00127|                                    {% endfor %}
00128|                                </select>
00129|                            </td>
00130|                            <td><input type="text" name="new_amount" placeholder="Monto" style="max-width:110px;"></td>
00131|                            <td><input type="text" name="new_raw_une_value" style="max-width:100px;"></td>
00132|                            <td><input type="text" name="new_observations"></td>
00133|                            <td><input type="number" name="new_source_row_number" style="max-width:70px;"></td>
00134|                        </tr>
00135|                    </tbody>
00136|                </table>
00137|            </div>
00138|
00139|            {% include "pgc/admin/_save_footer.html" with reason_required=False %}
00140|    </div>
00141|</div>
00142|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZS5odG1sIiAlfQp7JSBsb2FkIGwxMG4gJX0KCnslIGJsb2NrIHRpdGxlICV9Q2xpZW50ZXMgbnVldm9zIOKAlCBicm93c2Uge3sgbGFiZWwgfX17JSBlbmRibG9jayAlfQoKeyUgYmxvY2sgY29udGVudCAlfQp7JSBpbmNsdWRlICJwZ2MvYWRtaW4vX3N0eWxlcy5odG1sIiAlfQoKPGRpdiBjbGFzcz0iYWRtIj4KICAgIHslIGluY2x1ZGUgInBnYy9hZG1pbi9fbmF2Lmh0bWwiIHdpdGggYWRtX25hdl9hY3RpdmU9ImNsaWVudHNfYnJvd3NlIiAlfQoKICAgIDxkaXYgY2xhc3M9ImFkbS1oZWFkZXIiPgogICAgICAgIDxkaXYgY2xhc3M9ImFkbS1oZWFkZXItdG9wIj4KICAgICAgICAgICAgPGRpdj4KICAgICAgICAgICAgICAgIDxwIGNsYXNzPSJtdXRlZCIgc3R5bGU9Im1hcmdpbjowOyI+RWRpdG9yIGRlIHJlZ2lzdHJvcyDCtyBjbGllbnRlcyBudWV2b3M8L3A+CiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJhZG0tcGVyaW9kLWxhYmVsIj57eyBsYWJlbCB9fTwvZGl2PgogICAgICAgICAgICAgICAgPHAgY2xhc3M9Im11dGVkIiBzdHlsZT0ibWFyZ2luOjA7Ij57eyByb3dfY291bnQgfX0gcmVnaXN0cm8ocykKICAgICAgICAgICAgICAgICAgICB7JSBpZiBub3QgaGVhZGVyICV9PHNwYW4gc3R5bGU9ImNvbG9yOiNiNDUzMDk7Ij4gwrcgc2luIGVuY2FiZXphZG8gYcO6biAoc2UgY3JlYSBhbCBhZ3JlZ2FyIGVsIHByaW1lcm8pPC9zcGFuPnslIGVuZGlmICV9CiAgICAgICAgICAgICAgICA8L3A+CiAgICAgICAgICAgIDwvZGl2PgogICAgICAgICAgICB7JSBpbmNsdWRlICJwZ2MvYWRtaW4vX3BlcmlvZF9zZWxlY3QuaHRtbCIgJX0KICAgICAgICA8L2Rpdj4KICAgIDwvZGl2PgoKICAgIDxkaXYgY2xhc3M9ImFkbS1wYW5lbCI+CiAgICAgICAgPGgzIHN0eWxlPSJtYXJnaW4tdG9wOjA7Ij5Ccm93c2UgwrcgZWRpdGFyIC8gZWxpbWluYXIgLyBhZ3JlZ2FyPC9oMz4KICAgICAgICA8cCBjbGFzcz0ic3VidGl0bGUiPkVkaXRlIGNlbGRhcywgbWFycXVlIEVsaW1pbmFyLCBvIGNvbXBsZXRlIGxhIGZpbGEgbnVldmEgYWwgZmluYWwuIEd1YXJkZSBhbCB0ZXJtaW5hci48L3A+CgogICAgICAgIDxmb3JtIG1ldGhvZD0icG9zdCI+CiAgICAgICAgICAgIHslIGNzcmZfdG9rZW4gJX0KICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ieWVhciIgdmFsdWU9Int7IHllYXIgfX0iPgogICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aCIgdmFsdWU9Int7IG1vbnRoIH19Ij4KICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ibW9udGhfZnJvbSIgdmFsdWU9Int7IG1vbnRoX2Zyb20gfX0iPgogICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aF90byIgdmFsdWU9Int7IG1vbnRoX3RvIH19Ij4KCiAgICAgICAgICAgIDxkaXYgY2xhc3M9ImFkbS1zY3JvbGwiPgogICAgICAgICAgICAgICAgPHRhYmxlIGNsYXNzPSJhZG0tZWRpdC1ncmlkIGFkbS1icm93c2UtZ3JpZCI+CiAgICAgICAgICAgICAgICAgICAgPHRoZWFkPgogICAgICAgICAgICAgICAgICAgICAgICA8dHI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGg+RWxpbWluYXI8L3RoPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRoPklkPC90aD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0aD5NZXM8L3RoPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRoPlVORTwvdGg+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGg+Q2xpZW50ZTwvdGg+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGg+TklUPC90aD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0aD5PcGVyYWNpw7NuPC90aD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0aD5Db250cmF0b3M8L3RoPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRoPsK/TnVldm8/PC90aD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0aD5Nb25lZGE8L3RoPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRoPk1vbnRvPC90aD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0aD5VTkUgcmF3PC90aD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0aD5PYnNlcnZhY2nDs248L3RoPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRoPkZpbGEgb3JpZ2VuPC90aD4KICAgICAgICAgICAgICAgICAgICAgICAgPC90cj4KICAgICAgICAgICAgICAgICAgICA8L3RoZWFkPgogICAgICAgICAgICAgICAgICAgIDx0Ym9keT4KICAgICAgICAgICAgICAgICAgICAgICAgeyUgZm9yIHJvdyBpbiByb3dzICV9CiAgICAgICAgICAgICAgICAgICAgICAgIDx0cj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0iY2hlY2tib3giIG5hbWU9ImRlbGV0ZV9pZHMiIHZhbHVlPSJ7eyByb3cuaWQgfX0iIHRpdGxlPSJFbGltaW5hciBlc3RlIHJlZ2lzdHJvIj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGQgY2xhc3M9Im11dGVkIj57eyByb3cuaWQgfX08L3RkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkIGNsYXNzPSJtdXRlZCI+e3sgcm93Lm1vbnRofHN0cmluZ2Zvcm1hdDoiMDJkIiB9fTwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHNlbGVjdCBuYW1lPSJyb3dfe3sgcm93LmlkIH19X3VuZSIgcmVxdWlyZWQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGZvciB1bmUgaW4gdW5lcyAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8b3B0aW9uIHZhbHVlPSJ7eyB1bmUuaWQgfX0iIHslIGlmIHJvdy51bmVfaWQgPT0gdW5lLmlkICV9c2VsZWN0ZWR7JSBlbmRpZiAlfT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHt7IHVuZS5zaG9ydCB9fSB7eyB1bmUubmFtZV9lcyB9fQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L29wdGlvbj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPC9zZWxlY3Q+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3RkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkPjxpbnB1dCB0eXBlPSJ0ZXh0IiBuYW1lPSJyb3dfe3sgcm93LmlkIH19X2NsaWVudF9uYW1lIiB2YWx1ZT0ie3sgcm93LmNsaWVudF9uYW1lIH19Ij48L3RkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkPjxpbnB1dCB0eXBlPSJ0ZXh0IiBuYW1lPSJyb3dfe3sgcm93LmlkIH19X25pdCIgdmFsdWU9Int7IHJvdy5uaXQgfX0iIHN0eWxlPSJtYXgtd2lkdGg6MTEwcHg7Ij48L3RkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkPjxpbnB1dCB0eXBlPSJ0ZXh0IiBuYW1lPSJyb3dfe3sgcm93LmlkIH19X29wZXJhdGlvbl9jb2RlIiB2YWx1ZT0ie3sgcm93Lm9wZXJhdGlvbl9jb2RlIH19IiBzdHlsZT0ibWF4LXdpZHRoOjEyMHB4OyI+PC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD48aW5wdXQgdHlwZT0ibnVtYmVyIiBuYW1lPSJyb3dfe3sgcm93LmlkIH19X3ByZXZpb3VzX2NvbnRyYWN0cyIgdmFsdWU9Int7IHJvdy5wcmV2aW91c19jb250cmFjdHMgfX0iIHN0eWxlPSJtYXgtd2lkdGg6NzBweDsiPjwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGQgc3R5bGU9InRleHQtYWxpZ246Y2VudGVyOyI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImNoZWNrYm94IiBuYW1lPSJyb3dfe3sgcm93LmlkIH19X2NvdW50c19hc19uZXciIHZhbHVlPSIxIiB7JSBpZiByb3cuY291bnRzX2FzX25ldyAlfWNoZWNrZWR7JSBlbmRpZiAlfT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHNlbGVjdCBuYW1lPSJyb3dfe3sgcm93LmlkIH19X2N1cnJlbmN5Ij4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPG9wdGlvbiB2YWx1ZT0iIj7igJQ8L29wdGlvbj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZm9yIGN1ciBpbiBjdXJyZW5jaWVzICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9Int7IGN1ci5pZCB9fSIgeyUgaWYgcm93LmN1cnJlbmN5X2lkID09IGN1ci5pZCAlfXNlbGVjdGVkeyUgZW5kaWYgJX0+e3sgY3VyLmNvZGUgfX17JSBpZiBjdXIuc3ltYm9sICV9ICh7eyBjdXIuc3ltYm9sIH19KXslIGVuZGlmICV9PC9vcHRpb24+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvc2VsZWN0PgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD48aW5wdXQgdHlwZT0idGV4dCIgbmFtZT0icm93X3t7IHJvdy5pZCB9fV9hbW91bnQiIHZhbHVlPSJ7JSBpZiByb3cuYW1vdW50ICE9IE5vbmUgJX17eyByb3cuYW1vdW50IH19eyUgZW5kaWYgJX0iIHN0eWxlPSJtYXgtd2lkdGg6MTEwcHg7Ij48L3RkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkPjxpbnB1dCB0eXBlPSJ0ZXh0IiBuYW1lPSJyb3dfe3sgcm93LmlkIH19X3Jhd191bmVfdmFsdWUiIHZhbHVlPSJ7eyByb3cucmF3X3VuZV92YWx1ZSB9fSIgc3R5bGU9Im1heC13aWR0aDoxMDBweDsiPjwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGQ+PGlucHV0IHR5cGU9InRleHQiIG5hbWU9InJvd197eyByb3cuaWQgfX1fb2JzZXJ2YXRpb25zIiB2YWx1ZT0ie3sgcm93Lm9ic2VydmF0aW9ucyB9fSI+PC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD48aW5wdXQgdHlwZT0ibnVtYmVyIiBuYW1lPSJyb3dfe3sgcm93LmlkIH19X3NvdXJjZV9yb3dfbnVtYmVyIiB2YWx1ZT0ieyUgaWYgcm93LnNvdXJjZV9yb3dfbnVtYmVyICE9IE5vbmUgJX17eyByb3cuc291cmNlX3Jvd19udW1iZXIgfX17JSBlbmRpZiAlfSIgc3R5bGU9Im1heC13aWR0aDo3MHB4OyI+PC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgPC90cj4KICAgICAgICAgICAgICAgICAgICAgICAgeyUgZW1wdHkgJX0KICAgICAgICAgICAgICAgICAgICAgICAgPHRyPjx0ZCBjb2xzcGFuPSIxNCIgY2xhc3M9Im11dGVkIj5TaW4gcmVnaXN0cm9zIGVuIGVzdGUgcGVyw61vZG8uPC90ZD48L3RyPgogICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRmb3IgJX0KCiAgICAgICAgICAgICAgICAgICAgICAgIDx0ciBjbGFzcz0iYWRtLWJyb3dzZS1uZXciPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkIGNsYXNzPSJtdXRlZCI+TnVldm88L3RkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkIGNsYXNzPSJtdXRlZCI+4oCUPC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8c2VsZWN0IG5hbWU9Im5ld19tb250aCI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGZvciBtIGluIG1vbnRoX2Nob2ljZXMgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgaWYgbSA+PSBtb250aF9mcm9tIGFuZCBtIDw9IG1vbnRoX3RvICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9Int7IG0gfX0iIHslIGlmIG0gPT0gbW9udGggJX1zZWxlY3RlZHslIGVuZGlmICV9Pnt7IG18c3RyaW5nZm9ybWF0OiIwMmQiIH19PC9vcHRpb24+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvc2VsZWN0PgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8c2VsZWN0IG5hbWU9Im5ld191bmUiPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8b3B0aW9uIHZhbHVlPSIiPuKAlCBVTkUg4oCUPC9vcHRpb24+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGZvciB1bmUgaW4gdW5lcyAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8b3B0aW9uIHZhbHVlPSJ7eyB1bmUuaWQgfX0iPnt7IHVuZS5zaG9ydCB9fSB7eyB1bmUubmFtZV9lcyB9fTwvb3B0aW9uPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3NlbGVjdD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGQ+PGlucHV0IHR5cGU9InRleHQiIG5hbWU9Im5ld19jbGllbnRfbmFtZSIgcGxhY2Vob2xkZXI9IkNsaWVudGUiPjwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGQ+PGlucHV0IHR5cGU9InRleHQiIG5hbWU9Im5ld19uaXQiIHBsYWNlaG9sZGVyPSJOSVQiIHN0eWxlPSJtYXgtd2lkdGg6MTEwcHg7Ij48L3RkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkPjxpbnB1dCB0eXBlPSJ0ZXh0IiBuYW1lPSJuZXdfb3BlcmF0aW9uX2NvZGUiIHBsYWNlaG9sZGVyPSJPcGVyYWNpw7NuIiBzdHlsZT0ibWF4LXdpZHRoOjEyMHB4OyI+PC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD48aW5wdXQgdHlwZT0ibnVtYmVyIiBuYW1lPSJuZXdfcHJldmlvdXNfY29udHJhY3RzIiB2YWx1ZT0iMCIgc3R5bGU9Im1heC13aWR0aDo3MHB4OyI+PC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZCBzdHlsZT0idGV4dC1hbGlnbjpjZW50ZXI7Ij48aW5wdXQgdHlwZT0iY2hlY2tib3giIG5hbWU9Im5ld19jb3VudHNfYXNfbmV3IiB2YWx1ZT0iMSI+PC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8c2VsZWN0IG5hbWU9Im5ld19jdXJyZW5jeSI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9IiI+4oCUPC9vcHRpb24+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGZvciBjdXIgaW4gY3VycmVuY2llcyAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8b3B0aW9uIHZhbHVlPSJ7eyBjdXIuaWQgfX0iPnt7IGN1ci5jb2RlIH19eyUgaWYgY3VyLnN5bWJvbCAlfSAoe3sgY3VyLnN5bWJvbCB9fSl7JSBlbmRpZiAlfTwvb3B0aW9uPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3NlbGVjdD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGQ+PGlucHV0IHR5cGU9InRleHQiIG5hbWU9Im5ld19hbW91bnQiIHBsYWNlaG9sZGVyPSJNb250byIgc3R5bGU9Im1heC13aWR0aDoxMTBweDsiPjwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGQ+PGlucHV0IHR5cGU9InRleHQiIG5hbWU9Im5ld19yYXdfdW5lX3ZhbHVlIiBzdHlsZT0ibWF4LXdpZHRoOjEwMHB4OyI+PC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD48aW5wdXQgdHlwZT0idGV4dCIgbmFtZT0ibmV3X29ic2VydmF0aW9ucyI+PC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD48aW5wdXQgdHlwZT0ibnVtYmVyIiBuYW1lPSJuZXdfc291cmNlX3Jvd19udW1iZXIiIHN0eWxlPSJtYXgtd2lkdGg6NzBweDsiPjwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgIDwvdHI+CiAgICAgICAgICAgICAgICAgICAgPC90Ym9keT4KICAgICAgICAgICAgICAgIDwvdGFibGU+CiAgICAgICAgICAgIDwvZGl2PgoKICAgICAgICAgICAgeyUgaW5jbHVkZSAicGdjL2FkbWluL19zYXZlX2Zvb3Rlci5odG1sIiB3aXRoIHJlYXNvbl9yZXF1aXJlZD1GYWxzZSAlfQogICAgPC9kaXY+CjwvZGl2Pgp7JSBlbmRibG9jayAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgc/admin_new_clients_une.html
PATH_JSON="templates/pgc/admin_new_clients_une.html"
FILENAME=admin_new_clients_une.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=87
SIZE_BYTES_UTF8=4150
CONTENT_SHA256=e12c61c0b4527837cae5057a6e91c047a2fe8e76a2e9670a9a52c4dfd24a3771
ENDS_WITH_NEWLINE=TRUE
ORIGINAL_NEWLINE_STYLE=LF
CONTENT_FORMAT=VERBATIM_TEXT_WITH_NUMBERED_FALLBACK
DO_NOT_SUMMARIZE=TRUE
DO_NOT_NORMALIZE=TRUE
DO_NOT_FLATTEN=TRUE
PRESERVE_PUNCTUATION=TRUE
PRESERVE_LINE_BREAKS=TRUE
PRESERVE_INDENTATION=TRUE
PREFERRED_READING_ORDER=PATH_LITERAL,CONTENT_NUMBERED_BEGIN,CONTENT_BASE64_BEGIN,CONTENT_BEGIN
IDENTIFIER_SAFETY_RULE=If CONTENT_BEGIN appears compacted or visually flattened, do not infer exact identifiers, variable names, paths, or spacing from it; prefer CONTENT_NUMBERED_BEGIN or CONTENT_BASE64_BEGIN.
CONTENT_BEGIN
~~~~~html
{% extends "base.html" %}
{% load l10n %}

{% block title %}Clientes nuevos — UNE {{ label }}{% endblock %}

{% block content %}
{% include "pgc/admin/_styles.html" %}

<div class="adm">
    {% include "pgc/admin/_nav.html" with adm_nav_active="clients_une" %}

    <div class="adm-header">
        <div class="adm-header-top">
            <div>
                <p class="muted" style="margin:0;">Reasignar UNE · solo este campo</p>
                <div class="adm-period-label">{{ label }}</div>
                <p class="muted" style="margin:0;">{{ row_count }} registro(s). Opciones: 1 Factoraje · 2 Leasing · 3 Insurance · 4 Inversiones.</p>
            </div>
            {% include "pgc/admin/_period_select.html" %}
        </div>
    </div>

    <div class="adm-panel">
        <h3 style="margin-top:0;">Cambiar UNE</h3>
        <p class="subtitle">Los demás campos son de solo lectura. Elija una de las cuatro UNEs por fila.</p>

        <div class="adm-une-legend">
            {% for une in unes %}
            <span class="adm-une-legend-item"><strong>{{ une.short }}</strong> {{ une.name_es }}</span>
            {% endfor %}
        </div>

        <form method="post">
            {% csrf_token %}
            <input type="hidden" name="year" value="{{ year }}">
            <input type="hidden" name="month" value="{{ month }}">
            <input type="hidden" name="month_from" value="{{ month_from }}">
            <input type="hidden" name="month_to" value="{{ month_to }}">

            <div class="adm-scroll">
                <table class="adm-edit-grid adm-une-grid">
                    <thead>
                        <tr>
                            <th>Mes</th>
                            <th>Cliente</th>
                            <th>NIT</th>
                            <th>Operación</th>
                            <th>¿Nuevo?</th>
                            <th>Monto</th>
                            <th>UNE</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in rows %}
                        <tr>
                            <td class="muted">{{ row.month|stringformat:"02d" }}</td>
                            <td style="text-align:left;">{{ row.client_name|default:"—" }}</td>
                            <td>{{ row.nit|default:"—" }}</td>
                            <td>{{ row.operation_code|default:"—" }}</td>
                            <td>{% if row.counts_as_new %}<span style="color:#065f46;font-weight:600;">Sí</span>{% else %}<span style="color:#b91c1c;">No</span>{% endif %}</td>
                            <td>{% if row.currency %}{{ row.currency.code }} {% endif %}{% if row.amount != None %}{{ row.amount }}{% else %}—{% endif %}</td>
                            <td>
                                <div class="adm-une-pick" role="radiogroup" aria-label="UNE de {{ row.client_name }}">
                                    {% for une in unes %}
                                    <label class="adm-une-opt {% if row.une_id == une.id %}is-current{% endif %}">
                                        <input type="radio"
                                               name="une_{{ row.id }}"
                                               value="{{ une.id }}"
                                               {% if row.une_id == une.id %}checked{% endif %}>
                                        <span class="adm-une-short">{{ une.short }}</span>
                                        <span class="adm-une-name">{{ une.name_es }}</span>
                                    </label>
                                    {% endfor %}
                                </div>
                            </td>
                        </tr>
                        {% empty %}
                        <tr><td colspan="7" class="muted">Sin registros en este período.</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>

            {% include "pgc/admin/_save_footer.html" with reason_required=False %}
    </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base.html" %}
00002|{% load l10n %}
00003|
00004|{% block title %}Clientes nuevos — UNE {{ label }}{% endblock %}
00005|
00006|{% block content %}
00007|{% include "pgc/admin/_styles.html" %}
00008|
00009|<div class="adm">
00010|    {% include "pgc/admin/_nav.html" with adm_nav_active="clients_une" %}
00011|
00012|    <div class="adm-header">
00013|        <div class="adm-header-top">
00014|            <div>
00015|                <p class="muted" style="margin:0;">Reasignar UNE · solo este campo</p>
00016|                <div class="adm-period-label">{{ label }}</div>
00017|                <p class="muted" style="margin:0;">{{ row_count }} registro(s). Opciones: 1 Factoraje · 2 Leasing · 3 Insurance · 4 Inversiones.</p>
00018|            </div>
00019|            {% include "pgc/admin/_period_select.html" %}
00020|        </div>
00021|    </div>
00022|
00023|    <div class="adm-panel">
00024|        <h3 style="margin-top:0;">Cambiar UNE</h3>
00025|        <p class="subtitle">Los demás campos son de solo lectura. Elija una de las cuatro UNEs por fila.</p>
00026|
00027|        <div class="adm-une-legend">
00028|            {% for une in unes %}
00029|            <span class="adm-une-legend-item"><strong>{{ une.short }}</strong> {{ une.name_es }}</span>
00030|            {% endfor %}
00031|        </div>
00032|
00033|        <form method="post">
00034|            {% csrf_token %}
00035|            <input type="hidden" name="year" value="{{ year }}">
00036|            <input type="hidden" name="month" value="{{ month }}">
00037|            <input type="hidden" name="month_from" value="{{ month_from }}">
00038|            <input type="hidden" name="month_to" value="{{ month_to }}">
00039|
00040|            <div class="adm-scroll">
00041|                <table class="adm-edit-grid adm-une-grid">
00042|                    <thead>
00043|                        <tr>
00044|                            <th>Mes</th>
00045|                            <th>Cliente</th>
00046|                            <th>NIT</th>
00047|                            <th>Operación</th>
00048|                            <th>¿Nuevo?</th>
00049|                            <th>Monto</th>
00050|                            <th>UNE</th>
00051|                        </tr>
00052|                    </thead>
00053|                    <tbody>
00054|                        {% for row in rows %}
00055|                        <tr>
00056|                            <td class="muted">{{ row.month|stringformat:"02d" }}</td>
00057|                            <td style="text-align:left;">{{ row.client_name|default:"—" }}</td>
00058|                            <td>{{ row.nit|default:"—" }}</td>
00059|                            <td>{{ row.operation_code|default:"—" }}</td>
00060|                            <td>{% if row.counts_as_new %}<span style="color:#065f46;font-weight:600;">Sí</span>{% else %}<span style="color:#b91c1c;">No</span>{% endif %}</td>
00061|                            <td>{% if row.currency %}{{ row.currency.code }} {% endif %}{% if row.amount != None %}{{ row.amount }}{% else %}—{% endif %}</td>
00062|                            <td>
00063|                                <div class="adm-une-pick" role="radiogroup" aria-label="UNE de {{ row.client_name }}">
00064|                                    {% for une in unes %}
00065|                                    <label class="adm-une-opt {% if row.une_id == une.id %}is-current{% endif %}">
00066|                                        <input type="radio"
00067|                                               name="une_{{ row.id }}"
00068|                                               value="{{ une.id }}"
00069|                                               {% if row.une_id == une.id %}checked{% endif %}>
00070|                                        <span class="adm-une-short">{{ une.short }}</span>
00071|                                        <span class="adm-une-name">{{ une.name_es }}</span>
00072|                                    </label>
00073|                                    {% endfor %}
00074|                                </div>
00075|                            </td>
00076|                        </tr>
00077|                        {% empty %}
00078|                        <tr><td colspan="7" class="muted">Sin registros en este período.</td></tr>
00079|                        {% endfor %}
00080|                    </tbody>
00081|                </table>
00082|            </div>
00083|
00084|            {% include "pgc/admin/_save_footer.html" with reason_required=False %}
00085|    </div>
00086|</div>
00087|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZS5odG1sIiAlfQp7JSBsb2FkIGwxMG4gJX0KCnslIGJsb2NrIHRpdGxlICV9Q2xpZW50ZXMgbnVldm9zIOKAlCBVTkUge3sgbGFiZWwgfX17JSBlbmRibG9jayAlfQoKeyUgYmxvY2sgY29udGVudCAlfQp7JSBpbmNsdWRlICJwZ2MvYWRtaW4vX3N0eWxlcy5odG1sIiAlfQoKPGRpdiBjbGFzcz0iYWRtIj4KICAgIHslIGluY2x1ZGUgInBnYy9hZG1pbi9fbmF2Lmh0bWwiIHdpdGggYWRtX25hdl9hY3RpdmU9ImNsaWVudHNfdW5lIiAlfQoKICAgIDxkaXYgY2xhc3M9ImFkbS1oZWFkZXIiPgogICAgICAgIDxkaXYgY2xhc3M9ImFkbS1oZWFkZXItdG9wIj4KICAgICAgICAgICAgPGRpdj4KICAgICAgICAgICAgICAgIDxwIGNsYXNzPSJtdXRlZCIgc3R5bGU9Im1hcmdpbjowOyI+UmVhc2lnbmFyIFVORSDCtyBzb2xvIGVzdGUgY2FtcG88L3A+CiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJhZG0tcGVyaW9kLWxhYmVsIj57eyBsYWJlbCB9fTwvZGl2PgogICAgICAgICAgICAgICAgPHAgY2xhc3M9Im11dGVkIiBzdHlsZT0ibWFyZ2luOjA7Ij57eyByb3dfY291bnQgfX0gcmVnaXN0cm8ocykuIE9wY2lvbmVzOiAxIEZhY3RvcmFqZSDCtyAyIExlYXNpbmcgwrcgMyBJbnN1cmFuY2UgwrcgNCBJbnZlcnNpb25lcy48L3A+CiAgICAgICAgICAgIDwvZGl2PgogICAgICAgICAgICB7JSBpbmNsdWRlICJwZ2MvYWRtaW4vX3BlcmlvZF9zZWxlY3QuaHRtbCIgJX0KICAgICAgICA8L2Rpdj4KICAgIDwvZGl2PgoKICAgIDxkaXYgY2xhc3M9ImFkbS1wYW5lbCI+CiAgICAgICAgPGgzIHN0eWxlPSJtYXJnaW4tdG9wOjA7Ij5DYW1iaWFyIFVORTwvaDM+CiAgICAgICAgPHAgY2xhc3M9InN1YnRpdGxlIj5Mb3MgZGVtw6FzIGNhbXBvcyBzb24gZGUgc29sbyBsZWN0dXJhLiBFbGlqYSB1bmEgZGUgbGFzIGN1YXRybyBVTkVzIHBvciBmaWxhLjwvcD4KCiAgICAgICAgPGRpdiBjbGFzcz0iYWRtLXVuZS1sZWdlbmQiPgogICAgICAgICAgICB7JSBmb3IgdW5lIGluIHVuZXMgJX0KICAgICAgICAgICAgPHNwYW4gY2xhc3M9ImFkbS11bmUtbGVnZW5kLWl0ZW0iPjxzdHJvbmc+e3sgdW5lLnNob3J0IH19PC9zdHJvbmc+IHt7IHVuZS5uYW1lX2VzIH19PC9zcGFuPgogICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICA8L2Rpdj4KCiAgICAgICAgPGZvcm0gbWV0aG9kPSJwb3N0Ij4KICAgICAgICAgICAgeyUgY3NyZl90b2tlbiAlfQogICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJ5ZWFyIiB2YWx1ZT0ie3sgeWVhciB9fSI+CiAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9Im1vbnRoIiB2YWx1ZT0ie3sgbW9udGggfX0iPgogICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aF9mcm9tIiB2YWx1ZT0ie3sgbW9udGhfZnJvbSB9fSI+CiAgICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9Im1vbnRoX3RvIiB2YWx1ZT0ie3sgbW9udGhfdG8gfX0iPgoKICAgICAgICAgICAgPGRpdiBjbGFzcz0iYWRtLXNjcm9sbCI+CiAgICAgICAgICAgICAgICA8dGFibGUgY2xhc3M9ImFkbS1lZGl0LWdyaWQgYWRtLXVuZS1ncmlkIj4KICAgICAgICAgICAgICAgICAgICA8dGhlYWQ+CiAgICAgICAgICAgICAgICAgICAgICAgIDx0cj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0aD5NZXM8L3RoPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRoPkNsaWVudGU8L3RoPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRoPk5JVDwvdGg+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGg+T3BlcmFjacOzbjwvdGg+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGg+wr9OdWV2bz88L3RoPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRoPk1vbnRvPC90aD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0aD5VTkU8L3RoPgogICAgICAgICAgICAgICAgICAgICAgICA8L3RyPgogICAgICAgICAgICAgICAgICAgIDwvdGhlYWQ+CiAgICAgICAgICAgICAgICAgICAgPHRib2R5PgogICAgICAgICAgICAgICAgICAgICAgICB7JSBmb3Igcm93IGluIHJvd3MgJX0KICAgICAgICAgICAgICAgICAgICAgICAgPHRyPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkIGNsYXNzPSJtdXRlZCI+e3sgcm93Lm1vbnRofHN0cmluZ2Zvcm1hdDoiMDJkIiB9fTwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGQgc3R5bGU9InRleHQtYWxpZ246bGVmdDsiPnt7IHJvdy5jbGllbnRfbmFtZXxkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD57eyByb3cubml0fGRlZmF1bHQ6IuKAlCIgfX08L3RkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHRkPnt7IHJvdy5vcGVyYXRpb25fY29kZXxkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD57JSBpZiByb3cuY291bnRzX2FzX25ldyAlfTxzcGFuIHN0eWxlPSJjb2xvcjojMDY1ZjQ2O2ZvbnQtd2VpZ2h0OjYwMDsiPlPDrTwvc3Bhbj57JSBlbHNlICV9PHNwYW4gc3R5bGU9ImNvbG9yOiNiOTFjMWM7Ij5Obzwvc3Bhbj57JSBlbmRpZiAlfTwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8dGQ+eyUgaWYgcm93LmN1cnJlbmN5ICV9e3sgcm93LmN1cnJlbmN5LmNvZGUgfX0geyUgZW5kaWYgJX17JSBpZiByb3cuYW1vdW50ICE9IE5vbmUgJX17eyByb3cuYW1vdW50IH19eyUgZWxzZSAlfeKAlHslIGVuZGlmICV9PC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJhZG0tdW5lLXBpY2siIHJvbGU9InJhZGlvZ3JvdXAiIGFyaWEtbGFiZWw9IlVORSBkZSB7eyByb3cuY2xpZW50X25hbWUgfX0iPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBmb3IgdW5lIGluIHVuZXMgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPGxhYmVsIGNsYXNzPSJhZG0tdW5lLW9wdCB7JSBpZiByb3cudW5lX2lkID09IHVuZS5pZCAlfWlzLWN1cnJlbnR7JSBlbmRpZiAlfSI+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8aW5wdXQgdHlwZT0icmFkaW8iCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgbmFtZT0idW5lX3t7IHJvdy5pZCB9fSIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB2YWx1ZT0ie3sgdW5lLmlkIH19IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGlmIHJvdy51bmVfaWQgPT0gdW5lLmlkICV9Y2hlY2tlZHslIGVuZGlmICV9PgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHNwYW4gY2xhc3M9ImFkbS11bmUtc2hvcnQiPnt7IHVuZS5zaG9ydCB9fTwvc3Bhbj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJhZG0tdW5lLW5hbWUiPnt7IHVuZS5uYW1lX2VzIH19PC9zcGFuPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L2xhYmVsPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L2Rpdj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgIDwvdHI+CiAgICAgICAgICAgICAgICAgICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgICAgICAgICAgICAgICAgIDx0cj48dGQgY29sc3Bhbj0iNyIgY2xhc3M9Im11dGVkIj5TaW4gcmVnaXN0cm9zIGVuIGVzdGUgcGVyw61vZG8uPC90ZD48L3RyPgogICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgICAgICAgICAgICA8L3Rib2R5PgogICAgICAgICAgICAgICAgPC90YWJsZT4KICAgICAgICAgICAgPC9kaXY+CgogICAgICAgICAgICB7JSBpbmNsdWRlICJwZ2MvYWRtaW4vX3NhdmVfZm9vdGVyLmh0bWwiIHdpdGggcmVhc29uX3JlcXVpcmVkPUZhbHNlICV9CiAgICA8L2Rpdj4KPC9kaXY+CnslIGVuZGJsb2NrICV9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
