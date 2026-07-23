# CONCATENATED .HTML FILES

PART_NUMBER=4
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
PATH_LITERAL=templates/pgc/respuesta_reqs.html
PATH_JSON="templates/pgc/respuesta_reqs.html"
FILENAME=respuesta_reqs.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=286
SIZE_BYTES_UTF8=10731
CONTENT_SHA256=35d298732456c2b18a3fc986e394e21f40778d4367f8a83bc8e7cfe59c81fabe
ENDS_WITH_NEWLINE=FALSE
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

{% block title %}Respuesta a requerimientos vs meta{% endblock %}

{% block content %}
<style>
  .group_separator td {
    padding: 0;
    height: 14px;
    border-bottom: none;
    background: #ffffff;
  }
</style>
<div class="card">
    <div class="wcg-report-head" style="margin-top:0;">
      <h2 style="margin:0;">Respuesta a requerimientos vs meta</h2>
      {% include "includes/module_mark.html" with module="pgc" %}
    </div>
    <p class="muted">
        Meta y resultado mensual de respuesta a requerimientos por UNE y periodo.
    </p>

    <form method="get" class="filters">
        <div>
            <label for="start_year">Año inicial</label><br>
            <select name="start_year" id="start_year">
                {% for p in available_periods %}
                    <option value="{{ p.year }}"
                        {% if report_filter.start_year == p.year and report_filter.start_month == p.month %}selected{% endif %}>
                        {{ p.year }}
                    </option>
                {% endfor %}
            </select>
        </div>

        <div>
            <label for="start_month">Mes inicial</label><br>
            <select name="start_month" id="start_month">
                {% for p in available_periods %}
                    <option value="{{ p.month }}"
                        {% if report_filter.start_year == p.year and report_filter.start_month == p.month %}selected{% endif %}>
                        {{ p.month|stringformat:"02d" }}
                    </option>
                {% endfor %}
            </select>
        </div>

        <div>
            <label for="month_count">Cantidad de meses</label><br>
            <select name="month_count" id="month_count">
                {% for opt in month_count_options %}
                    <option value="{{ opt }}" {% if report_filter.month_count == opt %}selected{% endif %}>
                        {{ opt }}
                    </option>
                {% endfor %}
            </select>
        </div>

        <div>
          <label for="sort">Sort</label><br>
          <select id="sort">
            <option value="unes"
              {% if report_sort.group_mode == "une" %}selected{% endif %}>
              UNEs
            </option>
            <option value="fechas_asc"
              {% if report_sort.group_mode == "period" and report_sort.date_order == "asc" %}selected{% endif %}>
              Fechas ascendentes
            </option>
            <option value="fechas_desc"
              {% if report_sort.group_mode == "period" and report_sort.date_order == "desc" %}selected{% endif %}>
              Fechas descendentes
            </option>
          </select>
          <input type="hidden" name="date_order" id="date_order"
                 value="{% if report_sort.group_mode == 'period' and report_sort.date_order == 'desc' %}desc{% else %}asc{% endif %}">
          <input type="hidden" name="group_mode" id="group_mode"
                 value="{% if report_sort.group_mode == 'period' %}period{% else %}une{% endif %}">
        </div>
      
        <div style="align-self:end;">
            <button type="button" id="btn-export-md">.md export</button>
        </div>
    </form>

    <table>
        <thead>
            <tr>
                <th style="text-align:left;">UNE</th>
                <th style="text-align:center;">Periodo</th>
                <th style="text-align:center;">Meta respuesta reqs</th>
                <th style="text-align:center;">Respuesta reqs real</th>
                <th style="text-align:center;">Cumple</th>
                <th style="text-align:center;">Puntos asignados</th>
                <th style="text-align:center;">Total del mes</th>
            </tr>
        </thead>
        <tbody>
            {% for row in rows %}
                {% if row.is_separator %}
                    <tr class="group_separator">
                        <td colspan="8"></td>
                    </tr>
                {% else %}
                    <tr>
                        <td>{{ row.target.une.name_es }}</td>
                        <td>{{ row.target.year }}-{{ row.target.month|stringformat:"02d" }}</td>
                        <td>
                            {% if row.target.target_value %}
                                {{ row.target.target_value|floatformat:0|unlocalize }}
                            {% else %}
                                —
                            {% endif %}
                        </td>
                        <td>
                            {% if row.result %}
                                {{ row.result.measured_value|floatformat:0|unlocalize }}
                            {% else %}
                                —
                            {% endif %}
                        </td>
                        <td>
                            {% if row.result and row.result.is_achieved %}
                                <span class="ok">Sí</span>
                            {% else %}
                                <span class="bad">No</span>
                            {% endif %}
                        </td>
                        <td>
                            {% if row.result %}
                                {{ row.result.points_awarded }}
                            {% else %}
                                0
                            {% endif %}
                        </td>
                        <td>
                            {% if row.scorecard %}
                                {{ row.scorecard.total_points }}
                            {% else %}
                                0
                            {% endif %}
                        </td>
                        <td>
                            <a
                                href="{% url 'pgc:clientes_nuevos_detail' %}?une={{ row.target.une.id }}&year={{ row.target.year }}&month={{ row.target.month }}"
                                class="detail-icon-link"
                                aria-label="Ver detalle de clientes nuevos"
                            >
                                <span class="detail-icon"></span>
                            </a>
                        </td>
                    </tr>
                {% endif %}
            {% empty %}
                <tr>
                    <td colspan="8">No hay datos de respuesta a requerimientos para los filtros seleccionados.</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
    const startPeriod = document.getElementById("start_period");
    const startYear = document.getElementById("start_year");
    const startMonth = document.getElementById("start_month");
    const sort = document.getElementById("sort");
    const dateOrder = document.getElementById("date_order");
    const groupMode = document.getElementById("group_mode");
    const btn = document.getElementById("btn-export-md");

    function syncPeriodFields() {
        if (!startPeriod) return;
        const option = startPeriod.options[startPeriod.selectedIndex];
        if (!option) return;
        startYear.value = option.dataset.year || "";
        startMonth.value = option.dataset.month || "";
    }

    function syncSortFields() {
        if (!sort) return;
        if (sort.value === "unes") {
            groupMode.value = "une";
            dateOrder.value = "asc";
        } else if (sort.value === "fechas_desc") {
            groupMode.value = "period";
            dateOrder.value = "desc";
        } else {
            groupMode.value = "period";
            dateOrder.value = "asc";
        }
    }


    const filterForm = document.querySelector("form.filters");
    function applyFilters() {
        if (typeof syncPeriodFields === "function") syncPeriodFields();
        if (typeof syncSortFields === "function") syncSortFields();
        if (filterForm) filterForm.submit();
    }

    if (startPeriod) {
        startPeriod.addEventListener("change", applyFilters);
        syncPeriodFields();
    }

    if (sort) {
        sort.addEventListener("change", applyFilters);
        syncSortFields();
    }

    ["month_count", "mode", "start_year", "start_month", "year", "month", "une"].forEach(function (id) {
        const el = document.getElementById(id);
        if (el && el.tagName === "SELECT") {
            el.addEventListener("change", applyFilters);
        }
    });

    if (!btn) return;

    btn.addEventListener("click", async function () {
        syncPeriodFields();
        syncSortFields();

        const params = new URLSearchParams({
            start_year: startYear.value || "",
            start_month: startMonth.value || "",
            month_count: document.getElementById("month_count")?.value || "",
            date_order: dateOrder.value || "asc",
            group_mode: groupMode.value || "une"
        });

        const url = `{% url 'pgc:respuesta_reqs_export_md' %}?` + params.toString();

        btn.disabled = true;
        const originalText = btn.textContent;
        btn.textContent = "Generando...";

        try {
            const response = await fetch(url, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            if (!response.ok) {
                throw new Error("No se pudo generar el archivo Markdown.");
            }

            const blob = await response.blob();

            let filename = "pgc-respuesta-reqs.md";
            const disposition = response.headers.get("Content-Disposition");
            if (disposition) {
                const utf8Match = disposition.match(/filename\*=UTF-8''([^;]+)/i);
                const asciiMatch = disposition.match(/filename="([^"]+)"/i);

                if (utf8Match && utf8Match[1]) {
                    filename = decodeURIComponent(utf8Match[1]);
                } else if (asciiMatch && asciiMatch[1]) {
                    filename = asciiMatch[1];
                }
            }

            const objectUrl = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = objectUrl;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(objectUrl);
        } catch (error) {
            alert(error.message || "Error generando la exportación.");
        } finally {
            btn.disabled = false;
            btn.textContent = originalText;
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
00004|{% block title %}Respuesta a requerimientos vs meta{% endblock %}
00005|
00006|{% block content %}
00007|<style>
00008|  .group_separator td {
00009|    padding: 0;
00010|    height: 14px;
00011|    border-bottom: none;
00012|    background: #ffffff;
00013|  }
00014|</style>
00015|<div class="card">
00016|    <div class="wcg-report-head" style="margin-top:0;">
00017|      <h2 style="margin:0;">Respuesta a requerimientos vs meta</h2>
00018|      {% include "includes/module_mark.html" with module="pgc" %}
00019|    </div>
00020|    <p class="muted">
00021|        Meta y resultado mensual de respuesta a requerimientos por UNE y periodo.
00022|    </p>
00023|
00024|    <form method="get" class="filters">
00025|        <div>
00026|            <label for="start_year">Año inicial</label><br>
00027|            <select name="start_year" id="start_year">
00028|                {% for p in available_periods %}
00029|                    <option value="{{ p.year }}"
00030|                        {% if report_filter.start_year == p.year and report_filter.start_month == p.month %}selected{% endif %}>
00031|                        {{ p.year }}
00032|                    </option>
00033|                {% endfor %}
00034|            </select>
00035|        </div>
00036|
00037|        <div>
00038|            <label for="start_month">Mes inicial</label><br>
00039|            <select name="start_month" id="start_month">
00040|                {% for p in available_periods %}
00041|                    <option value="{{ p.month }}"
00042|                        {% if report_filter.start_year == p.year and report_filter.start_month == p.month %}selected{% endif %}>
00043|                        {{ p.month|stringformat:"02d" }}
00044|                    </option>
00045|                {% endfor %}
00046|            </select>
00047|        </div>
00048|
00049|        <div>
00050|            <label for="month_count">Cantidad de meses</label><br>
00051|            <select name="month_count" id="month_count">
00052|                {% for opt in month_count_options %}
00053|                    <option value="{{ opt }}" {% if report_filter.month_count == opt %}selected{% endif %}>
00054|                        {{ opt }}
00055|                    </option>
00056|                {% endfor %}
00057|            </select>
00058|        </div>
00059|
00060|        <div>
00061|          <label for="sort">Sort</label><br>
00062|          <select id="sort">
00063|            <option value="unes"
00064|              {% if report_sort.group_mode == "une" %}selected{% endif %}>
00065|              UNEs
00066|            </option>
00067|            <option value="fechas_asc"
00068|              {% if report_sort.group_mode == "period" and report_sort.date_order == "asc" %}selected{% endif %}>
00069|              Fechas ascendentes
00070|            </option>
00071|            <option value="fechas_desc"
00072|              {% if report_sort.group_mode == "period" and report_sort.date_order == "desc" %}selected{% endif %}>
00073|              Fechas descendentes
00074|            </option>
00075|          </select>
00076|          <input type="hidden" name="date_order" id="date_order"
00077|                 value="{% if report_sort.group_mode == 'period' and report_sort.date_order == 'desc' %}desc{% else %}asc{% endif %}">
00078|          <input type="hidden" name="group_mode" id="group_mode"
00079|                 value="{% if report_sort.group_mode == 'period' %}period{% else %}une{% endif %}">
00080|        </div>
00081|      
00082|        <div style="align-self:end;">
00083|            <button type="button" id="btn-export-md">.md export</button>
00084|        </div>
00085|    </form>
00086|
00087|    <table>
00088|        <thead>
00089|            <tr>
00090|                <th style="text-align:left;">UNE</th>
00091|                <th style="text-align:center;">Periodo</th>
00092|                <th style="text-align:center;">Meta respuesta reqs</th>
00093|                <th style="text-align:center;">Respuesta reqs real</th>
00094|                <th style="text-align:center;">Cumple</th>
00095|                <th style="text-align:center;">Puntos asignados</th>
00096|                <th style="text-align:center;">Total del mes</th>
00097|            </tr>
00098|        </thead>
00099|        <tbody>
00100|            {% for row in rows %}
00101|                {% if row.is_separator %}
00102|                    <tr class="group_separator">
00103|                        <td colspan="8"></td>
00104|                    </tr>
00105|                {% else %}
00106|                    <tr>
00107|                        <td>{{ row.target.une.name_es }}</td>
00108|                        <td>{{ row.target.year }}-{{ row.target.month|stringformat:"02d" }}</td>
00109|                        <td>
00110|                            {% if row.target.target_value %}
00111|                                {{ row.target.target_value|floatformat:0|unlocalize }}
00112|                            {% else %}
00113|                                —
00114|                            {% endif %}
00115|                        </td>
00116|                        <td>
00117|                            {% if row.result %}
00118|                                {{ row.result.measured_value|floatformat:0|unlocalize }}
00119|                            {% else %}
00120|                                —
00121|                            {% endif %}
00122|                        </td>
00123|                        <td>
00124|                            {% if row.result and row.result.is_achieved %}
00125|                                <span class="ok">Sí</span>
00126|                            {% else %}
00127|                                <span class="bad">No</span>
00128|                            {% endif %}
00129|                        </td>
00130|                        <td>
00131|                            {% if row.result %}
00132|                                {{ row.result.points_awarded }}
00133|                            {% else %}
00134|                                0
00135|                            {% endif %}
00136|                        </td>
00137|                        <td>
00138|                            {% if row.scorecard %}
00139|                                {{ row.scorecard.total_points }}
00140|                            {% else %}
00141|                                0
00142|                            {% endif %}
00143|                        </td>
00144|                        <td>
00145|                            <a
00146|                                href="{% url 'pgc:clientes_nuevos_detail' %}?une={{ row.target.une.id }}&year={{ row.target.year }}&month={{ row.target.month }}"
00147|                                class="detail-icon-link"
00148|                                aria-label="Ver detalle de clientes nuevos"
00149|                            >
00150|                                <span class="detail-icon"></span>
00151|                            </a>
00152|                        </td>
00153|                    </tr>
00154|                {% endif %}
00155|            {% empty %}
00156|                <tr>
00157|                    <td colspan="8">No hay datos de respuesta a requerimientos para los filtros seleccionados.</td>
00158|                </tr>
00159|            {% endfor %}
00160|        </tbody>
00161|    </table>
00162|</div>
00163|
00164|<script>
00165|document.addEventListener("DOMContentLoaded", function () {
00166|    const startPeriod = document.getElementById("start_period");
00167|    const startYear = document.getElementById("start_year");
00168|    const startMonth = document.getElementById("start_month");
00169|    const sort = document.getElementById("sort");
00170|    const dateOrder = document.getElementById("date_order");
00171|    const groupMode = document.getElementById("group_mode");
00172|    const btn = document.getElementById("btn-export-md");
00173|
00174|    function syncPeriodFields() {
00175|        if (!startPeriod) return;
00176|        const option = startPeriod.options[startPeriod.selectedIndex];
00177|        if (!option) return;
00178|        startYear.value = option.dataset.year || "";
00179|        startMonth.value = option.dataset.month || "";
00180|    }
00181|
00182|    function syncSortFields() {
00183|        if (!sort) return;
00184|        if (sort.value === "unes") {
00185|            groupMode.value = "une";
00186|            dateOrder.value = "asc";
00187|        } else if (sort.value === "fechas_desc") {
00188|            groupMode.value = "period";
00189|            dateOrder.value = "desc";
00190|        } else {
00191|            groupMode.value = "period";
00192|            dateOrder.value = "asc";
00193|        }
00194|    }
00195|
00196|
00197|    const filterForm = document.querySelector("form.filters");
00198|    function applyFilters() {
00199|        if (typeof syncPeriodFields === "function") syncPeriodFields();
00200|        if (typeof syncSortFields === "function") syncSortFields();
00201|        if (filterForm) filterForm.submit();
00202|    }
00203|
00204|    if (startPeriod) {
00205|        startPeriod.addEventListener("change", applyFilters);
00206|        syncPeriodFields();
00207|    }
00208|
00209|    if (sort) {
00210|        sort.addEventListener("change", applyFilters);
00211|        syncSortFields();
00212|    }
00213|
00214|    ["month_count", "mode", "start_year", "start_month", "year", "month", "une"].forEach(function (id) {
00215|        const el = document.getElementById(id);
00216|        if (el && el.tagName === "SELECT") {
00217|            el.addEventListener("change", applyFilters);
00218|        }
00219|    });
00220|
00221|    if (!btn) return;
00222|
00223|    btn.addEventListener("click", async function () {
00224|        syncPeriodFields();
00225|        syncSortFields();
00226|
00227|        const params = new URLSearchParams({
00228|            start_year: startYear.value || "",
00229|            start_month: startMonth.value || "",
00230|            month_count: document.getElementById("month_count")?.value || "",
00231|            date_order: dateOrder.value || "asc",
00232|            group_mode: groupMode.value || "une"
00233|        });
00234|
00235|        const url = `{% url 'pgc:respuesta_reqs_export_md' %}?` + params.toString();
00236|
00237|        btn.disabled = true;
00238|        const originalText = btn.textContent;
00239|        btn.textContent = "Generando...";
00240|
00241|        try {
00242|            const response = await fetch(url, {
00243|                method: "GET",
00244|                headers: {
00245|                    "X-Requested-With": "XMLHttpRequest"
00246|                }
00247|            });
00248|
00249|            if (!response.ok) {
00250|                throw new Error("No se pudo generar el archivo Markdown.");
00251|            }
00252|
00253|            const blob = await response.blob();
00254|
00255|            let filename = "pgc-respuesta-reqs.md";
00256|            const disposition = response.headers.get("Content-Disposition");
00257|            if (disposition) {
00258|                const utf8Match = disposition.match(/filename\*=UTF-8''([^;]+)/i);
00259|                const asciiMatch = disposition.match(/filename="([^"]+)"/i);
00260|
00261|                if (utf8Match && utf8Match[1]) {
00262|                    filename = decodeURIComponent(utf8Match[1]);
00263|                } else if (asciiMatch && asciiMatch[1]) {
00264|                    filename = asciiMatch[1];
00265|                }
00266|            }
00267|
00268|            const objectUrl = window.URL.createObjectURL(blob);
00269|            const a = document.createElement("a");
00270|            a.href = objectUrl;
00271|            a.download = filename;
00272|            document.body.appendChild(a);
00273|            a.click();
00274|            a.remove();
00275|            window.URL.revokeObjectURL(objectUrl);
00276|        } catch (error) {
00277|            alert(error.message || "Error generando la exportación.");
00278|        } finally {
00279|            btn.disabled = false;
00280|            btn.textContent = originalText;
00281|        }
00282|    });
00283|});
00284|</script>
00285|{% endblock %}
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZS5odG1sIiAlfQp7JSBsb2FkIGwxMG4gJX0KCnslIGJsb2NrIHRpdGxlICV9UmVzcHVlc3RhIGEgcmVxdWVyaW1pZW50b3MgdnMgbWV0YXslIGVuZGJsb2NrICV9Cgp7JSBibG9jayBjb250ZW50ICV9CjxzdHlsZT4KICAuZ3JvdXBfc2VwYXJhdG9yIHRkIHsKICAgIHBhZGRpbmc6IDA7CiAgICBoZWlnaHQ6IDE0cHg7CiAgICBib3JkZXItYm90dG9tOiBub25lOwogICAgYmFja2dyb3VuZDogI2ZmZmZmZjsKICB9Cjwvc3R5bGU+CjxkaXYgY2xhc3M9ImNhcmQiPgogICAgPGRpdiBjbGFzcz0id2NnLXJlcG9ydC1oZWFkIiBzdHlsZT0ibWFyZ2luLXRvcDowOyI+CiAgICAgIDxoMiBzdHlsZT0ibWFyZ2luOjA7Ij5SZXNwdWVzdGEgYSByZXF1ZXJpbWllbnRvcyB2cyBtZXRhPC9oMj4KICAgICAgeyUgaW5jbHVkZSAiaW5jbHVkZXMvbW9kdWxlX21hcmsuaHRtbCIgd2l0aCBtb2R1bGU9InBnYyIgJX0KICAgIDwvZGl2PgogICAgPHAgY2xhc3M9Im11dGVkIj4KICAgICAgICBNZXRhIHkgcmVzdWx0YWRvIG1lbnN1YWwgZGUgcmVzcHVlc3RhIGEgcmVxdWVyaW1pZW50b3MgcG9yIFVORSB5IHBlcmlvZG8uCiAgICA8L3A+CgogICAgPGZvcm0gbWV0aG9kPSJnZXQiIGNsYXNzPSJmaWx0ZXJzIj4KICAgICAgICA8ZGl2PgogICAgICAgICAgICA8bGFiZWwgZm9yPSJzdGFydF95ZWFyIj5Bw7FvIGluaWNpYWw8L2xhYmVsPjxicj4KICAgICAgICAgICAgPHNlbGVjdCBuYW1lPSJzdGFydF95ZWFyIiBpZD0ic3RhcnRfeWVhciI+CiAgICAgICAgICAgICAgICB7JSBmb3IgcCBpbiBhdmFpbGFibGVfcGVyaW9kcyAlfQogICAgICAgICAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9Int7IHAueWVhciB9fSIKICAgICAgICAgICAgICAgICAgICAgICAgeyUgaWYgcmVwb3J0X2ZpbHRlci5zdGFydF95ZWFyID09IHAueWVhciBhbmQgcmVwb3J0X2ZpbHRlci5zdGFydF9tb250aCA9PSBwLm1vbnRoICV9c2VsZWN0ZWR7JSBlbmRpZiAlfT4KICAgICAgICAgICAgICAgICAgICAgICAge3sgcC55ZWFyIH19CiAgICAgICAgICAgICAgICAgICAgPC9vcHRpb24+CiAgICAgICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgICAgPC9zZWxlY3Q+CiAgICAgICAgPC9kaXY+CgogICAgICAgIDxkaXY+CiAgICAgICAgICAgIDxsYWJlbCBmb3I9InN0YXJ0X21vbnRoIj5NZXMgaW5pY2lhbDwvbGFiZWw+PGJyPgogICAgICAgICAgICA8c2VsZWN0IG5hbWU9InN0YXJ0X21vbnRoIiBpZD0ic3RhcnRfbW9udGgiPgogICAgICAgICAgICAgICAgeyUgZm9yIHAgaW4gYXZhaWxhYmxlX3BlcmlvZHMgJX0KICAgICAgICAgICAgICAgICAgICA8b3B0aW9uIHZhbHVlPSJ7eyBwLm1vbnRoIH19IgogICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiByZXBvcnRfZmlsdGVyLnN0YXJ0X3llYXIgPT0gcC55ZWFyIGFuZCByZXBvcnRfZmlsdGVyLnN0YXJ0X21vbnRoID09IHAubW9udGggJX1zZWxlY3RlZHslIGVuZGlmICV9PgogICAgICAgICAgICAgICAgICAgICAgICB7eyBwLm1vbnRofHN0cmluZ2Zvcm1hdDoiMDJkIiB9fQogICAgICAgICAgICAgICAgICAgIDwvb3B0aW9uPgogICAgICAgICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgICAgIDwvc2VsZWN0PgogICAgICAgIDwvZGl2PgoKICAgICAgICA8ZGl2PgogICAgICAgICAgICA8bGFiZWwgZm9yPSJtb250aF9jb3VudCI+Q2FudGlkYWQgZGUgbWVzZXM8L2xhYmVsPjxicj4KICAgICAgICAgICAgPHNlbGVjdCBuYW1lPSJtb250aF9jb3VudCIgaWQ9Im1vbnRoX2NvdW50Ij4KICAgICAgICAgICAgICAgIHslIGZvciBvcHQgaW4gbW9udGhfY291bnRfb3B0aW9ucyAlfQogICAgICAgICAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9Int7IG9wdCB9fSIgeyUgaWYgcmVwb3J0X2ZpbHRlci5tb250aF9jb3VudCA9PSBvcHQgJX1zZWxlY3RlZHslIGVuZGlmICV9PgogICAgICAgICAgICAgICAgICAgICAgICB7eyBvcHQgfX0KICAgICAgICAgICAgICAgICAgICA8L29wdGlvbj4KICAgICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICA8L3NlbGVjdD4KICAgICAgICA8L2Rpdj4KCiAgICAgICAgPGRpdj4KICAgICAgICAgIDxsYWJlbCBmb3I9InNvcnQiPlNvcnQ8L2xhYmVsPjxicj4KICAgICAgICAgIDxzZWxlY3QgaWQ9InNvcnQiPgogICAgICAgICAgICA8b3B0aW9uIHZhbHVlPSJ1bmVzIgogICAgICAgICAgICAgIHslIGlmIHJlcG9ydF9zb3J0Lmdyb3VwX21vZGUgPT0gInVuZSIgJX1zZWxlY3RlZHslIGVuZGlmICV9PgogICAgICAgICAgICAgIFVORXMKICAgICAgICAgICAgPC9vcHRpb24+CiAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9ImZlY2hhc19hc2MiCiAgICAgICAgICAgICAgeyUgaWYgcmVwb3J0X3NvcnQuZ3JvdXBfbW9kZSA9PSAicGVyaW9kIiBhbmQgcmVwb3J0X3NvcnQuZGF0ZV9vcmRlciA9PSAiYXNjIiAlfXNlbGVjdGVkeyUgZW5kaWYgJX0+CiAgICAgICAgICAgICAgRmVjaGFzIGFzY2VuZGVudGVzCiAgICAgICAgICAgIDwvb3B0aW9uPgogICAgICAgICAgICA8b3B0aW9uIHZhbHVlPSJmZWNoYXNfZGVzYyIKICAgICAgICAgICAgICB7JSBpZiByZXBvcnRfc29ydC5ncm91cF9tb2RlID09ICJwZXJpb2QiIGFuZCByZXBvcnRfc29ydC5kYXRlX29yZGVyID09ICJkZXNjIiAlfXNlbGVjdGVkeyUgZW5kaWYgJX0+CiAgICAgICAgICAgICAgRmVjaGFzIGRlc2NlbmRlbnRlcwogICAgICAgICAgICA8L29wdGlvbj4KICAgICAgICAgIDwvc2VsZWN0PgogICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0iZGF0ZV9vcmRlciIgaWQ9ImRhdGVfb3JkZXIiCiAgICAgICAgICAgICAgICAgdmFsdWU9InslIGlmIHJlcG9ydF9zb3J0Lmdyb3VwX21vZGUgPT0gJ3BlcmlvZCcgYW5kIHJlcG9ydF9zb3J0LmRhdGVfb3JkZXIgPT0gJ2Rlc2MnICV9ZGVzY3slIGVsc2UgJX1hc2N7JSBlbmRpZiAlfSI+CiAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJncm91cF9tb2RlIiBpZD0iZ3JvdXBfbW9kZSIKICAgICAgICAgICAgICAgICB2YWx1ZT0ieyUgaWYgcmVwb3J0X3NvcnQuZ3JvdXBfbW9kZSA9PSAncGVyaW9kJyAlfXBlcmlvZHslIGVsc2UgJX11bmV7JSBlbmRpZiAlfSI+CiAgICAgICAgPC9kaXY+CiAgICAgIAogICAgICAgIDxkaXYgc3R5bGU9ImFsaWduLXNlbGY6ZW5kOyI+CiAgICAgICAgICAgIDxidXR0b24gdHlwZT0iYnV0dG9uIiBpZD0iYnRuLWV4cG9ydC1tZCI+Lm1kIGV4cG9ydDwvYnV0dG9uPgogICAgICAgIDwvZGl2PgogICAgPC9mb3JtPgoKICAgIDx0YWJsZT4KICAgICAgICA8dGhlYWQ+CiAgICAgICAgICAgIDx0cj4KICAgICAgICAgICAgICAgIDx0aCBzdHlsZT0idGV4dC1hbGlnbjpsZWZ0OyI+VU5FPC90aD4KICAgICAgICAgICAgICAgIDx0aCBzdHlsZT0idGV4dC1hbGlnbjpjZW50ZXI7Ij5QZXJpb2RvPC90aD4KICAgICAgICAgICAgICAgIDx0aCBzdHlsZT0idGV4dC1hbGlnbjpjZW50ZXI7Ij5NZXRhIHJlc3B1ZXN0YSByZXFzPC90aD4KICAgICAgICAgICAgICAgIDx0aCBzdHlsZT0idGV4dC1hbGlnbjpjZW50ZXI7Ij5SZXNwdWVzdGEgcmVxcyByZWFsPC90aD4KICAgICAgICAgICAgICAgIDx0aCBzdHlsZT0idGV4dC1hbGlnbjpjZW50ZXI7Ij5DdW1wbGU8L3RoPgogICAgICAgICAgICAgICAgPHRoIHN0eWxlPSJ0ZXh0LWFsaWduOmNlbnRlcjsiPlB1bnRvcyBhc2lnbmFkb3M8L3RoPgogICAgICAgICAgICAgICAgPHRoIHN0eWxlPSJ0ZXh0LWFsaWduOmNlbnRlcjsiPlRvdGFsIGRlbCBtZXM8L3RoPgogICAgICAgICAgICA8L3RyPgogICAgICAgIDwvdGhlYWQ+CiAgICAgICAgPHRib2R5PgogICAgICAgICAgICB7JSBmb3Igcm93IGluIHJvd3MgJX0KICAgICAgICAgICAgICAgIHslIGlmIHJvdy5pc19zZXBhcmF0b3IgJX0KICAgICAgICAgICAgICAgICAgICA8dHIgY2xhc3M9Imdyb3VwX3NlcGFyYXRvciI+CiAgICAgICAgICAgICAgICAgICAgICAgIDx0ZCBjb2xzcGFuPSI4Ij48L3RkPgogICAgICAgICAgICAgICAgICAgIDwvdHI+CiAgICAgICAgICAgICAgICB7JSBlbHNlICV9CiAgICAgICAgICAgICAgICAgICAgPHRyPgogICAgICAgICAgICAgICAgICAgICAgICA8dGQ+e3sgcm93LnRhcmdldC51bmUubmFtZV9lcyB9fTwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD57eyByb3cudGFyZ2V0LnllYXIgfX0te3sgcm93LnRhcmdldC5tb250aHxzdHJpbmdmb3JtYXQ6IjAyZCIgfX08L3RkPgogICAgICAgICAgICAgICAgICAgICAgICA8dGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiByb3cudGFyZ2V0LnRhcmdldF92YWx1ZSAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHt7IHJvdy50YXJnZXQudGFyZ2V0X3ZhbHVlfGZsb2F0Zm9ybWF0OjB8dW5sb2NhbGl6ZSB9fQogICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIOKAlAogICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgPHRkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgaWYgcm93LnJlc3VsdCAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHt7IHJvdy5yZXN1bHQubWVhc3VyZWRfdmFsdWV8ZmxvYXRmb3JtYXQ6MHx1bmxvY2FsaXplIH19CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbHNlICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg4oCUCiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgICAgICAgICAgICAgICA8L3RkPgogICAgICAgICAgICAgICAgICAgICAgICA8dGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiByb3cucmVzdWx0IGFuZCByb3cucmVzdWx0LmlzX2FjaGlldmVkICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHNwYW4gY2xhc3M9Im9rIj5Tw608L3NwYW4+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbHNlICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHNwYW4gY2xhc3M9ImJhZCI+Tm88L3NwYW4+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgICAgICAgICAgICAgICA8L3RkPgogICAgICAgICAgICAgICAgICAgICAgICA8dGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiByb3cucmVzdWx0ICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAge3sgcm93LnJlc3VsdC5wb2ludHNfYXdhcmRlZCB9fQogICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDAKICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGlmIHJvdy5zY29yZWNhcmQgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7eyByb3cuc2NvcmVjYXJkLnRvdGFsX3BvaW50cyB9fQogICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDAKICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxhCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgaHJlZj0ieyUgdXJsICdwZ2M6Y2xpZW50ZXNfbnVldm9zX2RldGFpbCcgJX0/dW5lPXt7IHJvdy50YXJnZXQudW5lLmlkIH19JnllYXI9e3sgcm93LnRhcmdldC55ZWFyIH19Jm1vbnRoPXt7IHJvdy50YXJnZXQubW9udGggfX0iCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgY2xhc3M9ImRldGFpbC1pY29uLWxpbmsiCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYXJpYS1sYWJlbD0iVmVyIGRldGFsbGUgZGUgY2xpZW50ZXMgbnVldm9zIgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJkZXRhaWwtaWNvbiI+PC9zcGFuPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPC9hPgogICAgICAgICAgICAgICAgICAgICAgICA8L3RkPgogICAgICAgICAgICAgICAgICAgIDwvdHI+CiAgICAgICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgICB7JSBlbXB0eSAlfQogICAgICAgICAgICAgICAgPHRyPgogICAgICAgICAgICAgICAgICAgIDx0ZCBjb2xzcGFuPSI4Ij5ObyBoYXkgZGF0b3MgZGUgcmVzcHVlc3RhIGEgcmVxdWVyaW1pZW50b3MgcGFyYSBsb3MgZmlsdHJvcyBzZWxlY2Npb25hZG9zLjwvdGQ+CiAgICAgICAgICAgICAgICA8L3RyPgogICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICA8L3Rib2R5PgogICAgPC90YWJsZT4KPC9kaXY+Cgo8c2NyaXB0Pgpkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCJET01Db250ZW50TG9hZGVkIiwgZnVuY3Rpb24gKCkgewogICAgY29uc3Qgc3RhcnRQZXJpb2QgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgic3RhcnRfcGVyaW9kIik7CiAgICBjb25zdCBzdGFydFllYXIgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgic3RhcnRfeWVhciIpOwogICAgY29uc3Qgc3RhcnRNb250aCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJzdGFydF9tb250aCIpOwogICAgY29uc3Qgc29ydCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJzb3J0Iik7CiAgICBjb25zdCBkYXRlT3JkZXIgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiZGF0ZV9vcmRlciIpOwogICAgY29uc3QgZ3JvdXBNb2RlID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImdyb3VwX21vZGUiKTsKICAgIGNvbnN0IGJ0biA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJidG4tZXhwb3J0LW1kIik7CgogICAgZnVuY3Rpb24gc3luY1BlcmlvZEZpZWxkcygpIHsKICAgICAgICBpZiAoIXN0YXJ0UGVyaW9kKSByZXR1cm47CiAgICAgICAgY29uc3Qgb3B0aW9uID0gc3RhcnRQZXJpb2Qub3B0aW9uc1tzdGFydFBlcmlvZC5zZWxlY3RlZEluZGV4XTsKICAgICAgICBpZiAoIW9wdGlvbikgcmV0dXJuOwogICAgICAgIHN0YXJ0WWVhci52YWx1ZSA9IG9wdGlvbi5kYXRhc2V0LnllYXIgfHwgIiI7CiAgICAgICAgc3RhcnRNb250aC52YWx1ZSA9IG9wdGlvbi5kYXRhc2V0Lm1vbnRoIHx8ICIiOwogICAgfQoKICAgIGZ1bmN0aW9uIHN5bmNTb3J0RmllbGRzKCkgewogICAgICAgIGlmICghc29ydCkgcmV0dXJuOwogICAgICAgIGlmIChzb3J0LnZhbHVlID09PSAidW5lcyIpIHsKICAgICAgICAgICAgZ3JvdXBNb2RlLnZhbHVlID0gInVuZSI7CiAgICAgICAgICAgIGRhdGVPcmRlci52YWx1ZSA9ICJhc2MiOwogICAgICAgIH0gZWxzZSBpZiAoc29ydC52YWx1ZSA9PT0gImZlY2hhc19kZXNjIikgewogICAgICAgICAgICBncm91cE1vZGUudmFsdWUgPSAicGVyaW9kIjsKICAgICAgICAgICAgZGF0ZU9yZGVyLnZhbHVlID0gImRlc2MiOwogICAgICAgIH0gZWxzZSB7CiAgICAgICAgICAgIGdyb3VwTW9kZS52YWx1ZSA9ICJwZXJpb2QiOwogICAgICAgICAgICBkYXRlT3JkZXIudmFsdWUgPSAiYXNjIjsKICAgICAgICB9CiAgICB9CgoKICAgIGNvbnN0IGZpbHRlckZvcm0gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCJmb3JtLmZpbHRlcnMiKTsKICAgIGZ1bmN0aW9uIGFwcGx5RmlsdGVycygpIHsKICAgICAgICBpZiAodHlwZW9mIHN5bmNQZXJpb2RGaWVsZHMgPT09ICJmdW5jdGlvbiIpIHN5bmNQZXJpb2RGaWVsZHMoKTsKICAgICAgICBpZiAodHlwZW9mIHN5bmNTb3J0RmllbGRzID09PSAiZnVuY3Rpb24iKSBzeW5jU29ydEZpZWxkcygpOwogICAgICAgIGlmIChmaWx0ZXJGb3JtKSBmaWx0ZXJGb3JtLnN1Ym1pdCgpOwogICAgfQoKICAgIGlmIChzdGFydFBlcmlvZCkgewogICAgICAgIHN0YXJ0UGVyaW9kLmFkZEV2ZW50TGlzdGVuZXIoImNoYW5nZSIsIGFwcGx5RmlsdGVycyk7CiAgICAgICAgc3luY1BlcmlvZEZpZWxkcygpOwogICAgfQoKICAgIGlmIChzb3J0KSB7CiAgICAgICAgc29ydC5hZGRFdmVudExpc3RlbmVyKCJjaGFuZ2UiLCBhcHBseUZpbHRlcnMpOwogICAgICAgIHN5bmNTb3J0RmllbGRzKCk7CiAgICB9CgogICAgWyJtb250aF9jb3VudCIsICJtb2RlIiwgInN0YXJ0X3llYXIiLCAic3RhcnRfbW9udGgiLCAieWVhciIsICJtb250aCIsICJ1bmUiXS5mb3JFYWNoKGZ1bmN0aW9uIChpZCkgewogICAgICAgIGNvbnN0IGVsID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoaWQpOwogICAgICAgIGlmIChlbCAmJiBlbC50YWdOYW1lID09PSAiU0VMRUNUIikgewogICAgICAgICAgICBlbC5hZGRFdmVudExpc3RlbmVyKCJjaGFuZ2UiLCBhcHBseUZpbHRlcnMpOwogICAgICAgIH0KICAgIH0pOwoKICAgIGlmICghYnRuKSByZXR1cm47CgogICAgYnRuLmFkZEV2ZW50TGlzdGVuZXIoImNsaWNrIiwgYXN5bmMgZnVuY3Rpb24gKCkgewogICAgICAgIHN5bmNQZXJpb2RGaWVsZHMoKTsKICAgICAgICBzeW5jU29ydEZpZWxkcygpOwoKICAgICAgICBjb25zdCBwYXJhbXMgPSBuZXcgVVJMU2VhcmNoUGFyYW1zKHsKICAgICAgICAgICAgc3RhcnRfeWVhcjogc3RhcnRZZWFyLnZhbHVlIHx8ICIiLAogICAgICAgICAgICBzdGFydF9tb250aDogc3RhcnRNb250aC52YWx1ZSB8fCAiIiwKICAgICAgICAgICAgbW9udGhfY291bnQ6IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJtb250aF9jb3VudCIpPy52YWx1ZSB8fCAiIiwKICAgICAgICAgICAgZGF0ZV9vcmRlcjogZGF0ZU9yZGVyLnZhbHVlIHx8ICJhc2MiLAogICAgICAgICAgICBncm91cF9tb2RlOiBncm91cE1vZGUudmFsdWUgfHwgInVuZSIKICAgICAgICB9KTsKCiAgICAgICAgY29uc3QgdXJsID0gYHslIHVybCAncGdjOnJlc3B1ZXN0YV9yZXFzX2V4cG9ydF9tZCcgJX0/YCArIHBhcmFtcy50b1N0cmluZygpOwoKICAgICAgICBidG4uZGlzYWJsZWQgPSB0cnVlOwogICAgICAgIGNvbnN0IG9yaWdpbmFsVGV4dCA9IGJ0bi50ZXh0Q29udGVudDsKICAgICAgICBidG4udGV4dENvbnRlbnQgPSAiR2VuZXJhbmRvLi4uIjsKCiAgICAgICAgdHJ5IHsKICAgICAgICAgICAgY29uc3QgcmVzcG9uc2UgPSBhd2FpdCBmZXRjaCh1cmwsIHsKICAgICAgICAgICAgICAgIG1ldGhvZDogIkdFVCIsCiAgICAgICAgICAgICAgICBoZWFkZXJzOiB7CiAgICAgICAgICAgICAgICAgICAgIlgtUmVxdWVzdGVkLVdpdGgiOiAiWE1MSHR0cFJlcXVlc3QiCiAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgIH0pOwoKICAgICAgICAgICAgaWYgKCFyZXNwb25zZS5vaykgewogICAgICAgICAgICAgICAgdGhyb3cgbmV3IEVycm9yKCJObyBzZSBwdWRvIGdlbmVyYXIgZWwgYXJjaGl2byBNYXJrZG93bi4iKTsKICAgICAgICAgICAgfQoKICAgICAgICAgICAgY29uc3QgYmxvYiA9IGF3YWl0IHJlc3BvbnNlLmJsb2IoKTsKCiAgICAgICAgICAgIGxldCBmaWxlbmFtZSA9ICJwZ2MtcmVzcHVlc3RhLXJlcXMubWQiOwogICAgICAgICAgICBjb25zdCBkaXNwb3NpdGlvbiA9IHJlc3BvbnNlLmhlYWRlcnMuZ2V0KCJDb250ZW50LURpc3Bvc2l0aW9uIik7CiAgICAgICAgICAgIGlmIChkaXNwb3NpdGlvbikgewogICAgICAgICAgICAgICAgY29uc3QgdXRmOE1hdGNoID0gZGlzcG9zaXRpb24ubWF0Y2goL2ZpbGVuYW1lXCo9VVRGLTgnJyhbXjtdKykvaSk7CiAgICAgICAgICAgICAgICBjb25zdCBhc2NpaU1hdGNoID0gZGlzcG9zaXRpb24ubWF0Y2goL2ZpbGVuYW1lPSIoW14iXSspIi9pKTsKCiAgICAgICAgICAgICAgICBpZiAodXRmOE1hdGNoICYmIHV0ZjhNYXRjaFsxXSkgewogICAgICAgICAgICAgICAgICAgIGZpbGVuYW1lID0gZGVjb2RlVVJJQ29tcG9uZW50KHV0ZjhNYXRjaFsxXSk7CiAgICAgICAgICAgICAgICB9IGVsc2UgaWYgKGFzY2lpTWF0Y2ggJiYgYXNjaWlNYXRjaFsxXSkgewogICAgICAgICAgICAgICAgICAgIGZpbGVuYW1lID0gYXNjaWlNYXRjaFsxXTsKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgfQoKICAgICAgICAgICAgY29uc3Qgb2JqZWN0VXJsID0gd2luZG93LlVSTC5jcmVhdGVPYmplY3RVUkwoYmxvYik7CiAgICAgICAgICAgIGNvbnN0IGEgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCJhIik7CiAgICAgICAgICAgIGEuaHJlZiA9IG9iamVjdFVybDsKICAgICAgICAgICAgYS5kb3dubG9hZCA9IGZpbGVuYW1lOwogICAgICAgICAgICBkb2N1bWVudC5ib2R5LmFwcGVuZENoaWxkKGEpOwogICAgICAgICAgICBhLmNsaWNrKCk7CiAgICAgICAgICAgIGEucmVtb3ZlKCk7CiAgICAgICAgICAgIHdpbmRvdy5VUkwucmV2b2tlT2JqZWN0VVJMKG9iamVjdFVybCk7CiAgICAgICAgfSBjYXRjaCAoZXJyb3IpIHsKICAgICAgICAgICAgYWxlcnQoZXJyb3IubWVzc2FnZSB8fCAiRXJyb3IgZ2VuZXJhbmRvIGxhIGV4cG9ydGFjacOzbi4iKTsKICAgICAgICB9IGZpbmFsbHkgewogICAgICAgICAgICBidG4uZGlzYWJsZWQgPSBmYWxzZTsKICAgICAgICAgICAgYnRuLnRleHRDb250ZW50ID0gb3JpZ2luYWxUZXh0OwogICAgICAgIH0KICAgIH0pOwp9KTsKPC9zY3JpcHQ+CnslIGVuZGJsb2NrICV9
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgc/venta_cruzada.html
PATH_JSON="templates/pgc/venta_cruzada.html"
FILENAME=venta_cruzada.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=279
SIZE_BYTES_UTF8=9795
CONTENT_SHA256=c1d7a2ef3346447a06c203a4a4eef32a255ef3990028e1687a32472f76b7673b
ENDS_WITH_NEWLINE=FALSE
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

{% block title %}Venta cruzada vs meta{% endblock %}

{% block content %}
<style>
  .group_separator td {
    padding: 0;
    height: 14px;
    border-bottom: none;
    background: #ffffff;
  }
</style>
<div class="card">
    <div class="wcg-report-head" style="margin-top:0;">
      <h2 style="margin:0;">Venta cruzada vs meta</h2>
      {% include "includes/module_mark.html" with module="pgc" %}
    </div>
    <p class="muted">
        Meta y resultado mensual de venta cruzada por UNE y periodo.
    </p>

    <form method="get" class="filters">
        <div>
            <label for="start_year">Año inicial</label><br>
            <select name="start_year" id="start_year">
                {% for p in available_periods %}
                    <option value="{{ p.year }}"
                        {% if report_filter.start_year == p.year and report_filter.start_month == p.month %}selected{% endif %}>
                        {{ p.year }}
                    </option>
                {% endfor %}
            </select>
        </div>

        <div>
            <label for="start_month">Mes inicial</label><br>
            <select name="start_month" id="start_month">
                {% for p in available_periods %}
                    <option value="{{ p.month }}"
                        {% if report_filter.start_year == p.year and report_filter.start_month == p.month %}selected{% endif %}>
                        {{ p.month|stringformat:"02d" }}
                    </option>
                {% endfor %}
            </select>
        </div>

        <div>
            <label for="month_count">Cantidad de meses</label><br>
            <select name="month_count" id="month_count">
                {% for opt in month_count_options %}
                    <option value="{{ opt }}" {% if report_filter.month_count == opt %}selected{% endif %}>
                        {{ opt }}
                    </option>
                {% endfor %}
            </select>
        </div>

        <div>
          <label for="sort">Sort</label><br>
          <select id="sort">
            <option value="unes"
              {% if report_sort.group_mode == "une" %}selected{% endif %}>
              UNEs
            </option>
            <option value="fechas_asc"
              {% if report_sort.group_mode == "period" and report_sort.date_order == "asc" %}selected{% endif %}>
              Fechas ascendentes
            </option>
            <option value="fechas_desc"
              {% if report_sort.group_mode == "period" and report_sort.date_order == "desc" %}selected{% endif %}>
              Fechas descendentes
            </option>
          </select>
          <input type="hidden" name="date_order" id="date_order"
                 value="{% if report_sort.group_mode == 'period' and report_sort.date_order == 'desc' %}desc{% else %}asc{% endif %}">
          <input type="hidden" name="group_mode" id="group_mode"
                 value="{% if report_sort.group_mode == 'period' %}period{% else %}une{% endif %}">
        </div>
      
        <div style="align-self:end;">
            <button type="button" id="btn-export-md">.md export</button>
        </div>
    </form>

    <table>
        <thead>
            <tr>
                <th style="text-align:left;">UNE</th>
                <th style="text-align:center;">Periodo</th>
                <th style="text-align:center;">Meta venta cruzada</th>
                <th style="text-align:center;">Venta cruzada real</th>
                <th style="text-align:center;">Cumple</th>
                <th style="text-align:center;">Puntos asignados</th>
                <th style="text-align:center;">Total del mes</th>
            </tr>
        </thead>

        <tbody>
          {% for row in rows %}
          {% if row.is_separator %}
          <tr class="group_separator">
            <td colspan="7"></td>
          </tr>
          {% else %}
          <tr>
            <td style="text-align:left;">{{ row.target.une.name_es }}</td>
            <td style="text-align:center;">{{ row.target.year }}-{{ row.target.month|stringformat:"02d" }}</td>
            <td style="text-align:center;">
              {% if row.target.target_value %}
              {{ row.target.target_value|floatformat:0|unlocalize }}
              {% else %}
              —
              {% endif %}
            </td>
            <td style="text-align:center;">
              {% if row.result and row.result.measured_value != None %}
              {{ row.result.measured_value|floatformat:0|unlocalize }}
              {% else %}
              —
              {% endif %}
            </td>
            <td style="text-align:center;">
              {% if row.result and row.result.is_achieved %}
              <span class="ok">Sí</span>
              {% else %}
              <span class="bad">No</span>
              {% endif %}
            </td>
            <td style="text-align:center;">
              {% if row.result %}
              {{ row.result.points_awarded }}
              {% else %}
              0
              {% endif %}
            </td>
            <td style="text-align:center;">
              {% if row.scorecard %}
              {{ row.scorecard.total_points }}
              {% else %}
              0
              {% endif %}
            </td>
          </tr>
          {% endif %}
          {% empty %}
          <tr>
            <td colspan="7" style="text-align:center;">No hay datos de venta cruzada para los filtros seleccionados.</td>
          </tr>
          {% endfor %}
        </tbody>
          
    </table>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
    const startPeriod = document.getElementById("start_period");
    const startYear = document.getElementById("start_year");
    const startMonth = document.getElementById("start_month");
    const sort = document.getElementById("sort");
    const dateOrder = document.getElementById("date_order");
    const groupMode = document.getElementById("group_mode");
    const btn = document.getElementById("btn-export-md");

    function syncPeriodFields() {
        if (!startPeriod) return;
        const option = startPeriod.options[startPeriod.selectedIndex];
        if (!option) return;
        startYear.value = option.dataset.year || "";
        startMonth.value = option.dataset.month || "";
    }

    function syncSortFields() {
        if (!sort) return;
        if (sort.value === "unes") {
            groupMode.value = "une";
            dateOrder.value = "asc";
        } else if (sort.value === "fechas_desc") {
            groupMode.value = "period";
            dateOrder.value = "desc";
        } else {
            groupMode.value = "period";
            dateOrder.value = "asc";
        }
    }


    const filterForm = document.querySelector("form.filters");
    function applyFilters() {
        if (typeof syncPeriodFields === "function") syncPeriodFields();
        if (typeof syncSortFields === "function") syncSortFields();
        if (filterForm) filterForm.submit();
    }

    if (startPeriod) {
        startPeriod.addEventListener("change", applyFilters);
        syncPeriodFields();
    }

    if (sort) {
        sort.addEventListener("change", applyFilters);
        syncSortFields();
    }

    ["month_count", "mode", "start_year", "start_month", "year", "month", "une"].forEach(function (id) {
        const el = document.getElementById(id);
        if (el && el.tagName === "SELECT") {
            el.addEventListener("change", applyFilters);
        }
    });

    if (!btn) return;

    btn.addEventListener("click", async function () {
        syncPeriodFields();
        syncSortFields();

        const params = new URLSearchParams({
            start_year: startYear.value || "",
            start_month: startMonth.value || "",
            month_count: document.getElementById("month_count")?.value || "",
            date_order: dateOrder.value || "asc",
            group_mode: groupMode.value || "une"
        });

        const url = `{% url 'pgc:venta_cruzada_export_md' %}?` + params.toString();

        btn.disabled = true;
        const originalText = btn.textContent;
        btn.textContent = "Generando...";

        try {
            const response = await fetch(url, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            if (!response.ok) {
                throw new Error("No se pudo generar el archivo Markdown.");
            }

            const blob = await response.blob();

            let filename = "pgc-venta-cruzada.md";
            const disposition = response.headers.get("Content-Disposition");
            if (disposition) {
                const utf8Match = disposition.match(/filename\*=UTF-8''([^;]+)/i);
                const asciiMatch = disposition.match(/filename="([^"]+)"/i);

                if (utf8Match && utf8Match[1]) {
                    filename = decodeURIComponent(utf8Match[1]);
                } else if (asciiMatch && asciiMatch[1]) {
                    filename = asciiMatch[1];
                }
            }

            const objectUrl = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = objectUrl;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(objectUrl);
        } catch (error) {
            alert(error.message || "Error generando la exportación.");
        } finally {
            btn.disabled = false;
            btn.textContent = originalText;
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
00004|{% block title %}Venta cruzada vs meta{% endblock %}
00005|
00006|{% block content %}
00007|<style>
00008|  .group_separator td {
00009|    padding: 0;
00010|    height: 14px;
00011|    border-bottom: none;
00012|    background: #ffffff;
00013|  }
00014|</style>
00015|<div class="card">
00016|    <div class="wcg-report-head" style="margin-top:0;">
00017|      <h2 style="margin:0;">Venta cruzada vs meta</h2>
00018|      {% include "includes/module_mark.html" with module="pgc" %}
00019|    </div>
00020|    <p class="muted">
00021|        Meta y resultado mensual de venta cruzada por UNE y periodo.
00022|    </p>
00023|
00024|    <form method="get" class="filters">
00025|        <div>
00026|            <label for="start_year">Año inicial</label><br>
00027|            <select name="start_year" id="start_year">
00028|                {% for p in available_periods %}
00029|                    <option value="{{ p.year }}"
00030|                        {% if report_filter.start_year == p.year and report_filter.start_month == p.month %}selected{% endif %}>
00031|                        {{ p.year }}
00032|                    </option>
00033|                {% endfor %}
00034|            </select>
00035|        </div>
00036|
00037|        <div>
00038|            <label for="start_month">Mes inicial</label><br>
00039|            <select name="start_month" id="start_month">
00040|                {% for p in available_periods %}
00041|                    <option value="{{ p.month }}"
00042|                        {% if report_filter.start_year == p.year and report_filter.start_month == p.month %}selected{% endif %}>
00043|                        {{ p.month|stringformat:"02d" }}
00044|                    </option>
00045|                {% endfor %}
00046|            </select>
00047|        </div>
00048|
00049|        <div>
00050|            <label for="month_count">Cantidad de meses</label><br>
00051|            <select name="month_count" id="month_count">
00052|                {% for opt in month_count_options %}
00053|                    <option value="{{ opt }}" {% if report_filter.month_count == opt %}selected{% endif %}>
00054|                        {{ opt }}
00055|                    </option>
00056|                {% endfor %}
00057|            </select>
00058|        </div>
00059|
00060|        <div>
00061|          <label for="sort">Sort</label><br>
00062|          <select id="sort">
00063|            <option value="unes"
00064|              {% if report_sort.group_mode == "une" %}selected{% endif %}>
00065|              UNEs
00066|            </option>
00067|            <option value="fechas_asc"
00068|              {% if report_sort.group_mode == "period" and report_sort.date_order == "asc" %}selected{% endif %}>
00069|              Fechas ascendentes
00070|            </option>
00071|            <option value="fechas_desc"
00072|              {% if report_sort.group_mode == "period" and report_sort.date_order == "desc" %}selected{% endif %}>
00073|              Fechas descendentes
00074|            </option>
00075|          </select>
00076|          <input type="hidden" name="date_order" id="date_order"
00077|                 value="{% if report_sort.group_mode == 'period' and report_sort.date_order == 'desc' %}desc{% else %}asc{% endif %}">
00078|          <input type="hidden" name="group_mode" id="group_mode"
00079|                 value="{% if report_sort.group_mode == 'period' %}period{% else %}une{% endif %}">
00080|        </div>
00081|      
00082|        <div style="align-self:end;">
00083|            <button type="button" id="btn-export-md">.md export</button>
00084|        </div>
00085|    </form>
00086|
00087|    <table>
00088|        <thead>
00089|            <tr>
00090|                <th style="text-align:left;">UNE</th>
00091|                <th style="text-align:center;">Periodo</th>
00092|                <th style="text-align:center;">Meta venta cruzada</th>
00093|                <th style="text-align:center;">Venta cruzada real</th>
00094|                <th style="text-align:center;">Cumple</th>
00095|                <th style="text-align:center;">Puntos asignados</th>
00096|                <th style="text-align:center;">Total del mes</th>
00097|            </tr>
00098|        </thead>
00099|
00100|        <tbody>
00101|          {% for row in rows %}
00102|          {% if row.is_separator %}
00103|          <tr class="group_separator">
00104|            <td colspan="7"></td>
00105|          </tr>
00106|          {% else %}
00107|          <tr>
00108|            <td style="text-align:left;">{{ row.target.une.name_es }}</td>
00109|            <td style="text-align:center;">{{ row.target.year }}-{{ row.target.month|stringformat:"02d" }}</td>
00110|            <td style="text-align:center;">
00111|              {% if row.target.target_value %}
00112|              {{ row.target.target_value|floatformat:0|unlocalize }}
00113|              {% else %}
00114|              —
00115|              {% endif %}
00116|            </td>
00117|            <td style="text-align:center;">
00118|              {% if row.result and row.result.measured_value != None %}
00119|              {{ row.result.measured_value|floatformat:0|unlocalize }}
00120|              {% else %}
00121|              —
00122|              {% endif %}
00123|            </td>
00124|            <td style="text-align:center;">
00125|              {% if row.result and row.result.is_achieved %}
00126|              <span class="ok">Sí</span>
00127|              {% else %}
00128|              <span class="bad">No</span>
00129|              {% endif %}
00130|            </td>
00131|            <td style="text-align:center;">
00132|              {% if row.result %}
00133|              {{ row.result.points_awarded }}
00134|              {% else %}
00135|              0
00136|              {% endif %}
00137|            </td>
00138|            <td style="text-align:center;">
00139|              {% if row.scorecard %}
00140|              {{ row.scorecard.total_points }}
00141|              {% else %}
00142|              0
00143|              {% endif %}
00144|            </td>
00145|          </tr>
00146|          {% endif %}
00147|          {% empty %}
00148|          <tr>
00149|            <td colspan="7" style="text-align:center;">No hay datos de venta cruzada para los filtros seleccionados.</td>
00150|          </tr>
00151|          {% endfor %}
00152|        </tbody>
00153|          
00154|    </table>
00155|</div>
00156|
00157|<script>
00158|document.addEventListener("DOMContentLoaded", function () {
00159|    const startPeriod = document.getElementById("start_period");
00160|    const startYear = document.getElementById("start_year");
00161|    const startMonth = document.getElementById("start_month");
00162|    const sort = document.getElementById("sort");
00163|    const dateOrder = document.getElementById("date_order");
00164|    const groupMode = document.getElementById("group_mode");
00165|    const btn = document.getElementById("btn-export-md");
00166|
00167|    function syncPeriodFields() {
00168|        if (!startPeriod) return;
00169|        const option = startPeriod.options[startPeriod.selectedIndex];
00170|        if (!option) return;
00171|        startYear.value = option.dataset.year || "";
00172|        startMonth.value = option.dataset.month || "";
00173|    }
00174|
00175|    function syncSortFields() {
00176|        if (!sort) return;
00177|        if (sort.value === "unes") {
00178|            groupMode.value = "une";
00179|            dateOrder.value = "asc";
00180|        } else if (sort.value === "fechas_desc") {
00181|            groupMode.value = "period";
00182|            dateOrder.value = "desc";
00183|        } else {
00184|            groupMode.value = "period";
00185|            dateOrder.value = "asc";
00186|        }
00187|    }
00188|
00189|
00190|    const filterForm = document.querySelector("form.filters");
00191|    function applyFilters() {
00192|        if (typeof syncPeriodFields === "function") syncPeriodFields();
00193|        if (typeof syncSortFields === "function") syncSortFields();
00194|        if (filterForm) filterForm.submit();
00195|    }
00196|
00197|    if (startPeriod) {
00198|        startPeriod.addEventListener("change", applyFilters);
00199|        syncPeriodFields();
00200|    }
00201|
00202|    if (sort) {
00203|        sort.addEventListener("change", applyFilters);
00204|        syncSortFields();
00205|    }
00206|
00207|    ["month_count", "mode", "start_year", "start_month", "year", "month", "une"].forEach(function (id) {
00208|        const el = document.getElementById(id);
00209|        if (el && el.tagName === "SELECT") {
00210|            el.addEventListener("change", applyFilters);
00211|        }
00212|    });
00213|
00214|    if (!btn) return;
00215|
00216|    btn.addEventListener("click", async function () {
00217|        syncPeriodFields();
00218|        syncSortFields();
00219|
00220|        const params = new URLSearchParams({
00221|            start_year: startYear.value || "",
00222|            start_month: startMonth.value || "",
00223|            month_count: document.getElementById("month_count")?.value || "",
00224|            date_order: dateOrder.value || "asc",
00225|            group_mode: groupMode.value || "une"
00226|        });
00227|
00228|        const url = `{% url 'pgc:venta_cruzada_export_md' %}?` + params.toString();
00229|
00230|        btn.disabled = true;
00231|        const originalText = btn.textContent;
00232|        btn.textContent = "Generando...";
00233|
00234|        try {
00235|            const response = await fetch(url, {
00236|                method: "GET",
00237|                headers: {
00238|                    "X-Requested-With": "XMLHttpRequest"
00239|                }
00240|            });
00241|
00242|            if (!response.ok) {
00243|                throw new Error("No se pudo generar el archivo Markdown.");
00244|            }
00245|
00246|            const blob = await response.blob();
00247|
00248|            let filename = "pgc-venta-cruzada.md";
00249|            const disposition = response.headers.get("Content-Disposition");
00250|            if (disposition) {
00251|                const utf8Match = disposition.match(/filename\*=UTF-8''([^;]+)/i);
00252|                const asciiMatch = disposition.match(/filename="([^"]+)"/i);
00253|
00254|                if (utf8Match && utf8Match[1]) {
00255|                    filename = decodeURIComponent(utf8Match[1]);
00256|                } else if (asciiMatch && asciiMatch[1]) {
00257|                    filename = asciiMatch[1];
00258|                }
00259|            }
00260|
00261|            const objectUrl = window.URL.createObjectURL(blob);
00262|            const a = document.createElement("a");
00263|            a.href = objectUrl;
00264|            a.download = filename;
00265|            document.body.appendChild(a);
00266|            a.click();
00267|            a.remove();
00268|            window.URL.revokeObjectURL(objectUrl);
00269|        } catch (error) {
00270|            alert(error.message || "Error generando la exportación.");
00271|        } finally {
00272|            btn.disabled = false;
00273|            btn.textContent = originalText;
00274|        }
00275|    });
00276|});
00277|</script>
00278|{% endblock %}
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZS5odG1sIiAlfQp7JSBsb2FkIGwxMG4gJX0KCnslIGJsb2NrIHRpdGxlICV9VmVudGEgY3J1emFkYSB2cyBtZXRheyUgZW5kYmxvY2sgJX0KCnslIGJsb2NrIGNvbnRlbnQgJX0KPHN0eWxlPgogIC5ncm91cF9zZXBhcmF0b3IgdGQgewogICAgcGFkZGluZzogMDsKICAgIGhlaWdodDogMTRweDsKICAgIGJvcmRlci1ib3R0b206IG5vbmU7CiAgICBiYWNrZ3JvdW5kOiAjZmZmZmZmOwogIH0KPC9zdHlsZT4KPGRpdiBjbGFzcz0iY2FyZCI+CiAgICA8ZGl2IGNsYXNzPSJ3Y2ctcmVwb3J0LWhlYWQiIHN0eWxlPSJtYXJnaW4tdG9wOjA7Ij4KICAgICAgPGgyIHN0eWxlPSJtYXJnaW46MDsiPlZlbnRhIGNydXphZGEgdnMgbWV0YTwvaDI+CiAgICAgIHslIGluY2x1ZGUgImluY2x1ZGVzL21vZHVsZV9tYXJrLmh0bWwiIHdpdGggbW9kdWxlPSJwZ2MiICV9CiAgICA8L2Rpdj4KICAgIDxwIGNsYXNzPSJtdXRlZCI+CiAgICAgICAgTWV0YSB5IHJlc3VsdGFkbyBtZW5zdWFsIGRlIHZlbnRhIGNydXphZGEgcG9yIFVORSB5IHBlcmlvZG8uCiAgICA8L3A+CgogICAgPGZvcm0gbWV0aG9kPSJnZXQiIGNsYXNzPSJmaWx0ZXJzIj4KICAgICAgICA8ZGl2PgogICAgICAgICAgICA8bGFiZWwgZm9yPSJzdGFydF95ZWFyIj5Bw7FvIGluaWNpYWw8L2xhYmVsPjxicj4KICAgICAgICAgICAgPHNlbGVjdCBuYW1lPSJzdGFydF95ZWFyIiBpZD0ic3RhcnRfeWVhciI+CiAgICAgICAgICAgICAgICB7JSBmb3IgcCBpbiBhdmFpbGFibGVfcGVyaW9kcyAlfQogICAgICAgICAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9Int7IHAueWVhciB9fSIKICAgICAgICAgICAgICAgICAgICAgICAgeyUgaWYgcmVwb3J0X2ZpbHRlci5zdGFydF95ZWFyID09IHAueWVhciBhbmQgcmVwb3J0X2ZpbHRlci5zdGFydF9tb250aCA9PSBwLm1vbnRoICV9c2VsZWN0ZWR7JSBlbmRpZiAlfT4KICAgICAgICAgICAgICAgICAgICAgICAge3sgcC55ZWFyIH19CiAgICAgICAgICAgICAgICAgICAgPC9vcHRpb24+CiAgICAgICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgICAgPC9zZWxlY3Q+CiAgICAgICAgPC9kaXY+CgogICAgICAgIDxkaXY+CiAgICAgICAgICAgIDxsYWJlbCBmb3I9InN0YXJ0X21vbnRoIj5NZXMgaW5pY2lhbDwvbGFiZWw+PGJyPgogICAgICAgICAgICA8c2VsZWN0IG5hbWU9InN0YXJ0X21vbnRoIiBpZD0ic3RhcnRfbW9udGgiPgogICAgICAgICAgICAgICAgeyUgZm9yIHAgaW4gYXZhaWxhYmxlX3BlcmlvZHMgJX0KICAgICAgICAgICAgICAgICAgICA8b3B0aW9uIHZhbHVlPSJ7eyBwLm1vbnRoIH19IgogICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiByZXBvcnRfZmlsdGVyLnN0YXJ0X3llYXIgPT0gcC55ZWFyIGFuZCByZXBvcnRfZmlsdGVyLnN0YXJ0X21vbnRoID09IHAubW9udGggJX1zZWxlY3RlZHslIGVuZGlmICV9PgogICAgICAgICAgICAgICAgICAgICAgICB7eyBwLm1vbnRofHN0cmluZ2Zvcm1hdDoiMDJkIiB9fQogICAgICAgICAgICAgICAgICAgIDwvb3B0aW9uPgogICAgICAgICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgICAgIDwvc2VsZWN0PgogICAgICAgIDwvZGl2PgoKICAgICAgICA8ZGl2PgogICAgICAgICAgICA8bGFiZWwgZm9yPSJtb250aF9jb3VudCI+Q2FudGlkYWQgZGUgbWVzZXM8L2xhYmVsPjxicj4KICAgICAgICAgICAgPHNlbGVjdCBuYW1lPSJtb250aF9jb3VudCIgaWQ9Im1vbnRoX2NvdW50Ij4KICAgICAgICAgICAgICAgIHslIGZvciBvcHQgaW4gbW9udGhfY291bnRfb3B0aW9ucyAlfQogICAgICAgICAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9Int7IG9wdCB9fSIgeyUgaWYgcmVwb3J0X2ZpbHRlci5tb250aF9jb3VudCA9PSBvcHQgJX1zZWxlY3RlZHslIGVuZGlmICV9PgogICAgICAgICAgICAgICAgICAgICAgICB7eyBvcHQgfX0KICAgICAgICAgICAgICAgICAgICA8L29wdGlvbj4KICAgICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICA8L3NlbGVjdD4KICAgICAgICA8L2Rpdj4KCiAgICAgICAgPGRpdj4KICAgICAgICAgIDxsYWJlbCBmb3I9InNvcnQiPlNvcnQ8L2xhYmVsPjxicj4KICAgICAgICAgIDxzZWxlY3QgaWQ9InNvcnQiPgogICAgICAgICAgICA8b3B0aW9uIHZhbHVlPSJ1bmVzIgogICAgICAgICAgICAgIHslIGlmIHJlcG9ydF9zb3J0Lmdyb3VwX21vZGUgPT0gInVuZSIgJX1zZWxlY3RlZHslIGVuZGlmICV9PgogICAgICAgICAgICAgIFVORXMKICAgICAgICAgICAgPC9vcHRpb24+CiAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9ImZlY2hhc19hc2MiCiAgICAgICAgICAgICAgeyUgaWYgcmVwb3J0X3NvcnQuZ3JvdXBfbW9kZSA9PSAicGVyaW9kIiBhbmQgcmVwb3J0X3NvcnQuZGF0ZV9vcmRlciA9PSAiYXNjIiAlfXNlbGVjdGVkeyUgZW5kaWYgJX0+CiAgICAgICAgICAgICAgRmVjaGFzIGFzY2VuZGVudGVzCiAgICAgICAgICAgIDwvb3B0aW9uPgogICAgICAgICAgICA8b3B0aW9uIHZhbHVlPSJmZWNoYXNfZGVzYyIKICAgICAgICAgICAgICB7JSBpZiByZXBvcnRfc29ydC5ncm91cF9tb2RlID09ICJwZXJpb2QiIGFuZCByZXBvcnRfc29ydC5kYXRlX29yZGVyID09ICJkZXNjIiAlfXNlbGVjdGVkeyUgZW5kaWYgJX0+CiAgICAgICAgICAgICAgRmVjaGFzIGRlc2NlbmRlbnRlcwogICAgICAgICAgICA8L29wdGlvbj4KICAgICAgICAgIDwvc2VsZWN0PgogICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0iZGF0ZV9vcmRlciIgaWQ9ImRhdGVfb3JkZXIiCiAgICAgICAgICAgICAgICAgdmFsdWU9InslIGlmIHJlcG9ydF9zb3J0Lmdyb3VwX21vZGUgPT0gJ3BlcmlvZCcgYW5kIHJlcG9ydF9zb3J0LmRhdGVfb3JkZXIgPT0gJ2Rlc2MnICV9ZGVzY3slIGVsc2UgJX1hc2N7JSBlbmRpZiAlfSI+CiAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJncm91cF9tb2RlIiBpZD0iZ3JvdXBfbW9kZSIKICAgICAgICAgICAgICAgICB2YWx1ZT0ieyUgaWYgcmVwb3J0X3NvcnQuZ3JvdXBfbW9kZSA9PSAncGVyaW9kJyAlfXBlcmlvZHslIGVsc2UgJX11bmV7JSBlbmRpZiAlfSI+CiAgICAgICAgPC9kaXY+CiAgICAgIAogICAgICAgIDxkaXYgc3R5bGU9ImFsaWduLXNlbGY6ZW5kOyI+CiAgICAgICAgICAgIDxidXR0b24gdHlwZT0iYnV0dG9uIiBpZD0iYnRuLWV4cG9ydC1tZCI+Lm1kIGV4cG9ydDwvYnV0dG9uPgogICAgICAgIDwvZGl2PgogICAgPC9mb3JtPgoKICAgIDx0YWJsZT4KICAgICAgICA8dGhlYWQ+CiAgICAgICAgICAgIDx0cj4KICAgICAgICAgICAgICAgIDx0aCBzdHlsZT0idGV4dC1hbGlnbjpsZWZ0OyI+VU5FPC90aD4KICAgICAgICAgICAgICAgIDx0aCBzdHlsZT0idGV4dC1hbGlnbjpjZW50ZXI7Ij5QZXJpb2RvPC90aD4KICAgICAgICAgICAgICAgIDx0aCBzdHlsZT0idGV4dC1hbGlnbjpjZW50ZXI7Ij5NZXRhIHZlbnRhIGNydXphZGE8L3RoPgogICAgICAgICAgICAgICAgPHRoIHN0eWxlPSJ0ZXh0LWFsaWduOmNlbnRlcjsiPlZlbnRhIGNydXphZGEgcmVhbDwvdGg+CiAgICAgICAgICAgICAgICA8dGggc3R5bGU9InRleHQtYWxpZ246Y2VudGVyOyI+Q3VtcGxlPC90aD4KICAgICAgICAgICAgICAgIDx0aCBzdHlsZT0idGV4dC1hbGlnbjpjZW50ZXI7Ij5QdW50b3MgYXNpZ25hZG9zPC90aD4KICAgICAgICAgICAgICAgIDx0aCBzdHlsZT0idGV4dC1hbGlnbjpjZW50ZXI7Ij5Ub3RhbCBkZWwgbWVzPC90aD4KICAgICAgICAgICAgPC90cj4KICAgICAgICA8L3RoZWFkPgoKICAgICAgICA8dGJvZHk+CiAgICAgICAgICB7JSBmb3Igcm93IGluIHJvd3MgJX0KICAgICAgICAgIHslIGlmIHJvdy5pc19zZXBhcmF0b3IgJX0KICAgICAgICAgIDx0ciBjbGFzcz0iZ3JvdXBfc2VwYXJhdG9yIj4KICAgICAgICAgICAgPHRkIGNvbHNwYW49IjciPjwvdGQ+CiAgICAgICAgICA8L3RyPgogICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgPHRyPgogICAgICAgICAgICA8dGQgc3R5bGU9InRleHQtYWxpZ246bGVmdDsiPnt7IHJvdy50YXJnZXQudW5lLm5hbWVfZXMgfX08L3RkPgogICAgICAgICAgICA8dGQgc3R5bGU9InRleHQtYWxpZ246Y2VudGVyOyI+e3sgcm93LnRhcmdldC55ZWFyIH19LXt7IHJvdy50YXJnZXQubW9udGh8c3RyaW5nZm9ybWF0OiIwMmQiIH19PC90ZD4KICAgICAgICAgICAgPHRkIHN0eWxlPSJ0ZXh0LWFsaWduOmNlbnRlcjsiPgogICAgICAgICAgICAgIHslIGlmIHJvdy50YXJnZXQudGFyZ2V0X3ZhbHVlICV9CiAgICAgICAgICAgICAge3sgcm93LnRhcmdldC50YXJnZXRfdmFsdWV8ZmxvYXRmb3JtYXQ6MHx1bmxvY2FsaXplIH19CiAgICAgICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgICAgIOKAlAogICAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgIDwvdGQ+CiAgICAgICAgICAgIDx0ZCBzdHlsZT0idGV4dC1hbGlnbjpjZW50ZXI7Ij4KICAgICAgICAgICAgICB7JSBpZiByb3cucmVzdWx0IGFuZCByb3cucmVzdWx0Lm1lYXN1cmVkX3ZhbHVlICE9IE5vbmUgJX0KICAgICAgICAgICAgICB7eyByb3cucmVzdWx0Lm1lYXN1cmVkX3ZhbHVlfGZsb2F0Zm9ybWF0OjB8dW5sb2NhbGl6ZSB9fQogICAgICAgICAgICAgIHslIGVsc2UgJX0KICAgICAgICAgICAgICDigJQKICAgICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgICA8L3RkPgogICAgICAgICAgICA8dGQgc3R5bGU9InRleHQtYWxpZ246Y2VudGVyOyI+CiAgICAgICAgICAgICAgeyUgaWYgcm93LnJlc3VsdCBhbmQgcm93LnJlc3VsdC5pc19hY2hpZXZlZCAlfQogICAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJvayI+U8OtPC9zcGFuPgogICAgICAgICAgICAgIHslIGVsc2UgJX0KICAgICAgICAgICAgICA8c3BhbiBjbGFzcz0iYmFkIj5Obzwvc3Bhbj4KICAgICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgICA8L3RkPgogICAgICAgICAgICA8dGQgc3R5bGU9InRleHQtYWxpZ246Y2VudGVyOyI+CiAgICAgICAgICAgICAgeyUgaWYgcm93LnJlc3VsdCAlfQogICAgICAgICAgICAgIHt7IHJvdy5yZXN1bHQucG9pbnRzX2F3YXJkZWQgfX0KICAgICAgICAgICAgICB7JSBlbHNlICV9CiAgICAgICAgICAgICAgMAogICAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgIDwvdGQ+CiAgICAgICAgICAgIDx0ZCBzdHlsZT0idGV4dC1hbGlnbjpjZW50ZXI7Ij4KICAgICAgICAgICAgICB7JSBpZiByb3cuc2NvcmVjYXJkICV9CiAgICAgICAgICAgICAge3sgcm93LnNjb3JlY2FyZC50b3RhbF9wb2ludHMgfX0KICAgICAgICAgICAgICB7JSBlbHNlICV9CiAgICAgICAgICAgICAgMAogICAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgIDwvdGQ+CiAgICAgICAgICA8L3RyPgogICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgICA8dHI+CiAgICAgICAgICAgIDx0ZCBjb2xzcGFuPSI3IiBzdHlsZT0idGV4dC1hbGlnbjpjZW50ZXI7Ij5ObyBoYXkgZGF0b3MgZGUgdmVudGEgY3J1emFkYSBwYXJhIGxvcyBmaWx0cm9zIHNlbGVjY2lvbmFkb3MuPC90ZD4KICAgICAgICAgIDwvdHI+CiAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICA8L3Rib2R5PgogICAgICAgICAgCiAgICA8L3RhYmxlPgo8L2Rpdj4KCjxzY3JpcHQ+CmRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoIkRPTUNvbnRlbnRMb2FkZWQiLCBmdW5jdGlvbiAoKSB7CiAgICBjb25zdCBzdGFydFBlcmlvZCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJzdGFydF9wZXJpb2QiKTsKICAgIGNvbnN0IHN0YXJ0WWVhciA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJzdGFydF95ZWFyIik7CiAgICBjb25zdCBzdGFydE1vbnRoID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoInN0YXJ0X21vbnRoIik7CiAgICBjb25zdCBzb3J0ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoInNvcnQiKTsKICAgIGNvbnN0IGRhdGVPcmRlciA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJkYXRlX29yZGVyIik7CiAgICBjb25zdCBncm91cE1vZGUgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiZ3JvdXBfbW9kZSIpOwogICAgY29uc3QgYnRuID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImJ0bi1leHBvcnQtbWQiKTsKCiAgICBmdW5jdGlvbiBzeW5jUGVyaW9kRmllbGRzKCkgewogICAgICAgIGlmICghc3RhcnRQZXJpb2QpIHJldHVybjsKICAgICAgICBjb25zdCBvcHRpb24gPSBzdGFydFBlcmlvZC5vcHRpb25zW3N0YXJ0UGVyaW9kLnNlbGVjdGVkSW5kZXhdOwogICAgICAgIGlmICghb3B0aW9uKSByZXR1cm47CiAgICAgICAgc3RhcnRZZWFyLnZhbHVlID0gb3B0aW9uLmRhdGFzZXQueWVhciB8fCAiIjsKICAgICAgICBzdGFydE1vbnRoLnZhbHVlID0gb3B0aW9uLmRhdGFzZXQubW9udGggfHwgIiI7CiAgICB9CgogICAgZnVuY3Rpb24gc3luY1NvcnRGaWVsZHMoKSB7CiAgICAgICAgaWYgKCFzb3J0KSByZXR1cm47CiAgICAgICAgaWYgKHNvcnQudmFsdWUgPT09ICJ1bmVzIikgewogICAgICAgICAgICBncm91cE1vZGUudmFsdWUgPSAidW5lIjsKICAgICAgICAgICAgZGF0ZU9yZGVyLnZhbHVlID0gImFzYyI7CiAgICAgICAgfSBlbHNlIGlmIChzb3J0LnZhbHVlID09PSAiZmVjaGFzX2Rlc2MiKSB7CiAgICAgICAgICAgIGdyb3VwTW9kZS52YWx1ZSA9ICJwZXJpb2QiOwogICAgICAgICAgICBkYXRlT3JkZXIudmFsdWUgPSAiZGVzYyI7CiAgICAgICAgfSBlbHNlIHsKICAgICAgICAgICAgZ3JvdXBNb2RlLnZhbHVlID0gInBlcmlvZCI7CiAgICAgICAgICAgIGRhdGVPcmRlci52YWx1ZSA9ICJhc2MiOwogICAgICAgIH0KICAgIH0KCgogICAgY29uc3QgZmlsdGVyRm9ybSA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoImZvcm0uZmlsdGVycyIpOwogICAgZnVuY3Rpb24gYXBwbHlGaWx0ZXJzKCkgewogICAgICAgIGlmICh0eXBlb2Ygc3luY1BlcmlvZEZpZWxkcyA9PT0gImZ1bmN0aW9uIikgc3luY1BlcmlvZEZpZWxkcygpOwogICAgICAgIGlmICh0eXBlb2Ygc3luY1NvcnRGaWVsZHMgPT09ICJmdW5jdGlvbiIpIHN5bmNTb3J0RmllbGRzKCk7CiAgICAgICAgaWYgKGZpbHRlckZvcm0pIGZpbHRlckZvcm0uc3VibWl0KCk7CiAgICB9CgogICAgaWYgKHN0YXJ0UGVyaW9kKSB7CiAgICAgICAgc3RhcnRQZXJpb2QuYWRkRXZlbnRMaXN0ZW5lcigiY2hhbmdlIiwgYXBwbHlGaWx0ZXJzKTsKICAgICAgICBzeW5jUGVyaW9kRmllbGRzKCk7CiAgICB9CgogICAgaWYgKHNvcnQpIHsKICAgICAgICBzb3J0LmFkZEV2ZW50TGlzdGVuZXIoImNoYW5nZSIsIGFwcGx5RmlsdGVycyk7CiAgICAgICAgc3luY1NvcnRGaWVsZHMoKTsKICAgIH0KCiAgICBbIm1vbnRoX2NvdW50IiwgIm1vZGUiLCAic3RhcnRfeWVhciIsICJzdGFydF9tb250aCIsICJ5ZWFyIiwgIm1vbnRoIiwgInVuZSJdLmZvckVhY2goZnVuY3Rpb24gKGlkKSB7CiAgICAgICAgY29uc3QgZWwgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZChpZCk7CiAgICAgICAgaWYgKGVsICYmIGVsLnRhZ05hbWUgPT09ICJTRUxFQ1QiKSB7CiAgICAgICAgICAgIGVsLmFkZEV2ZW50TGlzdGVuZXIoImNoYW5nZSIsIGFwcGx5RmlsdGVycyk7CiAgICAgICAgfQogICAgfSk7CgogICAgaWYgKCFidG4pIHJldHVybjsKCiAgICBidG4uYWRkRXZlbnRMaXN0ZW5lcigiY2xpY2siLCBhc3luYyBmdW5jdGlvbiAoKSB7CiAgICAgICAgc3luY1BlcmlvZEZpZWxkcygpOwogICAgICAgIHN5bmNTb3J0RmllbGRzKCk7CgogICAgICAgIGNvbnN0IHBhcmFtcyA9IG5ldyBVUkxTZWFyY2hQYXJhbXMoewogICAgICAgICAgICBzdGFydF95ZWFyOiBzdGFydFllYXIudmFsdWUgfHwgIiIsCiAgICAgICAgICAgIHN0YXJ0X21vbnRoOiBzdGFydE1vbnRoLnZhbHVlIHx8ICIiLAogICAgICAgICAgICBtb250aF9jb3VudDogZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoIm1vbnRoX2NvdW50Iik/LnZhbHVlIHx8ICIiLAogICAgICAgICAgICBkYXRlX29yZGVyOiBkYXRlT3JkZXIudmFsdWUgfHwgImFzYyIsCiAgICAgICAgICAgIGdyb3VwX21vZGU6IGdyb3VwTW9kZS52YWx1ZSB8fCAidW5lIgogICAgICAgIH0pOwoKICAgICAgICBjb25zdCB1cmwgPSBgeyUgdXJsICdwZ2M6dmVudGFfY3J1emFkYV9leHBvcnRfbWQnICV9P2AgKyBwYXJhbXMudG9TdHJpbmcoKTsKCiAgICAgICAgYnRuLmRpc2FibGVkID0gdHJ1ZTsKICAgICAgICBjb25zdCBvcmlnaW5hbFRleHQgPSBidG4udGV4dENvbnRlbnQ7CiAgICAgICAgYnRuLnRleHRDb250ZW50ID0gIkdlbmVyYW5kby4uLiI7CgogICAgICAgIHRyeSB7CiAgICAgICAgICAgIGNvbnN0IHJlc3BvbnNlID0gYXdhaXQgZmV0Y2godXJsLCB7CiAgICAgICAgICAgICAgICBtZXRob2Q6ICJHRVQiLAogICAgICAgICAgICAgICAgaGVhZGVyczogewogICAgICAgICAgICAgICAgICAgICJYLVJlcXVlc3RlZC1XaXRoIjogIlhNTEh0dHBSZXF1ZXN0IgogICAgICAgICAgICAgICAgfQogICAgICAgICAgICB9KTsKCiAgICAgICAgICAgIGlmICghcmVzcG9uc2Uub2spIHsKICAgICAgICAgICAgICAgIHRocm93IG5ldyBFcnJvcigiTm8gc2UgcHVkbyBnZW5lcmFyIGVsIGFyY2hpdm8gTWFya2Rvd24uIik7CiAgICAgICAgICAgIH0KCiAgICAgICAgICAgIGNvbnN0IGJsb2IgPSBhd2FpdCByZXNwb25zZS5ibG9iKCk7CgogICAgICAgICAgICBsZXQgZmlsZW5hbWUgPSAicGdjLXZlbnRhLWNydXphZGEubWQiOwogICAgICAgICAgICBjb25zdCBkaXNwb3NpdGlvbiA9IHJlc3BvbnNlLmhlYWRlcnMuZ2V0KCJDb250ZW50LURpc3Bvc2l0aW9uIik7CiAgICAgICAgICAgIGlmIChkaXNwb3NpdGlvbikgewogICAgICAgICAgICAgICAgY29uc3QgdXRmOE1hdGNoID0gZGlzcG9zaXRpb24ubWF0Y2goL2ZpbGVuYW1lXCo9VVRGLTgnJyhbXjtdKykvaSk7CiAgICAgICAgICAgICAgICBjb25zdCBhc2NpaU1hdGNoID0gZGlzcG9zaXRpb24ubWF0Y2goL2ZpbGVuYW1lPSIoW14iXSspIi9pKTsKCiAgICAgICAgICAgICAgICBpZiAodXRmOE1hdGNoICYmIHV0ZjhNYXRjaFsxXSkgewogICAgICAgICAgICAgICAgICAgIGZpbGVuYW1lID0gZGVjb2RlVVJJQ29tcG9uZW50KHV0ZjhNYXRjaFsxXSk7CiAgICAgICAgICAgICAgICB9IGVsc2UgaWYgKGFzY2lpTWF0Y2ggJiYgYXNjaWlNYXRjaFsxXSkgewogICAgICAgICAgICAgICAgICAgIGZpbGVuYW1lID0gYXNjaWlNYXRjaFsxXTsKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgfQoKICAgICAgICAgICAgY29uc3Qgb2JqZWN0VXJsID0gd2luZG93LlVSTC5jcmVhdGVPYmplY3RVUkwoYmxvYik7CiAgICAgICAgICAgIGNvbnN0IGEgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCJhIik7CiAgICAgICAgICAgIGEuaHJlZiA9IG9iamVjdFVybDsKICAgICAgICAgICAgYS5kb3dubG9hZCA9IGZpbGVuYW1lOwogICAgICAgICAgICBkb2N1bWVudC5ib2R5LmFwcGVuZENoaWxkKGEpOwogICAgICAgICAgICBhLmNsaWNrKCk7CiAgICAgICAgICAgIGEucmVtb3ZlKCk7CiAgICAgICAgICAgIHdpbmRvdy5VUkwucmV2b2tlT2JqZWN0VVJMKG9iamVjdFVybCk7CiAgICAgICAgfSBjYXRjaCAoZXJyb3IpIHsKICAgICAgICAgICAgYWxlcnQoZXJyb3IubWVzc2FnZSB8fCAiRXJyb3IgZ2VuZXJhbmRvIGxhIGV4cG9ydGFjacOzbi4iKTsKICAgICAgICB9IGZpbmFsbHkgewogICAgICAgICAgICBidG4uZGlzYWJsZWQgPSBmYWxzZTsKICAgICAgICAgICAgYnRuLnRleHRDb250ZW50ID0gb3JpZ2luYWxUZXh0OwogICAgICAgIH0KICAgIH0pOwp9KTsKPC9zY3JpcHQ+CnslIGVuZGJsb2NrICV9
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgc/venta_cruzada_detail.html
PATH_JSON="templates/pgc/venta_cruzada_detail.html"
FILENAME=venta_cruzada_detail.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=84
SIZE_BYTES_UTF8=2877
CONTENT_SHA256=fcbc598d725df7699249fa6ab9238830d12fec64edf72be85ad69d40d06ab377
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
{% block title %}Detalle venta cruzada
<script>
document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form.filters");
    if (!form) return;
    form.querySelectorAll("select").forEach(function (sel) {
        sel.addEventListener("change", function () { form.submit(); });
    });
});
</script>

{% endblock %}

{% block content %}
<div class="card">
    <h2>Detalle de venta cruzada</h2>

    <form method="get" class="filters">
        <div>
            <label for="year">Año</label><br>
            <select name="year" id="year">
                <option value="">Todos</option>
                {% for y in available_years %}
                    <option value="{{ y }}" {% if selected_year == y|stringformat:"s" %}selected{% endif %}>{{ y }}</option>
                {% endfor %}
            </select>
        </div>

        <div>
            <label for="month">Mes</label><br>
            <select name="month" id="month">
                <option value="">Todos</option>
                {% for m in months %}
                    <option value="{{ m }}" {% if selected_month == m|stringformat:"s" %}selected{% endif %}>{{ m }}</option>
                {% endfor %}
            </select>
        </div>

        <div>
            <label for="une">UNE origen</label><br>
            <select name="une" id="une">
                <option value="">Todas</option>
                {% for item in unes %}
                    <option value="{{ item.code }}" {% if selected_une == item.code %}selected{% endif %}>{{ item.name_es }}</option>
                {% endfor %}
            </select>
        </div>

    </form>

    <table>
        <thead>
            <tr>
                <th>Periodo</th>
                <th>UNE origen</th>
                <th>UNE destino</th>
                <th>Cliente</th>
                <th>Operación</th>
                <th>Fecha</th>
                <th>Moneda</th>
            </tr>
        </thead>
        <tbody>
            {% for row in rows %}
            <tr>
                <td>{{ row.year }}-{{ row.month|stringformat:"02d" }}</td>
                <td>{{ row.une_origin.name_es|default:row.raw_une_origin }}</td>
                <td>{{ row.une_destination.name_es|default:row.raw_une_destination }}</td>
                <td>{{ row.client_name|default:"—" }}</td>
                <td>{{ row.operation_code|default:"—" }}</td>
                <td>{{ row.date|default:"—" }}</td>
                <td>{% if row.currency %}{{ row.currency.code }}{% else %}—{% endif %}</td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="7" style="text-align:center;">No hay detalles de venta cruzada para los filtros seleccionados.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}


~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base.html" %}
00002|{% block title %}Detalle venta cruzada
00003|<script>
00004|document.addEventListener("DOMContentLoaded", function () {
00005|    const form = document.querySelector("form.filters");
00006|    if (!form) return;
00007|    form.querySelectorAll("select").forEach(function (sel) {
00008|        sel.addEventListener("change", function () { form.submit(); });
00009|    });
00010|});
00011|</script>
00012|
00013|{% endblock %}
00014|
00015|{% block content %}
00016|<div class="card">
00017|    <h2>Detalle de venta cruzada</h2>
00018|
00019|    <form method="get" class="filters">
00020|        <div>
00021|            <label for="year">Año</label><br>
00022|            <select name="year" id="year">
00023|                <option value="">Todos</option>
00024|                {% for y in available_years %}
00025|                    <option value="{{ y }}" {% if selected_year == y|stringformat:"s" %}selected{% endif %}>{{ y }}</option>
00026|                {% endfor %}
00027|            </select>
00028|        </div>
00029|
00030|        <div>
00031|            <label for="month">Mes</label><br>
00032|            <select name="month" id="month">
00033|                <option value="">Todos</option>
00034|                {% for m in months %}
00035|                    <option value="{{ m }}" {% if selected_month == m|stringformat:"s" %}selected{% endif %}>{{ m }}</option>
00036|                {% endfor %}
00037|            </select>
00038|        </div>
00039|
00040|        <div>
00041|            <label for="une">UNE origen</label><br>
00042|            <select name="une" id="une">
00043|                <option value="">Todas</option>
00044|                {% for item in unes %}
00045|                    <option value="{{ item.code }}" {% if selected_une == item.code %}selected{% endif %}>{{ item.name_es }}</option>
00046|                {% endfor %}
00047|            </select>
00048|        </div>
00049|
00050|    </form>
00051|
00052|    <table>
00053|        <thead>
00054|            <tr>
00055|                <th>Periodo</th>
00056|                <th>UNE origen</th>
00057|                <th>UNE destino</th>
00058|                <th>Cliente</th>
00059|                <th>Operación</th>
00060|                <th>Fecha</th>
00061|                <th>Moneda</th>
00062|            </tr>
00063|        </thead>
00064|        <tbody>
00065|            {% for row in rows %}
00066|            <tr>
00067|                <td>{{ row.year }}-{{ row.month|stringformat:"02d" }}</td>
00068|                <td>{{ row.une_origin.name_es|default:row.raw_une_origin }}</td>
00069|                <td>{{ row.une_destination.name_es|default:row.raw_une_destination }}</td>
00070|                <td>{{ row.client_name|default:"—" }}</td>
00071|                <td>{{ row.operation_code|default:"—" }}</td>
00072|                <td>{{ row.date|default:"—" }}</td>
00073|                <td>{% if row.currency %}{{ row.currency.code }}{% else %}—{% endif %}</td>
00074|            </tr>
00075|            {% empty %}
00076|            <tr>
00077|                <td colspan="7" style="text-align:center;">No hay detalles de venta cruzada para los filtros seleccionados.</td>
00078|            </tr>
00079|            {% endfor %}
00080|        </tbody>
00081|    </table>
00082|</div>
00083|{% endblock %}
00084|

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZS5odG1sIiAlfQp7JSBibG9jayB0aXRsZSAlfURldGFsbGUgdmVudGEgY3J1emFkYQo8c2NyaXB0Pgpkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCJET01Db250ZW50TG9hZGVkIiwgZnVuY3Rpb24gKCkgewogICAgY29uc3QgZm9ybSA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoImZvcm0uZmlsdGVycyIpOwogICAgaWYgKCFmb3JtKSByZXR1cm47CiAgICBmb3JtLnF1ZXJ5U2VsZWN0b3JBbGwoInNlbGVjdCIpLmZvckVhY2goZnVuY3Rpb24gKHNlbCkgewogICAgICAgIHNlbC5hZGRFdmVudExpc3RlbmVyKCJjaGFuZ2UiLCBmdW5jdGlvbiAoKSB7IGZvcm0uc3VibWl0KCk7IH0pOwogICAgfSk7Cn0pOwo8L3NjcmlwdD4KCnslIGVuZGJsb2NrICV9Cgp7JSBibG9jayBjb250ZW50ICV9CjxkaXYgY2xhc3M9ImNhcmQiPgogICAgPGgyPkRldGFsbGUgZGUgdmVudGEgY3J1emFkYTwvaDI+CgogICAgPGZvcm0gbWV0aG9kPSJnZXQiIGNsYXNzPSJmaWx0ZXJzIj4KICAgICAgICA8ZGl2PgogICAgICAgICAgICA8bGFiZWwgZm9yPSJ5ZWFyIj5Bw7FvPC9sYWJlbD48YnI+CiAgICAgICAgICAgIDxzZWxlY3QgbmFtZT0ieWVhciIgaWQ9InllYXIiPgogICAgICAgICAgICAgICAgPG9wdGlvbiB2YWx1ZT0iIj5Ub2Rvczwvb3B0aW9uPgogICAgICAgICAgICAgICAgeyUgZm9yIHkgaW4gYXZhaWxhYmxlX3llYXJzICV9CiAgICAgICAgICAgICAgICAgICAgPG9wdGlvbiB2YWx1ZT0ie3sgeSB9fSIgeyUgaWYgc2VsZWN0ZWRfeWVhciA9PSB5fHN0cmluZ2Zvcm1hdDoicyIgJX1zZWxlY3RlZHslIGVuZGlmICV9Pnt7IHkgfX08L29wdGlvbj4KICAgICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICA8L3NlbGVjdD4KICAgICAgICA8L2Rpdj4KCiAgICAgICAgPGRpdj4KICAgICAgICAgICAgPGxhYmVsIGZvcj0ibW9udGgiPk1lczwvbGFiZWw+PGJyPgogICAgICAgICAgICA8c2VsZWN0IG5hbWU9Im1vbnRoIiBpZD0ibW9udGgiPgogICAgICAgICAgICAgICAgPG9wdGlvbiB2YWx1ZT0iIj5Ub2Rvczwvb3B0aW9uPgogICAgICAgICAgICAgICAgeyUgZm9yIG0gaW4gbW9udGhzICV9CiAgICAgICAgICAgICAgICAgICAgPG9wdGlvbiB2YWx1ZT0ie3sgbSB9fSIgeyUgaWYgc2VsZWN0ZWRfbW9udGggPT0gbXxzdHJpbmdmb3JtYXQ6InMiICV9c2VsZWN0ZWR7JSBlbmRpZiAlfT57eyBtIH19PC9vcHRpb24+CiAgICAgICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgICAgPC9zZWxlY3Q+CiAgICAgICAgPC9kaXY+CgogICAgICAgIDxkaXY+CiAgICAgICAgICAgIDxsYWJlbCBmb3I9InVuZSI+VU5FIG9yaWdlbjwvbGFiZWw+PGJyPgogICAgICAgICAgICA8c2VsZWN0IG5hbWU9InVuZSIgaWQ9InVuZSI+CiAgICAgICAgICAgICAgICA8b3B0aW9uIHZhbHVlPSIiPlRvZGFzPC9vcHRpb24+CiAgICAgICAgICAgICAgICB7JSBmb3IgaXRlbSBpbiB1bmVzICV9CiAgICAgICAgICAgICAgICAgICAgPG9wdGlvbiB2YWx1ZT0ie3sgaXRlbS5jb2RlIH19IiB7JSBpZiBzZWxlY3RlZF91bmUgPT0gaXRlbS5jb2RlICV9c2VsZWN0ZWR7JSBlbmRpZiAlfT57eyBpdGVtLm5hbWVfZXMgfX08L29wdGlvbj4KICAgICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICA8L3NlbGVjdD4KICAgICAgICA8L2Rpdj4KCiAgICA8L2Zvcm0+CgogICAgPHRhYmxlPgogICAgICAgIDx0aGVhZD4KICAgICAgICAgICAgPHRyPgogICAgICAgICAgICAgICAgPHRoPlBlcmlvZG88L3RoPgogICAgICAgICAgICAgICAgPHRoPlVORSBvcmlnZW48L3RoPgogICAgICAgICAgICAgICAgPHRoPlVORSBkZXN0aW5vPC90aD4KICAgICAgICAgICAgICAgIDx0aD5DbGllbnRlPC90aD4KICAgICAgICAgICAgICAgIDx0aD5PcGVyYWNpw7NuPC90aD4KICAgICAgICAgICAgICAgIDx0aD5GZWNoYTwvdGg+CiAgICAgICAgICAgICAgICA8dGg+TW9uZWRhPC90aD4KICAgICAgICAgICAgPC90cj4KICAgICAgICA8L3RoZWFkPgogICAgICAgIDx0Ym9keT4KICAgICAgICAgICAgeyUgZm9yIHJvdyBpbiByb3dzICV9CiAgICAgICAgICAgIDx0cj4KICAgICAgICAgICAgICAgIDx0ZD57eyByb3cueWVhciB9fS17eyByb3cubW9udGh8c3RyaW5nZm9ybWF0OiIwMmQiIH19PC90ZD4KICAgICAgICAgICAgICAgIDx0ZD57eyByb3cudW5lX29yaWdpbi5uYW1lX2VzfGRlZmF1bHQ6cm93LnJhd191bmVfb3JpZ2luIH19PC90ZD4KICAgICAgICAgICAgICAgIDx0ZD57eyByb3cudW5lX2Rlc3RpbmF0aW9uLm5hbWVfZXN8ZGVmYXVsdDpyb3cucmF3X3VuZV9kZXN0aW5hdGlvbiB9fTwvdGQ+CiAgICAgICAgICAgICAgICA8dGQ+e3sgcm93LmNsaWVudF9uYW1lfGRlZmF1bHQ6IuKAlCIgfX08L3RkPgogICAgICAgICAgICAgICAgPHRkPnt7IHJvdy5vcGVyYXRpb25fY29kZXxkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgICAgICAgIDx0ZD57eyByb3cuZGF0ZXxkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgICAgICAgIDx0ZD57JSBpZiByb3cuY3VycmVuY3kgJX17eyByb3cuY3VycmVuY3kuY29kZSB9fXslIGVsc2UgJX3igJR7JSBlbmRpZiAlfTwvdGQ+CiAgICAgICAgICAgIDwvdHI+CiAgICAgICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgICAgIDx0cj4KICAgICAgICAgICAgICAgIDx0ZCBjb2xzcGFuPSI3IiBzdHlsZT0idGV4dC1hbGlnbjpjZW50ZXI7Ij5ObyBoYXkgZGV0YWxsZXMgZGUgdmVudGEgY3J1emFkYSBwYXJhIGxvcyBmaWx0cm9zIHNlbGVjY2lvbmFkb3MuPC90ZD4KICAgICAgICAgICAgPC90cj4KICAgICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgPC90Ym9keT4KICAgIDwvdGFibGU+CjwvZGl2Pgp7JSBlbmRibG9jayAlfQoK
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgo/pgodashboard.html
PATH_JSON="templates/pgo/pgodashboard.html"
FILENAME=pgodashboard.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=155
SIZE_BYTES_UTF8=6121
CONTENT_SHA256=ee09b004d8c92d7dba26b687e53357365046b01755a2d0f88576538e9d8eda4e
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
{% extends "base_wcg.html" %}
{% block title %}PGO — WCG{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-2 mt-2">
  <div class="wcg-report-head">
    <h1 class="h4 fw-semibold mb-0">PGO — Operación y tickets</h1>
    {% include "includes/module_mark.html" with module="pgo" %}
  </div>
  <div class="d-flex gap-1 flex-wrap">
    <a href="{% url 'pgo:export_tickets' %}" class="btn btn-sm btn-outline-primary">Exportar CSV</a>
    <a href="{% url 'pgo:ticket_list' %}" class="btn btn-sm btn-outline-primary">Ver todos</a>
    <a href="{% url 'pgo:resultados' %}" class="btn btn-sm btn-outline-secondary">Resultados</a>
  </div>
</div>

<div class="row g-2 mb-3">
  <div class="col-md-2 col-6">
    <div class="card border-0 shadow-sm text-center"><div class="card-body py-2">
      <div class="stat-value" style="font-size:1.35rem;">{{ total_tickets }}</div><div class="text-muted small">Total</div>
    </div></div>
  </div>
  <div class="col-md-2 col-6">
    <div class="card border-0 shadow-sm text-center"><div class="card-body py-2">
      <div class="stat-value" style="font-size:1.35rem;">{{ tickets_abiertos }}</div><div class="text-muted small">Abiertos</div>
    </div></div>
  </div>
  <div class="col-md-2 col-6">
    <div class="card border-0 shadow-sm text-center"><div class="card-body py-2">
      <div class="stat-value" style="font-size:1.35rem;">{{ tickets_cerrados }}</div><div class="text-muted small">Cerrados</div>
    </div></div>
  </div>
  <div class="col-md-2 col-6">
    <div class="card border-0 shadow-sm text-center"><div class="card-body py-2">
      <div class="stat-value text-warning" style="font-size:1.35rem;">{{ tickets_vencidos }}</div><div class="text-muted small">SLA vencido</div>
    </div></div>
  </div>
  <div class="col-md-2 col-6">
    <div class="card border-0 shadow-sm text-center"><div class="card-body py-2">
      <div class="stat-value" style="font-size:1.35rem;">{% if tiempo_promedio %}{{ tiempo_promedio|floatformat:1 }}{% else %}—{% endif %}</div>
      <div class="text-muted small">Horas promedio</div>
    </div></div>
  </div>
</div>

<div class="row g-3 mb-4">
  <div class="col-md-4">
    <div class="card border-0 shadow-sm h-100">
      <div class="card-header bg-white fw-semibold small">Por estado</div>
      <ul class="list-group list-group-flush small">
        {% for row in por_estado %}
        <li class="list-group-item d-flex justify-content-between">
          <span>{{ row.estado }}</span>
          <span class="badge text-bg-secondary">{{ row.total }}</span>
        </li>
        {% empty %}
        <li class="list-group-item text-muted">Sin datos.</li>
        {% endfor %}
      </ul>
    </div>
  </div>
  <div class="col-md-4">
    <div class="card border-0 shadow-sm h-100">
      <div class="card-header bg-white fw-semibold small">Por prioridad</div>
      <ul class="list-group list-group-flush small">
        {% for row in por_prioridad %}
        <li class="list-group-item d-flex justify-content-between">
          <span>{{ row.prioridad }}</span>
          <span class="badge text-bg-secondary">{{ row.total }}</span>
        </li>
        {% empty %}
        <li class="list-group-item text-muted">Sin prioridades.</li>
        {% endfor %}
      </ul>
    </div>
  </div>
  <div class="col-md-4">
    <div class="card border-0 shadow-sm h-100">
      <div class="card-header bg-white fw-semibold small">Por unidad</div>
      <ul class="list-group list-group-flush small">
        {% for row in por_unidad %}
        <li class="list-group-item d-flex justify-content-between">
          <span>{{ row.unidad_negocio__nombre|default:"—" }}</span>
          <span class="badge text-bg-secondary">{{ row.total }}</span>
        </li>
        {% empty %}
        <li class="list-group-item text-muted">Sin datos.</li>
        {% endfor %}
      </ul>
    </div>
  </div>
</div>

{% if total_tickets == 0 %}
{% include "includes/empty_state.html" with title="Sin tickets PGO" message="Cargue el control de tickets desde Administración → Importación General." %}
{% endif %}

<div class="card border-0 shadow-sm mb-4">
  <div class="card-header bg-white fw-semibold">Tickets recientes</div>
  <div class="table-responsive">
    <table class="table table-hover table-wcg mb-0 small">
      <thead>
        <tr>
          <th>ID</th>
          <th>Título</th>
          <th>Estado</th>
          <th>Prioridad</th>
          <th>Unidad</th>
          <th>Apertura</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {% for ticket in tickets_recientes %}
        <tr>
          <td>{{ ticket.codigo }}</td>
          <td>{{ ticket.titulo|truncatechars:55 }}</td>
          <td>{{ ticket.get_estado_display }}</td>
          <td>{{ ticket.get_prioridad_display }}</td>
          <td>{{ ticket.unidad_negocio.nombre|default:"—" }}</td>
          <td>{{ ticket.fecha_apertura|date:"d/m/Y H:i" }}</td>
          <td class="text-end">
            <a href="{% url 'pgo:ticket_detail' ticket.codigo %}" class="btn btn-sm btn-outline-primary">Ver</a>
          </td>
        </tr>
        {% empty %}
        <tr><td colspan="7" class="text-center text-muted py-4">No hay tickets.</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>

{% if resultados %}
<div class="card border-0 shadow-sm">
  <div class="card-header bg-white fw-semibold">Resultados por período</div>
  <div class="table-responsive">
    <table class="table table-sm mb-0">
      <thead><tr><th>Período</th><th>Unidad</th><th>Cerrados</th><th>Abiertos</th><th>T. prom (h)</th><th>SLA %</th></tr></thead>
      <tbody>
        {% for r in resultados %}
        <tr>
          <td>{{ r.periodo }}</td>
          <td>{{ r.unidad_negocio.nombre }}</td>
          <td>{{ r.tickets_cerrados }}</td>
          <td>{{ r.tickets_abiertos }}</td>
          <td>{{ r.tiempo_promedio_horas }}</td>
          <td>{{ r.cumplimiento_sla_pct }}%</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endif %}
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}PGO — WCG{% endblock %}
00003|{% block content %}
00004|<div class="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-2 mt-2">
00005|  <div class="wcg-report-head">
00006|    <h1 class="h4 fw-semibold mb-0">PGO — Operación y tickets</h1>
00007|    {% include "includes/module_mark.html" with module="pgo" %}
00008|  </div>
00009|  <div class="d-flex gap-1 flex-wrap">
00010|    <a href="{% url 'pgo:export_tickets' %}" class="btn btn-sm btn-outline-primary">Exportar CSV</a>
00011|    <a href="{% url 'pgo:ticket_list' %}" class="btn btn-sm btn-outline-primary">Ver todos</a>
00012|    <a href="{% url 'pgo:resultados' %}" class="btn btn-sm btn-outline-secondary">Resultados</a>
00013|  </div>
00014|</div>
00015|
00016|<div class="row g-2 mb-3">
00017|  <div class="col-md-2 col-6">
00018|    <div class="card border-0 shadow-sm text-center"><div class="card-body py-2">
00019|      <div class="stat-value" style="font-size:1.35rem;">{{ total_tickets }}</div><div class="text-muted small">Total</div>
00020|    </div></div>
00021|  </div>
00022|  <div class="col-md-2 col-6">
00023|    <div class="card border-0 shadow-sm text-center"><div class="card-body py-2">
00024|      <div class="stat-value" style="font-size:1.35rem;">{{ tickets_abiertos }}</div><div class="text-muted small">Abiertos</div>
00025|    </div></div>
00026|  </div>
00027|  <div class="col-md-2 col-6">
00028|    <div class="card border-0 shadow-sm text-center"><div class="card-body py-2">
00029|      <div class="stat-value" style="font-size:1.35rem;">{{ tickets_cerrados }}</div><div class="text-muted small">Cerrados</div>
00030|    </div></div>
00031|  </div>
00032|  <div class="col-md-2 col-6">
00033|    <div class="card border-0 shadow-sm text-center"><div class="card-body py-2">
00034|      <div class="stat-value text-warning" style="font-size:1.35rem;">{{ tickets_vencidos }}</div><div class="text-muted small">SLA vencido</div>
00035|    </div></div>
00036|  </div>
00037|  <div class="col-md-2 col-6">
00038|    <div class="card border-0 shadow-sm text-center"><div class="card-body py-2">
00039|      <div class="stat-value" style="font-size:1.35rem;">{% if tiempo_promedio %}{{ tiempo_promedio|floatformat:1 }}{% else %}—{% endif %}</div>
00040|      <div class="text-muted small">Horas promedio</div>
00041|    </div></div>
00042|  </div>
00043|</div>
00044|
00045|<div class="row g-3 mb-4">
00046|  <div class="col-md-4">
00047|    <div class="card border-0 shadow-sm h-100">
00048|      <div class="card-header bg-white fw-semibold small">Por estado</div>
00049|      <ul class="list-group list-group-flush small">
00050|        {% for row in por_estado %}
00051|        <li class="list-group-item d-flex justify-content-between">
00052|          <span>{{ row.estado }}</span>
00053|          <span class="badge text-bg-secondary">{{ row.total }}</span>
00054|        </li>
00055|        {% empty %}
00056|        <li class="list-group-item text-muted">Sin datos.</li>
00057|        {% endfor %}
00058|      </ul>
00059|    </div>
00060|  </div>
00061|  <div class="col-md-4">
00062|    <div class="card border-0 shadow-sm h-100">
00063|      <div class="card-header bg-white fw-semibold small">Por prioridad</div>
00064|      <ul class="list-group list-group-flush small">
00065|        {% for row in por_prioridad %}
00066|        <li class="list-group-item d-flex justify-content-between">
00067|          <span>{{ row.prioridad }}</span>
00068|          <span class="badge text-bg-secondary">{{ row.total }}</span>
00069|        </li>
00070|        {% empty %}
00071|        <li class="list-group-item text-muted">Sin prioridades.</li>
00072|        {% endfor %}
00073|      </ul>
00074|    </div>
00075|  </div>
00076|  <div class="col-md-4">
00077|    <div class="card border-0 shadow-sm h-100">
00078|      <div class="card-header bg-white fw-semibold small">Por unidad</div>
00079|      <ul class="list-group list-group-flush small">
00080|        {% for row in por_unidad %}
00081|        <li class="list-group-item d-flex justify-content-between">
00082|          <span>{{ row.unidad_negocio__nombre|default:"—" }}</span>
00083|          <span class="badge text-bg-secondary">{{ row.total }}</span>
00084|        </li>
00085|        {% empty %}
00086|        <li class="list-group-item text-muted">Sin datos.</li>
00087|        {% endfor %}
00088|      </ul>
00089|    </div>
00090|  </div>
00091|</div>
00092|
00093|{% if total_tickets == 0 %}
00094|{% include "includes/empty_state.html" with title="Sin tickets PGO" message="Cargue el control de tickets desde Administración → Importación General." %}
00095|{% endif %}
00096|
00097|<div class="card border-0 shadow-sm mb-4">
00098|  <div class="card-header bg-white fw-semibold">Tickets recientes</div>
00099|  <div class="table-responsive">
00100|    <table class="table table-hover table-wcg mb-0 small">
00101|      <thead>
00102|        <tr>
00103|          <th>ID</th>
00104|          <th>Título</th>
00105|          <th>Estado</th>
00106|          <th>Prioridad</th>
00107|          <th>Unidad</th>
00108|          <th>Apertura</th>
00109|          <th></th>
00110|        </tr>
00111|      </thead>
00112|      <tbody>
00113|        {% for ticket in tickets_recientes %}
00114|        <tr>
00115|          <td>{{ ticket.codigo }}</td>
00116|          <td>{{ ticket.titulo|truncatechars:55 }}</td>
00117|          <td>{{ ticket.get_estado_display }}</td>
00118|          <td>{{ ticket.get_prioridad_display }}</td>
00119|          <td>{{ ticket.unidad_negocio.nombre|default:"—" }}</td>
00120|          <td>{{ ticket.fecha_apertura|date:"d/m/Y H:i" }}</td>
00121|          <td class="text-end">
00122|            <a href="{% url 'pgo:ticket_detail' ticket.codigo %}" class="btn btn-sm btn-outline-primary">Ver</a>
00123|          </td>
00124|        </tr>
00125|        {% empty %}
00126|        <tr><td colspan="7" class="text-center text-muted py-4">No hay tickets.</td></tr>
00127|        {% endfor %}
00128|      </tbody>
00129|    </table>
00130|  </div>
00131|</div>
00132|
00133|{% if resultados %}
00134|<div class="card border-0 shadow-sm">
00135|  <div class="card-header bg-white fw-semibold">Resultados por período</div>
00136|  <div class="table-responsive">
00137|    <table class="table table-sm mb-0">
00138|      <thead><tr><th>Período</th><th>Unidad</th><th>Cerrados</th><th>Abiertos</th><th>T. prom (h)</th><th>SLA %</th></tr></thead>
00139|      <tbody>
00140|        {% for r in resultados %}
00141|        <tr>
00142|          <td>{{ r.periodo }}</td>
00143|          <td>{{ r.unidad_negocio.nombre }}</td>
00144|          <td>{{ r.tickets_cerrados }}</td>
00145|          <td>{{ r.tickets_abiertos }}</td>
00146|          <td>{{ r.tiempo_promedio_horas }}</td>
00147|          <td>{{ r.cumplimiento_sla_pct }}%</td>
00148|        </tr>
00149|        {% endfor %}
00150|      </tbody>
00151|    </table>
00152|  </div>
00153|</div>
00154|{% endif %}
00155|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1QR08g4oCUIFdDR3slIGVuZGJsb2NrICV9CnslIGJsb2NrIGNvbnRlbnQgJX0KPGRpdiBjbGFzcz0iZC1mbGV4IGp1c3RpZnktY29udGVudC1iZXR3ZWVuIGFsaWduLWl0ZW1zLXN0YXJ0IG1iLTMgZmxleC13cmFwIGdhcC0yIG10LTIiPgogIDxkaXYgY2xhc3M9IndjZy1yZXBvcnQtaGVhZCI+CiAgICA8aDEgY2xhc3M9Img0IGZ3LXNlbWlib2xkIG1iLTAiPlBHTyDigJQgT3BlcmFjacOzbiB5IHRpY2tldHM8L2gxPgogICAgeyUgaW5jbHVkZSAiaW5jbHVkZXMvbW9kdWxlX21hcmsuaHRtbCIgd2l0aCBtb2R1bGU9InBnbyIgJX0KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJkLWZsZXggZ2FwLTEgZmxleC13cmFwIj4KICAgIDxhIGhyZWY9InslIHVybCAncGdvOmV4cG9ydF90aWNrZXRzJyAlfSIgY2xhc3M9ImJ0biBidG4tc20gYnRuLW91dGxpbmUtcHJpbWFyeSI+RXhwb3J0YXIgQ1NWPC9hPgogICAgPGEgaHJlZj0ieyUgdXJsICdwZ286dGlja2V0X2xpc3QnICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1wcmltYXJ5Ij5WZXIgdG9kb3M8L2E+CiAgICA8YSBocmVmPSJ7JSB1cmwgJ3BnbzpyZXN1bHRhZG9zJyAlfSIgY2xhc3M9ImJ0biBidG4tc20gYnRuLW91dGxpbmUtc2Vjb25kYXJ5Ij5SZXN1bHRhZG9zPC9hPgogIDwvZGl2Pgo8L2Rpdj4KCjxkaXYgY2xhc3M9InJvdyBnLTIgbWItMyI+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTIgY29sLTYiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20gdGV4dC1jZW50ZXIiPjxkaXYgY2xhc3M9ImNhcmQtYm9keSBweS0yIj4KICAgICAgPGRpdiBjbGFzcz0ic3RhdC12YWx1ZSIgc3R5bGU9ImZvbnQtc2l6ZToxLjM1cmVtOyI+e3sgdG90YWxfdGlja2V0cyB9fTwvZGl2PjxkaXYgY2xhc3M9InRleHQtbXV0ZWQgc21hbGwiPlRvdGFsPC9kaXY+CiAgICA8L2Rpdj48L2Rpdj4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtMiBjb2wtNiI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSB0ZXh0LWNlbnRlciI+PGRpdiBjbGFzcz0iY2FyZC1ib2R5IHB5LTIiPgogICAgICA8ZGl2IGNsYXNzPSJzdGF0LXZhbHVlIiBzdHlsZT0iZm9udC1zaXplOjEuMzVyZW07Ij57eyB0aWNrZXRzX2FiaWVydG9zIH19PC9kaXY+PGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+QWJpZXJ0b3M8L2Rpdj4KICAgIDwvZGl2PjwvZGl2PgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1tZC0yIGNvbC02Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIHRleHQtY2VudGVyIj48ZGl2IGNsYXNzPSJjYXJkLWJvZHkgcHktMiI+CiAgICAgIDxkaXYgY2xhc3M9InN0YXQtdmFsdWUiIHN0eWxlPSJmb250LXNpemU6MS4zNXJlbTsiPnt7IHRpY2tldHNfY2VycmFkb3MgfX08L2Rpdj48ZGl2IGNsYXNzPSJ0ZXh0LW11dGVkIHNtYWxsIj5DZXJyYWRvczwvZGl2PgogICAgPC9kaXY+PC9kaXY+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTIgY29sLTYiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20gdGV4dC1jZW50ZXIiPjxkaXYgY2xhc3M9ImNhcmQtYm9keSBweS0yIj4KICAgICAgPGRpdiBjbGFzcz0ic3RhdC12YWx1ZSB0ZXh0LXdhcm5pbmciIHN0eWxlPSJmb250LXNpemU6MS4zNXJlbTsiPnt7IHRpY2tldHNfdmVuY2lkb3MgfX08L2Rpdj48ZGl2IGNsYXNzPSJ0ZXh0LW11dGVkIHNtYWxsIj5TTEEgdmVuY2lkbzwvZGl2PgogICAgPC9kaXY+PC9kaXY+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTIgY29sLTYiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20gdGV4dC1jZW50ZXIiPjxkaXYgY2xhc3M9ImNhcmQtYm9keSBweS0yIj4KICAgICAgPGRpdiBjbGFzcz0ic3RhdC12YWx1ZSIgc3R5bGU9ImZvbnQtc2l6ZToxLjM1cmVtOyI+eyUgaWYgdGllbXBvX3Byb21lZGlvICV9e3sgdGllbXBvX3Byb21lZGlvfGZsb2F0Zm9ybWF0OjEgfX17JSBlbHNlICV94oCUeyUgZW5kaWYgJX08L2Rpdj4KICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+SG9yYXMgcHJvbWVkaW88L2Rpdj4KICAgIDwvZGl2PjwvZGl2PgogIDwvZGl2Pgo8L2Rpdj4KCjxkaXYgY2xhc3M9InJvdyBnLTMgbWItNCI+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTQiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20gaC0xMDAiPgogICAgICA8ZGl2IGNsYXNzPSJjYXJkLWhlYWRlciBiZy13aGl0ZSBmdy1zZW1pYm9sZCBzbWFsbCI+UG9yIGVzdGFkbzwvZGl2PgogICAgICA8dWwgY2xhc3M9Imxpc3QtZ3JvdXAgbGlzdC1ncm91cC1mbHVzaCBzbWFsbCI+CiAgICAgICAgeyUgZm9yIHJvdyBpbiBwb3JfZXN0YWRvICV9CiAgICAgICAgPGxpIGNsYXNzPSJsaXN0LWdyb3VwLWl0ZW0gZC1mbGV4IGp1c3RpZnktY29udGVudC1iZXR3ZWVuIj4KICAgICAgICAgIDxzcGFuPnt7IHJvdy5lc3RhZG8gfX08L3NwYW4+CiAgICAgICAgICA8c3BhbiBjbGFzcz0iYmFkZ2UgdGV4dC1iZy1zZWNvbmRhcnkiPnt7IHJvdy50b3RhbCB9fTwvc3Bhbj4KICAgICAgICA8L2xpPgogICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgPGxpIGNsYXNzPSJsaXN0LWdyb3VwLWl0ZW0gdGV4dC1tdXRlZCI+U2luIGRhdG9zLjwvbGk+CiAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgIDwvdWw+CiAgICA8L2Rpdj4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtNCI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSBoLTEwMCI+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtaGVhZGVyIGJnLXdoaXRlIGZ3LXNlbWlib2xkIHNtYWxsIj5Qb3IgcHJpb3JpZGFkPC9kaXY+CiAgICAgIDx1bCBjbGFzcz0ibGlzdC1ncm91cCBsaXN0LWdyb3VwLWZsdXNoIHNtYWxsIj4KICAgICAgICB7JSBmb3Igcm93IGluIHBvcl9wcmlvcmlkYWQgJX0KICAgICAgICA8bGkgY2xhc3M9Imxpc3QtZ3JvdXAtaXRlbSBkLWZsZXgganVzdGlmeS1jb250ZW50LWJldHdlZW4iPgogICAgICAgICAgPHNwYW4+e3sgcm93LnByaW9yaWRhZCB9fTwvc3Bhbj4KICAgICAgICAgIDxzcGFuIGNsYXNzPSJiYWRnZSB0ZXh0LWJnLXNlY29uZGFyeSI+e3sgcm93LnRvdGFsIH19PC9zcGFuPgogICAgICAgIDwvbGk+CiAgICAgICAgeyUgZW1wdHkgJX0KICAgICAgICA8bGkgY2xhc3M9Imxpc3QtZ3JvdXAtaXRlbSB0ZXh0LW11dGVkIj5TaW4gcHJpb3JpZGFkZXMuPC9saT4KICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgPC91bD4KICAgIDwvZGl2PgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1tZC00Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIGgtMTAwIj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIgYmctd2hpdGUgZnctc2VtaWJvbGQgc21hbGwiPlBvciB1bmlkYWQ8L2Rpdj4KICAgICAgPHVsIGNsYXNzPSJsaXN0LWdyb3VwIGxpc3QtZ3JvdXAtZmx1c2ggc21hbGwiPgogICAgICAgIHslIGZvciByb3cgaW4gcG9yX3VuaWRhZCAlfQogICAgICAgIDxsaSBjbGFzcz0ibGlzdC1ncm91cC1pdGVtIGQtZmxleCBqdXN0aWZ5LWNvbnRlbnQtYmV0d2VlbiI+CiAgICAgICAgICA8c3Bhbj57eyByb3cudW5pZGFkX25lZ29jaW9fX25vbWJyZXxkZWZhdWx0OiLigJQiIH19PC9zcGFuPgogICAgICAgICAgPHNwYW4gY2xhc3M9ImJhZGdlIHRleHQtYmctc2Vjb25kYXJ5Ij57eyByb3cudG90YWwgfX08L3NwYW4+CiAgICAgICAgPC9saT4KICAgICAgICB7JSBlbXB0eSAlfQogICAgICAgIDxsaSBjbGFzcz0ibGlzdC1ncm91cC1pdGVtIHRleHQtbXV0ZWQiPlNpbiBkYXRvcy48L2xpPgogICAgICAgIHslIGVuZGZvciAlfQogICAgICA8L3VsPgogICAgPC9kaXY+CiAgPC9kaXY+CjwvZGl2PgoKeyUgaWYgdG90YWxfdGlja2V0cyA9PSAwICV9CnslIGluY2x1ZGUgImluY2x1ZGVzL2VtcHR5X3N0YXRlLmh0bWwiIHdpdGggdGl0bGU9IlNpbiB0aWNrZXRzIFBHTyIgbWVzc2FnZT0iQ2FyZ3VlIGVsIGNvbnRyb2wgZGUgdGlja2V0cyBkZXNkZSBBZG1pbmlzdHJhY2nDs24g4oaSIEltcG9ydGFjacOzbiBHZW5lcmFsLiIgJX0KeyUgZW5kaWYgJX0KCjxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIG1iLTQiPgogIDxkaXYgY2xhc3M9ImNhcmQtaGVhZGVyIGJnLXdoaXRlIGZ3LXNlbWlib2xkIj5UaWNrZXRzIHJlY2llbnRlczwvZGl2PgogIDxkaXYgY2xhc3M9InRhYmxlLXJlc3BvbnNpdmUiPgogICAgPHRhYmxlIGNsYXNzPSJ0YWJsZSB0YWJsZS1ob3ZlciB0YWJsZS13Y2cgbWItMCBzbWFsbCI+CiAgICAgIDx0aGVhZD4KICAgICAgICA8dHI+CiAgICAgICAgICA8dGg+SUQ8L3RoPgogICAgICAgICAgPHRoPlTDrXR1bG88L3RoPgogICAgICAgICAgPHRoPkVzdGFkbzwvdGg+CiAgICAgICAgICA8dGg+UHJpb3JpZGFkPC90aD4KICAgICAgICAgIDx0aD5VbmlkYWQ8L3RoPgogICAgICAgICAgPHRoPkFwZXJ0dXJhPC90aD4KICAgICAgICAgIDx0aD48L3RoPgogICAgICAgIDwvdHI+CiAgICAgIDwvdGhlYWQ+CiAgICAgIDx0Ym9keT4KICAgICAgICB7JSBmb3IgdGlja2V0IGluIHRpY2tldHNfcmVjaWVudGVzICV9CiAgICAgICAgPHRyPgogICAgICAgICAgPHRkPnt7IHRpY2tldC5jb2RpZ28gfX08L3RkPgogICAgICAgICAgPHRkPnt7IHRpY2tldC50aXR1bG98dHJ1bmNhdGVjaGFyczo1NSB9fTwvdGQ+CiAgICAgICAgICA8dGQ+e3sgdGlja2V0LmdldF9lc3RhZG9fZGlzcGxheSB9fTwvdGQ+CiAgICAgICAgICA8dGQ+e3sgdGlja2V0LmdldF9wcmlvcmlkYWRfZGlzcGxheSB9fTwvdGQ+CiAgICAgICAgICA8dGQ+e3sgdGlja2V0LnVuaWRhZF9uZWdvY2lvLm5vbWJyZXxkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgIDx0ZD57eyB0aWNrZXQuZmVjaGFfYXBlcnR1cmF8ZGF0ZToiZC9tL1kgSDppIiB9fTwvdGQ+CiAgICAgICAgICA8dGQgY2xhc3M9InRleHQtZW5kIj4KICAgICAgICAgICAgPGEgaHJlZj0ieyUgdXJsICdwZ286dGlja2V0X2RldGFpbCcgdGlja2V0LmNvZGlnbyAlfSIgY2xhc3M9ImJ0biBidG4tc20gYnRuLW91dGxpbmUtcHJpbWFyeSI+VmVyPC9hPgogICAgICAgICAgPC90ZD4KICAgICAgICA8L3RyPgogICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgPHRyPjx0ZCBjb2xzcGFuPSI3IiBjbGFzcz0idGV4dC1jZW50ZXIgdGV4dC1tdXRlZCBweS00Ij5ObyBoYXkgdGlja2V0cy48L3RkPjwvdHI+CiAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgIDwvdGJvZHk+CiAgICA8L3RhYmxlPgogIDwvZGl2Pgo8L2Rpdj4KCnslIGlmIHJlc3VsdGFkb3MgJX0KPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20iPgogIDxkaXYgY2xhc3M9ImNhcmQtaGVhZGVyIGJnLXdoaXRlIGZ3LXNlbWlib2xkIj5SZXN1bHRhZG9zIHBvciBwZXLDrW9kbzwvZGl2PgogIDxkaXYgY2xhc3M9InRhYmxlLXJlc3BvbnNpdmUiPgogICAgPHRhYmxlIGNsYXNzPSJ0YWJsZSB0YWJsZS1zbSBtYi0wIj4KICAgICAgPHRoZWFkPjx0cj48dGg+UGVyw61vZG88L3RoPjx0aD5VbmlkYWQ8L3RoPjx0aD5DZXJyYWRvczwvdGg+PHRoPkFiaWVydG9zPC90aD48dGg+VC4gcHJvbSAoaCk8L3RoPjx0aD5TTEEgJTwvdGg+PC90cj48L3RoZWFkPgogICAgICA8dGJvZHk+CiAgICAgICAgeyUgZm9yIHIgaW4gcmVzdWx0YWRvcyAlfQogICAgICAgIDx0cj4KICAgICAgICAgIDx0ZD57eyByLnBlcmlvZG8gfX08L3RkPgogICAgICAgICAgPHRkPnt7IHIudW5pZGFkX25lZ29jaW8ubm9tYnJlIH19PC90ZD4KICAgICAgICAgIDx0ZD57eyByLnRpY2tldHNfY2VycmFkb3MgfX08L3RkPgogICAgICAgICAgPHRkPnt7IHIudGlja2V0c19hYmllcnRvcyB9fTwvdGQ+CiAgICAgICAgICA8dGQ+e3sgci50aWVtcG9fcHJvbWVkaW9faG9yYXMgfX08L3RkPgogICAgICAgICAgPHRkPnt7IHIuY3VtcGxpbWllbnRvX3NsYV9wY3QgfX0lPC90ZD4KICAgICAgICA8L3RyPgogICAgICAgIHslIGVuZGZvciAlfQogICAgICA8L3Rib2R5PgogICAgPC90YWJsZT4KICA8L2Rpdj4KPC9kaXY+CnslIGVuZGlmICV9CnslIGVuZGJsb2NrICV9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgo/pgoimportform.html
PATH_JSON="templates/pgo/pgoimportform.html"
FILENAME=pgoimportform.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=11
SIZE_BYTES_UTF8=653
CONTENT_SHA256=6f245db4a4fd1f5911973b9e9f87fd7dcf2ee2ffbc1286ed66a2416a61dae9ec
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
{% extends "base_wcg.html" %}
{% block title %}Importar tickets — PGO{% endblock %}
{% block content %}
<h1>Importar tickets</h1>
<form method="post" enctype="multipart/form-data" class="card p-3">
    {% csrf_token %}{{ form.as_p }}
    <button type="submit" class="btn btn-primary mt-2">Importar</button>
    <a href="{% url 'pgo:dashboard' %}" class="btn btn-link">Volver</a>
</form>
{% if batch %}<div class="card mt-3 p-3"><p>Creados: {{ batch.creados }} · Actualizados: {{ batch.actualizados }} · Errores: {{ batch.errores }}</p>{% if batch.log_texto %}<pre class="small">{{ batch.log_texto }}</pre>{% endif %}</div>{% endif %}
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}Importar tickets — PGO{% endblock %}
00003|{% block content %}
00004|<h1>Importar tickets</h1>
00005|<form method="post" enctype="multipart/form-data" class="card p-3">
00006|    {% csrf_token %}{{ form.as_p }}
00007|    <button type="submit" class="btn btn-primary mt-2">Importar</button>
00008|    <a href="{% url 'pgo:dashboard' %}" class="btn btn-link">Volver</a>
00009|</form>
00010|{% if batch %}<div class="card mt-3 p-3"><p>Creados: {{ batch.creados }} · Actualizados: {{ batch.actualizados }} · Errores: {{ batch.errores }}</p>{% if batch.log_texto %}<pre class="small">{{ batch.log_texto }}</pre>{% endif %}</div>{% endif %}
00011|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1JbXBvcnRhciB0aWNrZXRzIOKAlCBQR097JSBlbmRibG9jayAlfQp7JSBibG9jayBjb250ZW50ICV9CjxoMT5JbXBvcnRhciB0aWNrZXRzPC9oMT4KPGZvcm0gbWV0aG9kPSJwb3N0IiBlbmN0eXBlPSJtdWx0aXBhcnQvZm9ybS1kYXRhIiBjbGFzcz0iY2FyZCBwLTMiPgogICAgeyUgY3NyZl90b2tlbiAlfXt7IGZvcm0uYXNfcCB9fQogICAgPGJ1dHRvbiB0eXBlPSJzdWJtaXQiIGNsYXNzPSJidG4gYnRuLXByaW1hcnkgbXQtMiI+SW1wb3J0YXI8L2J1dHRvbj4KICAgIDxhIGhyZWY9InslIHVybCAncGdvOmRhc2hib2FyZCcgJX0iIGNsYXNzPSJidG4gYnRuLWxpbmsiPlZvbHZlcjwvYT4KPC9mb3JtPgp7JSBpZiBiYXRjaCAlfTxkaXYgY2xhc3M9ImNhcmQgbXQtMyBwLTMiPjxwPkNyZWFkb3M6IHt7IGJhdGNoLmNyZWFkb3MgfX0gwrcgQWN0dWFsaXphZG9zOiB7eyBiYXRjaC5hY3R1YWxpemFkb3MgfX0gwrcgRXJyb3Jlczoge3sgYmF0Y2guZXJyb3JlcyB9fTwvcD57JSBpZiBiYXRjaC5sb2dfdGV4dG8gJX08cHJlIGNsYXNzPSJzbWFsbCI+e3sgYmF0Y2gubG9nX3RleHRvIH19PC9wcmU+eyUgZW5kaWYgJX08L2Rpdj57JSBlbmRpZiAlfQp7JSBlbmRibG9jayAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgo/pgoresultados.html
PATH_JSON="templates/pgo/pgoresultados.html"
FILENAME=pgoresultados.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=30
SIZE_BYTES_UTF8=1191
CONTENT_SHA256=01c5dd76b0319d70f5882bdf4cab39a166780c69e380692463fdc81da099814a
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
{% extends "base_wcg.html" %}
{% block title %}PGO — Resultados{% endblock %}
{% block content %}
<div class="d-flex justify-content-between mb-3 mt-2">
  <div class="wcg-report-head">
    <h1 class="h4 fw-semibold mb-0">PGO — Resultados por período</h1>
    {% include "includes/module_mark.html" with module="pgo" %}
  </div>
  <a href="{% url 'pgo:dashboard' %}" class="btn btn-sm btn-outline-secondary">← Dashboard</a>
</div>
<div class="card border-0 shadow-sm">
  <table class="table table-hover table-wcg mb-0">
    <thead><tr><th>Período</th><th>Unidad</th><th>Cerrados</th><th>Abiertos</th><th>T. promedio (h)</th><th>SLA %</th></tr></thead>
    <tbody>
      {% for r in resultados %}
      <tr>
        <td>{{ r.periodo }}</td>
        <td>{{ r.unidad_negocio.nombre }}</td>
        <td>{{ r.tickets_cerrados }}</td>
        <td>{{ r.tickets_abiertos }}</td>
        <td>{{ r.tiempo_promedio_horas }}</td>
        <td>{{ r.cumplimiento_sla_pct }}%</td>
      </tr>
      {% empty %}
      <tr><td colspan="6" class="text-muted text-center py-4">Sin resultados. Importe tickets y se recalcularán.</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}PGO — Resultados{% endblock %}
00003|{% block content %}
00004|<div class="d-flex justify-content-between mb-3 mt-2">
00005|  <div class="wcg-report-head">
00006|    <h1 class="h4 fw-semibold mb-0">PGO — Resultados por período</h1>
00007|    {% include "includes/module_mark.html" with module="pgo" %}
00008|  </div>
00009|  <a href="{% url 'pgo:dashboard' %}" class="btn btn-sm btn-outline-secondary">← Dashboard</a>
00010|</div>
00011|<div class="card border-0 shadow-sm">
00012|  <table class="table table-hover table-wcg mb-0">
00013|    <thead><tr><th>Período</th><th>Unidad</th><th>Cerrados</th><th>Abiertos</th><th>T. promedio (h)</th><th>SLA %</th></tr></thead>
00014|    <tbody>
00015|      {% for r in resultados %}
00016|      <tr>
00017|        <td>{{ r.periodo }}</td>
00018|        <td>{{ r.unidad_negocio.nombre }}</td>
00019|        <td>{{ r.tickets_cerrados }}</td>
00020|        <td>{{ r.tickets_abiertos }}</td>
00021|        <td>{{ r.tiempo_promedio_horas }}</td>
00022|        <td>{{ r.cumplimiento_sla_pct }}%</td>
00023|      </tr>
00024|      {% empty %}
00025|      <tr><td colspan="6" class="text-muted text-center py-4">Sin resultados. Importe tickets y se recalcularán.</td></tr>
00026|      {% endfor %}
00027|    </tbody>
00028|  </table>
00029|</div>
00030|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1QR08g4oCUIFJlc3VsdGFkb3N7JSBlbmRibG9jayAlfQp7JSBibG9jayBjb250ZW50ICV9CjxkaXYgY2xhc3M9ImQtZmxleCBqdXN0aWZ5LWNvbnRlbnQtYmV0d2VlbiBtYi0zIG10LTIiPgogIDxkaXYgY2xhc3M9IndjZy1yZXBvcnQtaGVhZCI+CiAgICA8aDEgY2xhc3M9Img0IGZ3LXNlbWlib2xkIG1iLTAiPlBHTyDigJQgUmVzdWx0YWRvcyBwb3IgcGVyw61vZG88L2gxPgogICAgeyUgaW5jbHVkZSAiaW5jbHVkZXMvbW9kdWxlX21hcmsuaHRtbCIgd2l0aCBtb2R1bGU9InBnbyIgJX0KICA8L2Rpdj4KICA8YSBocmVmPSJ7JSB1cmwgJ3BnbzpkYXNoYm9hcmQnICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1zZWNvbmRhcnkiPuKGkCBEYXNoYm9hcmQ8L2E+CjwvZGl2Pgo8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSI+CiAgPHRhYmxlIGNsYXNzPSJ0YWJsZSB0YWJsZS1ob3ZlciB0YWJsZS13Y2cgbWItMCI+CiAgICA8dGhlYWQ+PHRyPjx0aD5QZXLDrW9kbzwvdGg+PHRoPlVuaWRhZDwvdGg+PHRoPkNlcnJhZG9zPC90aD48dGg+QWJpZXJ0b3M8L3RoPjx0aD5ULiBwcm9tZWRpbyAoaCk8L3RoPjx0aD5TTEEgJTwvdGg+PC90cj48L3RoZWFkPgogICAgPHRib2R5PgogICAgICB7JSBmb3IgciBpbiByZXN1bHRhZG9zICV9CiAgICAgIDx0cj4KICAgICAgICA8dGQ+e3sgci5wZXJpb2RvIH19PC90ZD4KICAgICAgICA8dGQ+e3sgci51bmlkYWRfbmVnb2Npby5ub21icmUgfX08L3RkPgogICAgICAgIDx0ZD57eyByLnRpY2tldHNfY2VycmFkb3MgfX08L3RkPgogICAgICAgIDx0ZD57eyByLnRpY2tldHNfYWJpZXJ0b3MgfX08L3RkPgogICAgICAgIDx0ZD57eyByLnRpZW1wb19wcm9tZWRpb19ob3JhcyB9fTwvdGQ+CiAgICAgICAgPHRkPnt7IHIuY3VtcGxpbWllbnRvX3NsYV9wY3QgfX0lPC90ZD4KICAgICAgPC90cj4KICAgICAgeyUgZW1wdHkgJX0KICAgICAgPHRyPjx0ZCBjb2xzcGFuPSI2IiBjbGFzcz0idGV4dC1tdXRlZCB0ZXh0LWNlbnRlciBweS00Ij5TaW4gcmVzdWx0YWRvcy4gSW1wb3J0ZSB0aWNrZXRzIHkgc2UgcmVjYWxjdWxhcsOhbi48L3RkPjwvdHI+CiAgICAgIHslIGVuZGZvciAlfQogICAgPC90Ym9keT4KICA8L3RhYmxlPgo8L2Rpdj4KeyUgZW5kYmxvY2sgJX0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgo/pgoresumenunidad.html
PATH_JSON="templates/pgo/pgoresumenunidad.html"
FILENAME=pgoresumenunidad.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=8
SIZE_BYTES_UTF8=519
CONTENT_SHA256=312dc03d9867d59b58c5db8395f18ce02011d131059344842e7f1b3a807181ce
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
{% extends "base_wcg.html" %}
{% block title %}PGO — Resumen por unidad{% endblock %}
{% block content %}
<h1>Resumen por unidad</h1>
<table class="table table-sm bg-white"><thead><tr><th>Código</th><th>Unidad</th><th>Total tickets</th></tr></thead>
<tbody>{% for r in data %}<tr><td>{{ r.unidad_negocio__code|default:"—" }}</td><td>{{ r.unidad_negocio__nombre|default:"—" }}</td><td>{{ r.total }}</td></tr>{% endfor %}</tbody></table>
<p><a href="{% url 'pgo:dashboard' %}">← Dashboard</a></p>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}PGO — Resumen por unidad{% endblock %}
00003|{% block content %}
00004|<h1>Resumen por unidad</h1>
00005|<table class="table table-sm bg-white"><thead><tr><th>Código</th><th>Unidad</th><th>Total tickets</th></tr></thead>
00006|<tbody>{% for r in data %}<tr><td>{{ r.unidad_negocio__code|default:"—" }}</td><td>{{ r.unidad_negocio__nombre|default:"—" }}</td><td>{{ r.total }}</td></tr>{% endfor %}</tbody></table>
00007|<p><a href="{% url 'pgo:dashboard' %}">← Dashboard</a></p>
00008|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1QR08g4oCUIFJlc3VtZW4gcG9yIHVuaWRhZHslIGVuZGJsb2NrICV9CnslIGJsb2NrIGNvbnRlbnQgJX0KPGgxPlJlc3VtZW4gcG9yIHVuaWRhZDwvaDE+Cjx0YWJsZSBjbGFzcz0idGFibGUgdGFibGUtc20gYmctd2hpdGUiPjx0aGVhZD48dHI+PHRoPkPDs2RpZ288L3RoPjx0aD5VbmlkYWQ8L3RoPjx0aD5Ub3RhbCB0aWNrZXRzPC90aD48L3RyPjwvdGhlYWQ+Cjx0Ym9keT57JSBmb3IgciBpbiBkYXRhICV9PHRyPjx0ZD57eyByLnVuaWRhZF9uZWdvY2lvX19jb2RlfGRlZmF1bHQ6IuKAlCIgfX08L3RkPjx0ZD57eyByLnVuaWRhZF9uZWdvY2lvX19ub21icmV8ZGVmYXVsdDoi4oCUIiB9fTwvdGQ+PHRkPnt7IHIudG90YWwgfX08L3RkPjwvdHI+eyUgZW5kZm9yICV9PC90Ym9keT48L3RhYmxlPgo8cD48YSBocmVmPSJ7JSB1cmwgJ3BnbzpkYXNoYm9hcmQnICV9Ij7ihpAgRGFzaGJvYXJkPC9hPjwvcD4KeyUgZW5kYmxvY2sgJX0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgo/pgoresumenusuario.html
PATH_JSON="templates/pgo/pgoresumenusuario.html"
FILENAME=pgoresumenusuario.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=8
SIZE_BYTES_UTF8=487
CONTENT_SHA256=2353ce437e28f064c283a118d6606e642c5682f2b0a52cac0caf647a3c6c5c6d
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
{% extends "base_wcg.html" %}
{% block title %}PGO — Resumen por usuario{% endblock %}
{% block content %}
<h1>Resumen por usuario</h1>
<table class="table table-sm bg-white"><thead><tr><th>Usuario</th><th>Total</th><th>Abiertos</th></tr></thead>
<tbody>{% for r in data %}<tr><td>{{ r.asignado_a__username|default:"—" }}</td><td>{{ r.total }}</td><td>{{ r.abiertos }}</td></tr>{% endfor %}</tbody></table>
<p><a href="{% url 'pgo:dashboard' %}">← Dashboard</a></p>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}PGO — Resumen por usuario{% endblock %}
00003|{% block content %}
00004|<h1>Resumen por usuario</h1>
00005|<table class="table table-sm bg-white"><thead><tr><th>Usuario</th><th>Total</th><th>Abiertos</th></tr></thead>
00006|<tbody>{% for r in data %}<tr><td>{{ r.asignado_a__username|default:"—" }}</td><td>{{ r.total }}</td><td>{{ r.abiertos }}</td></tr>{% endfor %}</tbody></table>
00007|<p><a href="{% url 'pgo:dashboard' %}">← Dashboard</a></p>
00008|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1QR08g4oCUIFJlc3VtZW4gcG9yIHVzdWFyaW97JSBlbmRibG9jayAlfQp7JSBibG9jayBjb250ZW50ICV9CjxoMT5SZXN1bWVuIHBvciB1c3VhcmlvPC9oMT4KPHRhYmxlIGNsYXNzPSJ0YWJsZSB0YWJsZS1zbSBiZy13aGl0ZSI+PHRoZWFkPjx0cj48dGg+VXN1YXJpbzwvdGg+PHRoPlRvdGFsPC90aD48dGg+QWJpZXJ0b3M8L3RoPjwvdHI+PC90aGVhZD4KPHRib2R5PnslIGZvciByIGluIGRhdGEgJX08dHI+PHRkPnt7IHIuYXNpZ25hZG9fYV9fdXNlcm5hbWV8ZGVmYXVsdDoi4oCUIiB9fTwvdGQ+PHRkPnt7IHIudG90YWwgfX08L3RkPjx0ZD57eyByLmFiaWVydG9zIH19PC90ZD48L3RyPnslIGVuZGZvciAlfTwvdGJvZHk+PC90YWJsZT4KPHA+PGEgaHJlZj0ieyUgdXJsICdwZ286ZGFzaGJvYXJkJyAlfSI+4oaQIERhc2hib2FyZDwvYT48L3A+CnslIGVuZGJsb2NrICV9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgo/pgoticketdetail.html
PATH_JSON="templates/pgo/pgoticketdetail.html"
FILENAME=pgoticketdetail.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=10
SIZE_BYTES_UTF8=644
CONTENT_SHA256=b1ad6b4008a029eb1cebcaba6789f9b42e277bdd7e606f516d8dd5befd5dc454
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
{% extends "base_wcg.html" %}
{% block title %}Ticket {{ ticket.codigo }}{% endblock %}
{% block content %}
<h1>{{ ticket.codigo }} — {{ ticket.titulo }}</h1>
<p class="text-muted">{{ ticket.get_estado_display }} · {{ ticket.get_prioridad_display }}{% if ticket.entidad %} · {{ ticket.entidad.nombre }}{% endif %}</p>
<p>{{ ticket.descripcion }}</p>
<h5>Eventos</h5>
<ul>{% for e in eventos %}<li class="small">{{ e.fecha|date:"d/m/Y H:i" }} — {{ e.get_tipo_display }}: {{ e.descripcion }}</li>{% empty %}<li class="text-muted">Sin eventos</li>{% endfor %}</ul>
<p><a href="{% url 'pgo:ticket_list' %}">← Tickets</a></p>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}Ticket {{ ticket.codigo }}{% endblock %}
00003|{% block content %}
00004|<h1>{{ ticket.codigo }} — {{ ticket.titulo }}</h1>
00005|<p class="text-muted">{{ ticket.get_estado_display }} · {{ ticket.get_prioridad_display }}{% if ticket.entidad %} · {{ ticket.entidad.nombre }}{% endif %}</p>
00006|<p>{{ ticket.descripcion }}</p>
00007|<h5>Eventos</h5>
00008|<ul>{% for e in eventos %}<li class="small">{{ e.fecha|date:"d/m/Y H:i" }} — {{ e.get_tipo_display }}: {{ e.descripcion }}</li>{% empty %}<li class="text-muted">Sin eventos</li>{% endfor %}</ul>
00009|<p><a href="{% url 'pgo:ticket_list' %}">← Tickets</a></p>
00010|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1UaWNrZXQge3sgdGlja2V0LmNvZGlnbyB9fXslIGVuZGJsb2NrICV9CnslIGJsb2NrIGNvbnRlbnQgJX0KPGgxPnt7IHRpY2tldC5jb2RpZ28gfX0g4oCUIHt7IHRpY2tldC50aXR1bG8gfX08L2gxPgo8cCBjbGFzcz0idGV4dC1tdXRlZCI+e3sgdGlja2V0LmdldF9lc3RhZG9fZGlzcGxheSB9fSDCtyB7eyB0aWNrZXQuZ2V0X3ByaW9yaWRhZF9kaXNwbGF5IH19eyUgaWYgdGlja2V0LmVudGlkYWQgJX0gwrcge3sgdGlja2V0LmVudGlkYWQubm9tYnJlIH19eyUgZW5kaWYgJX08L3A+CjxwPnt7IHRpY2tldC5kZXNjcmlwY2lvbiB9fTwvcD4KPGg1PkV2ZW50b3M8L2g1Pgo8dWw+eyUgZm9yIGUgaW4gZXZlbnRvcyAlfTxsaSBjbGFzcz0ic21hbGwiPnt7IGUuZmVjaGF8ZGF0ZToiZC9tL1kgSDppIiB9fSDigJQge3sgZS5nZXRfdGlwb19kaXNwbGF5IH19OiB7eyBlLmRlc2NyaXBjaW9uIH19PC9saT57JSBlbXB0eSAlfTxsaSBjbGFzcz0idGV4dC1tdXRlZCI+U2luIGV2ZW50b3M8L2xpPnslIGVuZGZvciAlfTwvdWw+CjxwPjxhIGhyZWY9InslIHVybCAncGdvOnRpY2tldF9saXN0JyAlfSI+4oaQIFRpY2tldHM8L2E+PC9wPgp7JSBlbmRibG9jayAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgo/pgoticketlist.html
PATH_JSON="templates/pgo/pgoticketlist.html"
FILENAME=pgoticketlist.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=56
SIZE_BYTES_UTF8=2768
CONTENT_SHA256=647f255d495ed737fcf9c37a20a383cfe202e784b15f483bde09004500bf4708
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
{% extends "base_wcg.html" %}
{% block title %}PGO — Tickets{% endblock %}
{% block content %}
<div class="d-flex justify-content-between mb-3 mt-2 flex-wrap gap-2">
  <div class="wcg-report-head">
    <h1 class="h4 fw-semibold mb-0">Tickets</h1>
    {% include "includes/module_mark.html" with module="pgo" %}
  </div>
  <div class="d-flex gap-1">
    <a href="{% url 'pgo:dashboard' %}" class="btn btn-sm btn-outline-secondary">Dashboard</a>
    <a href="{% url 'pgo:export_tickets' %}" class="btn btn-sm btn-outline-primary">Exportar</a>
  </div>
</div>
<form method="get" class="row g-2 mb-3">
  <div class="col-md-3">
    <select name="estado" class="form-select form-select-sm">
      <option value="">Todos los estados</option>
      {% for v,l in estados %}<option value="{{ v }}"{% if request.GET.estado == v %} selected{% endif %}>{{ l }}</option>{% endfor %}
    </select>
  </div>
  <div class="col-md-3">
    <select name="prioridad" class="form-select form-select-sm">
      <option value="">Todas las prioridades</option>
      {% for v,l in prioridades %}<option value="{{ v }}"{% if request.GET.prioridad == v %} selected{% endif %}>{{ l }}</option>{% endfor %}
    </select>
  </div>
  <div class="col-md-2"><button class="btn btn-primary btn-sm w-100" type="submit">Filtrar</button></div>
</form>
<div class="card border-0 shadow-sm">
<table class="table table-hover table-wcg mb-0 small">
<thead><tr><th>Código</th><th>Título</th><th>Estado</th><th>Prioridad</th><th>Unidad</th><th>Apertura</th><th></th></tr></thead>
<tbody>
{% for t in tickets %}
<tr>
  <td>{{ t.codigo }}</td>
  <td>{{ t.titulo|truncatechars:60 }}</td>
  <td>{{ t.get_estado_display }}</td>
  <td>{{ t.get_prioridad_display }}</td>
  <td>{{ t.unidad_negocio.nombre|default:"—" }}</td>
  <td>{{ t.fecha_apertura|date:"d/m/Y" }}</td>
  <td><a href="{% url 'pgo:ticket_detail' t.codigo %}" class="btn btn-sm btn-outline-primary">Ver</a></td>
</tr>
{% empty %}
<tr><td colspan="7" class="text-muted text-center py-4">Sin tickets</td></tr>
{% endfor %}
</tbody>
</table>
</div>
{% if is_paginated %}
<nav class="mt-3"><ul class="pagination pagination-sm justify-content-center">
{% if page_obj.has_previous %}<li class="page-item"><a class="page-link" href="?page={{ page_obj.previous_page_number }}&estado={{ request.GET.estado }}&prioridad={{ request.GET.prioridad }}">Anterior</a></li>{% endif %}
<li class="page-item disabled"><span class="page-link">{{ page_obj.number }}/{{ page_obj.paginator.num_pages }}</span></li>
{% if page_obj.has_next %}<li class="page-item"><a class="page-link" href="?page={{ page_obj.next_page_number }}&estado={{ request.GET.estado }}&prioridad={{ request.GET.prioridad }}">Siguiente</a></li>{% endif %}
</ul></nav>
{% endif %}
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}PGO — Tickets{% endblock %}
00003|{% block content %}
00004|<div class="d-flex justify-content-between mb-3 mt-2 flex-wrap gap-2">
00005|  <div class="wcg-report-head">
00006|    <h1 class="h4 fw-semibold mb-0">Tickets</h1>
00007|    {% include "includes/module_mark.html" with module="pgo" %}
00008|  </div>
00009|  <div class="d-flex gap-1">
00010|    <a href="{% url 'pgo:dashboard' %}" class="btn btn-sm btn-outline-secondary">Dashboard</a>
00011|    <a href="{% url 'pgo:export_tickets' %}" class="btn btn-sm btn-outline-primary">Exportar</a>
00012|  </div>
00013|</div>
00014|<form method="get" class="row g-2 mb-3">
00015|  <div class="col-md-3">
00016|    <select name="estado" class="form-select form-select-sm">
00017|      <option value="">Todos los estados</option>
00018|      {% for v,l in estados %}<option value="{{ v }}"{% if request.GET.estado == v %} selected{% endif %}>{{ l }}</option>{% endfor %}
00019|    </select>
00020|  </div>
00021|  <div class="col-md-3">
00022|    <select name="prioridad" class="form-select form-select-sm">
00023|      <option value="">Todas las prioridades</option>
00024|      {% for v,l in prioridades %}<option value="{{ v }}"{% if request.GET.prioridad == v %} selected{% endif %}>{{ l }}</option>{% endfor %}
00025|    </select>
00026|  </div>
00027|  <div class="col-md-2"><button class="btn btn-primary btn-sm w-100" type="submit">Filtrar</button></div>
00028|</form>
00029|<div class="card border-0 shadow-sm">
00030|<table class="table table-hover table-wcg mb-0 small">
00031|<thead><tr><th>Código</th><th>Título</th><th>Estado</th><th>Prioridad</th><th>Unidad</th><th>Apertura</th><th></th></tr></thead>
00032|<tbody>
00033|{% for t in tickets %}
00034|<tr>
00035|  <td>{{ t.codigo }}</td>
00036|  <td>{{ t.titulo|truncatechars:60 }}</td>
00037|  <td>{{ t.get_estado_display }}</td>
00038|  <td>{{ t.get_prioridad_display }}</td>
00039|  <td>{{ t.unidad_negocio.nombre|default:"—" }}</td>
00040|  <td>{{ t.fecha_apertura|date:"d/m/Y" }}</td>
00041|  <td><a href="{% url 'pgo:ticket_detail' t.codigo %}" class="btn btn-sm btn-outline-primary">Ver</a></td>
00042|</tr>
00043|{% empty %}
00044|<tr><td colspan="7" class="text-muted text-center py-4">Sin tickets</td></tr>
00045|{% endfor %}
00046|</tbody>
00047|</table>
00048|</div>
00049|{% if is_paginated %}
00050|<nav class="mt-3"><ul class="pagination pagination-sm justify-content-center">
00051|{% if page_obj.has_previous %}<li class="page-item"><a class="page-link" href="?page={{ page_obj.previous_page_number }}&estado={{ request.GET.estado }}&prioridad={{ request.GET.prioridad }}">Anterior</a></li>{% endif %}
00052|<li class="page-item disabled"><span class="page-link">{{ page_obj.number }}/{{ page_obj.paginator.num_pages }}</span></li>
00053|{% if page_obj.has_next %}<li class="page-item"><a class="page-link" href="?page={{ page_obj.next_page_number }}&estado={{ request.GET.estado }}&prioridad={{ request.GET.prioridad }}">Siguiente</a></li>{% endif %}
00054|</ul></nav>
00055|{% endif %}
00056|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1QR08g4oCUIFRpY2tldHN7JSBlbmRibG9jayAlfQp7JSBibG9jayBjb250ZW50ICV9CjxkaXYgY2xhc3M9ImQtZmxleCBqdXN0aWZ5LWNvbnRlbnQtYmV0d2VlbiBtYi0zIG10LTIgZmxleC13cmFwIGdhcC0yIj4KICA8ZGl2IGNsYXNzPSJ3Y2ctcmVwb3J0LWhlYWQiPgogICAgPGgxIGNsYXNzPSJoNCBmdy1zZW1pYm9sZCBtYi0wIj5UaWNrZXRzPC9oMT4KICAgIHslIGluY2x1ZGUgImluY2x1ZGVzL21vZHVsZV9tYXJrLmh0bWwiIHdpdGggbW9kdWxlPSJwZ28iICV9CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iZC1mbGV4IGdhcC0xIj4KICAgIDxhIGhyZWY9InslIHVybCAncGdvOmRhc2hib2FyZCcgJX0iIGNsYXNzPSJidG4gYnRuLXNtIGJ0bi1vdXRsaW5lLXNlY29uZGFyeSI+RGFzaGJvYXJkPC9hPgogICAgPGEgaHJlZj0ieyUgdXJsICdwZ286ZXhwb3J0X3RpY2tldHMnICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1wcmltYXJ5Ij5FeHBvcnRhcjwvYT4KICA8L2Rpdj4KPC9kaXY+Cjxmb3JtIG1ldGhvZD0iZ2V0IiBjbGFzcz0icm93IGctMiBtYi0zIj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtMyI+CiAgICA8c2VsZWN0IG5hbWU9ImVzdGFkbyIgY2xhc3M9ImZvcm0tc2VsZWN0IGZvcm0tc2VsZWN0LXNtIj4KICAgICAgPG9wdGlvbiB2YWx1ZT0iIj5Ub2RvcyBsb3MgZXN0YWRvczwvb3B0aW9uPgogICAgICB7JSBmb3IgdixsIGluIGVzdGFkb3MgJX08b3B0aW9uIHZhbHVlPSJ7eyB2IH19InslIGlmIHJlcXVlc3QuR0VULmVzdGFkbyA9PSB2ICV9IHNlbGVjdGVkeyUgZW5kaWYgJX0+e3sgbCB9fTwvb3B0aW9uPnslIGVuZGZvciAlfQogICAgPC9zZWxlY3Q+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTMiPgogICAgPHNlbGVjdCBuYW1lPSJwcmlvcmlkYWQiIGNsYXNzPSJmb3JtLXNlbGVjdCBmb3JtLXNlbGVjdC1zbSI+CiAgICAgIDxvcHRpb24gdmFsdWU9IiI+VG9kYXMgbGFzIHByaW9yaWRhZGVzPC9vcHRpb24+CiAgICAgIHslIGZvciB2LGwgaW4gcHJpb3JpZGFkZXMgJX08b3B0aW9uIHZhbHVlPSJ7eyB2IH19InslIGlmIHJlcXVlc3QuR0VULnByaW9yaWRhZCA9PSB2ICV9IHNlbGVjdGVkeyUgZW5kaWYgJX0+e3sgbCB9fTwvb3B0aW9uPnslIGVuZGZvciAlfQogICAgPC9zZWxlY3Q+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTIiPjxidXR0b24gY2xhc3M9ImJ0biBidG4tcHJpbWFyeSBidG4tc20gdy0xMDAiIHR5cGU9InN1Ym1pdCI+RmlsdHJhcjwvYnV0dG9uPjwvZGl2Pgo8L2Zvcm0+CjxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIj4KPHRhYmxlIGNsYXNzPSJ0YWJsZSB0YWJsZS1ob3ZlciB0YWJsZS13Y2cgbWItMCBzbWFsbCI+Cjx0aGVhZD48dHI+PHRoPkPDs2RpZ288L3RoPjx0aD5Uw610dWxvPC90aD48dGg+RXN0YWRvPC90aD48dGg+UHJpb3JpZGFkPC90aD48dGg+VW5pZGFkPC90aD48dGg+QXBlcnR1cmE8L3RoPjx0aD48L3RoPjwvdHI+PC90aGVhZD4KPHRib2R5Pgp7JSBmb3IgdCBpbiB0aWNrZXRzICV9Cjx0cj4KICA8dGQ+e3sgdC5jb2RpZ28gfX08L3RkPgogIDx0ZD57eyB0LnRpdHVsb3x0cnVuY2F0ZWNoYXJzOjYwIH19PC90ZD4KICA8dGQ+e3sgdC5nZXRfZXN0YWRvX2Rpc3BsYXkgfX08L3RkPgogIDx0ZD57eyB0LmdldF9wcmlvcmlkYWRfZGlzcGxheSB9fTwvdGQ+CiAgPHRkPnt7IHQudW5pZGFkX25lZ29jaW8ubm9tYnJlfGRlZmF1bHQ6IuKAlCIgfX08L3RkPgogIDx0ZD57eyB0LmZlY2hhX2FwZXJ0dXJhfGRhdGU6ImQvbS9ZIiB9fTwvdGQ+CiAgPHRkPjxhIGhyZWY9InslIHVybCAncGdvOnRpY2tldF9kZXRhaWwnIHQuY29kaWdvICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1wcmltYXJ5Ij5WZXI8L2E+PC90ZD4KPC90cj4KeyUgZW1wdHkgJX0KPHRyPjx0ZCBjb2xzcGFuPSI3IiBjbGFzcz0idGV4dC1tdXRlZCB0ZXh0LWNlbnRlciBweS00Ij5TaW4gdGlja2V0czwvdGQ+PC90cj4KeyUgZW5kZm9yICV9CjwvdGJvZHk+CjwvdGFibGU+CjwvZGl2Pgp7JSBpZiBpc19wYWdpbmF0ZWQgJX0KPG5hdiBjbGFzcz0ibXQtMyI+PHVsIGNsYXNzPSJwYWdpbmF0aW9uIHBhZ2luYXRpb24tc20ganVzdGlmeS1jb250ZW50LWNlbnRlciI+CnslIGlmIHBhZ2Vfb2JqLmhhc19wcmV2aW91cyAlfTxsaSBjbGFzcz0icGFnZS1pdGVtIj48YSBjbGFzcz0icGFnZS1saW5rIiBocmVmPSI/cGFnZT17eyBwYWdlX29iai5wcmV2aW91c19wYWdlX251bWJlciB9fSZlc3RhZG89e3sgcmVxdWVzdC5HRVQuZXN0YWRvIH19JnByaW9yaWRhZD17eyByZXF1ZXN0LkdFVC5wcmlvcmlkYWQgfX0iPkFudGVyaW9yPC9hPjwvbGk+eyUgZW5kaWYgJX0KPGxpIGNsYXNzPSJwYWdlLWl0ZW0gZGlzYWJsZWQiPjxzcGFuIGNsYXNzPSJwYWdlLWxpbmsiPnt7IHBhZ2Vfb2JqLm51bWJlciB9fS97eyBwYWdlX29iai5wYWdpbmF0b3IubnVtX3BhZ2VzIH19PC9zcGFuPjwvbGk+CnslIGlmIHBhZ2Vfb2JqLmhhc19uZXh0ICV9PGxpIGNsYXNzPSJwYWdlLWl0ZW0iPjxhIGNsYXNzPSJwYWdlLWxpbmsiIGhyZWY9Ij9wYWdlPXt7IHBhZ2Vfb2JqLm5leHRfcGFnZV9udW1iZXIgfX0mZXN0YWRvPXt7IHJlcXVlc3QuR0VULmVzdGFkbyB9fSZwcmlvcmlkYWQ9e3sgcmVxdWVzdC5HRVQucHJpb3JpZGFkIH19Ij5TaWd1aWVudGU8L2E+PC9saT57JSBlbmRpZiAlfQo8L3VsPjwvbmF2Pgp7JSBlbmRpZiAlfQp7JSBlbmRibG9jayAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/portal/ayuda.html
PATH_JSON="templates/portal/ayuda.html"
FILENAME=ayuda.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=50
SIZE_BYTES_UTF8=2796
CONTENT_SHA256=627dcbe8734d0cd6d5cd41451e3986cb617a3ebdc263ab86c49804f4e62a9eaf
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
{% extends "base_wcg.html" %}
{% block title %}Guía de uso — WCG{% endblock %}
{% block content %}
<div class="mb-4 mt-2">
  <h1 class="h3 fw-semibold mb-1">Guía de uso — WCG</h1>
  <p class="text-muted mb-0">Referencia rápida para demo interna y uso gerencial.</p>
</div>

<div class="row g-3">
  <div class="col-lg-8">
    <div class="card border-0 shadow-sm mb-3">
      <div class="card-header bg-white fw-semibold">¿Qué es cada módulo?</div>
      <div class="card-body small">
        <dl>
          <dt>CRM — Clientes</dt>
          <dd class="mb-3">Maestro de entidades, contactos, productos WCF/WCL/WCI, interacciones y tareas.</dd>
          <dt>Balón de Riesgo</dt>
          <dd class="mb-3">Mora y saldos vencidos por operación (snapshots leasing + rentas).</dd>
          <dt>PGO — Operación</dt>
          <dd class="mb-3">Tickets helpdesk, tiempos, SLA y resultados por período.</dd>
          <dt>PGC</dt>
          <dd class="mb-0">Plan comercial, clientes nuevos y venta cruzada (<code>/pgc/</code>).</dd>
        </dl>
      </div>
    </div>

    <div class="card border-0 shadow-sm mb-3">
      <div class="card-header bg-white fw-semibold">Ruta sugerida para demo (15–20 min)</div>
      <ol class="list-group list-group-flush small">
        <li class="list-group-item"><strong>1.</strong> <a href="{% url 'portal:home' %}">Menú principal</a> — las cuatro opciones del producto.</li>
        <li class="list-group-item"><strong>2.</strong> <a href="{% url 'pgc:dashboard' %}">📊 PGC</a> — plan comercial.</li>
        <li class="list-group-item"><strong>3.</strong> <a href="{% url 'pgo:dashboard' %}">⚙️ PGO</a> — tickets y SLA.</li>
        <li class="list-group-item"><strong>4.</strong> <a href="{% url 'crm:entidad_list' %}">👥 CRM</a> — listado, filtros, detalle, export CSV.</li>
        <li class="list-group-item"><strong>5.</strong> <a href="{% url 'risk:comando_balon' %}">⚽ Comando Balón</a> — mora, alertas, historial.</li>
        <li class="list-group-item"><strong>6.</strong> <a href="{% url 'portal:estado' %}">Estado del sistema</a> — KPIs e importaciones recientes.</li>
        <li class="list-group-item"><strong>7.</strong> <a href="{% url 'imports:import_hub' %}">Administración → Importación</a> — carga unificada.</li>
      </ol>
    </div>
  </div>
  <div class="col-lg-4">
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white fw-semibold">Carga de datos</div>
      <div class="card-body small">
        <p>En producción: <code>python manage.py bootstrap_wcg_demo</code></p>
        <p class="mb-0">O suba archivos en <a href="{% url 'imports:import_hub' %}">Administración → Importación General</a>.</p>
      </div>
    </div>
  </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}Guía de uso — WCG{% endblock %}
00003|{% block content %}
00004|<div class="mb-4 mt-2">
00005|  <h1 class="h3 fw-semibold mb-1">Guía de uso — WCG</h1>
00006|  <p class="text-muted mb-0">Referencia rápida para demo interna y uso gerencial.</p>
00007|</div>
00008|
00009|<div class="row g-3">
00010|  <div class="col-lg-8">
00011|    <div class="card border-0 shadow-sm mb-3">
00012|      <div class="card-header bg-white fw-semibold">¿Qué es cada módulo?</div>
00013|      <div class="card-body small">
00014|        <dl>
00015|          <dt>CRM — Clientes</dt>
00016|          <dd class="mb-3">Maestro de entidades, contactos, productos WCF/WCL/WCI, interacciones y tareas.</dd>
00017|          <dt>Balón de Riesgo</dt>
00018|          <dd class="mb-3">Mora y saldos vencidos por operación (snapshots leasing + rentas).</dd>
00019|          <dt>PGO — Operación</dt>
00020|          <dd class="mb-3">Tickets helpdesk, tiempos, SLA y resultados por período.</dd>
00021|          <dt>PGC</dt>
00022|          <dd class="mb-0">Plan comercial, clientes nuevos y venta cruzada (<code>/pgc/</code>).</dd>
00023|        </dl>
00024|      </div>
00025|    </div>
00026|
00027|    <div class="card border-0 shadow-sm mb-3">
00028|      <div class="card-header bg-white fw-semibold">Ruta sugerida para demo (15–20 min)</div>
00029|      <ol class="list-group list-group-flush small">
00030|        <li class="list-group-item"><strong>1.</strong> <a href="{% url 'portal:home' %}">Menú principal</a> — las cuatro opciones del producto.</li>
00031|        <li class="list-group-item"><strong>2.</strong> <a href="{% url 'pgc:dashboard' %}">📊 PGC</a> — plan comercial.</li>
00032|        <li class="list-group-item"><strong>3.</strong> <a href="{% url 'pgo:dashboard' %}">⚙️ PGO</a> — tickets y SLA.</li>
00033|        <li class="list-group-item"><strong>4.</strong> <a href="{% url 'crm:entidad_list' %}">👥 CRM</a> — listado, filtros, detalle, export CSV.</li>
00034|        <li class="list-group-item"><strong>5.</strong> <a href="{% url 'risk:comando_balon' %}">⚽ Comando Balón</a> — mora, alertas, historial.</li>
00035|        <li class="list-group-item"><strong>6.</strong> <a href="{% url 'portal:estado' %}">Estado del sistema</a> — KPIs e importaciones recientes.</li>
00036|        <li class="list-group-item"><strong>7.</strong> <a href="{% url 'imports:import_hub' %}">Administración → Importación</a> — carga unificada.</li>
00037|      </ol>
00038|    </div>
00039|  </div>
00040|  <div class="col-lg-4">
00041|    <div class="card border-0 shadow-sm">
00042|      <div class="card-header bg-white fw-semibold">Carga de datos</div>
00043|      <div class="card-body small">
00044|        <p>En producción: <code>python manage.py bootstrap_wcg_demo</code></p>
00045|        <p class="mb-0">O suba archivos en <a href="{% url 'imports:import_hub' %}">Administración → Importación General</a>.</p>
00046|      </div>
00047|    </div>
00048|  </div>
00049|</div>
00050|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1HdcOtYSBkZSB1c28g4oCUIFdDR3slIGVuZGJsb2NrICV9CnslIGJsb2NrIGNvbnRlbnQgJX0KPGRpdiBjbGFzcz0ibWItNCBtdC0yIj4KICA8aDEgY2xhc3M9ImgzIGZ3LXNlbWlib2xkIG1iLTEiPkd1w61hIGRlIHVzbyDigJQgV0NHPC9oMT4KICA8cCBjbGFzcz0idGV4dC1tdXRlZCBtYi0wIj5SZWZlcmVuY2lhIHLDoXBpZGEgcGFyYSBkZW1vIGludGVybmEgeSB1c28gZ2VyZW5jaWFsLjwvcD4KPC9kaXY+Cgo8ZGl2IGNsYXNzPSJyb3cgZy0zIj4KICA8ZGl2IGNsYXNzPSJjb2wtbGctOCI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSBtYi0zIj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIgYmctd2hpdGUgZnctc2VtaWJvbGQiPsK/UXXDqSBlcyBjYWRhIG3Ds2R1bG8/PC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtYm9keSBzbWFsbCI+CiAgICAgICAgPGRsPgogICAgICAgICAgPGR0PkNSTSDigJQgQ2xpZW50ZXM8L2R0PgogICAgICAgICAgPGRkIGNsYXNzPSJtYi0zIj5NYWVzdHJvIGRlIGVudGlkYWRlcywgY29udGFjdG9zLCBwcm9kdWN0b3MgV0NGL1dDTC9XQ0ksIGludGVyYWNjaW9uZXMgeSB0YXJlYXMuPC9kZD4KICAgICAgICAgIDxkdD5CYWzDs24gZGUgUmllc2dvPC9kdD4KICAgICAgICAgIDxkZCBjbGFzcz0ibWItMyI+TW9yYSB5IHNhbGRvcyB2ZW5jaWRvcyBwb3Igb3BlcmFjacOzbiAoc25hcHNob3RzIGxlYXNpbmcgKyByZW50YXMpLjwvZGQ+CiAgICAgICAgICA8ZHQ+UEdPIOKAlCBPcGVyYWNpw7NuPC9kdD4KICAgICAgICAgIDxkZCBjbGFzcz0ibWItMyI+VGlja2V0cyBoZWxwZGVzaywgdGllbXBvcywgU0xBIHkgcmVzdWx0YWRvcyBwb3IgcGVyw61vZG8uPC9kZD4KICAgICAgICAgIDxkdD5QR0M8L2R0PgogICAgICAgICAgPGRkIGNsYXNzPSJtYi0wIj5QbGFuIGNvbWVyY2lhbCwgY2xpZW50ZXMgbnVldm9zIHkgdmVudGEgY3J1emFkYSAoPGNvZGU+L3BnYy88L2NvZGU+KS48L2RkPgogICAgICAgIDwvZGw+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20gbWItMyI+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtaGVhZGVyIGJnLXdoaXRlIGZ3LXNlbWlib2xkIj5SdXRhIHN1Z2VyaWRhIHBhcmEgZGVtbyAoMTXigJMyMCBtaW4pPC9kaXY+CiAgICAgIDxvbCBjbGFzcz0ibGlzdC1ncm91cCBsaXN0LWdyb3VwLWZsdXNoIHNtYWxsIj4KICAgICAgICA8bGkgY2xhc3M9Imxpc3QtZ3JvdXAtaXRlbSI+PHN0cm9uZz4xLjwvc3Ryb25nPiA8YSBocmVmPSJ7JSB1cmwgJ3BvcnRhbDpob21lJyAlfSI+TWVuw7ogcHJpbmNpcGFsPC9hPiDigJQgbGFzIGN1YXRybyBvcGNpb25lcyBkZWwgcHJvZHVjdG8uPC9saT4KICAgICAgICA8bGkgY2xhc3M9Imxpc3QtZ3JvdXAtaXRlbSI+PHN0cm9uZz4yLjwvc3Ryb25nPiA8YSBocmVmPSJ7JSB1cmwgJ3BnYzpkYXNoYm9hcmQnICV9Ij7wn5OKIFBHQzwvYT4g4oCUIHBsYW4gY29tZXJjaWFsLjwvbGk+CiAgICAgICAgPGxpIGNsYXNzPSJsaXN0LWdyb3VwLWl0ZW0iPjxzdHJvbmc+My48L3N0cm9uZz4gPGEgaHJlZj0ieyUgdXJsICdwZ286ZGFzaGJvYXJkJyAlfSI+4pqZ77iPIFBHTzwvYT4g4oCUIHRpY2tldHMgeSBTTEEuPC9saT4KICAgICAgICA8bGkgY2xhc3M9Imxpc3QtZ3JvdXAtaXRlbSI+PHN0cm9uZz40Ljwvc3Ryb25nPiA8YSBocmVmPSJ7JSB1cmwgJ2NybTplbnRpZGFkX2xpc3QnICV9Ij7wn5GlIENSTTwvYT4g4oCUIGxpc3RhZG8sIGZpbHRyb3MsIGRldGFsbGUsIGV4cG9ydCBDU1YuPC9saT4KICAgICAgICA8bGkgY2xhc3M9Imxpc3QtZ3JvdXAtaXRlbSI+PHN0cm9uZz41Ljwvc3Ryb25nPiA8YSBocmVmPSJ7JSB1cmwgJ3Jpc2s6Y29tYW5kb19iYWxvbicgJX0iPuKavSBDb21hbmRvIEJhbMOzbjwvYT4g4oCUIG1vcmEsIGFsZXJ0YXMsIGhpc3RvcmlhbC48L2xpPgogICAgICAgIDxsaSBjbGFzcz0ibGlzdC1ncm91cC1pdGVtIj48c3Ryb25nPjYuPC9zdHJvbmc+IDxhIGhyZWY9InslIHVybCAncG9ydGFsOmVzdGFkbycgJX0iPkVzdGFkbyBkZWwgc2lzdGVtYTwvYT4g4oCUIEtQSXMgZSBpbXBvcnRhY2lvbmVzIHJlY2llbnRlcy48L2xpPgogICAgICAgIDxsaSBjbGFzcz0ibGlzdC1ncm91cC1pdGVtIj48c3Ryb25nPjcuPC9zdHJvbmc+IDxhIGhyZWY9InslIHVybCAnaW1wb3J0czppbXBvcnRfaHViJyAlfSI+QWRtaW5pc3RyYWNpw7NuIOKGkiBJbXBvcnRhY2nDs248L2E+IOKAlCBjYXJnYSB1bmlmaWNhZGEuPC9saT4KICAgICAgPC9vbD4KICAgIDwvZGl2PgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1sZy00Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIgYmctd2hpdGUgZnctc2VtaWJvbGQiPkNhcmdhIGRlIGRhdG9zPC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtYm9keSBzbWFsbCI+CiAgICAgICAgPHA+RW4gcHJvZHVjY2nDs246IDxjb2RlPnB5dGhvbiBtYW5hZ2UucHkgYm9vdHN0cmFwX3djZ19kZW1vPC9jb2RlPjwvcD4KICAgICAgICA8cCBjbGFzcz0ibWItMCI+TyBzdWJhIGFyY2hpdm9zIGVuIDxhIGhyZWY9InslIHVybCAnaW1wb3J0czppbXBvcnRfaHViJyAlfSI+QWRtaW5pc3RyYWNpw7NuIOKGkiBJbXBvcnRhY2nDs24gR2VuZXJhbDwvYT4uPC9wPgogICAgICA8L2Rpdj4KICAgIDwvZGl2PgogIDwvZGl2Pgo8L2Rpdj4KeyUgZW5kYmxvY2sgJX0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/portal/estado.html
PATH_JSON="templates/portal/estado.html"
FILENAME=estado.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=97
SIZE_BYTES_UTF8=3694
CONTENT_SHA256=d9c85d511e01c93787170117a66d3ccb87e357e8a76b162bbd6b77d2ffc821ec
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
{% extends "base_wcg.html" %}
{% block title %}Estado del sistema — WCG{% endblock %}
{% block content %}
<div class="page-toolbar">
  <div>
    <p class="text-muted small mb-1 text-uppercase" style="letter-spacing:0.04em;font-weight:600;">Información</p>
    <h1 class="h3 mb-1">Estado del sistema</h1>
    <p class="text-muted mb-0">Resumen operativo e importaciones recientes. Las cargas de datos se hacen en Administración.</p>
  </div>
  <a class="wcg-home-link" href="{% url 'portal:home' %}">← Menú principal</a>
</div>

<div class="row g-3 mb-4">
  <div class="col-md-2 col-6">
    <div class="card border-0 h-100">
      <div class="card-body text-center py-3">
        <div class="stat-value">{{ stats.entidades_total }}</div>
        <div class="text-muted small">Entidades CRM</div>
        <div class="text-muted small">({{ stats.entidades_activas }} activas)</div>
      </div>
    </div>
  </div>
  <div class="col-md-2 col-6">
    <div class="card border-0 h-100">
      <div class="card-body text-center py-3">
        <div class="stat-value">{{ stats.tickets_total }}</div>
        <div class="text-muted small">Tickets PGO</div>
        <div class="text-muted small">({{ stats.tickets_abiertos }} abiertos)</div>
      </div>
    </div>
  </div>
  <div class="col-md-2 col-6">
    <div class="card border-0 h-100">
      <div class="card-body text-center py-3">
        <div class="stat-value">{{ stats.operaciones_riesgo }}</div>
        <div class="text-muted small">Operaciones riesgo</div>
        <div class="text-muted small">({{ stats.alertas_riesgo }} alertas)</div>
      </div>
    </div>
  </div>
  <div class="col-md-2 col-6">
    <div class="card border-0 h-100">
      <div class="card-body text-center py-3">
        <div class="stat-value">{{ stats.tareas_pendientes }}</div>
        <div class="text-muted small">Tareas CRM pendientes</div>
      </div>
    </div>
  </div>
  <div class="col-md-2 col-6">
    <div class="card border-0 h-100">
      <div class="card-body text-center py-3">
        <div class="stat-value">{{ stats.lotes_importacion }}</div>
        <div class="text-muted small">Lotes de importación</div>
      </div>
    </div>
  </div>
  <div class="col-md-2 col-6">
    <div class="card border-0 h-100">
      <div class="card-body text-center py-3">
        <div class="stat-value">{{ stats.snapshots }}</div>
        <div class="text-muted small">Snapshots riesgo</div>
      </div>
    </div>
  </div>
</div>

<div class="card border-0">
  <div class="card-header bg-white fw-semibold d-flex justify-content-between align-items-center">
    <span>Importaciones recientes</span>
    <a href="{% url 'imports:import_hub' %}" class="small">Administración → Importación</a>
  </div>
  <div class="table-responsive">
    <table class="table table-sm table-hover mb-0">
      <thead>
        <tr><th>Fecha</th><th>Módulo</th><th>Archivo</th><th>Estado</th><th>C/A/E</th></tr>
      </thead>
      <tbody>
        {% for batch in stats.importaciones_recientes %}
        <tr>
          <td>{{ batch.created_at|date:"d/m/Y H:i" }}</td>
          <td>{{ batch.modulo }}</td>
          <td class="small">{{ batch.archivo_nombre|truncatechars:48 }}</td>
          <td><span class="badge text-bg-secondary">{{ batch.status }}</span></td>
          <td class="small">{{ batch.creados }}/{{ batch.actualizados }}/{{ batch.errores }}</td>
        </tr>
        {% empty %}
        <tr>
          <td colspan="5" class="text-center py-3 text-muted">
            Aún no hay lotes. Use Administración → Importación General.
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}Estado del sistema — WCG{% endblock %}
00003|{% block content %}
00004|<div class="page-toolbar">
00005|  <div>
00006|    <p class="text-muted small mb-1 text-uppercase" style="letter-spacing:0.04em;font-weight:600;">Información</p>
00007|    <h1 class="h3 mb-1">Estado del sistema</h1>
00008|    <p class="text-muted mb-0">Resumen operativo e importaciones recientes. Las cargas de datos se hacen en Administración.</p>
00009|  </div>
00010|  <a class="wcg-home-link" href="{% url 'portal:home' %}">← Menú principal</a>
00011|</div>
00012|
00013|<div class="row g-3 mb-4">
00014|  <div class="col-md-2 col-6">
00015|    <div class="card border-0 h-100">
00016|      <div class="card-body text-center py-3">
00017|        <div class="stat-value">{{ stats.entidades_total }}</div>
00018|        <div class="text-muted small">Entidades CRM</div>
00019|        <div class="text-muted small">({{ stats.entidades_activas }} activas)</div>
00020|      </div>
00021|    </div>
00022|  </div>
00023|  <div class="col-md-2 col-6">
00024|    <div class="card border-0 h-100">
00025|      <div class="card-body text-center py-3">
00026|        <div class="stat-value">{{ stats.tickets_total }}</div>
00027|        <div class="text-muted small">Tickets PGO</div>
00028|        <div class="text-muted small">({{ stats.tickets_abiertos }} abiertos)</div>
00029|      </div>
00030|    </div>
00031|  </div>
00032|  <div class="col-md-2 col-6">
00033|    <div class="card border-0 h-100">
00034|      <div class="card-body text-center py-3">
00035|        <div class="stat-value">{{ stats.operaciones_riesgo }}</div>
00036|        <div class="text-muted small">Operaciones riesgo</div>
00037|        <div class="text-muted small">({{ stats.alertas_riesgo }} alertas)</div>
00038|      </div>
00039|    </div>
00040|  </div>
00041|  <div class="col-md-2 col-6">
00042|    <div class="card border-0 h-100">
00043|      <div class="card-body text-center py-3">
00044|        <div class="stat-value">{{ stats.tareas_pendientes }}</div>
00045|        <div class="text-muted small">Tareas CRM pendientes</div>
00046|      </div>
00047|    </div>
00048|  </div>
00049|  <div class="col-md-2 col-6">
00050|    <div class="card border-0 h-100">
00051|      <div class="card-body text-center py-3">
00052|        <div class="stat-value">{{ stats.lotes_importacion }}</div>
00053|        <div class="text-muted small">Lotes de importación</div>
00054|      </div>
00055|    </div>
00056|  </div>
00057|  <div class="col-md-2 col-6">
00058|    <div class="card border-0 h-100">
00059|      <div class="card-body text-center py-3">
00060|        <div class="stat-value">{{ stats.snapshots }}</div>
00061|        <div class="text-muted small">Snapshots riesgo</div>
00062|      </div>
00063|    </div>
00064|  </div>
00065|</div>
00066|
00067|<div class="card border-0">
00068|  <div class="card-header bg-white fw-semibold d-flex justify-content-between align-items-center">
00069|    <span>Importaciones recientes</span>
00070|    <a href="{% url 'imports:import_hub' %}" class="small">Administración → Importación</a>
00071|  </div>
00072|  <div class="table-responsive">
00073|    <table class="table table-sm table-hover mb-0">
00074|      <thead>
00075|        <tr><th>Fecha</th><th>Módulo</th><th>Archivo</th><th>Estado</th><th>C/A/E</th></tr>
00076|      </thead>
00077|      <tbody>
00078|        {% for batch in stats.importaciones_recientes %}
00079|        <tr>
00080|          <td>{{ batch.created_at|date:"d/m/Y H:i" }}</td>
00081|          <td>{{ batch.modulo }}</td>
00082|          <td class="small">{{ batch.archivo_nombre|truncatechars:48 }}</td>
00083|          <td><span class="badge text-bg-secondary">{{ batch.status }}</span></td>
00084|          <td class="small">{{ batch.creados }}/{{ batch.actualizados }}/{{ batch.errores }}</td>
00085|        </tr>
00086|        {% empty %}
00087|        <tr>
00088|          <td colspan="5" class="text-center py-3 text-muted">
00089|            Aún no hay lotes. Use Administración → Importación General.
00090|          </td>
00091|        </tr>
00092|        {% endfor %}
00093|      </tbody>
00094|    </table>
00095|  </div>
00096|</div>
00097|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1Fc3RhZG8gZGVsIHNpc3RlbWEg4oCUIFdDR3slIGVuZGJsb2NrICV9CnslIGJsb2NrIGNvbnRlbnQgJX0KPGRpdiBjbGFzcz0icGFnZS10b29sYmFyIj4KICA8ZGl2PgogICAgPHAgY2xhc3M9InRleHQtbXV0ZWQgc21hbGwgbWItMSB0ZXh0LXVwcGVyY2FzZSIgc3R5bGU9ImxldHRlci1zcGFjaW5nOjAuMDRlbTtmb250LXdlaWdodDo2MDA7Ij5JbmZvcm1hY2nDs248L3A+CiAgICA8aDEgY2xhc3M9ImgzIG1iLTEiPkVzdGFkbyBkZWwgc2lzdGVtYTwvaDE+CiAgICA8cCBjbGFzcz0idGV4dC1tdXRlZCBtYi0wIj5SZXN1bWVuIG9wZXJhdGl2byBlIGltcG9ydGFjaW9uZXMgcmVjaWVudGVzLiBMYXMgY2FyZ2FzIGRlIGRhdG9zIHNlIGhhY2VuIGVuIEFkbWluaXN0cmFjacOzbi48L3A+CiAgPC9kaXY+CiAgPGEgY2xhc3M9IndjZy1ob21lLWxpbmsiIGhyZWY9InslIHVybCAncG9ydGFsOmhvbWUnICV9Ij7ihpAgTWVuw7ogcHJpbmNpcGFsPC9hPgo8L2Rpdj4KCjxkaXYgY2xhc3M9InJvdyBnLTMgbWItNCI+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTIgY29sLTYiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBoLTEwMCI+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtYm9keSB0ZXh0LWNlbnRlciBweS0zIj4KICAgICAgICA8ZGl2IGNsYXNzPSJzdGF0LXZhbHVlIj57eyBzdGF0cy5lbnRpZGFkZXNfdG90YWwgfX08L2Rpdj4KICAgICAgICA8ZGl2IGNsYXNzPSJ0ZXh0LW11dGVkIHNtYWxsIj5FbnRpZGFkZXMgQ1JNPC9kaXY+CiAgICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+KHt7IHN0YXRzLmVudGlkYWRlc19hY3RpdmFzIH19IGFjdGl2YXMpPC9kaXY+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTIgY29sLTYiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBoLTEwMCI+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtYm9keSB0ZXh0LWNlbnRlciBweS0zIj4KICAgICAgICA8ZGl2IGNsYXNzPSJzdGF0LXZhbHVlIj57eyBzdGF0cy50aWNrZXRzX3RvdGFsIH19PC9kaXY+CiAgICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+VGlja2V0cyBQR088L2Rpdj4KICAgICAgICA8ZGl2IGNsYXNzPSJ0ZXh0LW11dGVkIHNtYWxsIj4oe3sgc3RhdHMudGlja2V0c19hYmllcnRvcyB9fSBhYmllcnRvcyk8L2Rpdj4KICAgICAgPC9kaXY+CiAgICA8L2Rpdj4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtMiBjb2wtNiI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIGgtMTAwIj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1ib2R5IHRleHQtY2VudGVyIHB5LTMiPgogICAgICAgIDxkaXYgY2xhc3M9InN0YXQtdmFsdWUiPnt7IHN0YXRzLm9wZXJhY2lvbmVzX3JpZXNnbyB9fTwvZGl2PgogICAgICAgIDxkaXYgY2xhc3M9InRleHQtbXV0ZWQgc21hbGwiPk9wZXJhY2lvbmVzIHJpZXNnbzwvZGl2PgogICAgICAgIDxkaXYgY2xhc3M9InRleHQtbXV0ZWQgc21hbGwiPih7eyBzdGF0cy5hbGVydGFzX3JpZXNnbyB9fSBhbGVydGFzKTwvZGl2PgogICAgICA8L2Rpdj4KICAgIDwvZGl2PgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1tZC0yIGNvbC02Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgaC0xMDAiPgogICAgICA8ZGl2IGNsYXNzPSJjYXJkLWJvZHkgdGV4dC1jZW50ZXIgcHktMyI+CiAgICAgICAgPGRpdiBjbGFzcz0ic3RhdC12YWx1ZSI+e3sgc3RhdHMudGFyZWFzX3BlbmRpZW50ZXMgfX08L2Rpdj4KICAgICAgICA8ZGl2IGNsYXNzPSJ0ZXh0LW11dGVkIHNtYWxsIj5UYXJlYXMgQ1JNIHBlbmRpZW50ZXM8L2Rpdj4KICAgICAgPC9kaXY+CiAgICA8L2Rpdj4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtMiBjb2wtNiI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIGgtMTAwIj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1ib2R5IHRleHQtY2VudGVyIHB5LTMiPgogICAgICAgIDxkaXYgY2xhc3M9InN0YXQtdmFsdWUiPnt7IHN0YXRzLmxvdGVzX2ltcG9ydGFjaW9uIH19PC9kaXY+CiAgICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+TG90ZXMgZGUgaW1wb3J0YWNpw7NuPC9kaXY+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTIgY29sLTYiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBoLTEwMCI+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtYm9keSB0ZXh0LWNlbnRlciBweS0zIj4KICAgICAgICA8ZGl2IGNsYXNzPSJzdGF0LXZhbHVlIj57eyBzdGF0cy5zbmFwc2hvdHMgfX08L2Rpdj4KICAgICAgICA8ZGl2IGNsYXNzPSJ0ZXh0LW11dGVkIHNtYWxsIj5TbmFwc2hvdHMgcmllc2dvPC9kaXY+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CiAgPC9kaXY+CjwvZGl2PgoKPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCI+CiAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIgYmctd2hpdGUgZnctc2VtaWJvbGQgZC1mbGV4IGp1c3RpZnktY29udGVudC1iZXR3ZWVuIGFsaWduLWl0ZW1zLWNlbnRlciI+CiAgICA8c3Bhbj5JbXBvcnRhY2lvbmVzIHJlY2llbnRlczwvc3Bhbj4KICAgIDxhIGhyZWY9InslIHVybCAnaW1wb3J0czppbXBvcnRfaHViJyAlfSIgY2xhc3M9InNtYWxsIj5BZG1pbmlzdHJhY2nDs24g4oaSIEltcG9ydGFjacOzbjwvYT4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJ0YWJsZS1yZXNwb25zaXZlIj4KICAgIDx0YWJsZSBjbGFzcz0idGFibGUgdGFibGUtc20gdGFibGUtaG92ZXIgbWItMCI+CiAgICAgIDx0aGVhZD4KICAgICAgICA8dHI+PHRoPkZlY2hhPC90aD48dGg+TcOzZHVsbzwvdGg+PHRoPkFyY2hpdm88L3RoPjx0aD5Fc3RhZG88L3RoPjx0aD5DL0EvRTwvdGg+PC90cj4KICAgICAgPC90aGVhZD4KICAgICAgPHRib2R5PgogICAgICAgIHslIGZvciBiYXRjaCBpbiBzdGF0cy5pbXBvcnRhY2lvbmVzX3JlY2llbnRlcyAlfQogICAgICAgIDx0cj4KICAgICAgICAgIDx0ZD57eyBiYXRjaC5jcmVhdGVkX2F0fGRhdGU6ImQvbS9ZIEg6aSIgfX08L3RkPgogICAgICAgICAgPHRkPnt7IGJhdGNoLm1vZHVsbyB9fTwvdGQ+CiAgICAgICAgICA8dGQgY2xhc3M9InNtYWxsIj57eyBiYXRjaC5hcmNoaXZvX25vbWJyZXx0cnVuY2F0ZWNoYXJzOjQ4IH19PC90ZD4KICAgICAgICAgIDx0ZD48c3BhbiBjbGFzcz0iYmFkZ2UgdGV4dC1iZy1zZWNvbmRhcnkiPnt7IGJhdGNoLnN0YXR1cyB9fTwvc3Bhbj48L3RkPgogICAgICAgICAgPHRkIGNsYXNzPSJzbWFsbCI+e3sgYmF0Y2guY3JlYWRvcyB9fS97eyBiYXRjaC5hY3R1YWxpemFkb3MgfX0ve3sgYmF0Y2guZXJyb3JlcyB9fTwvdGQ+CiAgICAgICAgPC90cj4KICAgICAgICB7JSBlbXB0eSAlfQogICAgICAgIDx0cj4KICAgICAgICAgIDx0ZCBjb2xzcGFuPSI1IiBjbGFzcz0idGV4dC1jZW50ZXIgcHktMyB0ZXh0LW11dGVkIj4KICAgICAgICAgICAgQcO6biBubyBoYXkgbG90ZXMuIFVzZSBBZG1pbmlzdHJhY2nDs24g4oaSIEltcG9ydGFjacOzbiBHZW5lcmFsLgogICAgICAgICAgPC90ZD4KICAgICAgICA8L3RyPgogICAgICAgIHslIGVuZGZvciAlfQogICAgICA8L3Rib2R5PgogICAgPC90YWJsZT4KICA8L2Rpdj4KPC9kaXY+CnslIGVuZGJsb2NrICV9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/portal/home_wcgone.html
PATH_JSON="templates/portal/home_wcgone.html"
FILENAME=home_wcgone.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=151
SIZE_BYTES_UTF8=5612
CONTENT_SHA256=df2d7e06297770bb70d54fed33741f627a48fedae14fd9ccc6979a50de8841ff
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
{% extends "wcgone_base.html" %}

{% block title %}Panel principal — WCG One{% endblock %}

{% block content %}
<div class="mb-4">
  <h1 class="h3 fw-semibold mb-1">WCG One</h1>
  <p class="text-muted mb-0">
    Panel gerencial de Working Capital Group: PGC, operación (PGO), clientes (CRM)
    y riesgo operativo (Balón).
  </p>
  <p class="small mt-2 mb-0">
    <a href="{% url 'portal:ayuda' %}">Guía de demo</a>
    · Cargas en <a href="{% url 'imports:import_hub' %}">Administración → Importación</a>
  </p>
</div>

<div class="row g-3 mb-4">
  <div class="col-md-2 col-6">
    <div class="card border-0 shadow-sm h-100">
      <div class="card-body text-center py-3">
        <div class="stat-value">{{ stats.entidades_total }}</div>
        <div class="text-muted small">Entidades CRM</div>
        <div class="text-muted small">({{ stats.entidades_activas }} activas)</div>
      </div>
    </div>
  </div>
  <div class="col-md-2 col-6">
    <div class="card border-0 shadow-sm h-100">
      <div class="card-body text-center py-3">
        <div class="stat-value">{{ stats.tickets_total }}</div>
        <div class="text-muted small">Tickets PGO</div>
        <div class="text-muted small">({{ stats.tickets_abiertos }} abiertos)</div>
      </div>
    </div>
  </div>
  <div class="col-md-2 col-6">
    <div class="card border-0 shadow-sm h-100">
      <div class="card-body text-center py-3">
        <div class="stat-value">{{ stats.operaciones_riesgo }}</div>
        <div class="text-muted small">Operaciones riesgo</div>
        <div class="text-muted small">({{ stats.snapshots }} snapshots)</div>
      </div>
    </div>
  </div>
  <div class="col-md-2 col-6">
    <div class="card border-0 shadow-sm h-100">
      <div class="card-body text-center py-3">
        <div class="stat-value">{{ stats.tareas_pendientes }}</div>
        <div class="text-muted small">Tareas CRM pendientes</div>
      </div>
    </div>
  </div>
  <div class="col-md-2 col-6">
    <div class="card border-0 shadow-sm h-100">
      <div class="card-body text-center py-3">
        <div class="stat-value">{{ stats.lotes_importacion }}</div>
        <div class="text-muted small">Lotes de importación</div>
      </div>
    </div>
  </div>
</div>

<div class="row g-4">
  <div class="col-md-6 col-lg-3">
    <div class="card card-module shadow-sm h-100">
      <div class="card-header">PGC</div>
      <div class="card-body d-flex flex-column">
        <p class="text-muted small flex-grow-1">
          Plan de gestión comercial histórico. Acceso al sistema PGC legado en operación.
        </p>
        <a href="{% url 'pgc:module_home' %}" class="btn btn-outline-primary btn-sm">Ir a PGC</a>
      </div>
    </div>
  </div>
  <div class="col-md-6 col-lg-3">
    <div class="card card-module shadow-sm h-100">
      <div class="card-header">PGO</div>
      <div class="card-body d-flex flex-column">
        <p class="text-muted small flex-grow-1">
          Indicadores de operación interna: tickets de helpdesk, tiempos de atención y cumplimiento de SLA.
        </p>
        <a href="{% url 'pgo:dashboard' %}" class="btn btn-outline-primary btn-sm">Dashboard</a>
      </div>
    </div>
  </div>
  <div class="col-md-6 col-lg-3">
    <div class="card card-module shadow-sm h-100">
      <div class="card-header">CRM</div>
      <div class="card-body d-flex flex-column">
        <p class="text-muted small flex-grow-1">
          Maestro único de clientes y prospectos: entidades, contactos, productos y seguimiento comercial.
        </p>
        <a href="{% url 'crm:entidad_list' %}" class="btn btn-outline-primary btn-sm">Ver clientes</a>
      </div>
    </div>
  </div>
  <div class="col-md-6 col-lg-3">
    <div class="card card-module shadow-sm h-100">
      <div class="card-header">Balón de Riesgo</div>
      <div class="card-body d-flex flex-column">
        <p class="text-muted small flex-grow-1">
          Cuadro de alerta operativa: mora, saldos vencidos y evolución por operación (snapshots leasing).
        </p>
        <a href="{% url 'risk:comando_balon' %}" class="btn btn-outline-primary btn-sm">Comando Balón</a>
      </div>
    </div>
  </div>
</div>

<div class="card border-0 shadow-sm mt-4">
  <div class="card-header bg-white fw-semibold d-flex justify-content-between">
    <span>Importaciones recientes</span>
    <a href="{% url 'imports:import_hub' %}" class="small">Administración → Importación</a>
  </div>
  <div class="table-responsive">
    <table class="table table-sm table-hover mb-0">
      <thead>
        <tr>
          <th>Fecha</th>
          <th>Módulo</th>
          <th>Archivo</th>
          <th>Estado</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {% for batch in stats.importaciones_recientes %}
        <tr>
          <td>{{ batch.fecha_carga|date:"d/m/Y H:i" }}</td>
          <td>{{ batch.modulo|upper }}</td>
          <td>{{ batch.archivo_nombre }}</td>
          <td><span class="badge text-bg-secondary">{{ batch.get_estado_display }}</span></td>
          <td class="text-end">
            <a href="{% url 'wcgone_core:import_batch_detail' batch.pk %}" class="btn btn-sm btn-link">Detalle</a>
          </td>
        </tr>
        {% empty %}
        <tr>
          <td colspan="5" class="text-center py-3">
            <div class="alert alert-info mb-0 small">
              Aún no hay importaciones. Use <strong>Administración → Importación General</strong>.
            </div>
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "wcgone_base.html" %}
00002|
00003|{% block title %}Panel principal — WCG One{% endblock %}
00004|
00005|{% block content %}
00006|<div class="mb-4">
00007|  <h1 class="h3 fw-semibold mb-1">WCG One</h1>
00008|  <p class="text-muted mb-0">
00009|    Panel gerencial de Working Capital Group: PGC, operación (PGO), clientes (CRM)
00010|    y riesgo operativo (Balón).
00011|  </p>
00012|  <p class="small mt-2 mb-0">
00013|    <a href="{% url 'portal:ayuda' %}">Guía de demo</a>
00014|    · Cargas en <a href="{% url 'imports:import_hub' %}">Administración → Importación</a>
00015|  </p>
00016|</div>
00017|
00018|<div class="row g-3 mb-4">
00019|  <div class="col-md-2 col-6">
00020|    <div class="card border-0 shadow-sm h-100">
00021|      <div class="card-body text-center py-3">
00022|        <div class="stat-value">{{ stats.entidades_total }}</div>
00023|        <div class="text-muted small">Entidades CRM</div>
00024|        <div class="text-muted small">({{ stats.entidades_activas }} activas)</div>
00025|      </div>
00026|    </div>
00027|  </div>
00028|  <div class="col-md-2 col-6">
00029|    <div class="card border-0 shadow-sm h-100">
00030|      <div class="card-body text-center py-3">
00031|        <div class="stat-value">{{ stats.tickets_total }}</div>
00032|        <div class="text-muted small">Tickets PGO</div>
00033|        <div class="text-muted small">({{ stats.tickets_abiertos }} abiertos)</div>
00034|      </div>
00035|    </div>
00036|  </div>
00037|  <div class="col-md-2 col-6">
00038|    <div class="card border-0 shadow-sm h-100">
00039|      <div class="card-body text-center py-3">
00040|        <div class="stat-value">{{ stats.operaciones_riesgo }}</div>
00041|        <div class="text-muted small">Operaciones riesgo</div>
00042|        <div class="text-muted small">({{ stats.snapshots }} snapshots)</div>
00043|      </div>
00044|    </div>
00045|  </div>
00046|  <div class="col-md-2 col-6">
00047|    <div class="card border-0 shadow-sm h-100">
00048|      <div class="card-body text-center py-3">
00049|        <div class="stat-value">{{ stats.tareas_pendientes }}</div>
00050|        <div class="text-muted small">Tareas CRM pendientes</div>
00051|      </div>
00052|    </div>
00053|  </div>
00054|  <div class="col-md-2 col-6">
00055|    <div class="card border-0 shadow-sm h-100">
00056|      <div class="card-body text-center py-3">
00057|        <div class="stat-value">{{ stats.lotes_importacion }}</div>
00058|        <div class="text-muted small">Lotes de importación</div>
00059|      </div>
00060|    </div>
00061|  </div>
00062|</div>
00063|
00064|<div class="row g-4">
00065|  <div class="col-md-6 col-lg-3">
00066|    <div class="card card-module shadow-sm h-100">
00067|      <div class="card-header">PGC</div>
00068|      <div class="card-body d-flex flex-column">
00069|        <p class="text-muted small flex-grow-1">
00070|          Plan de gestión comercial histórico. Acceso al sistema PGC legado en operación.
00071|        </p>
00072|        <a href="{% url 'pgc:module_home' %}" class="btn btn-outline-primary btn-sm">Ir a PGC</a>
00073|      </div>
00074|    </div>
00075|  </div>
00076|  <div class="col-md-6 col-lg-3">
00077|    <div class="card card-module shadow-sm h-100">
00078|      <div class="card-header">PGO</div>
00079|      <div class="card-body d-flex flex-column">
00080|        <p class="text-muted small flex-grow-1">
00081|          Indicadores de operación interna: tickets de helpdesk, tiempos de atención y cumplimiento de SLA.
00082|        </p>
00083|        <a href="{% url 'pgo:dashboard' %}" class="btn btn-outline-primary btn-sm">Dashboard</a>
00084|      </div>
00085|    </div>
00086|  </div>
00087|  <div class="col-md-6 col-lg-3">
00088|    <div class="card card-module shadow-sm h-100">
00089|      <div class="card-header">CRM</div>
00090|      <div class="card-body d-flex flex-column">
00091|        <p class="text-muted small flex-grow-1">
00092|          Maestro único de clientes y prospectos: entidades, contactos, productos y seguimiento comercial.
00093|        </p>
00094|        <a href="{% url 'crm:entidad_list' %}" class="btn btn-outline-primary btn-sm">Ver clientes</a>
00095|      </div>
00096|    </div>
00097|  </div>
00098|  <div class="col-md-6 col-lg-3">
00099|    <div class="card card-module shadow-sm h-100">
00100|      <div class="card-header">Balón de Riesgo</div>
00101|      <div class="card-body d-flex flex-column">
00102|        <p class="text-muted small flex-grow-1">
00103|          Cuadro de alerta operativa: mora, saldos vencidos y evolución por operación (snapshots leasing).
00104|        </p>
00105|        <a href="{% url 'risk:comando_balon' %}" class="btn btn-outline-primary btn-sm">Comando Balón</a>
00106|      </div>
00107|    </div>
00108|  </div>
00109|</div>
00110|
00111|<div class="card border-0 shadow-sm mt-4">
00112|  <div class="card-header bg-white fw-semibold d-flex justify-content-between">
00113|    <span>Importaciones recientes</span>
00114|    <a href="{% url 'imports:import_hub' %}" class="small">Administración → Importación</a>
00115|  </div>
00116|  <div class="table-responsive">
00117|    <table class="table table-sm table-hover mb-0">
00118|      <thead>
00119|        <tr>
00120|          <th>Fecha</th>
00121|          <th>Módulo</th>
00122|          <th>Archivo</th>
00123|          <th>Estado</th>
00124|          <th></th>
00125|        </tr>
00126|      </thead>
00127|      <tbody>
00128|        {% for batch in stats.importaciones_recientes %}
00129|        <tr>
00130|          <td>{{ batch.fecha_carga|date:"d/m/Y H:i" }}</td>
00131|          <td>{{ batch.modulo|upper }}</td>
00132|          <td>{{ batch.archivo_nombre }}</td>
00133|          <td><span class="badge text-bg-secondary">{{ batch.get_estado_display }}</span></td>
00134|          <td class="text-end">
00135|            <a href="{% url 'wcgone_core:import_batch_detail' batch.pk %}" class="btn btn-sm btn-link">Detalle</a>
00136|          </td>
00137|        </tr>
00138|        {% empty %}
00139|        <tr>
00140|          <td colspan="5" class="text-center py-3">
00141|            <div class="alert alert-info mb-0 small">
00142|              Aún no hay importaciones. Use <strong>Administración → Importación General</strong>.
00143|            </div>
00144|          </td>
00145|        </tr>
00146|        {% endfor %}
00147|      </tbody>
00148|    </table>
00149|  </div>
00150|</div>
00151|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAid2Nnb25lX2Jhc2UuaHRtbCIgJX0KCnslIGJsb2NrIHRpdGxlICV9UGFuZWwgcHJpbmNpcGFsIOKAlCBXQ0cgT25leyUgZW5kYmxvY2sgJX0KCnslIGJsb2NrIGNvbnRlbnQgJX0KPGRpdiBjbGFzcz0ibWItNCI+CiAgPGgxIGNsYXNzPSJoMyBmdy1zZW1pYm9sZCBtYi0xIj5XQ0cgT25lPC9oMT4KICA8cCBjbGFzcz0idGV4dC1tdXRlZCBtYi0wIj4KICAgIFBhbmVsIGdlcmVuY2lhbCBkZSBXb3JraW5nIENhcGl0YWwgR3JvdXA6IFBHQywgb3BlcmFjacOzbiAoUEdPKSwgY2xpZW50ZXMgKENSTSkKICAgIHkgcmllc2dvIG9wZXJhdGl2byAoQmFsw7NuKS4KICA8L3A+CiAgPHAgY2xhc3M9InNtYWxsIG10LTIgbWItMCI+CiAgICA8YSBocmVmPSJ7JSB1cmwgJ3BvcnRhbDpheXVkYScgJX0iPkd1w61hIGRlIGRlbW88L2E+CiAgICDCtyBDYXJnYXMgZW4gPGEgaHJlZj0ieyUgdXJsICdpbXBvcnRzOmltcG9ydF9odWInICV9Ij5BZG1pbmlzdHJhY2nDs24g4oaSIEltcG9ydGFjacOzbjwvYT4KICA8L3A+CjwvZGl2PgoKPGRpdiBjbGFzcz0icm93IGctMyBtYi00Ij4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtMiBjb2wtNiI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSBoLTEwMCI+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtYm9keSB0ZXh0LWNlbnRlciBweS0zIj4KICAgICAgICA8ZGl2IGNsYXNzPSJzdGF0LXZhbHVlIj57eyBzdGF0cy5lbnRpZGFkZXNfdG90YWwgfX08L2Rpdj4KICAgICAgICA8ZGl2IGNsYXNzPSJ0ZXh0LW11dGVkIHNtYWxsIj5FbnRpZGFkZXMgQ1JNPC9kaXY+CiAgICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+KHt7IHN0YXRzLmVudGlkYWRlc19hY3RpdmFzIH19IGFjdGl2YXMpPC9kaXY+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTIgY29sLTYiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20gaC0xMDAiPgogICAgICA8ZGl2IGNsYXNzPSJjYXJkLWJvZHkgdGV4dC1jZW50ZXIgcHktMyI+CiAgICAgICAgPGRpdiBjbGFzcz0ic3RhdC12YWx1ZSI+e3sgc3RhdHMudGlja2V0c190b3RhbCB9fTwvZGl2PgogICAgICAgIDxkaXYgY2xhc3M9InRleHQtbXV0ZWQgc21hbGwiPlRpY2tldHMgUEdPPC9kaXY+CiAgICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+KHt7IHN0YXRzLnRpY2tldHNfYWJpZXJ0b3MgfX0gYWJpZXJ0b3MpPC9kaXY+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTIgY29sLTYiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20gaC0xMDAiPgogICAgICA8ZGl2IGNsYXNzPSJjYXJkLWJvZHkgdGV4dC1jZW50ZXIgcHktMyI+CiAgICAgICAgPGRpdiBjbGFzcz0ic3RhdC12YWx1ZSI+e3sgc3RhdHMub3BlcmFjaW9uZXNfcmllc2dvIH19PC9kaXY+CiAgICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+T3BlcmFjaW9uZXMgcmllc2dvPC9kaXY+CiAgICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+KHt7IHN0YXRzLnNuYXBzaG90cyB9fSBzbmFwc2hvdHMpPC9kaXY+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTIgY29sLTYiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20gaC0xMDAiPgogICAgICA8ZGl2IGNsYXNzPSJjYXJkLWJvZHkgdGV4dC1jZW50ZXIgcHktMyI+CiAgICAgICAgPGRpdiBjbGFzcz0ic3RhdC12YWx1ZSI+e3sgc3RhdHMudGFyZWFzX3BlbmRpZW50ZXMgfX08L2Rpdj4KICAgICAgICA8ZGl2IGNsYXNzPSJ0ZXh0LW11dGVkIHNtYWxsIj5UYXJlYXMgQ1JNIHBlbmRpZW50ZXM8L2Rpdj4KICAgICAgPC9kaXY+CiAgICA8L2Rpdj4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtMiBjb2wtNiI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSBoLTEwMCI+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtYm9keSB0ZXh0LWNlbnRlciBweS0zIj4KICAgICAgICA8ZGl2IGNsYXNzPSJzdGF0LXZhbHVlIj57eyBzdGF0cy5sb3Rlc19pbXBvcnRhY2lvbiB9fTwvZGl2PgogICAgICAgIDxkaXYgY2xhc3M9InRleHQtbXV0ZWQgc21hbGwiPkxvdGVzIGRlIGltcG9ydGFjacOzbjwvZGl2PgogICAgICA8L2Rpdj4KICAgIDwvZGl2PgogIDwvZGl2Pgo8L2Rpdj4KCjxkaXYgY2xhc3M9InJvdyBnLTQiPgogIDxkaXYgY2xhc3M9ImNvbC1tZC02IGNvbC1sZy0zIj4KICAgIDxkaXYgY2xhc3M9ImNhcmQgY2FyZC1tb2R1bGUgc2hhZG93LXNtIGgtMTAwIj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIiPlBHQzwvZGl2PgogICAgICA8ZGl2IGNsYXNzPSJjYXJkLWJvZHkgZC1mbGV4IGZsZXgtY29sdW1uIj4KICAgICAgICA8cCBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCBmbGV4LWdyb3ctMSI+CiAgICAgICAgICBQbGFuIGRlIGdlc3Rpw7NuIGNvbWVyY2lhbCBoaXN0w7NyaWNvLiBBY2Nlc28gYWwgc2lzdGVtYSBQR0MgbGVnYWRvIGVuIG9wZXJhY2nDs24uCiAgICAgICAgPC9wPgogICAgICAgIDxhIGhyZWY9InslIHVybCAncGdjOm1vZHVsZV9ob21lJyAlfSIgY2xhc3M9ImJ0biBidG4tb3V0bGluZS1wcmltYXJ5IGJ0bi1zbSI+SXIgYSBQR0M8L2E+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTYgY29sLWxnLTMiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBjYXJkLW1vZHVsZSBzaGFkb3ctc20gaC0xMDAiPgogICAgICA8ZGl2IGNsYXNzPSJjYXJkLWhlYWRlciI+UEdPPC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtYm9keSBkLWZsZXggZmxleC1jb2x1bW4iPgogICAgICAgIDxwIGNsYXNzPSJ0ZXh0LW11dGVkIHNtYWxsIGZsZXgtZ3Jvdy0xIj4KICAgICAgICAgIEluZGljYWRvcmVzIGRlIG9wZXJhY2nDs24gaW50ZXJuYTogdGlja2V0cyBkZSBoZWxwZGVzaywgdGllbXBvcyBkZSBhdGVuY2nDs24geSBjdW1wbGltaWVudG8gZGUgU0xBLgogICAgICAgIDwvcD4KICAgICAgICA8YSBocmVmPSJ7JSB1cmwgJ3BnbzpkYXNoYm9hcmQnICV9IiBjbGFzcz0iYnRuIGJ0bi1vdXRsaW5lLXByaW1hcnkgYnRuLXNtIj5EYXNoYm9hcmQ8L2E+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTYgY29sLWxnLTMiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBjYXJkLW1vZHVsZSBzaGFkb3ctc20gaC0xMDAiPgogICAgICA8ZGl2IGNsYXNzPSJjYXJkLWhlYWRlciI+Q1JNPC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtYm9keSBkLWZsZXggZmxleC1jb2x1bW4iPgogICAgICAgIDxwIGNsYXNzPSJ0ZXh0LW11dGVkIHNtYWxsIGZsZXgtZ3Jvdy0xIj4KICAgICAgICAgIE1hZXN0cm8gw7puaWNvIGRlIGNsaWVudGVzIHkgcHJvc3BlY3RvczogZW50aWRhZGVzLCBjb250YWN0b3MsIHByb2R1Y3RvcyB5IHNlZ3VpbWllbnRvIGNvbWVyY2lhbC4KICAgICAgICA8L3A+CiAgICAgICAgPGEgaHJlZj0ieyUgdXJsICdjcm06ZW50aWRhZF9saXN0JyAlfSIgY2xhc3M9ImJ0biBidG4tb3V0bGluZS1wcmltYXJ5IGJ0bi1zbSI+VmVyIGNsaWVudGVzPC9hPgogICAgICA8L2Rpdj4KICAgIDwvZGl2PgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1tZC02IGNvbC1sZy0zIj4KICAgIDxkaXYgY2xhc3M9ImNhcmQgY2FyZC1tb2R1bGUgc2hhZG93LXNtIGgtMTAwIj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIiPkJhbMOzbiBkZSBSaWVzZ288L2Rpdj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1ib2R5IGQtZmxleCBmbGV4LWNvbHVtbiI+CiAgICAgICAgPHAgY2xhc3M9InRleHQtbXV0ZWQgc21hbGwgZmxleC1ncm93LTEiPgogICAgICAgICAgQ3VhZHJvIGRlIGFsZXJ0YSBvcGVyYXRpdmE6IG1vcmEsIHNhbGRvcyB2ZW5jaWRvcyB5IGV2b2x1Y2nDs24gcG9yIG9wZXJhY2nDs24gKHNuYXBzaG90cyBsZWFzaW5nKS4KICAgICAgICA8L3A+CiAgICAgICAgPGEgaHJlZj0ieyUgdXJsICdyaXNrOmNvbWFuZG9fYmFsb24nICV9IiBjbGFzcz0iYnRuIGJ0bi1vdXRsaW5lLXByaW1hcnkgYnRuLXNtIj5Db21hbmRvIEJhbMOzbjwvYT4KICAgICAgPC9kaXY+CiAgICA8L2Rpdj4KICA8L2Rpdj4KPC9kaXY+Cgo8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSBtdC00Ij4KICA8ZGl2IGNsYXNzPSJjYXJkLWhlYWRlciBiZy13aGl0ZSBmdy1zZW1pYm9sZCBkLWZsZXgganVzdGlmeS1jb250ZW50LWJldHdlZW4iPgogICAgPHNwYW4+SW1wb3J0YWNpb25lcyByZWNpZW50ZXM8L3NwYW4+CiAgICA8YSBocmVmPSJ7JSB1cmwgJ2ltcG9ydHM6aW1wb3J0X2h1YicgJX0iIGNsYXNzPSJzbWFsbCI+QWRtaW5pc3RyYWNpw7NuIOKGkiBJbXBvcnRhY2nDs248L2E+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0idGFibGUtcmVzcG9uc2l2ZSI+CiAgICA8dGFibGUgY2xhc3M9InRhYmxlIHRhYmxlLXNtIHRhYmxlLWhvdmVyIG1iLTAiPgogICAgICA8dGhlYWQ+CiAgICAgICAgPHRyPgogICAgICAgICAgPHRoPkZlY2hhPC90aD4KICAgICAgICAgIDx0aD5Nw7NkdWxvPC90aD4KICAgICAgICAgIDx0aD5BcmNoaXZvPC90aD4KICAgICAgICAgIDx0aD5Fc3RhZG88L3RoPgogICAgICAgICAgPHRoPjwvdGg+CiAgICAgICAgPC90cj4KICAgICAgPC90aGVhZD4KICAgICAgPHRib2R5PgogICAgICAgIHslIGZvciBiYXRjaCBpbiBzdGF0cy5pbXBvcnRhY2lvbmVzX3JlY2llbnRlcyAlfQogICAgICAgIDx0cj4KICAgICAgICAgIDx0ZD57eyBiYXRjaC5mZWNoYV9jYXJnYXxkYXRlOiJkL20vWSBIOmkiIH19PC90ZD4KICAgICAgICAgIDx0ZD57eyBiYXRjaC5tb2R1bG98dXBwZXIgfX08L3RkPgogICAgICAgICAgPHRkPnt7IGJhdGNoLmFyY2hpdm9fbm9tYnJlIH19PC90ZD4KICAgICAgICAgIDx0ZD48c3BhbiBjbGFzcz0iYmFkZ2UgdGV4dC1iZy1zZWNvbmRhcnkiPnt7IGJhdGNoLmdldF9lc3RhZG9fZGlzcGxheSB9fTwvc3Bhbj48L3RkPgogICAgICAgICAgPHRkIGNsYXNzPSJ0ZXh0LWVuZCI+CiAgICAgICAgICAgIDxhIGhyZWY9InslIHVybCAnd2Nnb25lX2NvcmU6aW1wb3J0X2JhdGNoX2RldGFpbCcgYmF0Y2gucGsgJX0iIGNsYXNzPSJidG4gYnRuLXNtIGJ0bi1saW5rIj5EZXRhbGxlPC9hPgogICAgICAgICAgPC90ZD4KICAgICAgICA8L3RyPgogICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgPHRyPgogICAgICAgICAgPHRkIGNvbHNwYW49IjUiIGNsYXNzPSJ0ZXh0LWNlbnRlciBweS0zIj4KICAgICAgICAgICAgPGRpdiBjbGFzcz0iYWxlcnQgYWxlcnQtaW5mbyBtYi0wIHNtYWxsIj4KICAgICAgICAgICAgICBBw7puIG5vIGhheSBpbXBvcnRhY2lvbmVzLiBVc2UgPHN0cm9uZz5BZG1pbmlzdHJhY2nDs24g4oaSIEltcG9ydGFjacOzbiBHZW5lcmFsPC9zdHJvbmc+LgogICAgICAgICAgICA8L2Rpdj4KICAgICAgICAgIDwvdGQ+CiAgICAgICAgPC90cj4KICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgPC90Ym9keT4KICAgIDwvdGFibGU+CiAgPC9kaXY+CjwvZGl2Pgp7JSBlbmRibG9jayAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/portal/splash_wcgone.html
PATH_JSON="templates/portal/splash_wcgone.html"
FILENAME=splash_wcgone.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=117
SIZE_BYTES_UTF8=2911
CONTENT_SHA256=3658c2c4e1b82f0452b0d4bfac382a5217b19c5c08d102a6be782212e5250314
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
{% load static %}
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>WCG One</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; }
    html, body {
      margin: 0;
      height: 100%;
      background: #0f1a2e;
      font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    }
    .splash-page {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0;
    }
    .splash-enter {
      position: relative;
      display: block;
      width: 100%;
      max-width: 100vw;
      max-height: 100vh;
      margin: 0;
      padding: 0;
      border: none;
      background: transparent;
      cursor: pointer;
      text-decoration: none;
      color: inherit;
      outline: none;
    }
    .splash-enter:focus-visible {
      outline: 2px solid rgba(255, 255, 255, 0.85);
      outline-offset: 4px;
    }
    .splash-enter picture,
    .splash-enter img {
      display: block;
      width: 100%;
      max-height: 100vh;
      object-fit: contain;
      margin: 0 auto;
    }
    .splash-overlay {
      position: absolute;
      left: 50%;
      bottom: clamp(1.25rem, 4vw, 2.5rem);
      transform: translateX(-50%);
      text-align: center;
      color: #fff;
      text-shadow: 0 1px 8px rgba(0, 0, 0, 0.65);
      pointer-events: none;
      padding: 0 1rem;
      max-width: 90vw;
    }
    .splash-overlay .lead {
      margin: 0 0 0.35rem;
      font-size: clamp(1rem, 2.5vw, 1.25rem);
      font-weight: 500;
      letter-spacing: 0.02em;
    }
    .splash-overlay .hint {
      margin: 0;
      font-size: clamp(0.75rem, 1.8vw, 0.875rem);
      opacity: 0.88;
    }
  </style>
</head>
<body>
  <div class="splash-page">
    <a
      href="{% url 'portal:home' %}"
      class="splash-enter"
      id="splash-enter"
      aria-label="Entrar a WCG One"
    >
      <picture>
        <source
          media="(max-width: 767px)"
          srcset="{% static 'portal/img/wcg_splash_v1v.jpg' %}"
        >
        <img
          src="{% static 'portal/img/wcg_splash_v1h.jpg' %}"
          alt="Working Capital Group — WCG One"
          width="1920"
          height="1080"
        >
      </picture>
      <div class="splash-overlay">
        <p class="lead">Haga clic para entrar</p>
        <p class="hint">También puede presionar Enter o Espacio</p>
      </div>
    </a>
  </div>
  <script>
    (function () {
      var link = document.getElementById("splash-enter");
      function goPanel() {
        window.location.href = link.href;
      }
      document.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " " || e.code === "Space") {
          e.preventDefault();
          goPanel();
        }
      });
      link.focus();
    })();
  </script>
</body>
</html>

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% load static %}
00002|<!DOCTYPE html>
00003|<html lang="es">
00004|<head>
00005|  <meta charset="utf-8">
00006|  <meta name="viewport" content="width=device-width, initial-scale=1">
00007|  <title>WCG One</title>
00008|  <style>
00009|    *, *::before, *::after { box-sizing: border-box; }
00010|    html, body {
00011|      margin: 0;
00012|      height: 100%;
00013|      background: #0f1a2e;
00014|      font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
00015|    }
00016|    .splash-page {
00017|      min-height: 100vh;
00018|      display: flex;
00019|      align-items: center;
00020|      justify-content: center;
00021|      padding: 0;
00022|    }
00023|    .splash-enter {
00024|      position: relative;
00025|      display: block;
00026|      width: 100%;
00027|      max-width: 100vw;
00028|      max-height: 100vh;
00029|      margin: 0;
00030|      padding: 0;
00031|      border: none;
00032|      background: transparent;
00033|      cursor: pointer;
00034|      text-decoration: none;
00035|      color: inherit;
00036|      outline: none;
00037|    }
00038|    .splash-enter:focus-visible {
00039|      outline: 2px solid rgba(255, 255, 255, 0.85);
00040|      outline-offset: 4px;
00041|    }
00042|    .splash-enter picture,
00043|    .splash-enter img {
00044|      display: block;
00045|      width: 100%;
00046|      max-height: 100vh;
00047|      object-fit: contain;
00048|      margin: 0 auto;
00049|    }
00050|    .splash-overlay {
00051|      position: absolute;
00052|      left: 50%;
00053|      bottom: clamp(1.25rem, 4vw, 2.5rem);
00054|      transform: translateX(-50%);
00055|      text-align: center;
00056|      color: #fff;
00057|      text-shadow: 0 1px 8px rgba(0, 0, 0, 0.65);
00058|      pointer-events: none;
00059|      padding: 0 1rem;
00060|      max-width: 90vw;
00061|    }
00062|    .splash-overlay .lead {
00063|      margin: 0 0 0.35rem;
00064|      font-size: clamp(1rem, 2.5vw, 1.25rem);
00065|      font-weight: 500;
00066|      letter-spacing: 0.02em;
00067|    }
00068|    .splash-overlay .hint {
00069|      margin: 0;
00070|      font-size: clamp(0.75rem, 1.8vw, 0.875rem);
00071|      opacity: 0.88;
00072|    }
00073|  </style>
00074|</head>
00075|<body>
00076|  <div class="splash-page">
00077|    <a
00078|      href="{% url 'portal:home' %}"
00079|      class="splash-enter"
00080|      id="splash-enter"
00081|      aria-label="Entrar a WCG One"
00082|    >
00083|      <picture>
00084|        <source
00085|          media="(max-width: 767px)"
00086|          srcset="{% static 'portal/img/wcg_splash_v1v.jpg' %}"
00087|        >
00088|        <img
00089|          src="{% static 'portal/img/wcg_splash_v1h.jpg' %}"
00090|          alt="Working Capital Group — WCG One"
00091|          width="1920"
00092|          height="1080"
00093|        >
00094|      </picture>
00095|      <div class="splash-overlay">
00096|        <p class="lead">Haga clic para entrar</p>
00097|        <p class="hint">También puede presionar Enter o Espacio</p>
00098|      </div>
00099|    </a>
00100|  </div>
00101|  <script>
00102|    (function () {
00103|      var link = document.getElementById("splash-enter");
00104|      function goPanel() {
00105|        window.location.href = link.href;
00106|      }
00107|      document.addEventListener("keydown", function (e) {
00108|        if (e.key === "Enter" || e.key === " " || e.code === "Space") {
00109|          e.preventDefault();
00110|          goPanel();
00111|        }
00112|      });
00113|      link.focus();
00114|    })();
00115|  </script>
00116|</body>
00117|</html>

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgbG9hZCBzdGF0aWMgJX0KPCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVzIj4KPGhlYWQ+CiAgPG1ldGEgY2hhcnNldD0idXRmLTgiPgogIDxtZXRhIG5hbWU9InZpZXdwb3J0IiBjb250ZW50PSJ3aWR0aD1kZXZpY2Utd2lkdGgsIGluaXRpYWwtc2NhbGU9MSI+CiAgPHRpdGxlPldDRyBPbmU8L3RpdGxlPgogIDxzdHlsZT4KICAgICosICo6OmJlZm9yZSwgKjo6YWZ0ZXIgeyBib3gtc2l6aW5nOiBib3JkZXItYm94OyB9CiAgICBodG1sLCBib2R5IHsKICAgICAgbWFyZ2luOiAwOwogICAgICBoZWlnaHQ6IDEwMCU7CiAgICAgIGJhY2tncm91bmQ6ICMwZjFhMmU7CiAgICAgIGZvbnQtZmFtaWx5OiBzeXN0ZW0tdWksIC1hcHBsZS1zeXN0ZW0sICJTZWdvZSBVSSIsIFJvYm90bywgc2Fucy1zZXJpZjsKICAgIH0KICAgIC5zcGxhc2gtcGFnZSB7CiAgICAgIG1pbi1oZWlnaHQ6IDEwMHZoOwogICAgICBkaXNwbGF5OiBmbGV4OwogICAgICBhbGlnbi1pdGVtczogY2VudGVyOwogICAgICBqdXN0aWZ5LWNvbnRlbnQ6IGNlbnRlcjsKICAgICAgcGFkZGluZzogMDsKICAgIH0KICAgIC5zcGxhc2gtZW50ZXIgewogICAgICBwb3NpdGlvbjogcmVsYXRpdmU7CiAgICAgIGRpc3BsYXk6IGJsb2NrOwogICAgICB3aWR0aDogMTAwJTsKICAgICAgbWF4LXdpZHRoOiAxMDB2dzsKICAgICAgbWF4LWhlaWdodDogMTAwdmg7CiAgICAgIG1hcmdpbjogMDsKICAgICAgcGFkZGluZzogMDsKICAgICAgYm9yZGVyOiBub25lOwogICAgICBiYWNrZ3JvdW5kOiB0cmFuc3BhcmVudDsKICAgICAgY3Vyc29yOiBwb2ludGVyOwogICAgICB0ZXh0LWRlY29yYXRpb246IG5vbmU7CiAgICAgIGNvbG9yOiBpbmhlcml0OwogICAgICBvdXRsaW5lOiBub25lOwogICAgfQogICAgLnNwbGFzaC1lbnRlcjpmb2N1cy12aXNpYmxlIHsKICAgICAgb3V0bGluZTogMnB4IHNvbGlkIHJnYmEoMjU1LCAyNTUsIDI1NSwgMC44NSk7CiAgICAgIG91dGxpbmUtb2Zmc2V0OiA0cHg7CiAgICB9CiAgICAuc3BsYXNoLWVudGVyIHBpY3R1cmUsCiAgICAuc3BsYXNoLWVudGVyIGltZyB7CiAgICAgIGRpc3BsYXk6IGJsb2NrOwogICAgICB3aWR0aDogMTAwJTsKICAgICAgbWF4LWhlaWdodDogMTAwdmg7CiAgICAgIG9iamVjdC1maXQ6IGNvbnRhaW47CiAgICAgIG1hcmdpbjogMCBhdXRvOwogICAgfQogICAgLnNwbGFzaC1vdmVybGF5IHsKICAgICAgcG9zaXRpb246IGFic29sdXRlOwogICAgICBsZWZ0OiA1MCU7CiAgICAgIGJvdHRvbTogY2xhbXAoMS4yNXJlbSwgNHZ3LCAyLjVyZW0pOwogICAgICB0cmFuc2Zvcm06IHRyYW5zbGF0ZVgoLTUwJSk7CiAgICAgIHRleHQtYWxpZ246IGNlbnRlcjsKICAgICAgY29sb3I6ICNmZmY7CiAgICAgIHRleHQtc2hhZG93OiAwIDFweCA4cHggcmdiYSgwLCAwLCAwLCAwLjY1KTsKICAgICAgcG9pbnRlci1ldmVudHM6IG5vbmU7CiAgICAgIHBhZGRpbmc6IDAgMXJlbTsKICAgICAgbWF4LXdpZHRoOiA5MHZ3OwogICAgfQogICAgLnNwbGFzaC1vdmVybGF5IC5sZWFkIHsKICAgICAgbWFyZ2luOiAwIDAgMC4zNXJlbTsKICAgICAgZm9udC1zaXplOiBjbGFtcCgxcmVtLCAyLjV2dywgMS4yNXJlbSk7CiAgICAgIGZvbnQtd2VpZ2h0OiA1MDA7CiAgICAgIGxldHRlci1zcGFjaW5nOiAwLjAyZW07CiAgICB9CiAgICAuc3BsYXNoLW92ZXJsYXkgLmhpbnQgewogICAgICBtYXJnaW46IDA7CiAgICAgIGZvbnQtc2l6ZTogY2xhbXAoMC43NXJlbSwgMS44dncsIDAuODc1cmVtKTsKICAgICAgb3BhY2l0eTogMC44ODsKICAgIH0KICA8L3N0eWxlPgo8L2hlYWQ+Cjxib2R5PgogIDxkaXYgY2xhc3M9InNwbGFzaC1wYWdlIj4KICAgIDxhCiAgICAgIGhyZWY9InslIHVybCAncG9ydGFsOmhvbWUnICV9IgogICAgICBjbGFzcz0ic3BsYXNoLWVudGVyIgogICAgICBpZD0ic3BsYXNoLWVudGVyIgogICAgICBhcmlhLWxhYmVsPSJFbnRyYXIgYSBXQ0cgT25lIgogICAgPgogICAgICA8cGljdHVyZT4KICAgICAgICA8c291cmNlCiAgICAgICAgICBtZWRpYT0iKG1heC13aWR0aDogNzY3cHgpIgogICAgICAgICAgc3Jjc2V0PSJ7JSBzdGF0aWMgJ3BvcnRhbC9pbWcvd2NnX3NwbGFzaF92MXYuanBnJyAlfSIKICAgICAgICA+CiAgICAgICAgPGltZwogICAgICAgICAgc3JjPSJ7JSBzdGF0aWMgJ3BvcnRhbC9pbWcvd2NnX3NwbGFzaF92MWguanBnJyAlfSIKICAgICAgICAgIGFsdD0iV29ya2luZyBDYXBpdGFsIEdyb3VwIOKAlCBXQ0cgT25lIgogICAgICAgICAgd2lkdGg9IjE5MjAiCiAgICAgICAgICBoZWlnaHQ9IjEwODAiCiAgICAgICAgPgogICAgICA8L3BpY3R1cmU+CiAgICAgIDxkaXYgY2xhc3M9InNwbGFzaC1vdmVybGF5Ij4KICAgICAgICA8cCBjbGFzcz0ibGVhZCI+SGFnYSBjbGljIHBhcmEgZW50cmFyPC9wPgogICAgICAgIDxwIGNsYXNzPSJoaW50Ij5UYW1iacOpbiBwdWVkZSBwcmVzaW9uYXIgRW50ZXIgbyBFc3BhY2lvPC9wPgogICAgICA8L2Rpdj4KICAgIDwvYT4KICA8L2Rpdj4KICA8c2NyaXB0PgogICAgKGZ1bmN0aW9uICgpIHsKICAgICAgdmFyIGxpbmsgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgic3BsYXNoLWVudGVyIik7CiAgICAgIGZ1bmN0aW9uIGdvUGFuZWwoKSB7CiAgICAgICAgd2luZG93LmxvY2F0aW9uLmhyZWYgPSBsaW5rLmhyZWY7CiAgICAgIH0KICAgICAgZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcigia2V5ZG93biIsIGZ1bmN0aW9uIChlKSB7CiAgICAgICAgaWYgKGUua2V5ID09PSAiRW50ZXIiIHx8IGUua2V5ID09PSAiICIgfHwgZS5jb2RlID09PSAiU3BhY2UiKSB7CiAgICAgICAgICBlLnByZXZlbnREZWZhdWx0KCk7CiAgICAgICAgICBnb1BhbmVsKCk7CiAgICAgICAgfQogICAgICB9KTsKICAgICAgbGluay5mb2N1cygpOwogICAgfSkoKTsKICA8L3NjcmlwdD4KPC9ib2R5Pgo8L2h0bWw+Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/registration/login.html
PATH_JSON="templates/registration/login.html"
FILENAME=login.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=36
SIZE_BYTES_UTF8=1056
CONTENT_SHA256=fc0d89c1d88ed00f3795c99da16a22872b8e4a2a1fc0ed01bfb1d173b394145a
ENDS_WITH_NEWLINE=FALSE
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

{% block content %}
<div style="max-width: 420px; margin: 3rem auto; padding: 2rem; border: 1px solid #ddd; border-radius: 12px;">
  <h1 style="margin-bottom: 1rem;">Iniciar sesión</h1>

  {% if form.errors %}
    <div style="margin-bottom: 1rem; color: #b00020;">
      Usuario o contraseña incorrectos. Intenta de nuevo.
    </div>
  {% endif %}

  {% if next %}
    <div style="margin-bottom: 1rem; color: #555;">
      Debes iniciar sesión para continuar.
    </div>
  {% endif %}

  <form method="post">
    {% csrf_token %}
    <div style="margin-bottom: 1rem;">
      <label for="{{ form.username.id_for_label }}">Usuario</label><br>
      {{ form.username }}
    </div>
    <div style="margin-bottom: 1rem;">
      <label for="{{ form.password.id_for_label }}">Contraseña</label><br>
      {{ form.password }}
    </div>
    <button type="submit" style="padding: 0.6rem 1rem;">Entrar</button>
    {% if next %}
      <input type="hidden" name="next" value="{{ next }}">
    {% endif %}
  </form>
</div>
{% endblock %}
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base.html" %}
00002|
00003|{% block content %}
00004|<div style="max-width: 420px; margin: 3rem auto; padding: 2rem; border: 1px solid #ddd; border-radius: 12px;">
00005|  <h1 style="margin-bottom: 1rem;">Iniciar sesión</h1>
00006|
00007|  {% if form.errors %}
00008|    <div style="margin-bottom: 1rem; color: #b00020;">
00009|      Usuario o contraseña incorrectos. Intenta de nuevo.
00010|    </div>
00011|  {% endif %}
00012|
00013|  {% if next %}
00014|    <div style="margin-bottom: 1rem; color: #555;">
00015|      Debes iniciar sesión para continuar.
00016|    </div>
00017|  {% endif %}
00018|
00019|  <form method="post">
00020|    {% csrf_token %}
00021|    <div style="margin-bottom: 1rem;">
00022|      <label for="{{ form.username.id_for_label }}">Usuario</label><br>
00023|      {{ form.username }}
00024|    </div>
00025|    <div style="margin-bottom: 1rem;">
00026|      <label for="{{ form.password.id_for_label }}">Contraseña</label><br>
00027|      {{ form.password }}
00028|    </div>
00029|    <button type="submit" style="padding: 0.6rem 1rem;">Entrar</button>
00030|    {% if next %}
00031|      <input type="hidden" name="next" value="{{ next }}">
00032|    {% endif %}
00033|  </form>
00034|</div>
00035|{% endblock %}
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZS5odG1sIiAlfQoKeyUgYmxvY2sgY29udGVudCAlfQo8ZGl2IHN0eWxlPSJtYXgtd2lkdGg6IDQyMHB4OyBtYXJnaW46IDNyZW0gYXV0bzsgcGFkZGluZzogMnJlbTsgYm9yZGVyOiAxcHggc29saWQgI2RkZDsgYm9yZGVyLXJhZGl1czogMTJweDsiPgogIDxoMSBzdHlsZT0ibWFyZ2luLWJvdHRvbTogMXJlbTsiPkluaWNpYXIgc2VzacOzbjwvaDE+CgogIHslIGlmIGZvcm0uZXJyb3JzICV9CiAgICA8ZGl2IHN0eWxlPSJtYXJnaW4tYm90dG9tOiAxcmVtOyBjb2xvcjogI2IwMDAyMDsiPgogICAgICBVc3VhcmlvIG8gY29udHJhc2XDsWEgaW5jb3JyZWN0b3MuIEludGVudGEgZGUgbnVldm8uCiAgICA8L2Rpdj4KICB7JSBlbmRpZiAlfQoKICB7JSBpZiBuZXh0ICV9CiAgICA8ZGl2IHN0eWxlPSJtYXJnaW4tYm90dG9tOiAxcmVtOyBjb2xvcjogIzU1NTsiPgogICAgICBEZWJlcyBpbmljaWFyIHNlc2nDs24gcGFyYSBjb250aW51YXIuCiAgICA8L2Rpdj4KICB7JSBlbmRpZiAlfQoKICA8Zm9ybSBtZXRob2Q9InBvc3QiPgogICAgeyUgY3NyZl90b2tlbiAlfQogICAgPGRpdiBzdHlsZT0ibWFyZ2luLWJvdHRvbTogMXJlbTsiPgogICAgICA8bGFiZWwgZm9yPSJ7eyBmb3JtLnVzZXJuYW1lLmlkX2Zvcl9sYWJlbCB9fSI+VXN1YXJpbzwvbGFiZWw+PGJyPgogICAgICB7eyBmb3JtLnVzZXJuYW1lIH19CiAgICA8L2Rpdj4KICAgIDxkaXYgc3R5bGU9Im1hcmdpbi1ib3R0b206IDFyZW07Ij4KICAgICAgPGxhYmVsIGZvcj0ie3sgZm9ybS5wYXNzd29yZC5pZF9mb3JfbGFiZWwgfX0iPkNvbnRyYXNlw7FhPC9sYWJlbD48YnI+CiAgICAgIHt7IGZvcm0ucGFzc3dvcmQgfX0KICAgIDwvZGl2PgogICAgPGJ1dHRvbiB0eXBlPSJzdWJtaXQiIHN0eWxlPSJwYWRkaW5nOiAwLjZyZW0gMXJlbTsiPkVudHJhcjwvYnV0dG9uPgogICAgeyUgaWYgbmV4dCAlfQogICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJuZXh0IiB2YWx1ZT0ie3sgbmV4dCB9fSI+CiAgICB7JSBlbmRpZiAlfQogIDwvZm9ybT4KPC9kaXY+CnslIGVuZGJsb2NrICV9
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/risk/riskclientdetail.html
PATH_JSON="templates/risk/riskclientdetail.html"
FILENAME=riskclientdetail.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=99
SIZE_BYTES_UTF8=4091
CONTENT_SHA256=9db06dcc4c54328f0853b9a6b380fc239fcd78e299dfc73e0bfb6b6d83a60615
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
{% extends "base_wcg.html" %}
{% block title %}{{ entidad.nombre }} — Riesgo{% endblock %}
{% block content %}
<div class="mb-2 mt-1">
  <a href="{% url 'risk:comando_balon' %}" class="btn btn-sm btn-outline-secondary">← Comando Balón</a>
  <a href="{% url 'risk:cliente_list' %}" class="btn btn-sm btn-outline-secondary">Clientes</a>
</div>
<div class="d-flex justify-content-between align-items-start mb-3">
  <div>
    <h1 class="h4 fw-semibold mb-1">{{ entidad.nombre }}</h1>
    <p class="text-muted small mb-0">
      {{ entidad.codigo }}
      {% if entidad.nit %} · NIT {{ entidad.nit }}{% endif %}
      {% if entidad.unidad_negocio %} · {{ entidad.unidad_negocio.nombre }}{% endif %}
    </p>
  </div>
  <a href="{% url 'crm:entidad_detail' entidad.codigo %}" class="btn btn-sm btn-outline-primary">Ver en CRM</a>
</div>

<div class="row g-3 mb-3">
  <div class="col-md-4">
    <div class="card border-0 shadow-sm"><div class="card-body text-center py-3">
      <div class="stat-value" style="font-size:1.35rem;">{{ snapshots|length }}</div>
      <div class="text-muted small">Snapshots</div>
    </div></div>
  </div>
  <div class="col-md-4">
    <div class="card border-0 shadow-sm"><div class="card-body text-center py-3">
      <div class="stat-value" style="font-size:1.35rem;">{{ programaciones|length }}</div>
      <div class="text-muted small">Pagos programados</div>
    </div></div>
  </div>
  <div class="col-md-4">
    <div class="card border-0 shadow-sm"><div class="card-body text-center py-3">
      <div class="stat-value" style="font-size:1.35rem;">{{ pagos|length }}</div>
      <div class="text-muted small">Pagos realizados</div>
    </div></div>
  </div>
</div>

<div class="card border-0 shadow-sm mb-3">
  <div class="card-header bg-white fw-semibold">Operaciones / snapshots</div>
  <div class="table-responsive">
    <table class="table table-hover table-wcg mb-0 small">
      <thead>
        <tr>
          <th>Fecha</th><th>Operación</th><th>Producto</th><th class="text-end">Saldo</th>
          <th class="text-end">Exigible</th><th class="text-center">Mora</th><th></th>
        </tr>
      </thead>
      <tbody>
        {% for s in snapshots %}
        <tr>
          <td>{{ s.fecha_snapshot|date:"d/m/Y" }}</td>
          <td>{{ s.referencia_operacion }}</td>
          <td>{{ s.producto.nombre|default:"—" }}</td>
          <td class="text-end">{{ s.saldo }}</td>
          <td class="text-end{% if s.monto_exigible > 0 %} text-danger{% endif %}">{{ s.monto_exigible }}</td>
          <td class="text-center">{% if s.dias_mora > 0 %}<span class="badge text-bg-warning">{{ s.dias_mora }}</span>{% else %}0{% endif %}</td>
          <td><a href="{% url 'risk:operacion_detail' s.pk %}" class="btn btn-sm btn-outline-primary">Detalle</a></td>
        </tr>
        {% empty %}
        <tr><td colspan="7" class="text-muted text-center py-3">Sin snapshots.</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>

<div class="row g-3">
  <div class="col-md-6">
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white fw-semibold">Estados financieros</div>
      <table class="table table-sm mb-0">
        <thead><tr><th>Período</th><th>Saldo</th><th>Mora</th></tr></thead>
        <tbody>
          {% for e in estados %}
          <tr><td>{{ e.periodo }}</td><td>{{ e.saldo_total }}</td><td>{{ e.mora_dias }}</td></tr>
          {% empty %}
          <tr><td colspan="3" class="text-muted">Sin datos</td></tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white fw-semibold">Contactos cobranza</div>
      <ul class="list-group list-group-flush small">
        {% for c in contactos_cobranza %}
        <li class="list-group-item">{{ c.nombre }} — {{ c.telefono|default:c.email }}</li>
        {% empty %}
        <li class="list-group-item text-muted">Sin contactos de cobranza.</li>
        {% endfor %}
      </ul>
    </div>
  </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}{{ entidad.nombre }} — Riesgo{% endblock %}
00003|{% block content %}
00004|<div class="mb-2 mt-1">
00005|  <a href="{% url 'risk:comando_balon' %}" class="btn btn-sm btn-outline-secondary">← Comando Balón</a>
00006|  <a href="{% url 'risk:cliente_list' %}" class="btn btn-sm btn-outline-secondary">Clientes</a>
00007|</div>
00008|<div class="d-flex justify-content-between align-items-start mb-3">
00009|  <div>
00010|    <h1 class="h4 fw-semibold mb-1">{{ entidad.nombre }}</h1>
00011|    <p class="text-muted small mb-0">
00012|      {{ entidad.codigo }}
00013|      {% if entidad.nit %} · NIT {{ entidad.nit }}{% endif %}
00014|      {% if entidad.unidad_negocio %} · {{ entidad.unidad_negocio.nombre }}{% endif %}
00015|    </p>
00016|  </div>
00017|  <a href="{% url 'crm:entidad_detail' entidad.codigo %}" class="btn btn-sm btn-outline-primary">Ver en CRM</a>
00018|</div>
00019|
00020|<div class="row g-3 mb-3">
00021|  <div class="col-md-4">
00022|    <div class="card border-0 shadow-sm"><div class="card-body text-center py-3">
00023|      <div class="stat-value" style="font-size:1.35rem;">{{ snapshots|length }}</div>
00024|      <div class="text-muted small">Snapshots</div>
00025|    </div></div>
00026|  </div>
00027|  <div class="col-md-4">
00028|    <div class="card border-0 shadow-sm"><div class="card-body text-center py-3">
00029|      <div class="stat-value" style="font-size:1.35rem;">{{ programaciones|length }}</div>
00030|      <div class="text-muted small">Pagos programados</div>
00031|    </div></div>
00032|  </div>
00033|  <div class="col-md-4">
00034|    <div class="card border-0 shadow-sm"><div class="card-body text-center py-3">
00035|      <div class="stat-value" style="font-size:1.35rem;">{{ pagos|length }}</div>
00036|      <div class="text-muted small">Pagos realizados</div>
00037|    </div></div>
00038|  </div>
00039|</div>
00040|
00041|<div class="card border-0 shadow-sm mb-3">
00042|  <div class="card-header bg-white fw-semibold">Operaciones / snapshots</div>
00043|  <div class="table-responsive">
00044|    <table class="table table-hover table-wcg mb-0 small">
00045|      <thead>
00046|        <tr>
00047|          <th>Fecha</th><th>Operación</th><th>Producto</th><th class="text-end">Saldo</th>
00048|          <th class="text-end">Exigible</th><th class="text-center">Mora</th><th></th>
00049|        </tr>
00050|      </thead>
00051|      <tbody>
00052|        {% for s in snapshots %}
00053|        <tr>
00054|          <td>{{ s.fecha_snapshot|date:"d/m/Y" }}</td>
00055|          <td>{{ s.referencia_operacion }}</td>
00056|          <td>{{ s.producto.nombre|default:"—" }}</td>
00057|          <td class="text-end">{{ s.saldo }}</td>
00058|          <td class="text-end{% if s.monto_exigible > 0 %} text-danger{% endif %}">{{ s.monto_exigible }}</td>
00059|          <td class="text-center">{% if s.dias_mora > 0 %}<span class="badge text-bg-warning">{{ s.dias_mora }}</span>{% else %}0{% endif %}</td>
00060|          <td><a href="{% url 'risk:operacion_detail' s.pk %}" class="btn btn-sm btn-outline-primary">Detalle</a></td>
00061|        </tr>
00062|        {% empty %}
00063|        <tr><td colspan="7" class="text-muted text-center py-3">Sin snapshots.</td></tr>
00064|        {% endfor %}
00065|      </tbody>
00066|    </table>
00067|  </div>
00068|</div>
00069|
00070|<div class="row g-3">
00071|  <div class="col-md-6">
00072|    <div class="card border-0 shadow-sm">
00073|      <div class="card-header bg-white fw-semibold">Estados financieros</div>
00074|      <table class="table table-sm mb-0">
00075|        <thead><tr><th>Período</th><th>Saldo</th><th>Mora</th></tr></thead>
00076|        <tbody>
00077|          {% for e in estados %}
00078|          <tr><td>{{ e.periodo }}</td><td>{{ e.saldo_total }}</td><td>{{ e.mora_dias }}</td></tr>
00079|          {% empty %}
00080|          <tr><td colspan="3" class="text-muted">Sin datos</td></tr>
00081|          {% endfor %}
00082|        </tbody>
00083|      </table>
00084|    </div>
00085|  </div>
00086|  <div class="col-md-6">
00087|    <div class="card border-0 shadow-sm">
00088|      <div class="card-header bg-white fw-semibold">Contactos cobranza</div>
00089|      <ul class="list-group list-group-flush small">
00090|        {% for c in contactos_cobranza %}
00091|        <li class="list-group-item">{{ c.nombre }} — {{ c.telefono|default:c.email }}</li>
00092|        {% empty %}
00093|        <li class="list-group-item text-muted">Sin contactos de cobranza.</li>
00094|        {% endfor %}
00095|      </ul>
00096|    </div>
00097|  </div>
00098|</div>
00099|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX17eyBlbnRpZGFkLm5vbWJyZSB9fSDigJQgUmllc2dveyUgZW5kYmxvY2sgJX0KeyUgYmxvY2sgY29udGVudCAlfQo8ZGl2IGNsYXNzPSJtYi0yIG10LTEiPgogIDxhIGhyZWY9InslIHVybCAncmlzazpjb21hbmRvX2JhbG9uJyAlfSIgY2xhc3M9ImJ0biBidG4tc20gYnRuLW91dGxpbmUtc2Vjb25kYXJ5Ij7ihpAgQ29tYW5kbyBCYWzDs248L2E+CiAgPGEgaHJlZj0ieyUgdXJsICdyaXNrOmNsaWVudGVfbGlzdCcgJX0iIGNsYXNzPSJidG4gYnRuLXNtIGJ0bi1vdXRsaW5lLXNlY29uZGFyeSI+Q2xpZW50ZXM8L2E+CjwvZGl2Pgo8ZGl2IGNsYXNzPSJkLWZsZXgganVzdGlmeS1jb250ZW50LWJldHdlZW4gYWxpZ24taXRlbXMtc3RhcnQgbWItMyI+CiAgPGRpdj4KICAgIDxoMSBjbGFzcz0iaDQgZnctc2VtaWJvbGQgbWItMSI+e3sgZW50aWRhZC5ub21icmUgfX08L2gxPgogICAgPHAgY2xhc3M9InRleHQtbXV0ZWQgc21hbGwgbWItMCI+CiAgICAgIHt7IGVudGlkYWQuY29kaWdvIH19CiAgICAgIHslIGlmIGVudGlkYWQubml0ICV9IMK3IE5JVCB7eyBlbnRpZGFkLm5pdCB9fXslIGVuZGlmICV9CiAgICAgIHslIGlmIGVudGlkYWQudW5pZGFkX25lZ29jaW8gJX0gwrcge3sgZW50aWRhZC51bmlkYWRfbmVnb2Npby5ub21icmUgfX17JSBlbmRpZiAlfQogICAgPC9wPgogIDwvZGl2PgogIDxhIGhyZWY9InslIHVybCAnY3JtOmVudGlkYWRfZGV0YWlsJyBlbnRpZGFkLmNvZGlnbyAlfSIgY2xhc3M9ImJ0biBidG4tc20gYnRuLW91dGxpbmUtcHJpbWFyeSI+VmVyIGVuIENSTTwvYT4KPC9kaXY+Cgo8ZGl2IGNsYXNzPSJyb3cgZy0zIG1iLTMiPgogIDxkaXYgY2xhc3M9ImNvbC1tZC00Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIj48ZGl2IGNsYXNzPSJjYXJkLWJvZHkgdGV4dC1jZW50ZXIgcHktMyI+CiAgICAgIDxkaXYgY2xhc3M9InN0YXQtdmFsdWUiIHN0eWxlPSJmb250LXNpemU6MS4zNXJlbTsiPnt7IHNuYXBzaG90c3xsZW5ndGggfX08L2Rpdj4KICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+U25hcHNob3RzPC9kaXY+CiAgICA8L2Rpdj48L2Rpdj4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtNCI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSI+PGRpdiBjbGFzcz0iY2FyZC1ib2R5IHRleHQtY2VudGVyIHB5LTMiPgogICAgICA8ZGl2IGNsYXNzPSJzdGF0LXZhbHVlIiBzdHlsZT0iZm9udC1zaXplOjEuMzVyZW07Ij57eyBwcm9ncmFtYWNpb25lc3xsZW5ndGggfX08L2Rpdj4KICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+UGFnb3MgcHJvZ3JhbWFkb3M8L2Rpdj4KICAgIDwvZGl2PjwvZGl2PgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1tZC00Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIj48ZGl2IGNsYXNzPSJjYXJkLWJvZHkgdGV4dC1jZW50ZXIgcHktMyI+CiAgICAgIDxkaXYgY2xhc3M9InN0YXQtdmFsdWUiIHN0eWxlPSJmb250LXNpemU6MS4zNXJlbTsiPnt7IHBhZ29zfGxlbmd0aCB9fTwvZGl2PgogICAgICA8ZGl2IGNsYXNzPSJ0ZXh0LW11dGVkIHNtYWxsIj5QYWdvcyByZWFsaXphZG9zPC9kaXY+CiAgICA8L2Rpdj48L2Rpdj4KICA8L2Rpdj4KPC9kaXY+Cgo8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSBtYi0zIj4KICA8ZGl2IGNsYXNzPSJjYXJkLWhlYWRlciBiZy13aGl0ZSBmdy1zZW1pYm9sZCI+T3BlcmFjaW9uZXMgLyBzbmFwc2hvdHM8L2Rpdj4KICA8ZGl2IGNsYXNzPSJ0YWJsZS1yZXNwb25zaXZlIj4KICAgIDx0YWJsZSBjbGFzcz0idGFibGUgdGFibGUtaG92ZXIgdGFibGUtd2NnIG1iLTAgc21hbGwiPgogICAgICA8dGhlYWQ+CiAgICAgICAgPHRyPgogICAgICAgICAgPHRoPkZlY2hhPC90aD48dGg+T3BlcmFjacOzbjwvdGg+PHRoPlByb2R1Y3RvPC90aD48dGggY2xhc3M9InRleHQtZW5kIj5TYWxkbzwvdGg+CiAgICAgICAgICA8dGggY2xhc3M9InRleHQtZW5kIj5FeGlnaWJsZTwvdGg+PHRoIGNsYXNzPSJ0ZXh0LWNlbnRlciI+TW9yYTwvdGg+PHRoPjwvdGg+CiAgICAgICAgPC90cj4KICAgICAgPC90aGVhZD4KICAgICAgPHRib2R5PgogICAgICAgIHslIGZvciBzIGluIHNuYXBzaG90cyAlfQogICAgICAgIDx0cj4KICAgICAgICAgIDx0ZD57eyBzLmZlY2hhX3NuYXBzaG90fGRhdGU6ImQvbS9ZIiB9fTwvdGQ+CiAgICAgICAgICA8dGQ+e3sgcy5yZWZlcmVuY2lhX29wZXJhY2lvbiB9fTwvdGQ+CiAgICAgICAgICA8dGQ+e3sgcy5wcm9kdWN0by5ub21icmV8ZGVmYXVsdDoi4oCUIiB9fTwvdGQ+CiAgICAgICAgICA8dGQgY2xhc3M9InRleHQtZW5kIj57eyBzLnNhbGRvIH19PC90ZD4KICAgICAgICAgIDx0ZCBjbGFzcz0idGV4dC1lbmR7JSBpZiBzLm1vbnRvX2V4aWdpYmxlID4gMCAlfSB0ZXh0LWRhbmdlcnslIGVuZGlmICV9Ij57eyBzLm1vbnRvX2V4aWdpYmxlIH19PC90ZD4KICAgICAgICAgIDx0ZCBjbGFzcz0idGV4dC1jZW50ZXIiPnslIGlmIHMuZGlhc19tb3JhID4gMCAlfTxzcGFuIGNsYXNzPSJiYWRnZSB0ZXh0LWJnLXdhcm5pbmciPnt7IHMuZGlhc19tb3JhIH19PC9zcGFuPnslIGVsc2UgJX0weyUgZW5kaWYgJX08L3RkPgogICAgICAgICAgPHRkPjxhIGhyZWY9InslIHVybCAncmlzazpvcGVyYWNpb25fZGV0YWlsJyBzLnBrICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1wcmltYXJ5Ij5EZXRhbGxlPC9hPjwvdGQ+CiAgICAgICAgPC90cj4KICAgICAgICB7JSBlbXB0eSAlfQogICAgICAgIDx0cj48dGQgY29sc3Bhbj0iNyIgY2xhc3M9InRleHQtbXV0ZWQgdGV4dC1jZW50ZXIgcHktMyI+U2luIHNuYXBzaG90cy48L3RkPjwvdHI+CiAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgIDwvdGJvZHk+CiAgICA8L3RhYmxlPgogIDwvZGl2Pgo8L2Rpdj4KCjxkaXYgY2xhc3M9InJvdyBnLTMiPgogIDxkaXYgY2xhc3M9ImNvbC1tZC02Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIgYmctd2hpdGUgZnctc2VtaWJvbGQiPkVzdGFkb3MgZmluYW5jaWVyb3M8L2Rpdj4KICAgICAgPHRhYmxlIGNsYXNzPSJ0YWJsZSB0YWJsZS1zbSBtYi0wIj4KICAgICAgICA8dGhlYWQ+PHRyPjx0aD5QZXLDrW9kbzwvdGg+PHRoPlNhbGRvPC90aD48dGg+TW9yYTwvdGg+PC90cj48L3RoZWFkPgogICAgICAgIDx0Ym9keT4KICAgICAgICAgIHslIGZvciBlIGluIGVzdGFkb3MgJX0KICAgICAgICAgIDx0cj48dGQ+e3sgZS5wZXJpb2RvIH19PC90ZD48dGQ+e3sgZS5zYWxkb190b3RhbCB9fTwvdGQ+PHRkPnt7IGUubW9yYV9kaWFzIH19PC90ZD48L3RyPgogICAgICAgICAgeyUgZW1wdHkgJX0KICAgICAgICAgIDx0cj48dGQgY29sc3Bhbj0iMyIgY2xhc3M9InRleHQtbXV0ZWQiPlNpbiBkYXRvczwvdGQ+PC90cj4KICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgIDwvdGJvZHk+CiAgICAgIDwvdGFibGU+CiAgICA8L2Rpdj4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtNiI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSI+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtaGVhZGVyIGJnLXdoaXRlIGZ3LXNlbWlib2xkIj5Db250YWN0b3MgY29icmFuemE8L2Rpdj4KICAgICAgPHVsIGNsYXNzPSJsaXN0LWdyb3VwIGxpc3QtZ3JvdXAtZmx1c2ggc21hbGwiPgogICAgICAgIHslIGZvciBjIGluIGNvbnRhY3Rvc19jb2JyYW56YSAlfQogICAgICAgIDxsaSBjbGFzcz0ibGlzdC1ncm91cC1pdGVtIj57eyBjLm5vbWJyZSB9fSDigJQge3sgYy50ZWxlZm9ub3xkZWZhdWx0OmMuZW1haWwgfX08L2xpPgogICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgPGxpIGNsYXNzPSJsaXN0LWdyb3VwLWl0ZW0gdGV4dC1tdXRlZCI+U2luIGNvbnRhY3RvcyBkZSBjb2JyYW56YS48L2xpPgogICAgICAgIHslIGVuZGZvciAlfQogICAgICA8L3VsPgogICAgPC9kaXY+CiAgPC9kaXY+CjwvZGl2Pgp7JSBlbmRibG9jayAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/risk/riskclientlist.html
PATH_JSON="templates/risk/riskclientlist.html"
FILENAME=riskclientlist.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=28
SIZE_BYTES_UTF8=1115
CONTENT_SHA256=24309b17fbacd0bf24b5d45463a7fef36005102f368ea3bb2824a928510d9fab
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
{% extends "base_wcg.html" %}
{% block title %}Clientes riesgo — WCG{% endblock %}
{% block content %}
<div class="d-flex justify-content-between mb-3 mt-2">
  <div class="wcg-report-head">
    <h1 class="h4 fw-semibold mb-0">Riesgo — Clientes con operaciones</h1>
    {% include "includes/module_mark.html" with module="risk" %}
  </div>
  <a href="{% url 'risk:comando_balon' %}" class="btn btn-sm btn-outline-secondary">← Comando Balón</a>
</div>
<div class="card border-0 shadow-sm">
  <table class="table table-hover table-wcg mb-0">
    <thead><tr><th>Cliente</th><th>Código</th><th>Unidad</th><th></th></tr></thead>
    <tbody>
      {% for c in clientes %}
      <tr>
        <td>{{ c.nombre }}</td>
        <td>{{ c.codigo }}</td>
        <td>{{ c.unidad_negocio.nombre|default:"—" }}</td>
        <td><a href="{% url 'risk:cliente_detail' c.codigo %}" class="btn btn-sm btn-outline-primary">Ver</a></td>
      </tr>
      {% empty %}
      <tr><td colspan="4" class="text-muted text-center py-4">Sin clientes de riesgo.</td></tr>
      {% endfor %}
    </tbody>
  </table>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}Clientes riesgo — WCG{% endblock %}
00003|{% block content %}
00004|<div class="d-flex justify-content-between mb-3 mt-2">
00005|  <div class="wcg-report-head">
00006|    <h1 class="h4 fw-semibold mb-0">Riesgo — Clientes con operaciones</h1>
00007|    {% include "includes/module_mark.html" with module="risk" %}
00008|  </div>
00009|  <a href="{% url 'risk:comando_balon' %}" class="btn btn-sm btn-outline-secondary">← Comando Balón</a>
00010|</div>
00011|<div class="card border-0 shadow-sm">
00012|  <table class="table table-hover table-wcg mb-0">
00013|    <thead><tr><th>Cliente</th><th>Código</th><th>Unidad</th><th></th></tr></thead>
00014|    <tbody>
00015|      {% for c in clientes %}
00016|      <tr>
00017|        <td>{{ c.nombre }}</td>
00018|        <td>{{ c.codigo }}</td>
00019|        <td>{{ c.unidad_negocio.nombre|default:"—" }}</td>
00020|        <td><a href="{% url 'risk:cliente_detail' c.codigo %}" class="btn btn-sm btn-outline-primary">Ver</a></td>
00021|      </tr>
00022|      {% empty %}
00023|      <tr><td colspan="4" class="text-muted text-center py-4">Sin clientes de riesgo.</td></tr>
00024|      {% endfor %}
00025|    </tbody>
00026|  </table>
00027|</div>
00028|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1DbGllbnRlcyByaWVzZ28g4oCUIFdDR3slIGVuZGJsb2NrICV9CnslIGJsb2NrIGNvbnRlbnQgJX0KPGRpdiBjbGFzcz0iZC1mbGV4IGp1c3RpZnktY29udGVudC1iZXR3ZWVuIG1iLTMgbXQtMiI+CiAgPGRpdiBjbGFzcz0id2NnLXJlcG9ydC1oZWFkIj4KICAgIDxoMSBjbGFzcz0iaDQgZnctc2VtaWJvbGQgbWItMCI+Umllc2dvIOKAlCBDbGllbnRlcyBjb24gb3BlcmFjaW9uZXM8L2gxPgogICAgeyUgaW5jbHVkZSAiaW5jbHVkZXMvbW9kdWxlX21hcmsuaHRtbCIgd2l0aCBtb2R1bGU9InJpc2siICV9CiAgPC9kaXY+CiAgPGEgaHJlZj0ieyUgdXJsICdyaXNrOmNvbWFuZG9fYmFsb24nICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1zZWNvbmRhcnkiPuKGkCBDb21hbmRvIEJhbMOzbjwvYT4KPC9kaXY+CjxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIj4KICA8dGFibGUgY2xhc3M9InRhYmxlIHRhYmxlLWhvdmVyIHRhYmxlLXdjZyBtYi0wIj4KICAgIDx0aGVhZD48dHI+PHRoPkNsaWVudGU8L3RoPjx0aD5Dw7NkaWdvPC90aD48dGg+VW5pZGFkPC90aD48dGg+PC90aD48L3RyPjwvdGhlYWQ+CiAgICA8dGJvZHk+CiAgICAgIHslIGZvciBjIGluIGNsaWVudGVzICV9CiAgICAgIDx0cj4KICAgICAgICA8dGQ+e3sgYy5ub21icmUgfX08L3RkPgogICAgICAgIDx0ZD57eyBjLmNvZGlnbyB9fTwvdGQ+CiAgICAgICAgPHRkPnt7IGMudW5pZGFkX25lZ29jaW8ubm9tYnJlfGRlZmF1bHQ6IuKAlCIgfX08L3RkPgogICAgICAgIDx0ZD48YSBocmVmPSJ7JSB1cmwgJ3Jpc2s6Y2xpZW50ZV9kZXRhaWwnIGMuY29kaWdvICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1wcmltYXJ5Ij5WZXI8L2E+PC90ZD4KICAgICAgPC90cj4KICAgICAgeyUgZW1wdHkgJX0KICAgICAgPHRyPjx0ZCBjb2xzcGFuPSI0IiBjbGFzcz0idGV4dC1tdXRlZCB0ZXh0LWNlbnRlciBweS00Ij5TaW4gY2xpZW50ZXMgZGUgcmllc2dvLjwvdGQ+PC90cj4KICAgICAgeyUgZW5kZm9yICV9CiAgICA8L3Rib2R5PgogIDwvdGFibGU+CjwvZGl2Pgp7JSBlbmRibG9jayAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/risk/riskcommandobalon.html
PATH_JSON="templates/risk/riskcommandobalon.html"
FILENAME=riskcommandobalon.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=153
SIZE_BYTES_UTF8=6329
CONTENT_SHA256=ddd33fc39e004f36445f7945c8367749d8595c0bf79a9adedd06444920ba1524
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
{% extends "base_wcg.html" %}
{% block title %}Comando Balón — WCG{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-2 mt-2">
  <div class="wcg-report-head">
    <h1 class="h4 fw-semibold mb-0">Riesgo — Comando Balón</h1>
    {% include "includes/module_mark.html" with module="risk" %}
  </div>
  <div class="d-flex gap-1 flex-wrap">
    <a href="{% url 'risk:export_comando_balon' %}?cliente={{ request.GET.cliente }}&nivel={{ request.GET.nivel }}" class="btn btn-sm btn-outline-primary">Exportar CSV</a>
    <a href="{% url 'risk:cliente_list' %}" class="btn btn-sm btn-outline-secondary">Clientes</a>
  </div>
</div>

<div class="row g-2 mb-3">
  <div class="col-md-2 col-6">
    <div class="card border-0 shadow-sm"><div class="card-body py-2 text-center">
      <div class="stat-value" style="font-size:1.35rem;">{{ summary.clientes }}</div>
      <div class="text-muted small">Clientes</div>
    </div></div>
  </div>
  <div class="col-md-2 col-6">
    <div class="card border-0 shadow-sm"><div class="card-body py-2 text-center">
      <div class="stat-value" style="font-size:1.35rem;">{{ summary.operaciones }}</div>
      <div class="text-muted small">Operaciones</div>
    </div></div>
  </div>
  <div class="col-md-2 col-6">
    <div class="card border-0 shadow-sm"><div class="card-body py-2 text-center">
      <div class="stat-value text-warning" style="font-size:1.35rem;">{{ summary.con_mora }}</div>
      <div class="text-muted small">Con mora</div>
    </div></div>
  </div>
  <div class="col-md-3 col-6">
    <div class="card border-0 shadow-sm"><div class="card-body py-2 text-center">
      <div class="stat-value text-danger" style="font-size:1.35rem;">{{ summary.suma_vencido|floatformat:0 }}</div>
      <div class="text-muted small">Suma saldos vencidos</div>
    </div></div>
  </div>
  <div class="col-md-3 col-6">
    <div class="card border-0 shadow-sm"><div class="card-body py-2 text-center">
      <div class="stat-value text-danger" style="font-size:1.35rem;">{{ summary.alertas }}</div>
      <div class="text-muted small">En alerta</div>
    </div></div>
  </div>
</div>

<form method="get" class="row g-2 mb-3">
  <div class="col-md-4">
    <input type="search" name="cliente" value="{{ request.GET.cliente }}" class="form-control form-control-sm" placeholder="Filtrar por cliente">
  </div>
  <div class="col-md-3">
    <select name="nivel" class="form-select form-select-sm">
      <option value="">Todos los niveles</option>
      {% for value, label in niveles %}
      <option value="{{ value }}"{% if request.GET.nivel == value %} selected{% endif %}>{{ label }}</option>
      {% endfor %}
    </select>
  </div>
  <div class="col-md-2">
    <select name="alerta" class="form-select form-select-sm">
      <option value="">Alerta / Normal</option>
      <option value="1"{% if request.GET.alerta == '1' %} selected{% endif %}>Solo alertas</option>
      <option value="0"{% if request.GET.alerta == '0' %} selected{% endif %}>Sin alerta</option>
    </select>
  </div>
  <div class="col-md-2">
    <button type="submit" class="btn btn-primary btn-sm w-100">Filtrar</button>
  </div>
</form>

{% if not snapshots and not request.GET %}
{% include "includes/empty_state.html" with title="Sin snapshots operativos" message="Cargue BaseLeasing desde Administración → Importación General." %}
{% endif %}

<div class="card border-0 shadow-sm">
  <div class="card-header bg-white small text-muted">
    Mostrando hasta 100 registros{% if summary.total_snapshots > 100 %} de {{ summary.total_snapshots }}{% endif %}.
  </div>
  <div class="table-responsive">
    <table class="table table-hover table-wcg mb-0 align-middle small">
      <thead>
        <tr>
          <th>Fecha</th>
          <th>Cliente</th>
          <th>Operación</th>
          <th>Producto</th>
          <th>Nivel</th>
          <th class="text-end">Saldo</th>
          <th class="text-end">Exigible</th>
          <th class="text-center">Días mora</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {% for snap in snapshots %}
        <tr{% if snap.alerta %} class="table-warning"{% endif %}>
          <td>{{ snap.fecha_snapshot|date:"d/m/Y" }}</td>
          <td>
            <a href="{% url 'risk:cliente_detail' snap.entidad.codigo %}">{{ snap.entidad.nombre }}</a>
          </td>
          <td>{{ snap.referencia_operacion }}</td>
          <td>{{ snap.producto.nombre|default:"—" }}</td>
          <td>
            <span class="badge text-bg-{% if snap.nivel_riesgo == 'CRITICO' or snap.nivel_riesgo == 'ALTO' %}danger{% elif snap.nivel_riesgo == 'MEDIO' %}warning{% else %}secondary{% endif %}">
              {{ snap.get_nivel_riesgo_display }}
            </span>
          </td>
          <td class="text-end">{{ snap.saldo }}</td>
          <td class="text-end">
            {% if snap.monto_exigible and snap.monto_exigible > 0 %}
            <span class="text-danger fw-semibold">{{ snap.monto_exigible }}</span>
            {% else %}
            {{ snap.monto_exigible }}
            {% endif %}
          </td>
          <td class="text-center">
            {% if snap.dias_mora > 0 %}
            <span class="badge text-bg-warning">{{ snap.dias_mora }}</span>
            {% else %}
            0
            {% endif %}
          </td>
          <td class="text-end">
            <a href="{% url 'risk:operacion_detail' snap.pk %}" class="btn btn-sm btn-outline-primary">Detalle</a>
          </td>
        </tr>
        {% empty %}
        <tr>
          <td colspan="9" class="text-center text-muted py-4">
            No hay resultados con los filtros actuales.
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>

{% if alertas %}
<div class="card border-0 shadow-sm mt-4">
  <div class="card-header bg-white fw-semibold text-danger">Alertas activas ({{ alertas|length }})</div>
  <ul class="list-group list-group-flush small">
    {% for a in alertas|slice:":15" %}
    <li class="list-group-item d-flex justify-content-between">
      <span>{{ a.entidad.nombre }} — {{ a.referencia_operacion }}</span>
      <span>{{ a.dias_mora }} días · Q{{ a.monto_exigible }}</span>
    </li>
    {% endfor %}
  </ul>
</div>
{% endif %}
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}Comando Balón — WCG{% endblock %}
00003|{% block content %}
00004|<div class="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-2 mt-2">
00005|  <div class="wcg-report-head">
00006|    <h1 class="h4 fw-semibold mb-0">Riesgo — Comando Balón</h1>
00007|    {% include "includes/module_mark.html" with module="risk" %}
00008|  </div>
00009|  <div class="d-flex gap-1 flex-wrap">
00010|    <a href="{% url 'risk:export_comando_balon' %}?cliente={{ request.GET.cliente }}&nivel={{ request.GET.nivel }}" class="btn btn-sm btn-outline-primary">Exportar CSV</a>
00011|    <a href="{% url 'risk:cliente_list' %}" class="btn btn-sm btn-outline-secondary">Clientes</a>
00012|  </div>
00013|</div>
00014|
00015|<div class="row g-2 mb-3">
00016|  <div class="col-md-2 col-6">
00017|    <div class="card border-0 shadow-sm"><div class="card-body py-2 text-center">
00018|      <div class="stat-value" style="font-size:1.35rem;">{{ summary.clientes }}</div>
00019|      <div class="text-muted small">Clientes</div>
00020|    </div></div>
00021|  </div>
00022|  <div class="col-md-2 col-6">
00023|    <div class="card border-0 shadow-sm"><div class="card-body py-2 text-center">
00024|      <div class="stat-value" style="font-size:1.35rem;">{{ summary.operaciones }}</div>
00025|      <div class="text-muted small">Operaciones</div>
00026|    </div></div>
00027|  </div>
00028|  <div class="col-md-2 col-6">
00029|    <div class="card border-0 shadow-sm"><div class="card-body py-2 text-center">
00030|      <div class="stat-value text-warning" style="font-size:1.35rem;">{{ summary.con_mora }}</div>
00031|      <div class="text-muted small">Con mora</div>
00032|    </div></div>
00033|  </div>
00034|  <div class="col-md-3 col-6">
00035|    <div class="card border-0 shadow-sm"><div class="card-body py-2 text-center">
00036|      <div class="stat-value text-danger" style="font-size:1.35rem;">{{ summary.suma_vencido|floatformat:0 }}</div>
00037|      <div class="text-muted small">Suma saldos vencidos</div>
00038|    </div></div>
00039|  </div>
00040|  <div class="col-md-3 col-6">
00041|    <div class="card border-0 shadow-sm"><div class="card-body py-2 text-center">
00042|      <div class="stat-value text-danger" style="font-size:1.35rem;">{{ summary.alertas }}</div>
00043|      <div class="text-muted small">En alerta</div>
00044|    </div></div>
00045|  </div>
00046|</div>
00047|
00048|<form method="get" class="row g-2 mb-3">
00049|  <div class="col-md-4">
00050|    <input type="search" name="cliente" value="{{ request.GET.cliente }}" class="form-control form-control-sm" placeholder="Filtrar por cliente">
00051|  </div>
00052|  <div class="col-md-3">
00053|    <select name="nivel" class="form-select form-select-sm">
00054|      <option value="">Todos los niveles</option>
00055|      {% for value, label in niveles %}
00056|      <option value="{{ value }}"{% if request.GET.nivel == value %} selected{% endif %}>{{ label }}</option>
00057|      {% endfor %}
00058|    </select>
00059|  </div>
00060|  <div class="col-md-2">
00061|    <select name="alerta" class="form-select form-select-sm">
00062|      <option value="">Alerta / Normal</option>
00063|      <option value="1"{% if request.GET.alerta == '1' %} selected{% endif %}>Solo alertas</option>
00064|      <option value="0"{% if request.GET.alerta == '0' %} selected{% endif %}>Sin alerta</option>
00065|    </select>
00066|  </div>
00067|  <div class="col-md-2">
00068|    <button type="submit" class="btn btn-primary btn-sm w-100">Filtrar</button>
00069|  </div>
00070|</form>
00071|
00072|{% if not snapshots and not request.GET %}
00073|{% include "includes/empty_state.html" with title="Sin snapshots operativos" message="Cargue BaseLeasing desde Administración → Importación General." %}
00074|{% endif %}
00075|
00076|<div class="card border-0 shadow-sm">
00077|  <div class="card-header bg-white small text-muted">
00078|    Mostrando hasta 100 registros{% if summary.total_snapshots > 100 %} de {{ summary.total_snapshots }}{% endif %}.
00079|  </div>
00080|  <div class="table-responsive">
00081|    <table class="table table-hover table-wcg mb-0 align-middle small">
00082|      <thead>
00083|        <tr>
00084|          <th>Fecha</th>
00085|          <th>Cliente</th>
00086|          <th>Operación</th>
00087|          <th>Producto</th>
00088|          <th>Nivel</th>
00089|          <th class="text-end">Saldo</th>
00090|          <th class="text-end">Exigible</th>
00091|          <th class="text-center">Días mora</th>
00092|          <th></th>
00093|        </tr>
00094|      </thead>
00095|      <tbody>
00096|        {% for snap in snapshots %}
00097|        <tr{% if snap.alerta %} class="table-warning"{% endif %}>
00098|          <td>{{ snap.fecha_snapshot|date:"d/m/Y" }}</td>
00099|          <td>
00100|            <a href="{% url 'risk:cliente_detail' snap.entidad.codigo %}">{{ snap.entidad.nombre }}</a>
00101|          </td>
00102|          <td>{{ snap.referencia_operacion }}</td>
00103|          <td>{{ snap.producto.nombre|default:"—" }}</td>
00104|          <td>
00105|            <span class="badge text-bg-{% if snap.nivel_riesgo == 'CRITICO' or snap.nivel_riesgo == 'ALTO' %}danger{% elif snap.nivel_riesgo == 'MEDIO' %}warning{% else %}secondary{% endif %}">
00106|              {{ snap.get_nivel_riesgo_display }}
00107|            </span>
00108|          </td>
00109|          <td class="text-end">{{ snap.saldo }}</td>
00110|          <td class="text-end">
00111|            {% if snap.monto_exigible and snap.monto_exigible > 0 %}
00112|            <span class="text-danger fw-semibold">{{ snap.monto_exigible }}</span>
00113|            {% else %}
00114|            {{ snap.monto_exigible }}
00115|            {% endif %}
00116|          </td>
00117|          <td class="text-center">
00118|            {% if snap.dias_mora > 0 %}
00119|            <span class="badge text-bg-warning">{{ snap.dias_mora }}</span>
00120|            {% else %}
00121|            0
00122|            {% endif %}
00123|          </td>
00124|          <td class="text-end">
00125|            <a href="{% url 'risk:operacion_detail' snap.pk %}" class="btn btn-sm btn-outline-primary">Detalle</a>
00126|          </td>
00127|        </tr>
00128|        {% empty %}
00129|        <tr>
00130|          <td colspan="9" class="text-center text-muted py-4">
00131|            No hay resultados con los filtros actuales.
00132|          </td>
00133|        </tr>
00134|        {% endfor %}
00135|      </tbody>
00136|    </table>
00137|  </div>
00138|</div>
00139|
00140|{% if alertas %}
00141|<div class="card border-0 shadow-sm mt-4">
00142|  <div class="card-header bg-white fw-semibold text-danger">Alertas activas ({{ alertas|length }})</div>
00143|  <ul class="list-group list-group-flush small">
00144|    {% for a in alertas|slice:":15" %}
00145|    <li class="list-group-item d-flex justify-content-between">
00146|      <span>{{ a.entidad.nombre }} — {{ a.referencia_operacion }}</span>
00147|      <span>{{ a.dias_mora }} días · Q{{ a.monto_exigible }}</span>
00148|    </li>
00149|    {% endfor %}
00150|  </ul>
00151|</div>
00152|{% endif %}
00153|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1Db21hbmRvIEJhbMOzbiDigJQgV0NHeyUgZW5kYmxvY2sgJX0KeyUgYmxvY2sgY29udGVudCAlfQo8ZGl2IGNsYXNzPSJkLWZsZXgganVzdGlmeS1jb250ZW50LWJldHdlZW4gYWxpZ24taXRlbXMtc3RhcnQgbWItMyBmbGV4LXdyYXAgZ2FwLTIgbXQtMiI+CiAgPGRpdiBjbGFzcz0id2NnLXJlcG9ydC1oZWFkIj4KICAgIDxoMSBjbGFzcz0iaDQgZnctc2VtaWJvbGQgbWItMCI+Umllc2dvIOKAlCBDb21hbmRvIEJhbMOzbjwvaDE+CiAgICB7JSBpbmNsdWRlICJpbmNsdWRlcy9tb2R1bGVfbWFyay5odG1sIiB3aXRoIG1vZHVsZT0icmlzayIgJX0KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJkLWZsZXggZ2FwLTEgZmxleC13cmFwIj4KICAgIDxhIGhyZWY9InslIHVybCAncmlzazpleHBvcnRfY29tYW5kb19iYWxvbicgJX0/Y2xpZW50ZT17eyByZXF1ZXN0LkdFVC5jbGllbnRlIH19Jm5pdmVsPXt7IHJlcXVlc3QuR0VULm5pdmVsIH19IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1wcmltYXJ5Ij5FeHBvcnRhciBDU1Y8L2E+CiAgICA8YSBocmVmPSJ7JSB1cmwgJ3Jpc2s6Y2xpZW50ZV9saXN0JyAlfSIgY2xhc3M9ImJ0biBidG4tc20gYnRuLW91dGxpbmUtc2Vjb25kYXJ5Ij5DbGllbnRlczwvYT4KICA8L2Rpdj4KPC9kaXY+Cgo8ZGl2IGNsYXNzPSJyb3cgZy0yIG1iLTMiPgogIDxkaXYgY2xhc3M9ImNvbC1tZC0yIGNvbC02Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIj48ZGl2IGNsYXNzPSJjYXJkLWJvZHkgcHktMiB0ZXh0LWNlbnRlciI+CiAgICAgIDxkaXYgY2xhc3M9InN0YXQtdmFsdWUiIHN0eWxlPSJmb250LXNpemU6MS4zNXJlbTsiPnt7IHN1bW1hcnkuY2xpZW50ZXMgfX08L2Rpdj4KICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+Q2xpZW50ZXM8L2Rpdj4KICAgIDwvZGl2PjwvZGl2PgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1tZC0yIGNvbC02Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIj48ZGl2IGNsYXNzPSJjYXJkLWJvZHkgcHktMiB0ZXh0LWNlbnRlciI+CiAgICAgIDxkaXYgY2xhc3M9InN0YXQtdmFsdWUiIHN0eWxlPSJmb250LXNpemU6MS4zNXJlbTsiPnt7IHN1bW1hcnkub3BlcmFjaW9uZXMgfX08L2Rpdj4KICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+T3BlcmFjaW9uZXM8L2Rpdj4KICAgIDwvZGl2PjwvZGl2PgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1tZC0yIGNvbC02Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIj48ZGl2IGNsYXNzPSJjYXJkLWJvZHkgcHktMiB0ZXh0LWNlbnRlciI+CiAgICAgIDxkaXYgY2xhc3M9InN0YXQtdmFsdWUgdGV4dC13YXJuaW5nIiBzdHlsZT0iZm9udC1zaXplOjEuMzVyZW07Ij57eyBzdW1tYXJ5LmNvbl9tb3JhIH19PC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9InRleHQtbXV0ZWQgc21hbGwiPkNvbiBtb3JhPC9kaXY+CiAgICA8L2Rpdj48L2Rpdj4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtMyBjb2wtNiI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSI+PGRpdiBjbGFzcz0iY2FyZC1ib2R5IHB5LTIgdGV4dC1jZW50ZXIiPgogICAgICA8ZGl2IGNsYXNzPSJzdGF0LXZhbHVlIHRleHQtZGFuZ2VyIiBzdHlsZT0iZm9udC1zaXplOjEuMzVyZW07Ij57eyBzdW1tYXJ5LnN1bWFfdmVuY2lkb3xmbG9hdGZvcm1hdDowIH19PC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9InRleHQtbXV0ZWQgc21hbGwiPlN1bWEgc2FsZG9zIHZlbmNpZG9zPC9kaXY+CiAgICA8L2Rpdj48L2Rpdj4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtMyBjb2wtNiI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSI+PGRpdiBjbGFzcz0iY2FyZC1ib2R5IHB5LTIgdGV4dC1jZW50ZXIiPgogICAgICA8ZGl2IGNsYXNzPSJzdGF0LXZhbHVlIHRleHQtZGFuZ2VyIiBzdHlsZT0iZm9udC1zaXplOjEuMzVyZW07Ij57eyBzdW1tYXJ5LmFsZXJ0YXMgfX08L2Rpdj4KICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+RW4gYWxlcnRhPC9kaXY+CiAgICA8L2Rpdj48L2Rpdj4KICA8L2Rpdj4KPC9kaXY+Cgo8Zm9ybSBtZXRob2Q9ImdldCIgY2xhc3M9InJvdyBnLTIgbWItMyI+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTQiPgogICAgPGlucHV0IHR5cGU9InNlYXJjaCIgbmFtZT0iY2xpZW50ZSIgdmFsdWU9Int7IHJlcXVlc3QuR0VULmNsaWVudGUgfX0iIGNsYXNzPSJmb3JtLWNvbnRyb2wgZm9ybS1jb250cm9sLXNtIiBwbGFjZWhvbGRlcj0iRmlsdHJhciBwb3IgY2xpZW50ZSI+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTMiPgogICAgPHNlbGVjdCBuYW1lPSJuaXZlbCIgY2xhc3M9ImZvcm0tc2VsZWN0IGZvcm0tc2VsZWN0LXNtIj4KICAgICAgPG9wdGlvbiB2YWx1ZT0iIj5Ub2RvcyBsb3Mgbml2ZWxlczwvb3B0aW9uPgogICAgICB7JSBmb3IgdmFsdWUsIGxhYmVsIGluIG5pdmVsZXMgJX0KICAgICAgPG9wdGlvbiB2YWx1ZT0ie3sgdmFsdWUgfX0ieyUgaWYgcmVxdWVzdC5HRVQubml2ZWwgPT0gdmFsdWUgJX0gc2VsZWN0ZWR7JSBlbmRpZiAlfT57eyBsYWJlbCB9fTwvb3B0aW9uPgogICAgICB7JSBlbmRmb3IgJX0KICAgIDwvc2VsZWN0PgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1tZC0yIj4KICAgIDxzZWxlY3QgbmFtZT0iYWxlcnRhIiBjbGFzcz0iZm9ybS1zZWxlY3QgZm9ybS1zZWxlY3Qtc20iPgogICAgICA8b3B0aW9uIHZhbHVlPSIiPkFsZXJ0YSAvIE5vcm1hbDwvb3B0aW9uPgogICAgICA8b3B0aW9uIHZhbHVlPSIxInslIGlmIHJlcXVlc3QuR0VULmFsZXJ0YSA9PSAnMScgJX0gc2VsZWN0ZWR7JSBlbmRpZiAlfT5Tb2xvIGFsZXJ0YXM8L29wdGlvbj4KICAgICAgPG9wdGlvbiB2YWx1ZT0iMCJ7JSBpZiByZXF1ZXN0LkdFVC5hbGVydGEgPT0gJzAnICV9IHNlbGVjdGVkeyUgZW5kaWYgJX0+U2luIGFsZXJ0YTwvb3B0aW9uPgogICAgPC9zZWxlY3Q+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTIiPgogICAgPGJ1dHRvbiB0eXBlPSJzdWJtaXQiIGNsYXNzPSJidG4gYnRuLXByaW1hcnkgYnRuLXNtIHctMTAwIj5GaWx0cmFyPC9idXR0b24+CiAgPC9kaXY+CjwvZm9ybT4KCnslIGlmIG5vdCBzbmFwc2hvdHMgYW5kIG5vdCByZXF1ZXN0LkdFVCAlfQp7JSBpbmNsdWRlICJpbmNsdWRlcy9lbXB0eV9zdGF0ZS5odG1sIiB3aXRoIHRpdGxlPSJTaW4gc25hcHNob3RzIG9wZXJhdGl2b3MiIG1lc3NhZ2U9IkNhcmd1ZSBCYXNlTGVhc2luZyBkZXNkZSBBZG1pbmlzdHJhY2nDs24g4oaSIEltcG9ydGFjacOzbiBHZW5lcmFsLiIgJX0KeyUgZW5kaWYgJX0KCjxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIj4KICA8ZGl2IGNsYXNzPSJjYXJkLWhlYWRlciBiZy13aGl0ZSBzbWFsbCB0ZXh0LW11dGVkIj4KICAgIE1vc3RyYW5kbyBoYXN0YSAxMDAgcmVnaXN0cm9zeyUgaWYgc3VtbWFyeS50b3RhbF9zbmFwc2hvdHMgPiAxMDAgJX0gZGUge3sgc3VtbWFyeS50b3RhbF9zbmFwc2hvdHMgfX17JSBlbmRpZiAlfS4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJ0YWJsZS1yZXNwb25zaXZlIj4KICAgIDx0YWJsZSBjbGFzcz0idGFibGUgdGFibGUtaG92ZXIgdGFibGUtd2NnIG1iLTAgYWxpZ24tbWlkZGxlIHNtYWxsIj4KICAgICAgPHRoZWFkPgogICAgICAgIDx0cj4KICAgICAgICAgIDx0aD5GZWNoYTwvdGg+CiAgICAgICAgICA8dGg+Q2xpZW50ZTwvdGg+CiAgICAgICAgICA8dGg+T3BlcmFjacOzbjwvdGg+CiAgICAgICAgICA8dGg+UHJvZHVjdG88L3RoPgogICAgICAgICAgPHRoPk5pdmVsPC90aD4KICAgICAgICAgIDx0aCBjbGFzcz0idGV4dC1lbmQiPlNhbGRvPC90aD4KICAgICAgICAgIDx0aCBjbGFzcz0idGV4dC1lbmQiPkV4aWdpYmxlPC90aD4KICAgICAgICAgIDx0aCBjbGFzcz0idGV4dC1jZW50ZXIiPkTDrWFzIG1vcmE8L3RoPgogICAgICAgICAgPHRoPjwvdGg+CiAgICAgICAgPC90cj4KICAgICAgPC90aGVhZD4KICAgICAgPHRib2R5PgogICAgICAgIHslIGZvciBzbmFwIGluIHNuYXBzaG90cyAlfQogICAgICAgIDx0cnslIGlmIHNuYXAuYWxlcnRhICV9IGNsYXNzPSJ0YWJsZS13YXJuaW5nInslIGVuZGlmICV9PgogICAgICAgICAgPHRkPnt7IHNuYXAuZmVjaGFfc25hcHNob3R8ZGF0ZToiZC9tL1kiIH19PC90ZD4KICAgICAgICAgIDx0ZD4KICAgICAgICAgICAgPGEgaHJlZj0ieyUgdXJsICdyaXNrOmNsaWVudGVfZGV0YWlsJyBzbmFwLmVudGlkYWQuY29kaWdvICV9Ij57eyBzbmFwLmVudGlkYWQubm9tYnJlIH19PC9hPgogICAgICAgICAgPC90ZD4KICAgICAgICAgIDx0ZD57eyBzbmFwLnJlZmVyZW5jaWFfb3BlcmFjaW9uIH19PC90ZD4KICAgICAgICAgIDx0ZD57eyBzbmFwLnByb2R1Y3RvLm5vbWJyZXxkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgIDx0ZD4KICAgICAgICAgICAgPHNwYW4gY2xhc3M9ImJhZGdlIHRleHQtYmcteyUgaWYgc25hcC5uaXZlbF9yaWVzZ28gPT0gJ0NSSVRJQ08nIG9yIHNuYXAubml2ZWxfcmllc2dvID09ICdBTFRPJyAlfWRhbmdlcnslIGVsaWYgc25hcC5uaXZlbF9yaWVzZ28gPT0gJ01FRElPJyAlfXdhcm5pbmd7JSBlbHNlICV9c2Vjb25kYXJ5eyUgZW5kaWYgJX0iPgogICAgICAgICAgICAgIHt7IHNuYXAuZ2V0X25pdmVsX3JpZXNnb19kaXNwbGF5IH19CiAgICAgICAgICAgIDwvc3Bhbj4KICAgICAgICAgIDwvdGQ+CiAgICAgICAgICA8dGQgY2xhc3M9InRleHQtZW5kIj57eyBzbmFwLnNhbGRvIH19PC90ZD4KICAgICAgICAgIDx0ZCBjbGFzcz0idGV4dC1lbmQiPgogICAgICAgICAgICB7JSBpZiBzbmFwLm1vbnRvX2V4aWdpYmxlIGFuZCBzbmFwLm1vbnRvX2V4aWdpYmxlID4gMCAlfQogICAgICAgICAgICA8c3BhbiBjbGFzcz0idGV4dC1kYW5nZXIgZnctc2VtaWJvbGQiPnt7IHNuYXAubW9udG9fZXhpZ2libGUgfX08L3NwYW4+CiAgICAgICAgICAgIHslIGVsc2UgJX0KICAgICAgICAgICAge3sgc25hcC5tb250b19leGlnaWJsZSB9fQogICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgPC90ZD4KICAgICAgICAgIDx0ZCBjbGFzcz0idGV4dC1jZW50ZXIiPgogICAgICAgICAgICB7JSBpZiBzbmFwLmRpYXNfbW9yYSA+IDAgJX0KICAgICAgICAgICAgPHNwYW4gY2xhc3M9ImJhZGdlIHRleHQtYmctd2FybmluZyI+e3sgc25hcC5kaWFzX21vcmEgfX08L3NwYW4+CiAgICAgICAgICAgIHslIGVsc2UgJX0KICAgICAgICAgICAgMAogICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgPC90ZD4KICAgICAgICAgIDx0ZCBjbGFzcz0idGV4dC1lbmQiPgogICAgICAgICAgICA8YSBocmVmPSJ7JSB1cmwgJ3Jpc2s6b3BlcmFjaW9uX2RldGFpbCcgc25hcC5wayAlfSIgY2xhc3M9ImJ0biBidG4tc20gYnRuLW91dGxpbmUtcHJpbWFyeSI+RGV0YWxsZTwvYT4KICAgICAgICAgIDwvdGQ+CiAgICAgICAgPC90cj4KICAgICAgICB7JSBlbXB0eSAlfQogICAgICAgIDx0cj4KICAgICAgICAgIDx0ZCBjb2xzcGFuPSI5IiBjbGFzcz0idGV4dC1jZW50ZXIgdGV4dC1tdXRlZCBweS00Ij4KICAgICAgICAgICAgTm8gaGF5IHJlc3VsdGFkb3MgY29uIGxvcyBmaWx0cm9zIGFjdHVhbGVzLgogICAgICAgICAgPC90ZD4KICAgICAgICA8L3RyPgogICAgICAgIHslIGVuZGZvciAlfQogICAgICA8L3Rib2R5PgogICAgPC90YWJsZT4KICA8L2Rpdj4KPC9kaXY+Cgp7JSBpZiBhbGVydGFzICV9CjxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIG10LTQiPgogIDxkaXYgY2xhc3M9ImNhcmQtaGVhZGVyIGJnLXdoaXRlIGZ3LXNlbWlib2xkIHRleHQtZGFuZ2VyIj5BbGVydGFzIGFjdGl2YXMgKHt7IGFsZXJ0YXN8bGVuZ3RoIH19KTwvZGl2PgogIDx1bCBjbGFzcz0ibGlzdC1ncm91cCBsaXN0LWdyb3VwLWZsdXNoIHNtYWxsIj4KICAgIHslIGZvciBhIGluIGFsZXJ0YXN8c2xpY2U6IjoxNSIgJX0KICAgIDxsaSBjbGFzcz0ibGlzdC1ncm91cC1pdGVtIGQtZmxleCBqdXN0aWZ5LWNvbnRlbnQtYmV0d2VlbiI+CiAgICAgIDxzcGFuPnt7IGEuZW50aWRhZC5ub21icmUgfX0g4oCUIHt7IGEucmVmZXJlbmNpYV9vcGVyYWNpb24gfX08L3NwYW4+CiAgICAgIDxzcGFuPnt7IGEuZGlhc19tb3JhIH19IGTDrWFzIMK3IFF7eyBhLm1vbnRvX2V4aWdpYmxlIH19PC9zcGFuPgogICAgPC9saT4KICAgIHslIGVuZGZvciAlfQogIDwvdWw+CjwvZGl2Pgp7JSBlbmRpZiAlfQp7JSBlbmRibG9jayAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/risk/riskimportform.html
PATH_JSON="templates/risk/riskimportform.html"
FILENAME=riskimportform.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=17
SIZE_BYTES_UTF8=752
CONTENT_SHA256=162e5d88a1e712839d041498770e356b97270f923ddc69c49efe2eaf8b78a918
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
{% extends "base_wcg.html" %}
{% block title %}Importar — Riesgo{% endblock %}
{% block content %}
<h1>Importar datos de riesgo</h1>
<form method="post" enctype="multipart/form-data" class="card p-3">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary mt-2">Importar</button>
    <a href="{% url 'risk:comando_balon' %}" class="btn btn-link">Volver</a>
</form>
{% if batch %}
<div class="card mt-3 p-3">
    <p>Estado: <strong>{{ batch.get_status_display }}</strong> — Creados: {{ batch.creados }} · Actualizados: {{ batch.actualizados }} · Errores: {{ batch.errores }}</p>
    {% if batch.log_texto %}<pre class="small bg-light p-2">{{ batch.log_texto }}</pre>{% endif %}
</div>
{% endif %}
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}Importar — Riesgo{% endblock %}
00003|{% block content %}
00004|<h1>Importar datos de riesgo</h1>
00005|<form method="post" enctype="multipart/form-data" class="card p-3">
00006|    {% csrf_token %}
00007|    {{ form.as_p }}
00008|    <button type="submit" class="btn btn-primary mt-2">Importar</button>
00009|    <a href="{% url 'risk:comando_balon' %}" class="btn btn-link">Volver</a>
00010|</form>
00011|{% if batch %}
00012|<div class="card mt-3 p-3">
00013|    <p>Estado: <strong>{{ batch.get_status_display }}</strong> — Creados: {{ batch.creados }} · Actualizados: {{ batch.actualizados }} · Errores: {{ batch.errores }}</p>
00014|    {% if batch.log_texto %}<pre class="small bg-light p-2">{{ batch.log_texto }}</pre>{% endif %}
00015|</div>
00016|{% endif %}
00017|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1JbXBvcnRhciDigJQgUmllc2dveyUgZW5kYmxvY2sgJX0KeyUgYmxvY2sgY29udGVudCAlfQo8aDE+SW1wb3J0YXIgZGF0b3MgZGUgcmllc2dvPC9oMT4KPGZvcm0gbWV0aG9kPSJwb3N0IiBlbmN0eXBlPSJtdWx0aXBhcnQvZm9ybS1kYXRhIiBjbGFzcz0iY2FyZCBwLTMiPgogICAgeyUgY3NyZl90b2tlbiAlfQogICAge3sgZm9ybS5hc19wIH19CiAgICA8YnV0dG9uIHR5cGU9InN1Ym1pdCIgY2xhc3M9ImJ0biBidG4tcHJpbWFyeSBtdC0yIj5JbXBvcnRhcjwvYnV0dG9uPgogICAgPGEgaHJlZj0ieyUgdXJsICdyaXNrOmNvbWFuZG9fYmFsb24nICV9IiBjbGFzcz0iYnRuIGJ0bi1saW5rIj5Wb2x2ZXI8L2E+CjwvZm9ybT4KeyUgaWYgYmF0Y2ggJX0KPGRpdiBjbGFzcz0iY2FyZCBtdC0zIHAtMyI+CiAgICA8cD5Fc3RhZG86IDxzdHJvbmc+e3sgYmF0Y2guZ2V0X3N0YXR1c19kaXNwbGF5IH19PC9zdHJvbmc+IOKAlCBDcmVhZG9zOiB7eyBiYXRjaC5jcmVhZG9zIH19IMK3IEFjdHVhbGl6YWRvczoge3sgYmF0Y2guYWN0dWFsaXphZG9zIH19IMK3IEVycm9yZXM6IHt7IGJhdGNoLmVycm9yZXMgfX08L3A+CiAgICB7JSBpZiBiYXRjaC5sb2dfdGV4dG8gJX08cHJlIGNsYXNzPSJzbWFsbCBiZy1saWdodCBwLTIiPnt7IGJhdGNoLmxvZ190ZXh0byB9fTwvcHJlPnslIGVuZGlmICV9CjwvZGl2Pgp7JSBlbmRpZiAlfQp7JSBlbmRibG9jayAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/risk/riskoperationdetail.html
PATH_JSON="templates/risk/riskoperationdetail.html"
FILENAME=riskoperationdetail.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=119
SIZE_BYTES_UTF8=4495
CONTENT_SHA256=f5f8aeb1e63fe0380a71563b8d3fd0bb888a199fc1a1986fb81384c94c55e845
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
{% extends "base_wcg.html" %}
{% block title %}Operación {{ snapshot.referencia_operacion }} — Balón de Riesgo{% endblock %}
{% block content %}
<div class="mb-3 mt-1">
  <h1 class="h4 fw-semibold mb-1">Operación {{ snapshot.referencia_operacion }}</h1>
  <p class="text-muted small mb-0">
    Cliente:
    <a href="{% url 'risk:cliente_detail' snapshot.entidad.codigo %}">{{ snapshot.entidad.nombre }}</a>
  </p>
</div>

<div class="row g-3 mb-3">
  <div class="col-md-3">
    <div class="card border-0 shadow-sm"><div class="card-body small">
      <div class="text-muted">Producto</div>
      <div class="fw-semibold">{{ snapshot.producto.nombre|default:"—" }}</div>
    </div></div>
  </div>
  <div class="col-md-3">
    <div class="card border-0 shadow-sm"><div class="card-body small">
      <div class="text-muted">Unidad</div>
      <div class="fw-semibold">{{ snapshot.entidad.unidad_negocio.nombre|default:"—" }}</div>
    </div></div>
  </div>
  <div class="col-md-3">
    <div class="card border-0 shadow-sm"><div class="card-body small">
      <div class="text-muted">Nivel riesgo</div>
      <div class="fw-semibold">{{ snapshot.get_nivel_riesgo_display }}</div>
    </div></div>
  </div>
  <div class="col-md-3">
    <div class="card border-0 shadow-sm"><div class="card-body small">
      <div class="text-muted">Alerta</div>
      <div class="fw-semibold">{% if snapshot.alerta %}Sí{% else %}No{% endif %}</div>
    </div></div>
  </div>
</div>

<div class="card border-0 shadow-sm mb-3">
  <div class="card-header bg-white fw-semibold">Historial de snapshots</div>
  <div class="table-responsive">
    <table class="table table-sm table-hover mb-0">
      <thead>
        <tr>
          <th>Fecha</th>
          <th>Nivel</th>
          <th class="text-end">Capital</th>
          <th class="text-end">Vencido</th>
          <th class="text-center">Días</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {% for h in historial %}
        <tr>
          <td>{{ h.fecha_snapshot|date:"d/m/Y" }}</td>
          <td>{{ h.get_nivel_riesgo_display }}</td>
          <td class="text-end">{{ h.saldo }}</td>
          <td class="text-end{% if h.monto_exigible > 0 %} text-danger fw-semibold{% endif %}">{{ h.monto_exigible }}</td>
          <td class="text-center">
            {% if h.dias_mora > 0 %}<span class="badge text-bg-warning">{{ h.dias_mora }}</span>{% else %}0{% endif %}
          </td>
          <td class="text-end"><a href="{% url 'risk:operacion_detail' h.pk %}" class="btn btn-sm btn-outline-primary">Ver</a></td>
        </tr>
        {% empty %}
        <tr><td colspan="6" class="text-muted text-center py-3">Sin snapshots para esta operación.</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>

<div class="row g-3">
  <div class="col-md-6">
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white fw-semibold">Pagos programados</div>
      <div class="table-responsive">
        <table class="table table-sm mb-0">
          <thead><tr><th>Fecha</th><th>Ref.</th><th class="text-end">Monto</th></tr></thead>
          <tbody>
            {% for p in pagos_programados %}
            <tr>
              <td>{{ p.fecha_programada|date:"d/m/Y" }}</td>
              <td class="small">{{ p.referencia }}</td>
              <td class="text-end">{{ p.monto }}</td>
            </tr>
            {% empty %}
            <tr><td colspan="3" class="text-muted py-3">Sin pagos programados.</td></tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white fw-semibold">Pagos realizados</div>
      <div class="table-responsive">
        <table class="table table-sm mb-0">
          <thead><tr><th>Fecha</th><th>Ref.</th><th class="text-end">Monto</th></tr></thead>
          <tbody>
            {% for p in pagos_realizados %}
            <tr>
              <td>{{ p.fecha_pago|date:"d/m/Y" }}</td>
              <td class="small">{{ p.referencia }}</td>
              <td class="text-end">{{ p.monto }}</td>
            </tr>
            {% empty %}
            <tr><td colspan="3" class="text-muted py-3">Sin pagos realizados.</td></tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>

<p class="mt-3"><a href="{% url 'risk:comando_balon' %}">← Comando Balón</a></p>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}Operación {{ snapshot.referencia_operacion }} — Balón de Riesgo{% endblock %}
00003|{% block content %}
00004|<div class="mb-3 mt-1">
00005|  <h1 class="h4 fw-semibold mb-1">Operación {{ snapshot.referencia_operacion }}</h1>
00006|  <p class="text-muted small mb-0">
00007|    Cliente:
00008|    <a href="{% url 'risk:cliente_detail' snapshot.entidad.codigo %}">{{ snapshot.entidad.nombre }}</a>
00009|  </p>
00010|</div>
00011|
00012|<div class="row g-3 mb-3">
00013|  <div class="col-md-3">
00014|    <div class="card border-0 shadow-sm"><div class="card-body small">
00015|      <div class="text-muted">Producto</div>
00016|      <div class="fw-semibold">{{ snapshot.producto.nombre|default:"—" }}</div>
00017|    </div></div>
00018|  </div>
00019|  <div class="col-md-3">
00020|    <div class="card border-0 shadow-sm"><div class="card-body small">
00021|      <div class="text-muted">Unidad</div>
00022|      <div class="fw-semibold">{{ snapshot.entidad.unidad_negocio.nombre|default:"—" }}</div>
00023|    </div></div>
00024|  </div>
00025|  <div class="col-md-3">
00026|    <div class="card border-0 shadow-sm"><div class="card-body small">
00027|      <div class="text-muted">Nivel riesgo</div>
00028|      <div class="fw-semibold">{{ snapshot.get_nivel_riesgo_display }}</div>
00029|    </div></div>
00030|  </div>
00031|  <div class="col-md-3">
00032|    <div class="card border-0 shadow-sm"><div class="card-body small">
00033|      <div class="text-muted">Alerta</div>
00034|      <div class="fw-semibold">{% if snapshot.alerta %}Sí{% else %}No{% endif %}</div>
00035|    </div></div>
00036|  </div>
00037|</div>
00038|
00039|<div class="card border-0 shadow-sm mb-3">
00040|  <div class="card-header bg-white fw-semibold">Historial de snapshots</div>
00041|  <div class="table-responsive">
00042|    <table class="table table-sm table-hover mb-0">
00043|      <thead>
00044|        <tr>
00045|          <th>Fecha</th>
00046|          <th>Nivel</th>
00047|          <th class="text-end">Capital</th>
00048|          <th class="text-end">Vencido</th>
00049|          <th class="text-center">Días</th>
00050|          <th></th>
00051|        </tr>
00052|      </thead>
00053|      <tbody>
00054|        {% for h in historial %}
00055|        <tr>
00056|          <td>{{ h.fecha_snapshot|date:"d/m/Y" }}</td>
00057|          <td>{{ h.get_nivel_riesgo_display }}</td>
00058|          <td class="text-end">{{ h.saldo }}</td>
00059|          <td class="text-end{% if h.monto_exigible > 0 %} text-danger fw-semibold{% endif %}">{{ h.monto_exigible }}</td>
00060|          <td class="text-center">
00061|            {% if h.dias_mora > 0 %}<span class="badge text-bg-warning">{{ h.dias_mora }}</span>{% else %}0{% endif %}
00062|          </td>
00063|          <td class="text-end"><a href="{% url 'risk:operacion_detail' h.pk %}" class="btn btn-sm btn-outline-primary">Ver</a></td>
00064|        </tr>
00065|        {% empty %}
00066|        <tr><td colspan="6" class="text-muted text-center py-3">Sin snapshots para esta operación.</td></tr>
00067|        {% endfor %}
00068|      </tbody>
00069|    </table>
00070|  </div>
00071|</div>
00072|
00073|<div class="row g-3">
00074|  <div class="col-md-6">
00075|    <div class="card border-0 shadow-sm">
00076|      <div class="card-header bg-white fw-semibold">Pagos programados</div>
00077|      <div class="table-responsive">
00078|        <table class="table table-sm mb-0">
00079|          <thead><tr><th>Fecha</th><th>Ref.</th><th class="text-end">Monto</th></tr></thead>
00080|          <tbody>
00081|            {% for p in pagos_programados %}
00082|            <tr>
00083|              <td>{{ p.fecha_programada|date:"d/m/Y" }}</td>
00084|              <td class="small">{{ p.referencia }}</td>
00085|              <td class="text-end">{{ p.monto }}</td>
00086|            </tr>
00087|            {% empty %}
00088|            <tr><td colspan="3" class="text-muted py-3">Sin pagos programados.</td></tr>
00089|            {% endfor %}
00090|          </tbody>
00091|        </table>
00092|      </div>
00093|    </div>
00094|  </div>
00095|  <div class="col-md-6">
00096|    <div class="card border-0 shadow-sm">
00097|      <div class="card-header bg-white fw-semibold">Pagos realizados</div>
00098|      <div class="table-responsive">
00099|        <table class="table table-sm mb-0">
00100|          <thead><tr><th>Fecha</th><th>Ref.</th><th class="text-end">Monto</th></tr></thead>
00101|          <tbody>
00102|            {% for p in pagos_realizados %}
00103|            <tr>
00104|              <td>{{ p.fecha_pago|date:"d/m/Y" }}</td>
00105|              <td class="small">{{ p.referencia }}</td>
00106|              <td class="text-end">{{ p.monto }}</td>
00107|            </tr>
00108|            {% empty %}
00109|            <tr><td colspan="3" class="text-muted py-3">Sin pagos realizados.</td></tr>
00110|            {% endfor %}
00111|          </tbody>
00112|        </table>
00113|      </div>
00114|    </div>
00115|  </div>
00116|</div>
00117|
00118|<p class="mt-3"><a href="{% url 'risk:comando_balon' %}">← Comando Balón</a></p>
00119|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1PcGVyYWNpw7NuIHt7IHNuYXBzaG90LnJlZmVyZW5jaWFfb3BlcmFjaW9uIH19IOKAlCBCYWzDs24gZGUgUmllc2dveyUgZW5kYmxvY2sgJX0KeyUgYmxvY2sgY29udGVudCAlfQo8ZGl2IGNsYXNzPSJtYi0zIG10LTEiPgogIDxoMSBjbGFzcz0iaDQgZnctc2VtaWJvbGQgbWItMSI+T3BlcmFjacOzbiB7eyBzbmFwc2hvdC5yZWZlcmVuY2lhX29wZXJhY2lvbiB9fTwvaDE+CiAgPHAgY2xhc3M9InRleHQtbXV0ZWQgc21hbGwgbWItMCI+CiAgICBDbGllbnRlOgogICAgPGEgaHJlZj0ieyUgdXJsICdyaXNrOmNsaWVudGVfZGV0YWlsJyBzbmFwc2hvdC5lbnRpZGFkLmNvZGlnbyAlfSI+e3sgc25hcHNob3QuZW50aWRhZC5ub21icmUgfX08L2E+CiAgPC9wPgo8L2Rpdj4KCjxkaXYgY2xhc3M9InJvdyBnLTMgbWItMyI+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTMiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20iPjxkaXYgY2xhc3M9ImNhcmQtYm9keSBzbWFsbCI+CiAgICAgIDxkaXYgY2xhc3M9InRleHQtbXV0ZWQiPlByb2R1Y3RvPC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9ImZ3LXNlbWlib2xkIj57eyBzbmFwc2hvdC5wcm9kdWN0by5ub21icmV8ZGVmYXVsdDoi4oCUIiB9fTwvZGl2PgogICAgPC9kaXY+PC9kaXY+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTMiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20iPjxkaXYgY2xhc3M9ImNhcmQtYm9keSBzbWFsbCI+CiAgICAgIDxkaXYgY2xhc3M9InRleHQtbXV0ZWQiPlVuaWRhZDwvZGl2PgogICAgICA8ZGl2IGNsYXNzPSJmdy1zZW1pYm9sZCI+e3sgc25hcHNob3QuZW50aWRhZC51bmlkYWRfbmVnb2Npby5ub21icmV8ZGVmYXVsdDoi4oCUIiB9fTwvZGl2PgogICAgPC9kaXY+PC9kaXY+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTMiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20iPjxkaXYgY2xhc3M9ImNhcmQtYm9keSBzbWFsbCI+CiAgICAgIDxkaXYgY2xhc3M9InRleHQtbXV0ZWQiPk5pdmVsIHJpZXNnbzwvZGl2PgogICAgICA8ZGl2IGNsYXNzPSJmdy1zZW1pYm9sZCI+e3sgc25hcHNob3QuZ2V0X25pdmVsX3JpZXNnb19kaXNwbGF5IH19PC9kaXY+CiAgICA8L2Rpdj48L2Rpdj4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtMyI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSI+PGRpdiBjbGFzcz0iY2FyZC1ib2R5IHNtYWxsIj4KICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCI+QWxlcnRhPC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9ImZ3LXNlbWlib2xkIj57JSBpZiBzbmFwc2hvdC5hbGVydGEgJX1Tw617JSBlbHNlICV9Tm97JSBlbmRpZiAlfTwvZGl2PgogICAgPC9kaXY+PC9kaXY+CiAgPC9kaXY+CjwvZGl2PgoKPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20gbWItMyI+CiAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIgYmctd2hpdGUgZnctc2VtaWJvbGQiPkhpc3RvcmlhbCBkZSBzbmFwc2hvdHM8L2Rpdj4KICA8ZGl2IGNsYXNzPSJ0YWJsZS1yZXNwb25zaXZlIj4KICAgIDx0YWJsZSBjbGFzcz0idGFibGUgdGFibGUtc20gdGFibGUtaG92ZXIgbWItMCI+CiAgICAgIDx0aGVhZD4KICAgICAgICA8dHI+CiAgICAgICAgICA8dGg+RmVjaGE8L3RoPgogICAgICAgICAgPHRoPk5pdmVsPC90aD4KICAgICAgICAgIDx0aCBjbGFzcz0idGV4dC1lbmQiPkNhcGl0YWw8L3RoPgogICAgICAgICAgPHRoIGNsYXNzPSJ0ZXh0LWVuZCI+VmVuY2lkbzwvdGg+CiAgICAgICAgICA8dGggY2xhc3M9InRleHQtY2VudGVyIj5Ew61hczwvdGg+CiAgICAgICAgICA8dGg+PC90aD4KICAgICAgICA8L3RyPgogICAgICA8L3RoZWFkPgogICAgICA8dGJvZHk+CiAgICAgICAgeyUgZm9yIGggaW4gaGlzdG9yaWFsICV9CiAgICAgICAgPHRyPgogICAgICAgICAgPHRkPnt7IGguZmVjaGFfc25hcHNob3R8ZGF0ZToiZC9tL1kiIH19PC90ZD4KICAgICAgICAgIDx0ZD57eyBoLmdldF9uaXZlbF9yaWVzZ29fZGlzcGxheSB9fTwvdGQ+CiAgICAgICAgICA8dGQgY2xhc3M9InRleHQtZW5kIj57eyBoLnNhbGRvIH19PC90ZD4KICAgICAgICAgIDx0ZCBjbGFzcz0idGV4dC1lbmR7JSBpZiBoLm1vbnRvX2V4aWdpYmxlID4gMCAlfSB0ZXh0LWRhbmdlciBmdy1zZW1pYm9sZHslIGVuZGlmICV9Ij57eyBoLm1vbnRvX2V4aWdpYmxlIH19PC90ZD4KICAgICAgICAgIDx0ZCBjbGFzcz0idGV4dC1jZW50ZXIiPgogICAgICAgICAgICB7JSBpZiBoLmRpYXNfbW9yYSA+IDAgJX08c3BhbiBjbGFzcz0iYmFkZ2UgdGV4dC1iZy13YXJuaW5nIj57eyBoLmRpYXNfbW9yYSB9fTwvc3Bhbj57JSBlbHNlICV9MHslIGVuZGlmICV9CiAgICAgICAgICA8L3RkPgogICAgICAgICAgPHRkIGNsYXNzPSJ0ZXh0LWVuZCI+PGEgaHJlZj0ieyUgdXJsICdyaXNrOm9wZXJhY2lvbl9kZXRhaWwnIGgucGsgJX0iIGNsYXNzPSJidG4gYnRuLXNtIGJ0bi1vdXRsaW5lLXByaW1hcnkiPlZlcjwvYT48L3RkPgogICAgICAgIDwvdHI+CiAgICAgICAgeyUgZW1wdHkgJX0KICAgICAgICA8dHI+PHRkIGNvbHNwYW49IjYiIGNsYXNzPSJ0ZXh0LW11dGVkIHRleHQtY2VudGVyIHB5LTMiPlNpbiBzbmFwc2hvdHMgcGFyYSBlc3RhIG9wZXJhY2nDs24uPC90ZD48L3RyPgogICAgICAgIHslIGVuZGZvciAlfQogICAgICA8L3Rib2R5PgogICAgPC90YWJsZT4KICA8L2Rpdj4KPC9kaXY+Cgo8ZGl2IGNsYXNzPSJyb3cgZy0zIj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtNiI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSI+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtaGVhZGVyIGJnLXdoaXRlIGZ3LXNlbWlib2xkIj5QYWdvcyBwcm9ncmFtYWRvczwvZGl2PgogICAgICA8ZGl2IGNsYXNzPSJ0YWJsZS1yZXNwb25zaXZlIj4KICAgICAgICA8dGFibGUgY2xhc3M9InRhYmxlIHRhYmxlLXNtIG1iLTAiPgogICAgICAgICAgPHRoZWFkPjx0cj48dGg+RmVjaGE8L3RoPjx0aD5SZWYuPC90aD48dGggY2xhc3M9InRleHQtZW5kIj5Nb250bzwvdGg+PC90cj48L3RoZWFkPgogICAgICAgICAgPHRib2R5PgogICAgICAgICAgICB7JSBmb3IgcCBpbiBwYWdvc19wcm9ncmFtYWRvcyAlfQogICAgICAgICAgICA8dHI+CiAgICAgICAgICAgICAgPHRkPnt7IHAuZmVjaGFfcHJvZ3JhbWFkYXxkYXRlOiJkL20vWSIgfX08L3RkPgogICAgICAgICAgICAgIDx0ZCBjbGFzcz0ic21hbGwiPnt7IHAucmVmZXJlbmNpYSB9fTwvdGQ+CiAgICAgICAgICAgICAgPHRkIGNsYXNzPSJ0ZXh0LWVuZCI+e3sgcC5tb250byB9fTwvdGQ+CiAgICAgICAgICAgIDwvdHI+CiAgICAgICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgICAgIDx0cj48dGQgY29sc3Bhbj0iMyIgY2xhc3M9InRleHQtbXV0ZWQgcHktMyI+U2luIHBhZ29zIHByb2dyYW1hZG9zLjwvdGQ+PC90cj4KICAgICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgICA8L3Rib2R5PgogICAgICAgIDwvdGFibGU+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTYiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20iPgogICAgICA8ZGl2IGNsYXNzPSJjYXJkLWhlYWRlciBiZy13aGl0ZSBmdy1zZW1pYm9sZCI+UGFnb3MgcmVhbGl6YWRvczwvZGl2PgogICAgICA8ZGl2IGNsYXNzPSJ0YWJsZS1yZXNwb25zaXZlIj4KICAgICAgICA8dGFibGUgY2xhc3M9InRhYmxlIHRhYmxlLXNtIG1iLTAiPgogICAgICAgICAgPHRoZWFkPjx0cj48dGg+RmVjaGE8L3RoPjx0aD5SZWYuPC90aD48dGggY2xhc3M9InRleHQtZW5kIj5Nb250bzwvdGg+PC90cj48L3RoZWFkPgogICAgICAgICAgPHRib2R5PgogICAgICAgICAgICB7JSBmb3IgcCBpbiBwYWdvc19yZWFsaXphZG9zICV9CiAgICAgICAgICAgIDx0cj4KICAgICAgICAgICAgICA8dGQ+e3sgcC5mZWNoYV9wYWdvfGRhdGU6ImQvbS9ZIiB9fTwvdGQ+CiAgICAgICAgICAgICAgPHRkIGNsYXNzPSJzbWFsbCI+e3sgcC5yZWZlcmVuY2lhIH19PC90ZD4KICAgICAgICAgICAgICA8dGQgY2xhc3M9InRleHQtZW5kIj57eyBwLm1vbnRvIH19PC90ZD4KICAgICAgICAgICAgPC90cj4KICAgICAgICAgICAgeyUgZW1wdHkgJX0KICAgICAgICAgICAgPHRyPjx0ZCBjb2xzcGFuPSIzIiBjbGFzcz0idGV4dC1tdXRlZCBweS0zIj5TaW4gcGFnb3MgcmVhbGl6YWRvcy48L3RkPjwvdHI+CiAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgPC90Ym9keT4KICAgICAgICA8L3RhYmxlPgogICAgICA8L2Rpdj4KICAgIDwvZGl2PgogIDwvZGl2Pgo8L2Rpdj4KCjxwIGNsYXNzPSJtdC0zIj48YSBocmVmPSJ7JSB1cmwgJ3Jpc2s6Y29tYW5kb19iYWxvbicgJX0iPuKGkCBDb21hbmRvIEJhbMOzbjwvYT48L3A+CnslIGVuZGJsb2NrICV9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/splash.html
PATH_JSON="templates/splash.html"
FILENAME=splash.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=112
SIZE_BYTES_UTF8=2372
CONTENT_SHA256=ee9bee014b8f6302397b9a5b6c238b8578d68b9035c4554f30f8becd1dfa1dfb
ENDS_WITH_NEWLINE=FALSE
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
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>PGC - WCG</title>
    {% load static %}
    <style>
      * { box-sizing: border-box; margin: 0; padding: 0; }

      html, body {
        height: 100%;
        width: 100%;
        overflow: hidden;
        background: #111827;
      }

      .splash-wrapper {
        position: relative;
        width: 100%;
        height: 100%;
        cursor: pointer;
        background: #111827;
      }

      .splash-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center center;
        display: block;
      }

      .splash-portrait {
        display: none;
      }

      .hint {
        position: absolute;
        bottom: 24px;
        right: 24px;
        padding: 8px 12px;
        border-radius: 6px;
        background: rgba(0,0,0,0.45);
        color: #f9fafb;
        font-family: Arial, sans-serif;
        font-size: 0.9rem;
      }

      @media (max-width: 768px) {
        .hint {
          left: 16px;
          right: 16px;
          text-align: center;
        }
      }

      @media (orientation: portrait) {
        .splash-landscape {
          display: none;
        }

        .splash-portrait {
          display: block;
        }

        .hint {
          display: none;
        }
      }
    </style>
</head>
<body>
    <div class="splash-wrapper" id="splash-root">
        <img
          class="splash-img splash-landscape"
          src="{% static 'img/splash.jpg' %}"
          alt="PGC - Working Capital Group"
        >
        <img
          class="splash-img splash-portrait"
          src="{% static 'img/splashv.jpg' %}"
          alt="PGC - Working Capital Group"
        >

        <div class="hint">
            Haz clic o presiona cualquier tecla para entrar al tablero.
        </div>
    </div>

    <script>
    (function () {
        function goDashboard() {
            window.location.href = "{% url 'portal:home' %}";
        }

        var root = document.getElementById("splash-root");

        if (root) {
            root.addEventListener("click", function (e) {
                e.preventDefault();
                goDashboard();
            });
        }

        document.addEventListener("keydown", function () {
            goDashboard();
        });
    })();
    </script>
</body>
</html>
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|<!DOCTYPE html>
00002|<html lang="es">
00003|<head>
00004|    <meta charset="UTF-8">
00005|    <title>PGC - WCG</title>
00006|    {% load static %}
00007|    <style>
00008|      * { box-sizing: border-box; margin: 0; padding: 0; }
00009|
00010|      html, body {
00011|        height: 100%;
00012|        width: 100%;
00013|        overflow: hidden;
00014|        background: #111827;
00015|      }
00016|
00017|      .splash-wrapper {
00018|        position: relative;
00019|        width: 100%;
00020|        height: 100%;
00021|        cursor: pointer;
00022|        background: #111827;
00023|      }
00024|
00025|      .splash-img {
00026|        width: 100%;
00027|        height: 100%;
00028|        object-fit: cover;
00029|        object-position: center center;
00030|        display: block;
00031|      }
00032|
00033|      .splash-portrait {
00034|        display: none;
00035|      }
00036|
00037|      .hint {
00038|        position: absolute;
00039|        bottom: 24px;
00040|        right: 24px;
00041|        padding: 8px 12px;
00042|        border-radius: 6px;
00043|        background: rgba(0,0,0,0.45);
00044|        color: #f9fafb;
00045|        font-family: Arial, sans-serif;
00046|        font-size: 0.9rem;
00047|      }
00048|
00049|      @media (max-width: 768px) {
00050|        .hint {
00051|          left: 16px;
00052|          right: 16px;
00053|          text-align: center;
00054|        }
00055|      }
00056|
00057|      @media (orientation: portrait) {
00058|        .splash-landscape {
00059|          display: none;
00060|        }
00061|
00062|        .splash-portrait {
00063|          display: block;
00064|        }
00065|
00066|        .hint {
00067|          display: none;
00068|        }
00069|      }
00070|    </style>
00071|</head>
00072|<body>
00073|    <div class="splash-wrapper" id="splash-root">
00074|        <img
00075|          class="splash-img splash-landscape"
00076|          src="{% static 'img/splash.jpg' %}"
00077|          alt="PGC - Working Capital Group"
00078|        >
00079|        <img
00080|          class="splash-img splash-portrait"
00081|          src="{% static 'img/splashv.jpg' %}"
00082|          alt="PGC - Working Capital Group"
00083|        >
00084|
00085|        <div class="hint">
00086|            Haz clic o presiona cualquier tecla para entrar al tablero.
00087|        </div>
00088|    </div>
00089|
00090|    <script>
00091|    (function () {
00092|        function goDashboard() {
00093|            window.location.href = "{% url 'portal:home' %}";
00094|        }
00095|
00096|        var root = document.getElementById("splash-root");
00097|
00098|        if (root) {
00099|            root.addEventListener("click", function (e) {
00100|                e.preventDefault();
00101|                goDashboard();
00102|            });
00103|        }
00104|
00105|        document.addEventListener("keydown", function () {
00106|            goDashboard();
00107|        });
00108|    })();
00109|    </script>
00110|</body>
00111|</html>
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
PCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVzIj4KPGhlYWQ+CiAgICA8bWV0YSBjaGFyc2V0PSJVVEYtOCI+CiAgICA8dGl0bGU+UEdDIC0gV0NHPC90aXRsZT4KICAgIHslIGxvYWQgc3RhdGljICV9CiAgICA8c3R5bGU+CiAgICAgICogeyBib3gtc2l6aW5nOiBib3JkZXItYm94OyBtYXJnaW46IDA7IHBhZGRpbmc6IDA7IH0KCiAgICAgIGh0bWwsIGJvZHkgewogICAgICAgIGhlaWdodDogMTAwJTsKICAgICAgICB3aWR0aDogMTAwJTsKICAgICAgICBvdmVyZmxvdzogaGlkZGVuOwogICAgICAgIGJhY2tncm91bmQ6ICMxMTE4Mjc7CiAgICAgIH0KCiAgICAgIC5zcGxhc2gtd3JhcHBlciB7CiAgICAgICAgcG9zaXRpb246IHJlbGF0aXZlOwogICAgICAgIHdpZHRoOiAxMDAlOwogICAgICAgIGhlaWdodDogMTAwJTsKICAgICAgICBjdXJzb3I6IHBvaW50ZXI7CiAgICAgICAgYmFja2dyb3VuZDogIzExMTgyNzsKICAgICAgfQoKICAgICAgLnNwbGFzaC1pbWcgewogICAgICAgIHdpZHRoOiAxMDAlOwogICAgICAgIGhlaWdodDogMTAwJTsKICAgICAgICBvYmplY3QtZml0OiBjb3ZlcjsKICAgICAgICBvYmplY3QtcG9zaXRpb246IGNlbnRlciBjZW50ZXI7CiAgICAgICAgZGlzcGxheTogYmxvY2s7CiAgICAgIH0KCiAgICAgIC5zcGxhc2gtcG9ydHJhaXQgewogICAgICAgIGRpc3BsYXk6IG5vbmU7CiAgICAgIH0KCiAgICAgIC5oaW50IHsKICAgICAgICBwb3NpdGlvbjogYWJzb2x1dGU7CiAgICAgICAgYm90dG9tOiAyNHB4OwogICAgICAgIHJpZ2h0OiAyNHB4OwogICAgICAgIHBhZGRpbmc6IDhweCAxMnB4OwogICAgICAgIGJvcmRlci1yYWRpdXM6IDZweDsKICAgICAgICBiYWNrZ3JvdW5kOiByZ2JhKDAsMCwwLDAuNDUpOwogICAgICAgIGNvbG9yOiAjZjlmYWZiOwogICAgICAgIGZvbnQtZmFtaWx5OiBBcmlhbCwgc2Fucy1zZXJpZjsKICAgICAgICBmb250LXNpemU6IDAuOXJlbTsKICAgICAgfQoKICAgICAgQG1lZGlhIChtYXgtd2lkdGg6IDc2OHB4KSB7CiAgICAgICAgLmhpbnQgewogICAgICAgICAgbGVmdDogMTZweDsKICAgICAgICAgIHJpZ2h0OiAxNnB4OwogICAgICAgICAgdGV4dC1hbGlnbjogY2VudGVyOwogICAgICAgIH0KICAgICAgfQoKICAgICAgQG1lZGlhIChvcmllbnRhdGlvbjogcG9ydHJhaXQpIHsKICAgICAgICAuc3BsYXNoLWxhbmRzY2FwZSB7CiAgICAgICAgICBkaXNwbGF5OiBub25lOwogICAgICAgIH0KCiAgICAgICAgLnNwbGFzaC1wb3J0cmFpdCB7CiAgICAgICAgICBkaXNwbGF5OiBibG9jazsKICAgICAgICB9CgogICAgICAgIC5oaW50IHsKICAgICAgICAgIGRpc3BsYXk6IG5vbmU7CiAgICAgICAgfQogICAgICB9CiAgICA8L3N0eWxlPgo8L2hlYWQ+Cjxib2R5PgogICAgPGRpdiBjbGFzcz0ic3BsYXNoLXdyYXBwZXIiIGlkPSJzcGxhc2gtcm9vdCI+CiAgICAgICAgPGltZwogICAgICAgICAgY2xhc3M9InNwbGFzaC1pbWcgc3BsYXNoLWxhbmRzY2FwZSIKICAgICAgICAgIHNyYz0ieyUgc3RhdGljICdpbWcvc3BsYXNoLmpwZycgJX0iCiAgICAgICAgICBhbHQ9IlBHQyAtIFdvcmtpbmcgQ2FwaXRhbCBHcm91cCIKICAgICAgICA+CiAgICAgICAgPGltZwogICAgICAgICAgY2xhc3M9InNwbGFzaC1pbWcgc3BsYXNoLXBvcnRyYWl0IgogICAgICAgICAgc3JjPSJ7JSBzdGF0aWMgJ2ltZy9zcGxhc2h2LmpwZycgJX0iCiAgICAgICAgICBhbHQ9IlBHQyAtIFdvcmtpbmcgQ2FwaXRhbCBHcm91cCIKICAgICAgICA+CgogICAgICAgIDxkaXYgY2xhc3M9ImhpbnQiPgogICAgICAgICAgICBIYXogY2xpYyBvIHByZXNpb25hIGN1YWxxdWllciB0ZWNsYSBwYXJhIGVudHJhciBhbCB0YWJsZXJvLgogICAgICAgIDwvZGl2PgogICAgPC9kaXY+CgogICAgPHNjcmlwdD4KICAgIChmdW5jdGlvbiAoKSB7CiAgICAgICAgZnVuY3Rpb24gZ29EYXNoYm9hcmQoKSB7CiAgICAgICAgICAgIHdpbmRvdy5sb2NhdGlvbi5ocmVmID0gInslIHVybCAncG9ydGFsOmhvbWUnICV9IjsKICAgICAgICB9CgogICAgICAgIHZhciByb290ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoInNwbGFzaC1yb290Iik7CgogICAgICAgIGlmIChyb290KSB7CiAgICAgICAgICAgIHJvb3QuYWRkRXZlbnRMaXN0ZW5lcigiY2xpY2siLCBmdW5jdGlvbiAoZSkgewogICAgICAgICAgICAgICAgZS5wcmV2ZW50RGVmYXVsdCgpOwogICAgICAgICAgICAgICAgZ29EYXNoYm9hcmQoKTsKICAgICAgICAgICAgfSk7CiAgICAgICAgfQoKICAgICAgICBkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCJrZXlkb3duIiwgZnVuY3Rpb24gKCkgewogICAgICAgICAgICBnb0Rhc2hib2FyZCgpOwogICAgICAgIH0pOwogICAgfSkoKTsKICAgIDwvc2NyaXB0Pgo8L2JvZHk+CjwvaHRtbD4=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/wcgone/crm/contacto_list.html
PATH_JSON="templates/wcgone/crm/contacto_list.html"
FILENAME=contacto_list.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=56
SIZE_BYTES_UTF8=1981
CONTENT_SHA256=70748e52fb77b56e514e5b7a7196f67850f6269eb61daadce028fc6b18c93c73
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
{% extends "wcgone_base.html" %}

{% block title %}Contactos — CRM — WCG One{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-2">
  <div class="wcg-report-head">
    <h1 class="h4 fw-semibold mb-0">CRM — Contactos</h1>
    {% include "includes/module_mark.html" with module="crm" %}
  </div>
  <div class="d-flex gap-1">
    <a href="{% url 'wcgone_crm:entidad_list' %}" class="btn btn-sm btn-outline-secondary">← Clientes</a>
    <a href="{% url 'wcgone_crm:tarea_list' %}" class="btn btn-sm btn-outline-secondary">Tareas</a>
  </div>
</div>

<form method="get" class="mb-3">
  <div class="input-group input-group-sm" style="max-width: 320px;">
    <input type="search" name="q" value="{{ request.GET.q }}" class="form-control" placeholder="Buscar nombre o email">
    <button class="btn btn-primary" type="submit">Buscar</button>
  </div>
</form>

<div class="card border-0 shadow-sm">
  <div class="table-responsive">
    <table class="table table-hover table-wcg mb-0">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Entidad</th>
          <th>Cargo</th>
          <th>Email</th>
          <th>Teléfono</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {% for contacto in contactos %}
        <tr>
          <td>{{ contacto.nombre }}</td>
          <td>{{ contacto.entidad.nombre }}</td>
          <td>{{ contacto.cargo|default:"—" }}</td>
          <td>{{ contacto.email|default:"—" }}</td>
          <td>{{ contacto.telefono_movil|default:"—" }}</td>
          <td class="text-end">
            <a href="{% url 'wcgone_crm:entidad_detail' contacto.entidad_id %}" class="btn btn-sm btn-outline-primary">Entidad</a>
          </td>
        </tr>
        {% empty %}
        <tr><td colspan="6" class="text-center text-muted py-4">No hay contactos registrados.</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "wcgone_base.html" %}
00002|
00003|{% block title %}Contactos — CRM — WCG One{% endblock %}
00004|
00005|{% block content %}
00006|<div class="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-2">
00007|  <div class="wcg-report-head">
00008|    <h1 class="h4 fw-semibold mb-0">CRM — Contactos</h1>
00009|    {% include "includes/module_mark.html" with module="crm" %}
00010|  </div>
00011|  <div class="d-flex gap-1">
00012|    <a href="{% url 'wcgone_crm:entidad_list' %}" class="btn btn-sm btn-outline-secondary">← Clientes</a>
00013|    <a href="{% url 'wcgone_crm:tarea_list' %}" class="btn btn-sm btn-outline-secondary">Tareas</a>
00014|  </div>
00015|</div>
00016|
00017|<form method="get" class="mb-3">
00018|  <div class="input-group input-group-sm" style="max-width: 320px;">
00019|    <input type="search" name="q" value="{{ request.GET.q }}" class="form-control" placeholder="Buscar nombre o email">
00020|    <button class="btn btn-primary" type="submit">Buscar</button>
00021|  </div>
00022|</form>
00023|
00024|<div class="card border-0 shadow-sm">
00025|  <div class="table-responsive">
00026|    <table class="table table-hover table-wcg mb-0">
00027|      <thead>
00028|        <tr>
00029|          <th>Nombre</th>
00030|          <th>Entidad</th>
00031|          <th>Cargo</th>
00032|          <th>Email</th>
00033|          <th>Teléfono</th>
00034|          <th></th>
00035|        </tr>
00036|      </thead>
00037|      <tbody>
00038|        {% for contacto in contactos %}
00039|        <tr>
00040|          <td>{{ contacto.nombre }}</td>
00041|          <td>{{ contacto.entidad.nombre }}</td>
00042|          <td>{{ contacto.cargo|default:"—" }}</td>
00043|          <td>{{ contacto.email|default:"—" }}</td>
00044|          <td>{{ contacto.telefono_movil|default:"—" }}</td>
00045|          <td class="text-end">
00046|            <a href="{% url 'wcgone_crm:entidad_detail' contacto.entidad_id %}" class="btn btn-sm btn-outline-primary">Entidad</a>
00047|          </td>
00048|        </tr>
00049|        {% empty %}
00050|        <tr><td colspan="6" class="text-center text-muted py-4">No hay contactos registrados.</td></tr>
00051|        {% endfor %}
00052|      </tbody>
00053|    </table>
00054|  </div>
00055|</div>
00056|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAid2Nnb25lX2Jhc2UuaHRtbCIgJX0KCnslIGJsb2NrIHRpdGxlICV9Q29udGFjdG9zIOKAlCBDUk0g4oCUIFdDRyBPbmV7JSBlbmRibG9jayAlfQoKeyUgYmxvY2sgY29udGVudCAlfQo8ZGl2IGNsYXNzPSJkLWZsZXgganVzdGlmeS1jb250ZW50LWJldHdlZW4gYWxpZ24taXRlbXMtc3RhcnQgbWItMyBmbGV4LXdyYXAgZ2FwLTIiPgogIDxkaXYgY2xhc3M9IndjZy1yZXBvcnQtaGVhZCI+CiAgICA8aDEgY2xhc3M9Img0IGZ3LXNlbWlib2xkIG1iLTAiPkNSTSDigJQgQ29udGFjdG9zPC9oMT4KICAgIHslIGluY2x1ZGUgImluY2x1ZGVzL21vZHVsZV9tYXJrLmh0bWwiIHdpdGggbW9kdWxlPSJjcm0iICV9CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iZC1mbGV4IGdhcC0xIj4KICAgIDxhIGhyZWY9InslIHVybCAnd2Nnb25lX2NybTplbnRpZGFkX2xpc3QnICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1zZWNvbmRhcnkiPuKGkCBDbGllbnRlczwvYT4KICAgIDxhIGhyZWY9InslIHVybCAnd2Nnb25lX2NybTp0YXJlYV9saXN0JyAlfSIgY2xhc3M9ImJ0biBidG4tc20gYnRuLW91dGxpbmUtc2Vjb25kYXJ5Ij5UYXJlYXM8L2E+CiAgPC9kaXY+CjwvZGl2PgoKPGZvcm0gbWV0aG9kPSJnZXQiIGNsYXNzPSJtYi0zIj4KICA8ZGl2IGNsYXNzPSJpbnB1dC1ncm91cCBpbnB1dC1ncm91cC1zbSIgc3R5bGU9Im1heC13aWR0aDogMzIwcHg7Ij4KICAgIDxpbnB1dCB0eXBlPSJzZWFyY2giIG5hbWU9InEiIHZhbHVlPSJ7eyByZXF1ZXN0LkdFVC5xIH19IiBjbGFzcz0iZm9ybS1jb250cm9sIiBwbGFjZWhvbGRlcj0iQnVzY2FyIG5vbWJyZSBvIGVtYWlsIj4KICAgIDxidXR0b24gY2xhc3M9ImJ0biBidG4tcHJpbWFyeSIgdHlwZT0ic3VibWl0Ij5CdXNjYXI8L2J1dHRvbj4KICA8L2Rpdj4KPC9mb3JtPgoKPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20iPgogIDxkaXYgY2xhc3M9InRhYmxlLXJlc3BvbnNpdmUiPgogICAgPHRhYmxlIGNsYXNzPSJ0YWJsZSB0YWJsZS1ob3ZlciB0YWJsZS13Y2cgbWItMCI+CiAgICAgIDx0aGVhZD4KICAgICAgICA8dHI+CiAgICAgICAgICA8dGg+Tm9tYnJlPC90aD4KICAgICAgICAgIDx0aD5FbnRpZGFkPC90aD4KICAgICAgICAgIDx0aD5DYXJnbzwvdGg+CiAgICAgICAgICA8dGg+RW1haWw8L3RoPgogICAgICAgICAgPHRoPlRlbMOpZm9ubzwvdGg+CiAgICAgICAgICA8dGg+PC90aD4KICAgICAgICA8L3RyPgogICAgICA8L3RoZWFkPgogICAgICA8dGJvZHk+CiAgICAgICAgeyUgZm9yIGNvbnRhY3RvIGluIGNvbnRhY3RvcyAlfQogICAgICAgIDx0cj4KICAgICAgICAgIDx0ZD57eyBjb250YWN0by5ub21icmUgfX08L3RkPgogICAgICAgICAgPHRkPnt7IGNvbnRhY3RvLmVudGlkYWQubm9tYnJlIH19PC90ZD4KICAgICAgICAgIDx0ZD57eyBjb250YWN0by5jYXJnb3xkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgIDx0ZD57eyBjb250YWN0by5lbWFpbHxkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgIDx0ZD57eyBjb250YWN0by50ZWxlZm9ub19tb3ZpbHxkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgIDx0ZCBjbGFzcz0idGV4dC1lbmQiPgogICAgICAgICAgICA8YSBocmVmPSJ7JSB1cmwgJ3djZ29uZV9jcm06ZW50aWRhZF9kZXRhaWwnIGNvbnRhY3RvLmVudGlkYWRfaWQgJX0iIGNsYXNzPSJidG4gYnRuLXNtIGJ0bi1vdXRsaW5lLXByaW1hcnkiPkVudGlkYWQ8L2E+CiAgICAgICAgICA8L3RkPgogICAgICAgIDwvdHI+CiAgICAgICAgeyUgZW1wdHkgJX0KICAgICAgICA8dHI+PHRkIGNvbHNwYW49IjYiIGNsYXNzPSJ0ZXh0LWNlbnRlciB0ZXh0LW11dGVkIHB5LTQiPk5vIGhheSBjb250YWN0b3MgcmVnaXN0cmFkb3MuPC90ZD48L3RyPgogICAgICAgIHslIGVuZGZvciAlfQogICAgICA8L3Rib2R5PgogICAgPC90YWJsZT4KICA8L2Rpdj4KPC9kaXY+CnslIGVuZGJsb2NrICV9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
