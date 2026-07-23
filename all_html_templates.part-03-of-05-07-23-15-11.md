# CONCATENATED .HTML FILES

PART_NUMBER=3
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
PATH_LITERAL=templates/pgc/admin_tv_charts.html
PATH_JSON="templates/pgc/admin_tv_charts.html"
FILENAME=admin_tv_charts.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=195
SIZE_BYTES_UTF8=6069
CONTENT_SHA256=8cd4d8d6461953a66e269fe391d75354623b9ad69a7b75e960aabc6bfcc91d45
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

{% block title %}Charts TV{% endblock %}

{% block content %}
{% include "pgc/admin/_styles.html" %}
<style>
  .tv-urls { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.84rem; line-height: 1.55; }
  .tv-live-grid, .tv-thumbs {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 12px;
    margin-top: 12px;
  }
  .tv-thumbs { grid-template-columns: repeat(4, minmax(0, 1fr)); }
  .tv-card, .tv-set {
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 10px 12px;
    background: #fff;
  }
  .tv-set { margin-bottom: 12px; }
  .tv-card img, .tv-thumbs img {
    width: 100%;
    aspect-ratio: 16 / 9;
    object-fit: contain;
    background: #f8fafc;
    border-radius: 6px;
    border: 1px solid #edf2f7;
    margin-top: 6px;
  }
  .tv-missing {
    width: 100%;
    aspect-ratio: 16 / 9;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #94a3b8;
    background: #f8fafc;
    border-radius: 6px;
    border: 1px dashed #cbd5e1;
    font-size: 0.82rem;
    margin-top: 6px;
  }
  .tv-set-head {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
    justify-content: space-between;
  }
  .tv-slot-label {
    display: flex;
    gap: 6px;
    align-items: center;
    font-size: 0.8rem;
  }
  .tv-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid #edf2f7;
  }
  @media (max-width: 720px) {
    .tv-thumbs { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  }
</style>

<div class="adm">
  {% include "pgc/admin/_nav.html" with adm_nav_active="tv_charts" show_django_admin=True %}

  <div class="adm-header">
    <div class="adm-header-top">
      <div>
        <p class="muted" style="margin:0;">Televisor · charts vivos</p>
        <div class="adm-period-label">TV charts</div>
      </div>
    </div>
  </div>

  <div class="adm-panel" style="margin-bottom:16px;">
    <h3 style="margin-top:0;">Vivos (lectura TV)</h3>
    <p class="muted" style="margin-top:0;">
      URLs públicas fijas. <strong>Exportación 4 charts</strong> guarda copia con fecha/hora
      en archivo <em>y</em> actualiza automáticamente los vivos (TV).
      Directorio servidor: <code>media/tv/</code> (archive + live).
      En Railway el disco es efímero: un redeploy borra estos PNG hasta volver a exportar
      (o monte un volumen en <code>media/</code>).
    </p>
    <div class="tv-urls">
      {% for slot in live_slots %}
      <div>
        {{ request.scheme }}://{{ request.get_host }}{{ slot.url }}
        {% if slot.exists %}· listo{% else %}· vacío{% endif %}
      </div>
      {% endfor %}
    </div>
    <div class="tv-live-grid">
      {% for slot in live_slots %}
      <div class="tv-card">
        <strong>{{ slot.name }}</strong>
        {% if slot.exists %}
        <img src="{{ slot.url }}?v={{ slot.size }}" alt="{{ slot.name }}">
        {% else %}
        <div class="tv-missing">Sin archivo</div>
        {% endif %}
      </div>
      {% endfor %}
    </div>
    {% if live_all_empty and archive_sets %}
    <p class="muted" style="margin-top:12px;">
      Hay sets en archivo pero los vivos están vacíos.
      Use <em>Activar este set en TV</em> abajo, o vuelva a generar con <strong>Exportación 4 charts</strong>
      (ahora actualiza vivos automáticamente).
    </p>
    {% endif %}
  </div>

  <div class="adm-panel">
    <h3 style="margin-top:0;">Archivo (nombres con fecha/hora)</h3>
    <p class="muted" style="margin-top:0;">
      Marque PNG y use <em>Copiar a TV</em> o <em>Borrar seleccionados</em>.
      O active un set completo g1–g4 de un sello.
    </p>

    {% if not archive_sets %}
    <p class="muted">
      Aún no hay PNG archivados. Use <strong>Exportación 4 charts</strong> en el Tablero principal;
      se descargan localmente y también se guardan aquí (archivo + vivos).
      Si está en Railway y acaba de redesplegar, el disco se vació: vuelva a exportar.
    </p>
    {% else %}
    <form method="post">
      {% csrf_token %}
      <input type="hidden" name="stamp" id="tv-stamp" value="">

      {% for aset in archive_sets %}
      <div class="tv-set">
        <div class="tv-set-head">
          <div>
            <strong>Sello {{ aset.stamp }}</strong>
            {% if aset.complete %}
            <span class="adm-badge loaded">completo</span>
            {% else %}
            <span class="adm-badge observed">incompleto</span>
            {% endif %}
          </div>
          {% if aset.complete %}
          <button
            type="submit"
            class="adm-btn adm-btn-primary"
            name="action"
            value="promote_stamp"
            onclick="document.getElementById('tv-stamp').value='{{ aset.stamp }}';"
          >Activar este set en TV</button>
          {% endif %}
        </div>
        <div class="tv-thumbs">
          {% for s in aset.slots %}
          <div>
            {% if s.file %}
            <label class="tv-slot-label">
              <input type="checkbox" name="files" value="{{ s.name }}">
              g{{ s.slot }}
            </label>
            <img src="{{ s.preview_url }}" alt="{{ s.name }}">
            {% else %}
            <div class="tv-slot-label muted">g{{ s.slot }}</div>
            <div class="tv-missing">falta</div>
            {% endif %}
          </div>
          {% endfor %}
        </div>
      </div>
      {% endfor %}

      <div class="tv-actions">
        <button type="submit" class="adm-btn adm-btn-primary" name="action" value="promote">
          Copiar seleccionados a TV
        </button>
        <button
          type="submit"
          class="adm-btn adm-btn-secondary"
          name="action"
          value="delete"
          onclick="return confirm('¿Borrar los PNG archivados seleccionados? Los vivos no se tocan.');"
        >Borrar seleccionados</button>
      </div>
    </form>
    {% endif %}
  </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base.html" %}
00002|
00003|{% block title %}Charts TV{% endblock %}
00004|
00005|{% block content %}
00006|{% include "pgc/admin/_styles.html" %}
00007|<style>
00008|  .tv-urls { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.84rem; line-height: 1.55; }
00009|  .tv-live-grid, .tv-thumbs {
00010|    display: grid;
00011|    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
00012|    gap: 12px;
00013|    margin-top: 12px;
00014|  }
00015|  .tv-thumbs { grid-template-columns: repeat(4, minmax(0, 1fr)); }
00016|  .tv-card, .tv-set {
00017|    border: 1px solid #e2e8f0;
00018|    border-radius: 10px;
00019|    padding: 10px 12px;
00020|    background: #fff;
00021|  }
00022|  .tv-set { margin-bottom: 12px; }
00023|  .tv-card img, .tv-thumbs img {
00024|    width: 100%;
00025|    aspect-ratio: 16 / 9;
00026|    object-fit: contain;
00027|    background: #f8fafc;
00028|    border-radius: 6px;
00029|    border: 1px solid #edf2f7;
00030|    margin-top: 6px;
00031|  }
00032|  .tv-missing {
00033|    width: 100%;
00034|    aspect-ratio: 16 / 9;
00035|    display: flex;
00036|    align-items: center;
00037|    justify-content: center;
00038|    color: #94a3b8;
00039|    background: #f8fafc;
00040|    border-radius: 6px;
00041|    border: 1px dashed #cbd5e1;
00042|    font-size: 0.82rem;
00043|    margin-top: 6px;
00044|  }
00045|  .tv-set-head {
00046|    display: flex;
00047|    flex-wrap: wrap;
00048|    gap: 10px;
00049|    align-items: center;
00050|    justify-content: space-between;
00051|  }
00052|  .tv-slot-label {
00053|    display: flex;
00054|    gap: 6px;
00055|    align-items: center;
00056|    font-size: 0.8rem;
00057|  }
00058|  .tv-actions {
00059|    display: flex;
00060|    flex-wrap: wrap;
00061|    gap: 8px;
00062|    margin-top: 14px;
00063|    padding-top: 12px;
00064|    border-top: 1px solid #edf2f7;
00065|  }
00066|  @media (max-width: 720px) {
00067|    .tv-thumbs { grid-template-columns: repeat(2, minmax(0, 1fr)); }
00068|  }
00069|</style>
00070|
00071|<div class="adm">
00072|  {% include "pgc/admin/_nav.html" with adm_nav_active="tv_charts" show_django_admin=True %}
00073|
00074|  <div class="adm-header">
00075|    <div class="adm-header-top">
00076|      <div>
00077|        <p class="muted" style="margin:0;">Televisor · charts vivos</p>
00078|        <div class="adm-period-label">TV charts</div>
00079|      </div>
00080|    </div>
00081|  </div>
00082|
00083|  <div class="adm-panel" style="margin-bottom:16px;">
00084|    <h3 style="margin-top:0;">Vivos (lectura TV)</h3>
00085|    <p class="muted" style="margin-top:0;">
00086|      URLs públicas fijas. <strong>Exportación 4 charts</strong> guarda copia con fecha/hora
00087|      en archivo <em>y</em> actualiza automáticamente los vivos (TV).
00088|      Directorio servidor: <code>media/tv/</code> (archive + live).
00089|      En Railway el disco es efímero: un redeploy borra estos PNG hasta volver a exportar
00090|      (o monte un volumen en <code>media/</code>).
00091|    </p>
00092|    <div class="tv-urls">
00093|      {% for slot in live_slots %}
00094|      <div>
00095|        {{ request.scheme }}://{{ request.get_host }}{{ slot.url }}
00096|        {% if slot.exists %}· listo{% else %}· vacío{% endif %}
00097|      </div>
00098|      {% endfor %}
00099|    </div>
00100|    <div class="tv-live-grid">
00101|      {% for slot in live_slots %}
00102|      <div class="tv-card">
00103|        <strong>{{ slot.name }}</strong>
00104|        {% if slot.exists %}
00105|        <img src="{{ slot.url }}?v={{ slot.size }}" alt="{{ slot.name }}">
00106|        {% else %}
00107|        <div class="tv-missing">Sin archivo</div>
00108|        {% endif %}
00109|      </div>
00110|      {% endfor %}
00111|    </div>
00112|    {% if live_all_empty and archive_sets %}
00113|    <p class="muted" style="margin-top:12px;">
00114|      Hay sets en archivo pero los vivos están vacíos.
00115|      Use <em>Activar este set en TV</em> abajo, o vuelva a generar con <strong>Exportación 4 charts</strong>
00116|      (ahora actualiza vivos automáticamente).
00117|    </p>
00118|    {% endif %}
00119|  </div>
00120|
00121|  <div class="adm-panel">
00122|    <h3 style="margin-top:0;">Archivo (nombres con fecha/hora)</h3>
00123|    <p class="muted" style="margin-top:0;">
00124|      Marque PNG y use <em>Copiar a TV</em> o <em>Borrar seleccionados</em>.
00125|      O active un set completo g1–g4 de un sello.
00126|    </p>
00127|
00128|    {% if not archive_sets %}
00129|    <p class="muted">
00130|      Aún no hay PNG archivados. Use <strong>Exportación 4 charts</strong> en el Tablero principal;
00131|      se descargan localmente y también se guardan aquí (archivo + vivos).
00132|      Si está en Railway y acaba de redesplegar, el disco se vació: vuelva a exportar.
00133|    </p>
00134|    {% else %}
00135|    <form method="post">
00136|      {% csrf_token %}
00137|      <input type="hidden" name="stamp" id="tv-stamp" value="">
00138|
00139|      {% for aset in archive_sets %}
00140|      <div class="tv-set">
00141|        <div class="tv-set-head">
00142|          <div>
00143|            <strong>Sello {{ aset.stamp }}</strong>
00144|            {% if aset.complete %}
00145|            <span class="adm-badge loaded">completo</span>
00146|            {% else %}
00147|            <span class="adm-badge observed">incompleto</span>
00148|            {% endif %}
00149|          </div>
00150|          {% if aset.complete %}
00151|          <button
00152|            type="submit"
00153|            class="adm-btn adm-btn-primary"
00154|            name="action"
00155|            value="promote_stamp"
00156|            onclick="document.getElementById('tv-stamp').value='{{ aset.stamp }}';"
00157|          >Activar este set en TV</button>
00158|          {% endif %}
00159|        </div>
00160|        <div class="tv-thumbs">
00161|          {% for s in aset.slots %}
00162|          <div>
00163|            {% if s.file %}
00164|            <label class="tv-slot-label">
00165|              <input type="checkbox" name="files" value="{{ s.name }}">
00166|              g{{ s.slot }}
00167|            </label>
00168|            <img src="{{ s.preview_url }}" alt="{{ s.name }}">
00169|            {% else %}
00170|            <div class="tv-slot-label muted">g{{ s.slot }}</div>
00171|            <div class="tv-missing">falta</div>
00172|            {% endif %}
00173|          </div>
00174|          {% endfor %}
00175|        </div>
00176|      </div>
00177|      {% endfor %}
00178|
00179|      <div class="tv-actions">
00180|        <button type="submit" class="adm-btn adm-btn-primary" name="action" value="promote">
00181|          Copiar seleccionados a TV
00182|        </button>
00183|        <button
00184|          type="submit"
00185|          class="adm-btn adm-btn-secondary"
00186|          name="action"
00187|          value="delete"
00188|          onclick="return confirm('¿Borrar los PNG archivados seleccionados? Los vivos no se tocan.');"
00189|        >Borrar seleccionados</button>
00190|      </div>
00191|    </form>
00192|    {% endif %}
00193|  </div>
00194|</div>
00195|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZS5odG1sIiAlfQoKeyUgYmxvY2sgdGl0bGUgJX1DaGFydHMgVFZ7JSBlbmRibG9jayAlfQoKeyUgYmxvY2sgY29udGVudCAlfQp7JSBpbmNsdWRlICJwZ2MvYWRtaW4vX3N0eWxlcy5odG1sIiAlfQo8c3R5bGU+CiAgLnR2LXVybHMgeyBmb250LWZhbWlseTogdWktbW9ub3NwYWNlLCBTRk1vbm8tUmVndWxhciwgTWVubG8sIENvbnNvbGFzLCBtb25vc3BhY2U7IGZvbnQtc2l6ZTogMC44NHJlbTsgbGluZS1oZWlnaHQ6IDEuNTU7IH0KICAudHYtbGl2ZS1ncmlkLCAudHYtdGh1bWJzIHsKICAgIGRpc3BsYXk6IGdyaWQ7CiAgICBncmlkLXRlbXBsYXRlLWNvbHVtbnM6IHJlcGVhdChhdXRvLWZpbGwsIG1pbm1heCgxODBweCwgMWZyKSk7CiAgICBnYXA6IDEycHg7CiAgICBtYXJnaW4tdG9wOiAxMnB4OwogIH0KICAudHYtdGh1bWJzIHsgZ3JpZC10ZW1wbGF0ZS1jb2x1bW5zOiByZXBlYXQoNCwgbWlubWF4KDAsIDFmcikpOyB9CiAgLnR2LWNhcmQsIC50di1zZXQgewogICAgYm9yZGVyOiAxcHggc29saWQgI2UyZThmMDsKICAgIGJvcmRlci1yYWRpdXM6IDEwcHg7CiAgICBwYWRkaW5nOiAxMHB4IDEycHg7CiAgICBiYWNrZ3JvdW5kOiAjZmZmOwogIH0KICAudHYtc2V0IHsgbWFyZ2luLWJvdHRvbTogMTJweDsgfQogIC50di1jYXJkIGltZywgLnR2LXRodW1icyBpbWcgewogICAgd2lkdGg6IDEwMCU7CiAgICBhc3BlY3QtcmF0aW86IDE2IC8gOTsKICAgIG9iamVjdC1maXQ6IGNvbnRhaW47CiAgICBiYWNrZ3JvdW5kOiAjZjhmYWZjOwogICAgYm9yZGVyLXJhZGl1czogNnB4OwogICAgYm9yZGVyOiAxcHggc29saWQgI2VkZjJmNzsKICAgIG1hcmdpbi10b3A6IDZweDsKICB9CiAgLnR2LW1pc3NpbmcgewogICAgd2lkdGg6IDEwMCU7CiAgICBhc3BlY3QtcmF0aW86IDE2IC8gOTsKICAgIGRpc3BsYXk6IGZsZXg7CiAgICBhbGlnbi1pdGVtczogY2VudGVyOwogICAganVzdGlmeS1jb250ZW50OiBjZW50ZXI7CiAgICBjb2xvcjogIzk0YTNiODsKICAgIGJhY2tncm91bmQ6ICNmOGZhZmM7CiAgICBib3JkZXItcmFkaXVzOiA2cHg7CiAgICBib3JkZXI6IDFweCBkYXNoZWQgI2NiZDVlMTsKICAgIGZvbnQtc2l6ZTogMC44MnJlbTsKICAgIG1hcmdpbi10b3A6IDZweDsKICB9CiAgLnR2LXNldC1oZWFkIHsKICAgIGRpc3BsYXk6IGZsZXg7CiAgICBmbGV4LXdyYXA6IHdyYXA7CiAgICBnYXA6IDEwcHg7CiAgICBhbGlnbi1pdGVtczogY2VudGVyOwogICAganVzdGlmeS1jb250ZW50OiBzcGFjZS1iZXR3ZWVuOwogIH0KICAudHYtc2xvdC1sYWJlbCB7CiAgICBkaXNwbGF5OiBmbGV4OwogICAgZ2FwOiA2cHg7CiAgICBhbGlnbi1pdGVtczogY2VudGVyOwogICAgZm9udC1zaXplOiAwLjhyZW07CiAgfQogIC50di1hY3Rpb25zIHsKICAgIGRpc3BsYXk6IGZsZXg7CiAgICBmbGV4LXdyYXA6IHdyYXA7CiAgICBnYXA6IDhweDsKICAgIG1hcmdpbi10b3A6IDE0cHg7CiAgICBwYWRkaW5nLXRvcDogMTJweDsKICAgIGJvcmRlci10b3A6IDFweCBzb2xpZCAjZWRmMmY3OwogIH0KICBAbWVkaWEgKG1heC13aWR0aDogNzIwcHgpIHsKICAgIC50di10aHVtYnMgeyBncmlkLXRlbXBsYXRlLWNvbHVtbnM6IHJlcGVhdCgyLCBtaW5tYXgoMCwgMWZyKSk7IH0KICB9Cjwvc3R5bGU+Cgo8ZGl2IGNsYXNzPSJhZG0iPgogIHslIGluY2x1ZGUgInBnYy9hZG1pbi9fbmF2Lmh0bWwiIHdpdGggYWRtX25hdl9hY3RpdmU9InR2X2NoYXJ0cyIgc2hvd19kamFuZ29fYWRtaW49VHJ1ZSAlfQoKICA8ZGl2IGNsYXNzPSJhZG0taGVhZGVyIj4KICAgIDxkaXYgY2xhc3M9ImFkbS1oZWFkZXItdG9wIj4KICAgICAgPGRpdj4KICAgICAgICA8cCBjbGFzcz0ibXV0ZWQiIHN0eWxlPSJtYXJnaW46MDsiPlRlbGV2aXNvciDCtyBjaGFydHMgdml2b3M8L3A+CiAgICAgICAgPGRpdiBjbGFzcz0iYWRtLXBlcmlvZC1sYWJlbCI+VFYgY2hhcnRzPC9kaXY+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CiAgPC9kaXY+CgogIDxkaXYgY2xhc3M9ImFkbS1wYW5lbCIgc3R5bGU9Im1hcmdpbi1ib3R0b206MTZweDsiPgogICAgPGgzIHN0eWxlPSJtYXJnaW4tdG9wOjA7Ij5WaXZvcyAobGVjdHVyYSBUVik8L2gzPgogICAgPHAgY2xhc3M9Im11dGVkIiBzdHlsZT0ibWFyZ2luLXRvcDowOyI+CiAgICAgIFVSTHMgcMO6YmxpY2FzIGZpamFzLiA8c3Ryb25nPkV4cG9ydGFjacOzbiA0IGNoYXJ0czwvc3Ryb25nPiBndWFyZGEgY29waWEgY29uIGZlY2hhL2hvcmEKICAgICAgZW4gYXJjaGl2byA8ZW0+eTwvZW0+IGFjdHVhbGl6YSBhdXRvbcOhdGljYW1lbnRlIGxvcyB2aXZvcyAoVFYpLgogICAgICBEaXJlY3RvcmlvIHNlcnZpZG9yOiA8Y29kZT5tZWRpYS90di88L2NvZGU+IChhcmNoaXZlICsgbGl2ZSkuCiAgICAgIEVuIFJhaWx3YXkgZWwgZGlzY28gZXMgZWbDrW1lcm86IHVuIHJlZGVwbG95IGJvcnJhIGVzdG9zIFBORyBoYXN0YSB2b2x2ZXIgYSBleHBvcnRhcgogICAgICAobyBtb250ZSB1biB2b2x1bWVuIGVuIDxjb2RlPm1lZGlhLzwvY29kZT4pLgogICAgPC9wPgogICAgPGRpdiBjbGFzcz0idHYtdXJscyI+CiAgICAgIHslIGZvciBzbG90IGluIGxpdmVfc2xvdHMgJX0KICAgICAgPGRpdj4KICAgICAgICB7eyByZXF1ZXN0LnNjaGVtZSB9fTovL3t7IHJlcXVlc3QuZ2V0X2hvc3QgfX17eyBzbG90LnVybCB9fQogICAgICAgIHslIGlmIHNsb3QuZXhpc3RzICV9wrcgbGlzdG97JSBlbHNlICV9wrcgdmFjw61veyUgZW5kaWYgJX0KICAgICAgPC9kaXY+CiAgICAgIHslIGVuZGZvciAlfQogICAgPC9kaXY+CiAgICA8ZGl2IGNsYXNzPSJ0di1saXZlLWdyaWQiPgogICAgICB7JSBmb3Igc2xvdCBpbiBsaXZlX3Nsb3RzICV9CiAgICAgIDxkaXYgY2xhc3M9InR2LWNhcmQiPgogICAgICAgIDxzdHJvbmc+e3sgc2xvdC5uYW1lIH19PC9zdHJvbmc+CiAgICAgICAgeyUgaWYgc2xvdC5leGlzdHMgJX0KICAgICAgICA8aW1nIHNyYz0ie3sgc2xvdC51cmwgfX0/dj17eyBzbG90LnNpemUgfX0iIGFsdD0ie3sgc2xvdC5uYW1lIH19Ij4KICAgICAgICB7JSBlbHNlICV9CiAgICAgICAgPGRpdiBjbGFzcz0idHYtbWlzc2luZyI+U2luIGFyY2hpdm88L2Rpdj4KICAgICAgICB7JSBlbmRpZiAlfQogICAgICA8L2Rpdj4KICAgICAgeyUgZW5kZm9yICV9CiAgICA8L2Rpdj4KICAgIHslIGlmIGxpdmVfYWxsX2VtcHR5IGFuZCBhcmNoaXZlX3NldHMgJX0KICAgIDxwIGNsYXNzPSJtdXRlZCIgc3R5bGU9Im1hcmdpbi10b3A6MTJweDsiPgogICAgICBIYXkgc2V0cyBlbiBhcmNoaXZvIHBlcm8gbG9zIHZpdm9zIGVzdMOhbiB2YWPDrW9zLgogICAgICBVc2UgPGVtPkFjdGl2YXIgZXN0ZSBzZXQgZW4gVFY8L2VtPiBhYmFqbywgbyB2dWVsdmEgYSBnZW5lcmFyIGNvbiA8c3Ryb25nPkV4cG9ydGFjacOzbiA0IGNoYXJ0czwvc3Ryb25nPgogICAgICAoYWhvcmEgYWN0dWFsaXphIHZpdm9zIGF1dG9tw6F0aWNhbWVudGUpLgogICAgPC9wPgogICAgeyUgZW5kaWYgJX0KICA8L2Rpdj4KCiAgPGRpdiBjbGFzcz0iYWRtLXBhbmVsIj4KICAgIDxoMyBzdHlsZT0ibWFyZ2luLXRvcDowOyI+QXJjaGl2byAobm9tYnJlcyBjb24gZmVjaGEvaG9yYSk8L2gzPgogICAgPHAgY2xhc3M9Im11dGVkIiBzdHlsZT0ibWFyZ2luLXRvcDowOyI+CiAgICAgIE1hcnF1ZSBQTkcgeSB1c2UgPGVtPkNvcGlhciBhIFRWPC9lbT4gbyA8ZW0+Qm9ycmFyIHNlbGVjY2lvbmFkb3M8L2VtPi4KICAgICAgTyBhY3RpdmUgdW4gc2V0IGNvbXBsZXRvIGcx4oCTZzQgZGUgdW4gc2VsbG8uCiAgICA8L3A+CgogICAgeyUgaWYgbm90IGFyY2hpdmVfc2V0cyAlfQogICAgPHAgY2xhc3M9Im11dGVkIj4KICAgICAgQcO6biBubyBoYXkgUE5HIGFyY2hpdmFkb3MuIFVzZSA8c3Ryb25nPkV4cG9ydGFjacOzbiA0IGNoYXJ0czwvc3Ryb25nPiBlbiBlbCBUYWJsZXJvIHByaW5jaXBhbDsKICAgICAgc2UgZGVzY2FyZ2FuIGxvY2FsbWVudGUgeSB0YW1iacOpbiBzZSBndWFyZGFuIGFxdcOtIChhcmNoaXZvICsgdml2b3MpLgogICAgICBTaSBlc3TDoSBlbiBSYWlsd2F5IHkgYWNhYmEgZGUgcmVkZXNwbGVnYXIsIGVsIGRpc2NvIHNlIHZhY2nDszogdnVlbHZhIGEgZXhwb3J0YXIuCiAgICA8L3A+CiAgICB7JSBlbHNlICV9CiAgICA8Zm9ybSBtZXRob2Q9InBvc3QiPgogICAgICB7JSBjc3JmX3Rva2VuICV9CiAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9InN0YW1wIiBpZD0idHYtc3RhbXAiIHZhbHVlPSIiPgoKICAgICAgeyUgZm9yIGFzZXQgaW4gYXJjaGl2ZV9zZXRzICV9CiAgICAgIDxkaXYgY2xhc3M9InR2LXNldCI+CiAgICAgICAgPGRpdiBjbGFzcz0idHYtc2V0LWhlYWQiPgogICAgICAgICAgPGRpdj4KICAgICAgICAgICAgPHN0cm9uZz5TZWxsbyB7eyBhc2V0LnN0YW1wIH19PC9zdHJvbmc+CiAgICAgICAgICAgIHslIGlmIGFzZXQuY29tcGxldGUgJX0KICAgICAgICAgICAgPHNwYW4gY2xhc3M9ImFkbS1iYWRnZSBsb2FkZWQiPmNvbXBsZXRvPC9zcGFuPgogICAgICAgICAgICB7JSBlbHNlICV9CiAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJhZG0tYmFkZ2Ugb2JzZXJ2ZWQiPmluY29tcGxldG88L3NwYW4+CiAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICA8L2Rpdj4KICAgICAgICAgIHslIGlmIGFzZXQuY29tcGxldGUgJX0KICAgICAgICAgIDxidXR0b24KICAgICAgICAgICAgdHlwZT0ic3VibWl0IgogICAgICAgICAgICBjbGFzcz0iYWRtLWJ0biBhZG0tYnRuLXByaW1hcnkiCiAgICAgICAgICAgIG5hbWU9ImFjdGlvbiIKICAgICAgICAgICAgdmFsdWU9InByb21vdGVfc3RhbXAiCiAgICAgICAgICAgIG9uY2xpY2s9ImRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCd0di1zdGFtcCcpLnZhbHVlPSd7eyBhc2V0LnN0YW1wIH19JzsiCiAgICAgICAgICA+QWN0aXZhciBlc3RlIHNldCBlbiBUVjwvYnV0dG9uPgogICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICA8L2Rpdj4KICAgICAgICA8ZGl2IGNsYXNzPSJ0di10aHVtYnMiPgogICAgICAgICAgeyUgZm9yIHMgaW4gYXNldC5zbG90cyAlfQogICAgICAgICAgPGRpdj4KICAgICAgICAgICAgeyUgaWYgcy5maWxlICV9CiAgICAgICAgICAgIDxsYWJlbCBjbGFzcz0idHYtc2xvdC1sYWJlbCI+CiAgICAgICAgICAgICAgPGlucHV0IHR5cGU9ImNoZWNrYm94IiBuYW1lPSJmaWxlcyIgdmFsdWU9Int7IHMubmFtZSB9fSI+CiAgICAgICAgICAgICAgZ3t7IHMuc2xvdCB9fQogICAgICAgICAgICA8L2xhYmVsPgogICAgICAgICAgICA8aW1nIHNyYz0ie3sgcy5wcmV2aWV3X3VybCB9fSIgYWx0PSJ7eyBzLm5hbWUgfX0iPgogICAgICAgICAgICB7JSBlbHNlICV9CiAgICAgICAgICAgIDxkaXYgY2xhc3M9InR2LXNsb3QtbGFiZWwgbXV0ZWQiPmd7eyBzLnNsb3QgfX08L2Rpdj4KICAgICAgICAgICAgPGRpdiBjbGFzcz0idHYtbWlzc2luZyI+ZmFsdGE8L2Rpdj4KICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgIDwvZGl2PgogICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgPC9kaXY+CiAgICAgIDwvZGl2PgogICAgICB7JSBlbmRmb3IgJX0KCiAgICAgIDxkaXYgY2xhc3M9InR2LWFjdGlvbnMiPgogICAgICAgIDxidXR0b24gdHlwZT0ic3VibWl0IiBjbGFzcz0iYWRtLWJ0biBhZG0tYnRuLXByaW1hcnkiIG5hbWU9ImFjdGlvbiIgdmFsdWU9InByb21vdGUiPgogICAgICAgICAgQ29waWFyIHNlbGVjY2lvbmFkb3MgYSBUVgogICAgICAgIDwvYnV0dG9uPgogICAgICAgIDxidXR0b24KICAgICAgICAgIHR5cGU9InN1Ym1pdCIKICAgICAgICAgIGNsYXNzPSJhZG0tYnRuIGFkbS1idG4tc2Vjb25kYXJ5IgogICAgICAgICAgbmFtZT0iYWN0aW9uIgogICAgICAgICAgdmFsdWU9ImRlbGV0ZSIKICAgICAgICAgIG9uY2xpY2s9InJldHVybiBjb25maXJtKCfCv0JvcnJhciBsb3MgUE5HIGFyY2hpdmFkb3Mgc2VsZWNjaW9uYWRvcz8gTG9zIHZpdm9zIG5vIHNlIHRvY2FuLicpOyIKICAgICAgICA+Qm9ycmFyIHNlbGVjY2lvbmFkb3M8L2J1dHRvbj4KICAgICAgPC9kaXY+CiAgICA8L2Zvcm0+CiAgICB7JSBlbmRpZiAlfQogIDwvZGl2Pgo8L2Rpdj4KeyUgZW5kYmxvY2sgJX0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgc/clientes_nuevos.html
PATH_JSON="templates/pgc/clientes_nuevos.html"
FILENAME=clientes_nuevos.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=311
SIZE_BYTES_UTF8=11535
CONTENT_SHA256=75c4a91c979177fd0958865052be5967049df9195c848840ceb78564978eecdf
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

{% block title %}Clientes vs meta{% endblock %}

{% block content %}
<div class="card">
    <div class="wcg-report-head" style="margin-top:0;">
      <h2 style="margin:0;">Clientes vs meta</h2>
      {% include "includes/module_mark.html" with module="pgc" %}
    </div>
    <p class="muted">
        Meta y resultado mensual con número de clientes nuevos por UNE y periodo, y detalle de todos los clientes.
    </p>
    <p class="muted" style="margin-top:4px;">
        <strong>Nota:</strong> el score de ingresos se calcula en USD.
        El Tablero reporta el resultado final en <strong>puntos</strong>.
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
                <th>UNE</th>
                <th>Periodo</th>
                <th>Meta clientes</th>
                <th>Clientes reales</th>
                <th>¿Cumple?</th>
                <th>Puntos asignados</th>
                <th>Total del mes</th>
                <th>Detalle</th>
            </tr>

            <style>
              .group_separator td {
                padding: 0;
                height: 14px;
                border-bottom: none;
                background: #ffffff;
              }
            
              .detail-icon-link {
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                justify-content: center;
              }
            
              .detail-icon {
                width: 14px;
                height: 14px;
                border-radius: 50%;
                border: 2px solid;
                box-sizing: border-box;
              }
            
              .detail-icon-link.has-detail .detail-icon {
                background-color: #22c55e;
                border-color: #15803d;
              }
            
              .detail-icon-link.no-detail .detail-icon {
                background-color: #e5e7eb;
                border-color: #9ca3af;
              }
            
              .detail-icon-link.has-detail:hover .detail-icon {
                border-color: #166534;
              }
            
              .detail-icon-link.no-detail:hover .detail-icon {
                border-color: #6b7280;
              }
            </style>
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
                            {% if row.real_value_override is not None %}
                                {{ row.real_value_override|floatformat:0|unlocalize }}
                            {% elif row.result %}
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
                                href="{% url 'pgc:clientes_nuevos_detail' %}?une_id={{ row.target.une.id }}&year={{ row.target.year }}&month={{ row.target.month }}"
                                class="detail-icon-link {% if row.has_detail %}has-detail{% else %}no-detail{% endif %}"
                                aria-label="Ver detalle de clientes"
                            >
                                <span class="detail-icon"></span>
                            </a>
                        </td>
                    </tr>
          
                {% endif %}
            {% empty %}
                <tr>
                    <td colspan="8">No hay datos de clientes para los filtros seleccionados.</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
    const startYear = document.getElementById("start_year");
    const startMonth = document.getElementById("start_month");
    const sort = document.getElementById("sort");
    const dateOrder = document.getElementById("date_order");
    const groupMode = document.getElementById("group_mode");
    const btn = document.getElementById("btn-export-md");

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
        if (typeof syncSortFields === "function") syncSortFields();
        if (filterForm) filterForm.submit();
    }

    if (sort) {
        sort.addEventListener("change", applyFilters);
        syncSortFields();
    }

    ["month_count", "start_year", "start_month"].forEach(function (id) {
        const el = document.getElementById(id);
        if (el && el.tagName === "SELECT") {
            el.addEventListener("change", applyFilters);
        }
    });

    if (!btn) return;

    btn.addEventListener("click", async function () {
        syncSortFields();
      
        const params = new URLSearchParams({
            start_year: startYear.value || "",
            start_month: startMonth.value || "",
            month_count: document.getElementById("month_count")?.value || "",
            date_order: dateOrder.value || "asc",
            group_mode: groupMode.value || "une"
        });

        const url = `{% url 'pgc:clientes_nuevos_export_md' %}?` + params.toString();

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

            let filename = "pgc-clientes-nuevos.md";
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
00004|{% block title %}Clientes vs meta{% endblock %}
00005|
00006|{% block content %}
00007|<div class="card">
00008|    <div class="wcg-report-head" style="margin-top:0;">
00009|      <h2 style="margin:0;">Clientes vs meta</h2>
00010|      {% include "includes/module_mark.html" with module="pgc" %}
00011|    </div>
00012|    <p class="muted">
00013|        Meta y resultado mensual con número de clientes nuevos por UNE y periodo, y detalle de todos los clientes.
00014|    </p>
00015|    <p class="muted" style="margin-top:4px;">
00016|        <strong>Nota:</strong> el score de ingresos se calcula en USD.
00017|        El Tablero reporta el resultado final en <strong>puntos</strong>.
00018|    </p>
00019|
00020|    <form method="get" class="filters">
00021|        <div>
00022|            <label for="start_year">Año inicial</label><br>
00023|            <select name="start_year" id="start_year">
00024|                {% for p in available_periods %}
00025|                    <option value="{{ p.year }}"
00026|                        {% if report_filter.start_year == p.year and report_filter.start_month == p.month %}selected{% endif %}>
00027|                        {{ p.year }}
00028|                    </option>
00029|                {% endfor %}
00030|            </select>
00031|        </div>
00032|
00033|        <div>
00034|            <label for="start_month">Mes inicial</label><br>
00035|            <select name="start_month" id="start_month">
00036|                {% for p in available_periods %}
00037|                    <option value="{{ p.month }}"
00038|                        {% if report_filter.start_year == p.year and report_filter.start_month == p.month %}selected{% endif %}>
00039|                        {{ p.month|stringformat:"02d" }}
00040|                    </option>
00041|                {% endfor %}
00042|            </select>
00043|        </div>
00044|
00045|        <div>
00046|            <label for="month_count">Cantidad de meses</label><br>
00047|            <select name="month_count" id="month_count">
00048|                {% for opt in month_count_options %}
00049|                    <option value="{{ opt }}" {% if report_filter.month_count == opt %}selected{% endif %}>
00050|                        {{ opt }}
00051|                    </option>
00052|                {% endfor %}
00053|            </select>
00054|        </div>
00055|
00056|        <div>
00057|          <label for="sort">Sort</label><br>
00058|          <select id="sort">
00059|            <option value="unes"
00060|              {% if report_sort.group_mode == "une" %}selected{% endif %}>
00061|              UNEs
00062|            </option>
00063|            <option value="fechas_asc"
00064|              {% if report_sort.group_mode == "period" and report_sort.date_order == "asc" %}selected{% endif %}>
00065|              Fechas ascendentes
00066|            </option>
00067|            <option value="fechas_desc"
00068|              {% if report_sort.group_mode == "period" and report_sort.date_order == "desc" %}selected{% endif %}>
00069|              Fechas descendentes
00070|            </option>
00071|          </select>
00072|          <input type="hidden" name="date_order" id="date_order"
00073|                 value="{% if report_sort.group_mode == 'period' and report_sort.date_order == 'desc' %}desc{% else %}asc{% endif %}">
00074|          <input type="hidden" name="group_mode" id="group_mode"
00075|                 value="{% if report_sort.group_mode == 'period' %}period{% else %}une{% endif %}">
00076|        </div>
00077|      
00078|        <div style="align-self:end;">
00079|            <button type="button" id="btn-export-md">.md export</button>
00080|        </div>
00081|    </form>
00082|
00083|    <table>
00084|        <thead>
00085|            <tr>
00086|                <th>UNE</th>
00087|                <th>Periodo</th>
00088|                <th>Meta clientes</th>
00089|                <th>Clientes reales</th>
00090|                <th>¿Cumple?</th>
00091|                <th>Puntos asignados</th>
00092|                <th>Total del mes</th>
00093|                <th>Detalle</th>
00094|            </tr>
00095|
00096|            <style>
00097|              .group_separator td {
00098|                padding: 0;
00099|                height: 14px;
00100|                border-bottom: none;
00101|                background: #ffffff;
00102|              }
00103|            
00104|              .detail-icon-link {
00105|                text-decoration: none;
00106|                display: inline-flex;
00107|                align-items: center;
00108|                justify-content: center;
00109|              }
00110|            
00111|              .detail-icon {
00112|                width: 14px;
00113|                height: 14px;
00114|                border-radius: 50%;
00115|                border: 2px solid;
00116|                box-sizing: border-box;
00117|              }
00118|            
00119|              .detail-icon-link.has-detail .detail-icon {
00120|                background-color: #22c55e;
00121|                border-color: #15803d;
00122|              }
00123|            
00124|              .detail-icon-link.no-detail .detail-icon {
00125|                background-color: #e5e7eb;
00126|                border-color: #9ca3af;
00127|              }
00128|            
00129|              .detail-icon-link.has-detail:hover .detail-icon {
00130|                border-color: #166534;
00131|              }
00132|            
00133|              .detail-icon-link.no-detail:hover .detail-icon {
00134|                border-color: #6b7280;
00135|              }
00136|            </style>
00137|        </thead>
00138|        <tbody>
00139|            {% for row in rows %}
00140|                {% if row.is_separator %}
00141|                    <tr class="group_separator">
00142|                        <td colspan="8"></td>
00143|                    </tr>
00144|                {% else %}
00145|                    <tr>
00146|                        <td>{{ row.target.une.name_es }}</td>
00147|                        <td>{{ row.target.year }}-{{ row.target.month|stringformat:"02d" }}</td>
00148|                        <td>
00149|                            {% if row.target.target_value %}
00150|                                {{ row.target.target_value|floatformat:0|unlocalize }}
00151|                            {% else %}
00152|                                —
00153|                            {% endif %}
00154|                        </td>
00155|                        <td>
00156|                            {% if row.real_value_override is not None %}
00157|                                {{ row.real_value_override|floatformat:0|unlocalize }}
00158|                            {% elif row.result %}
00159|                                {{ row.result.measured_value|floatformat:0|unlocalize }}
00160|                            {% else %}
00161|                                —
00162|                            {% endif %}
00163|                        </td>
00164|                        <td>
00165|                            {% if row.result and row.result.is_achieved %}
00166|                                <span class="ok">Sí</span>
00167|                            {% else %}
00168|                                <span class="bad">No</span>
00169|                            {% endif %}
00170|                        </td>
00171|                        <td>
00172|                            {% if row.result %}
00173|                                {{ row.result.points_awarded }}
00174|                            {% else %}
00175|                                0
00176|                            {% endif %}
00177|                        </td>
00178|                        <td>
00179|                            {% if row.scorecard %}
00180|                                {{ row.scorecard.total_points }}
00181|                            {% else %}
00182|                                0
00183|                            {% endif %}
00184|                        </td>
00185|                        <td>
00186|                            <a
00187|                                href="{% url 'pgc:clientes_nuevos_detail' %}?une_id={{ row.target.une.id }}&year={{ row.target.year }}&month={{ row.target.month }}"
00188|                                class="detail-icon-link {% if row.has_detail %}has-detail{% else %}no-detail{% endif %}"
00189|                                aria-label="Ver detalle de clientes"
00190|                            >
00191|                                <span class="detail-icon"></span>
00192|                            </a>
00193|                        </td>
00194|                    </tr>
00195|          
00196|                {% endif %}
00197|            {% empty %}
00198|                <tr>
00199|                    <td colspan="8">No hay datos de clientes para los filtros seleccionados.</td>
00200|                </tr>
00201|            {% endfor %}
00202|        </tbody>
00203|    </table>
00204|</div>
00205|
00206|<script>
00207|document.addEventListener("DOMContentLoaded", function () {
00208|    const startYear = document.getElementById("start_year");
00209|    const startMonth = document.getElementById("start_month");
00210|    const sort = document.getElementById("sort");
00211|    const dateOrder = document.getElementById("date_order");
00212|    const groupMode = document.getElementById("group_mode");
00213|    const btn = document.getElementById("btn-export-md");
00214|
00215|    function syncSortFields() {
00216|        if (!sort) return;
00217|        if (sort.value === "unes") {
00218|            groupMode.value = "une";
00219|            dateOrder.value = "asc";
00220|        } else if (sort.value === "fechas_desc") {
00221|            groupMode.value = "period";
00222|            dateOrder.value = "desc";
00223|        } else {
00224|            groupMode.value = "period";
00225|            dateOrder.value = "asc";
00226|        }
00227|    }
00228|
00229|    const filterForm = document.querySelector("form.filters");
00230|    function applyFilters() {
00231|        if (typeof syncSortFields === "function") syncSortFields();
00232|        if (filterForm) filterForm.submit();
00233|    }
00234|
00235|    if (sort) {
00236|        sort.addEventListener("change", applyFilters);
00237|        syncSortFields();
00238|    }
00239|
00240|    ["month_count", "start_year", "start_month"].forEach(function (id) {
00241|        const el = document.getElementById(id);
00242|        if (el && el.tagName === "SELECT") {
00243|            el.addEventListener("change", applyFilters);
00244|        }
00245|    });
00246|
00247|    if (!btn) return;
00248|
00249|    btn.addEventListener("click", async function () {
00250|        syncSortFields();
00251|      
00252|        const params = new URLSearchParams({
00253|            start_year: startYear.value || "",
00254|            start_month: startMonth.value || "",
00255|            month_count: document.getElementById("month_count")?.value || "",
00256|            date_order: dateOrder.value || "asc",
00257|            group_mode: groupMode.value || "une"
00258|        });
00259|
00260|        const url = `{% url 'pgc:clientes_nuevos_export_md' %}?` + params.toString();
00261|
00262|        btn.disabled = true;
00263|        const originalText = btn.textContent;
00264|        btn.textContent = "Generando...";
00265|
00266|        try {
00267|            const response = await fetch(url, {
00268|                method: "GET",
00269|                headers: {
00270|                    "X-Requested-With": "XMLHttpRequest"
00271|                }
00272|            });
00273|
00274|            if (!response.ok) {
00275|                throw new Error("No se pudo generar el archivo Markdown.");
00276|            }
00277|
00278|            const blob = await response.blob();
00279|
00280|            let filename = "pgc-clientes-nuevos.md";
00281|            const disposition = response.headers.get("Content-Disposition");
00282|            if (disposition) {
00283|                const utf8Match = disposition.match(/filename\*=UTF-8''([^;]+)/i);
00284|                const asciiMatch = disposition.match(/filename="([^"]+)"/i);
00285|
00286|                if (utf8Match && utf8Match[1]) {
00287|                    filename = decodeURIComponent(utf8Match[1]);
00288|                } else if (asciiMatch && asciiMatch[1]) {
00289|                    filename = asciiMatch[1];
00290|                }
00291|            }
00292|
00293|            const objectUrl = window.URL.createObjectURL(blob);
00294|            const a = document.createElement("a");
00295|            a.href = objectUrl;
00296|            a.download = filename;
00297|            document.body.appendChild(a);
00298|            a.click();
00299|            a.remove();
00300|            window.URL.revokeObjectURL(objectUrl);
00301|        } catch (error) {
00302|            alert(error.message || "Error generando la exportación.");
00303|        } finally {
00304|            btn.disabled = false;
00305|            btn.textContent = originalText;
00306|        }
00307|    });
00308|});
00309|</script>
00310|
00311|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZS5odG1sIiAlfQp7JSBsb2FkIGwxMG4gJX0KCnslIGJsb2NrIHRpdGxlICV9Q2xpZW50ZXMgdnMgbWV0YXslIGVuZGJsb2NrICV9Cgp7JSBibG9jayBjb250ZW50ICV9CjxkaXYgY2xhc3M9ImNhcmQiPgogICAgPGRpdiBjbGFzcz0id2NnLXJlcG9ydC1oZWFkIiBzdHlsZT0ibWFyZ2luLXRvcDowOyI+CiAgICAgIDxoMiBzdHlsZT0ibWFyZ2luOjA7Ij5DbGllbnRlcyB2cyBtZXRhPC9oMj4KICAgICAgeyUgaW5jbHVkZSAiaW5jbHVkZXMvbW9kdWxlX21hcmsuaHRtbCIgd2l0aCBtb2R1bGU9InBnYyIgJX0KICAgIDwvZGl2PgogICAgPHAgY2xhc3M9Im11dGVkIj4KICAgICAgICBNZXRhIHkgcmVzdWx0YWRvIG1lbnN1YWwgY29uIG7Dum1lcm8gZGUgY2xpZW50ZXMgbnVldm9zIHBvciBVTkUgeSBwZXJpb2RvLCB5IGRldGFsbGUgZGUgdG9kb3MgbG9zIGNsaWVudGVzLgogICAgPC9wPgogICAgPHAgY2xhc3M9Im11dGVkIiBzdHlsZT0ibWFyZ2luLXRvcDo0cHg7Ij4KICAgICAgICA8c3Ryb25nPk5vdGE6PC9zdHJvbmc+IGVsIHNjb3JlIGRlIGluZ3Jlc29zIHNlIGNhbGN1bGEgZW4gVVNELgogICAgICAgIEVsIFRhYmxlcm8gcmVwb3J0YSBlbCByZXN1bHRhZG8gZmluYWwgZW4gPHN0cm9uZz5wdW50b3M8L3N0cm9uZz4uCiAgICA8L3A+CgogICAgPGZvcm0gbWV0aG9kPSJnZXQiIGNsYXNzPSJmaWx0ZXJzIj4KICAgICAgICA8ZGl2PgogICAgICAgICAgICA8bGFiZWwgZm9yPSJzdGFydF95ZWFyIj5Bw7FvIGluaWNpYWw8L2xhYmVsPjxicj4KICAgICAgICAgICAgPHNlbGVjdCBuYW1lPSJzdGFydF95ZWFyIiBpZD0ic3RhcnRfeWVhciI+CiAgICAgICAgICAgICAgICB7JSBmb3IgcCBpbiBhdmFpbGFibGVfcGVyaW9kcyAlfQogICAgICAgICAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9Int7IHAueWVhciB9fSIKICAgICAgICAgICAgICAgICAgICAgICAgeyUgaWYgcmVwb3J0X2ZpbHRlci5zdGFydF95ZWFyID09IHAueWVhciBhbmQgcmVwb3J0X2ZpbHRlci5zdGFydF9tb250aCA9PSBwLm1vbnRoICV9c2VsZWN0ZWR7JSBlbmRpZiAlfT4KICAgICAgICAgICAgICAgICAgICAgICAge3sgcC55ZWFyIH19CiAgICAgICAgICAgICAgICAgICAgPC9vcHRpb24+CiAgICAgICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgICAgPC9zZWxlY3Q+CiAgICAgICAgPC9kaXY+CgogICAgICAgIDxkaXY+CiAgICAgICAgICAgIDxsYWJlbCBmb3I9InN0YXJ0X21vbnRoIj5NZXMgaW5pY2lhbDwvbGFiZWw+PGJyPgogICAgICAgICAgICA8c2VsZWN0IG5hbWU9InN0YXJ0X21vbnRoIiBpZD0ic3RhcnRfbW9udGgiPgogICAgICAgICAgICAgICAgeyUgZm9yIHAgaW4gYXZhaWxhYmxlX3BlcmlvZHMgJX0KICAgICAgICAgICAgICAgICAgICA8b3B0aW9uIHZhbHVlPSJ7eyBwLm1vbnRoIH19IgogICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiByZXBvcnRfZmlsdGVyLnN0YXJ0X3llYXIgPT0gcC55ZWFyIGFuZCByZXBvcnRfZmlsdGVyLnN0YXJ0X21vbnRoID09IHAubW9udGggJX1zZWxlY3RlZHslIGVuZGlmICV9PgogICAgICAgICAgICAgICAgICAgICAgICB7eyBwLm1vbnRofHN0cmluZ2Zvcm1hdDoiMDJkIiB9fQogICAgICAgICAgICAgICAgICAgIDwvb3B0aW9uPgogICAgICAgICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgICAgIDwvc2VsZWN0PgogICAgICAgIDwvZGl2PgoKICAgICAgICA8ZGl2PgogICAgICAgICAgICA8bGFiZWwgZm9yPSJtb250aF9jb3VudCI+Q2FudGlkYWQgZGUgbWVzZXM8L2xhYmVsPjxicj4KICAgICAgICAgICAgPHNlbGVjdCBuYW1lPSJtb250aF9jb3VudCIgaWQ9Im1vbnRoX2NvdW50Ij4KICAgICAgICAgICAgICAgIHslIGZvciBvcHQgaW4gbW9udGhfY291bnRfb3B0aW9ucyAlfQogICAgICAgICAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9Int7IG9wdCB9fSIgeyUgaWYgcmVwb3J0X2ZpbHRlci5tb250aF9jb3VudCA9PSBvcHQgJX1zZWxlY3RlZHslIGVuZGlmICV9PgogICAgICAgICAgICAgICAgICAgICAgICB7eyBvcHQgfX0KICAgICAgICAgICAgICAgICAgICA8L29wdGlvbj4KICAgICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICA8L3NlbGVjdD4KICAgICAgICA8L2Rpdj4KCiAgICAgICAgPGRpdj4KICAgICAgICAgIDxsYWJlbCBmb3I9InNvcnQiPlNvcnQ8L2xhYmVsPjxicj4KICAgICAgICAgIDxzZWxlY3QgaWQ9InNvcnQiPgogICAgICAgICAgICA8b3B0aW9uIHZhbHVlPSJ1bmVzIgogICAgICAgICAgICAgIHslIGlmIHJlcG9ydF9zb3J0Lmdyb3VwX21vZGUgPT0gInVuZSIgJX1zZWxlY3RlZHslIGVuZGlmICV9PgogICAgICAgICAgICAgIFVORXMKICAgICAgICAgICAgPC9vcHRpb24+CiAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9ImZlY2hhc19hc2MiCiAgICAgICAgICAgICAgeyUgaWYgcmVwb3J0X3NvcnQuZ3JvdXBfbW9kZSA9PSAicGVyaW9kIiBhbmQgcmVwb3J0X3NvcnQuZGF0ZV9vcmRlciA9PSAiYXNjIiAlfXNlbGVjdGVkeyUgZW5kaWYgJX0+CiAgICAgICAgICAgICAgRmVjaGFzIGFzY2VuZGVudGVzCiAgICAgICAgICAgIDwvb3B0aW9uPgogICAgICAgICAgICA8b3B0aW9uIHZhbHVlPSJmZWNoYXNfZGVzYyIKICAgICAgICAgICAgICB7JSBpZiByZXBvcnRfc29ydC5ncm91cF9tb2RlID09ICJwZXJpb2QiIGFuZCByZXBvcnRfc29ydC5kYXRlX29yZGVyID09ICJkZXNjIiAlfXNlbGVjdGVkeyUgZW5kaWYgJX0+CiAgICAgICAgICAgICAgRmVjaGFzIGRlc2NlbmRlbnRlcwogICAgICAgICAgICA8L29wdGlvbj4KICAgICAgICAgIDwvc2VsZWN0PgogICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0iZGF0ZV9vcmRlciIgaWQ9ImRhdGVfb3JkZXIiCiAgICAgICAgICAgICAgICAgdmFsdWU9InslIGlmIHJlcG9ydF9zb3J0Lmdyb3VwX21vZGUgPT0gJ3BlcmlvZCcgYW5kIHJlcG9ydF9zb3J0LmRhdGVfb3JkZXIgPT0gJ2Rlc2MnICV9ZGVzY3slIGVsc2UgJX1hc2N7JSBlbmRpZiAlfSI+CiAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJncm91cF9tb2RlIiBpZD0iZ3JvdXBfbW9kZSIKICAgICAgICAgICAgICAgICB2YWx1ZT0ieyUgaWYgcmVwb3J0X3NvcnQuZ3JvdXBfbW9kZSA9PSAncGVyaW9kJyAlfXBlcmlvZHslIGVsc2UgJX11bmV7JSBlbmRpZiAlfSI+CiAgICAgICAgPC9kaXY+CiAgICAgIAogICAgICAgIDxkaXYgc3R5bGU9ImFsaWduLXNlbGY6ZW5kOyI+CiAgICAgICAgICAgIDxidXR0b24gdHlwZT0iYnV0dG9uIiBpZD0iYnRuLWV4cG9ydC1tZCI+Lm1kIGV4cG9ydDwvYnV0dG9uPgogICAgICAgIDwvZGl2PgogICAgPC9mb3JtPgoKICAgIDx0YWJsZT4KICAgICAgICA8dGhlYWQ+CiAgICAgICAgICAgIDx0cj4KICAgICAgICAgICAgICAgIDx0aD5VTkU8L3RoPgogICAgICAgICAgICAgICAgPHRoPlBlcmlvZG88L3RoPgogICAgICAgICAgICAgICAgPHRoPk1ldGEgY2xpZW50ZXM8L3RoPgogICAgICAgICAgICAgICAgPHRoPkNsaWVudGVzIHJlYWxlczwvdGg+CiAgICAgICAgICAgICAgICA8dGg+wr9DdW1wbGU/PC90aD4KICAgICAgICAgICAgICAgIDx0aD5QdW50b3MgYXNpZ25hZG9zPC90aD4KICAgICAgICAgICAgICAgIDx0aD5Ub3RhbCBkZWwgbWVzPC90aD4KICAgICAgICAgICAgICAgIDx0aD5EZXRhbGxlPC90aD4KICAgICAgICAgICAgPC90cj4KCiAgICAgICAgICAgIDxzdHlsZT4KICAgICAgICAgICAgICAuZ3JvdXBfc2VwYXJhdG9yIHRkIHsKICAgICAgICAgICAgICAgIHBhZGRpbmc6IDA7CiAgICAgICAgICAgICAgICBoZWlnaHQ6IDE0cHg7CiAgICAgICAgICAgICAgICBib3JkZXItYm90dG9tOiBub25lOwogICAgICAgICAgICAgICAgYmFja2dyb3VuZDogI2ZmZmZmZjsKICAgICAgICAgICAgICB9CiAgICAgICAgICAgIAogICAgICAgICAgICAgIC5kZXRhaWwtaWNvbi1saW5rIHsKICAgICAgICAgICAgICAgIHRleHQtZGVjb3JhdGlvbjogbm9uZTsKICAgICAgICAgICAgICAgIGRpc3BsYXk6IGlubGluZS1mbGV4OwogICAgICAgICAgICAgICAgYWxpZ24taXRlbXM6IGNlbnRlcjsKICAgICAgICAgICAgICAgIGp1c3RpZnktY29udGVudDogY2VudGVyOwogICAgICAgICAgICAgIH0KICAgICAgICAgICAgCiAgICAgICAgICAgICAgLmRldGFpbC1pY29uIHsKICAgICAgICAgICAgICAgIHdpZHRoOiAxNHB4OwogICAgICAgICAgICAgICAgaGVpZ2h0OiAxNHB4OwogICAgICAgICAgICAgICAgYm9yZGVyLXJhZGl1czogNTAlOwogICAgICAgICAgICAgICAgYm9yZGVyOiAycHggc29saWQ7CiAgICAgICAgICAgICAgICBib3gtc2l6aW5nOiBib3JkZXItYm94OwogICAgICAgICAgICAgIH0KICAgICAgICAgICAgCiAgICAgICAgICAgICAgLmRldGFpbC1pY29uLWxpbmsuaGFzLWRldGFpbCAuZGV0YWlsLWljb24gewogICAgICAgICAgICAgICAgYmFja2dyb3VuZC1jb2xvcjogIzIyYzU1ZTsKICAgICAgICAgICAgICAgIGJvcmRlci1jb2xvcjogIzE1ODAzZDsKICAgICAgICAgICAgICB9CiAgICAgICAgICAgIAogICAgICAgICAgICAgIC5kZXRhaWwtaWNvbi1saW5rLm5vLWRldGFpbCAuZGV0YWlsLWljb24gewogICAgICAgICAgICAgICAgYmFja2dyb3VuZC1jb2xvcjogI2U1ZTdlYjsKICAgICAgICAgICAgICAgIGJvcmRlci1jb2xvcjogIzljYTNhZjsKICAgICAgICAgICAgICB9CiAgICAgICAgICAgIAogICAgICAgICAgICAgIC5kZXRhaWwtaWNvbi1saW5rLmhhcy1kZXRhaWw6aG92ZXIgLmRldGFpbC1pY29uIHsKICAgICAgICAgICAgICAgIGJvcmRlci1jb2xvcjogIzE2NjUzNDsKICAgICAgICAgICAgICB9CiAgICAgICAgICAgIAogICAgICAgICAgICAgIC5kZXRhaWwtaWNvbi1saW5rLm5vLWRldGFpbDpob3ZlciAuZGV0YWlsLWljb24gewogICAgICAgICAgICAgICAgYm9yZGVyLWNvbG9yOiAjNmI3MjgwOwogICAgICAgICAgICAgIH0KICAgICAgICAgICAgPC9zdHlsZT4KICAgICAgICA8L3RoZWFkPgogICAgICAgIDx0Ym9keT4KICAgICAgICAgICAgeyUgZm9yIHJvdyBpbiByb3dzICV9CiAgICAgICAgICAgICAgICB7JSBpZiByb3cuaXNfc2VwYXJhdG9yICV9CiAgICAgICAgICAgICAgICAgICAgPHRyIGNsYXNzPSJncm91cF9zZXBhcmF0b3IiPgogICAgICAgICAgICAgICAgICAgICAgICA8dGQgY29sc3Bhbj0iOCI+PC90ZD4KICAgICAgICAgICAgICAgICAgICA8L3RyPgogICAgICAgICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgICAgICAgICAgIDx0cj4KICAgICAgICAgICAgICAgICAgICAgICAgPHRkPnt7IHJvdy50YXJnZXQudW5lLm5hbWVfZXMgfX08L3RkPgogICAgICAgICAgICAgICAgICAgICAgICA8dGQ+e3sgcm93LnRhcmdldC55ZWFyIH19LXt7IHJvdy50YXJnZXQubW9udGh8c3RyaW5nZm9ybWF0OiIwMmQiIH19PC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgPHRkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgaWYgcm93LnRhcmdldC50YXJnZXRfdmFsdWUgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7eyByb3cudGFyZ2V0LnRhcmdldF92YWx1ZXxmbG9hdGZvcm1hdDowfHVubG9jYWxpemUgfX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVsc2UgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICDigJQKICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgICAgICAgICAgICAgIDwvdGQ+CiAgICAgICAgICAgICAgICAgICAgICAgIDx0ZD4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGlmIHJvdy5yZWFsX3ZhbHVlX292ZXJyaWRlIGlzIG5vdCBOb25lICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAge3sgcm93LnJlYWxfdmFsdWVfb3ZlcnJpZGV8ZmxvYXRmb3JtYXQ6MHx1bmxvY2FsaXplIH19CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbGlmIHJvdy5yZXN1bHQgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7eyByb3cucmVzdWx0Lm1lYXN1cmVkX3ZhbHVlfGZsb2F0Zm9ybWF0OjB8dW5sb2NhbGl6ZSB9fQogICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIOKAlAogICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgPHRkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgaWYgcm93LnJlc3VsdCBhbmQgcm93LnJlc3VsdC5pc19hY2hpZXZlZCAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJvayI+U8OtPC9zcGFuPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJiYWQiPk5vPC9zcGFuPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD4KICAgICAgICAgICAgICAgICAgICAgICAgPHRkPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgaWYgcm93LnJlc3VsdCAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHt7IHJvdy5yZXN1bHQucG9pbnRzX2F3YXJkZWQgfX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVsc2UgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAwCiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgICAgICAgICAgICAgICA8L3RkPgogICAgICAgICAgICAgICAgICAgICAgICA8dGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiByb3cuc2NvcmVjYXJkICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAge3sgcm93LnNjb3JlY2FyZC50b3RhbF9wb2ludHMgfX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVsc2UgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAwCiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgICAgICAgICAgICAgICA8L3RkPgogICAgICAgICAgICAgICAgICAgICAgICA8dGQ+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8YQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGhyZWY9InslIHVybCAncGdjOmNsaWVudGVzX251ZXZvc19kZXRhaWwnICV9P3VuZV9pZD17eyByb3cudGFyZ2V0LnVuZS5pZCB9fSZ5ZWFyPXt7IHJvdy50YXJnZXQueWVhciB9fSZtb250aD17eyByb3cudGFyZ2V0Lm1vbnRoIH19IgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGNsYXNzPSJkZXRhaWwtaWNvbi1saW5rIHslIGlmIHJvdy5oYXNfZGV0YWlsICV9aGFzLWRldGFpbHslIGVsc2UgJX1uby1kZXRhaWx7JSBlbmRpZiAlfSIKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBhcmlhLWxhYmVsPSJWZXIgZGV0YWxsZSBkZSBjbGllbnRlcyIKICAgICAgICAgICAgICAgICAgICAgICAgICAgID4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8c3BhbiBjbGFzcz0iZGV0YWlsLWljb24iPjwvc3Bhbj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvYT4KICAgICAgICAgICAgICAgICAgICAgICAgPC90ZD4KICAgICAgICAgICAgICAgICAgICA8L3RyPgogICAgICAgICAgCiAgICAgICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgICB7JSBlbXB0eSAlfQogICAgICAgICAgICAgICAgPHRyPgogICAgICAgICAgICAgICAgICAgIDx0ZCBjb2xzcGFuPSI4Ij5ObyBoYXkgZGF0b3MgZGUgY2xpZW50ZXMgcGFyYSBsb3MgZmlsdHJvcyBzZWxlY2Npb25hZG9zLjwvdGQ+CiAgICAgICAgICAgICAgICA8L3RyPgogICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICA8L3Rib2R5PgogICAgPC90YWJsZT4KPC9kaXY+Cgo8c2NyaXB0Pgpkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCJET01Db250ZW50TG9hZGVkIiwgZnVuY3Rpb24gKCkgewogICAgY29uc3Qgc3RhcnRZZWFyID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoInN0YXJ0X3llYXIiKTsKICAgIGNvbnN0IHN0YXJ0TW9udGggPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgic3RhcnRfbW9udGgiKTsKICAgIGNvbnN0IHNvcnQgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgic29ydCIpOwogICAgY29uc3QgZGF0ZU9yZGVyID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImRhdGVfb3JkZXIiKTsKICAgIGNvbnN0IGdyb3VwTW9kZSA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJncm91cF9tb2RlIik7CiAgICBjb25zdCBidG4gPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuLWV4cG9ydC1tZCIpOwoKICAgIGZ1bmN0aW9uIHN5bmNTb3J0RmllbGRzKCkgewogICAgICAgIGlmICghc29ydCkgcmV0dXJuOwogICAgICAgIGlmIChzb3J0LnZhbHVlID09PSAidW5lcyIpIHsKICAgICAgICAgICAgZ3JvdXBNb2RlLnZhbHVlID0gInVuZSI7CiAgICAgICAgICAgIGRhdGVPcmRlci52YWx1ZSA9ICJhc2MiOwogICAgICAgIH0gZWxzZSBpZiAoc29ydC52YWx1ZSA9PT0gImZlY2hhc19kZXNjIikgewogICAgICAgICAgICBncm91cE1vZGUudmFsdWUgPSAicGVyaW9kIjsKICAgICAgICAgICAgZGF0ZU9yZGVyLnZhbHVlID0gImRlc2MiOwogICAgICAgIH0gZWxzZSB7CiAgICAgICAgICAgIGdyb3VwTW9kZS52YWx1ZSA9ICJwZXJpb2QiOwogICAgICAgICAgICBkYXRlT3JkZXIudmFsdWUgPSAiYXNjIjsKICAgICAgICB9CiAgICB9CgogICAgY29uc3QgZmlsdGVyRm9ybSA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoImZvcm0uZmlsdGVycyIpOwogICAgZnVuY3Rpb24gYXBwbHlGaWx0ZXJzKCkgewogICAgICAgIGlmICh0eXBlb2Ygc3luY1NvcnRGaWVsZHMgPT09ICJmdW5jdGlvbiIpIHN5bmNTb3J0RmllbGRzKCk7CiAgICAgICAgaWYgKGZpbHRlckZvcm0pIGZpbHRlckZvcm0uc3VibWl0KCk7CiAgICB9CgogICAgaWYgKHNvcnQpIHsKICAgICAgICBzb3J0LmFkZEV2ZW50TGlzdGVuZXIoImNoYW5nZSIsIGFwcGx5RmlsdGVycyk7CiAgICAgICAgc3luY1NvcnRGaWVsZHMoKTsKICAgIH0KCiAgICBbIm1vbnRoX2NvdW50IiwgInN0YXJ0X3llYXIiLCAic3RhcnRfbW9udGgiXS5mb3JFYWNoKGZ1bmN0aW9uIChpZCkgewogICAgICAgIGNvbnN0IGVsID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoaWQpOwogICAgICAgIGlmIChlbCAmJiBlbC50YWdOYW1lID09PSAiU0VMRUNUIikgewogICAgICAgICAgICBlbC5hZGRFdmVudExpc3RlbmVyKCJjaGFuZ2UiLCBhcHBseUZpbHRlcnMpOwogICAgICAgIH0KICAgIH0pOwoKICAgIGlmICghYnRuKSByZXR1cm47CgogICAgYnRuLmFkZEV2ZW50TGlzdGVuZXIoImNsaWNrIiwgYXN5bmMgZnVuY3Rpb24gKCkgewogICAgICAgIHN5bmNTb3J0RmllbGRzKCk7CiAgICAgIAogICAgICAgIGNvbnN0IHBhcmFtcyA9IG5ldyBVUkxTZWFyY2hQYXJhbXMoewogICAgICAgICAgICBzdGFydF95ZWFyOiBzdGFydFllYXIudmFsdWUgfHwgIiIsCiAgICAgICAgICAgIHN0YXJ0X21vbnRoOiBzdGFydE1vbnRoLnZhbHVlIHx8ICIiLAogICAgICAgICAgICBtb250aF9jb3VudDogZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoIm1vbnRoX2NvdW50Iik/LnZhbHVlIHx8ICIiLAogICAgICAgICAgICBkYXRlX29yZGVyOiBkYXRlT3JkZXIudmFsdWUgfHwgImFzYyIsCiAgICAgICAgICAgIGdyb3VwX21vZGU6IGdyb3VwTW9kZS52YWx1ZSB8fCAidW5lIgogICAgICAgIH0pOwoKICAgICAgICBjb25zdCB1cmwgPSBgeyUgdXJsICdwZ2M6Y2xpZW50ZXNfbnVldm9zX2V4cG9ydF9tZCcgJX0/YCArIHBhcmFtcy50b1N0cmluZygpOwoKICAgICAgICBidG4uZGlzYWJsZWQgPSB0cnVlOwogICAgICAgIGNvbnN0IG9yaWdpbmFsVGV4dCA9IGJ0bi50ZXh0Q29udGVudDsKICAgICAgICBidG4udGV4dENvbnRlbnQgPSAiR2VuZXJhbmRvLi4uIjsKCiAgICAgICAgdHJ5IHsKICAgICAgICAgICAgY29uc3QgcmVzcG9uc2UgPSBhd2FpdCBmZXRjaCh1cmwsIHsKICAgICAgICAgICAgICAgIG1ldGhvZDogIkdFVCIsCiAgICAgICAgICAgICAgICBoZWFkZXJzOiB7CiAgICAgICAgICAgICAgICAgICAgIlgtUmVxdWVzdGVkLVdpdGgiOiAiWE1MSHR0cFJlcXVlc3QiCiAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgIH0pOwoKICAgICAgICAgICAgaWYgKCFyZXNwb25zZS5vaykgewogICAgICAgICAgICAgICAgdGhyb3cgbmV3IEVycm9yKCJObyBzZSBwdWRvIGdlbmVyYXIgZWwgYXJjaGl2byBNYXJrZG93bi4iKTsKICAgICAgICAgICAgfQoKICAgICAgICAgICAgY29uc3QgYmxvYiA9IGF3YWl0IHJlc3BvbnNlLmJsb2IoKTsKCiAgICAgICAgICAgIGxldCBmaWxlbmFtZSA9ICJwZ2MtY2xpZW50ZXMtbnVldm9zLm1kIjsKICAgICAgICAgICAgY29uc3QgZGlzcG9zaXRpb24gPSByZXNwb25zZS5oZWFkZXJzLmdldCgiQ29udGVudC1EaXNwb3NpdGlvbiIpOwogICAgICAgICAgICBpZiAoZGlzcG9zaXRpb24pIHsKICAgICAgICAgICAgICAgIGNvbnN0IHV0ZjhNYXRjaCA9IGRpc3Bvc2l0aW9uLm1hdGNoKC9maWxlbmFtZVwqPVVURi04JycoW147XSspL2kpOwogICAgICAgICAgICAgICAgY29uc3QgYXNjaWlNYXRjaCA9IGRpc3Bvc2l0aW9uLm1hdGNoKC9maWxlbmFtZT0iKFteIl0rKSIvaSk7CgogICAgICAgICAgICAgICAgaWYgKHV0ZjhNYXRjaCAmJiB1dGY4TWF0Y2hbMV0pIHsKICAgICAgICAgICAgICAgICAgICBmaWxlbmFtZSA9IGRlY29kZVVSSUNvbXBvbmVudCh1dGY4TWF0Y2hbMV0pOwogICAgICAgICAgICAgICAgfSBlbHNlIGlmIChhc2NpaU1hdGNoICYmIGFzY2lpTWF0Y2hbMV0pIHsKICAgICAgICAgICAgICAgICAgICBmaWxlbmFtZSA9IGFzY2lpTWF0Y2hbMV07CiAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgIH0KCiAgICAgICAgICAgIGNvbnN0IG9iamVjdFVybCA9IHdpbmRvdy5VUkwuY3JlYXRlT2JqZWN0VVJMKGJsb2IpOwogICAgICAgICAgICBjb25zdCBhID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgiYSIpOwogICAgICAgICAgICBhLmhyZWYgPSBvYmplY3RVcmw7CiAgICAgICAgICAgIGEuZG93bmxvYWQgPSBmaWxlbmFtZTsKICAgICAgICAgICAgZG9jdW1lbnQuYm9keS5hcHBlbmRDaGlsZChhKTsKICAgICAgICAgICAgYS5jbGljaygpOwogICAgICAgICAgICBhLnJlbW92ZSgpOwogICAgICAgICAgICB3aW5kb3cuVVJMLnJldm9rZU9iamVjdFVSTChvYmplY3RVcmwpOwogICAgICAgIH0gY2F0Y2ggKGVycm9yKSB7CiAgICAgICAgICAgIGFsZXJ0KGVycm9yLm1lc3NhZ2UgfHwgIkVycm9yIGdlbmVyYW5kbyBsYSBleHBvcnRhY2nDs24uIik7CiAgICAgICAgfSBmaW5hbGx5IHsKICAgICAgICAgICAgYnRuLmRpc2FibGVkID0gZmFsc2U7CiAgICAgICAgICAgIGJ0bi50ZXh0Q29udGVudCA9IG9yaWdpbmFsVGV4dDsKICAgICAgICB9CiAgICB9KTsKfSk7Cjwvc2NyaXB0PgoKeyUgZW5kYmxvY2sgJX0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgc/clientes_nuevos_detail.html
PATH_JSON="templates/pgc/clientes_nuevos_detail.html"
FILENAME=clientes_nuevos_detail.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=112
SIZE_BYTES_UTF8=3381
CONTENT_SHA256=22394121990059c238ecff98a578e5fb8e8ae625dc93f213798a509d0dff1de5
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

{% block title %}Detalle clientes nuevos{% endblock %}

{% block content %}
<style>
  .amt-prefix {
    font-weight: 600;
    color: #475569;
    margin-right: 2px;
  }
  .mon-cell {
    font-size: 0.85rem;
    font-weight: 600;
    color: #0f3d56;
  }
  .investment-total {
    margin-top: 8px;
    padding: 8px 10px;
    background: #f0fdfa;
    border: 1px solid #99f6e4;
    border-radius: 8px;
    font-size: 0.92rem;
  }
  .investment-total .usd-tag {
    font-size: 0.75rem;
    font-weight: 700;
    color: #0f766e;
    background: #ccfbf1;
    padding: 1px 6px;
    border-radius: 4px;
    margin-left: 4px;
  }
</style>
<div class="card">
  <h2 style="margin-top:0;">Detalle de clientes</h2>
  <p class="muted">
    UNE: <strong>{{ une.name_es }}</strong> |
    Periodo: <strong>{{ year }}-{{ month|stringformat:"02d" }}</strong>
  </p>

  {% if investment_ingresos_total is not None %}
    <p class="investment-total">
      Total Investment (USD):
      <strong>${{ investment_ingresos_total|floatformat:2|unlocalize }}</strong>
      <span class="usd-tag">USD</span>
    </p>
  {% endif %}
  
  <table>
    <thead>
      <tr>
        <th style="text-align:left;">Cliente</th>
        <th>NIT</th>
        <th>Operación</th>
        <th>Contratos previos</th>
        <th>¿Cuenta como nuevo?</th>
        <th title="Moneda original de la operación">Mon.</th>
        <th>Monto</th>
        <th style="text-align:left;">Observación</th>
      </tr>
    </thead>
    <tbody>
      {% for row in rows %}
      <tr>
        <td style="text-align:left;">{{ row.client_name|default:"-" }}</td>
        <td>{{ row.nit|default:"-" }}</td>
        <td>{{ row.operation_code|default:"-" }}</td>
        <td>{{ row.previous_contracts }}</td>
        <td>
          {% if row.counts_as_new %}
            <span class="ok">Sí</span>
          {% else %}
            <span class="bad">No</span>
          {% endif %}
        </td>
        <td class="mon-cell">
          {% if row.currency_code == "USD" or row.currency_code == "US$" or row.currency_code == "$" %}
            USD
          {% elif row.currency_code == "GTQ" or row.currency_code == "Q" or row.currency_code == "QUETZAL" or row.currency_code == "QUETZALES" %}
            Q
          {% else %}
            {{ row.currency_code|default:"-" }}
          {% endif %}
        </td>
        <td>
          {% if row.amount is not None %}
            {% if row.currency_code == "USD" or row.currency_code == "US$" or row.currency_code == "$" %}
              <span class="amt-prefix">$</span>{{ row.amount|floatformat:2|unlocalize }}
            {% elif row.currency_code == "GTQ" or row.currency_code == "Q" or row.currency_code == "QUETZAL" or row.currency_code == "QUETZALES" %}
              <span class="amt-prefix">Q</span>{{ row.amount|floatformat:2|unlocalize }}
            {% else %}
              {{ row.amount|floatformat:2|unlocalize }}
            {% endif %}
          {% else %}
            -
          {% endif %}
        </td>
        <td style="text-align:left;">{{ row.observations|default:"-" }}</td>
      </tr>
      {% empty %}
      <tr>
        <td colspan="8" style="text-align:center;">
          No existen registros importados para esta UNE y periodo.
        </td>
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
00002|{% load l10n %}
00003|
00004|{% block title %}Detalle clientes nuevos{% endblock %}
00005|
00006|{% block content %}
00007|<style>
00008|  .amt-prefix {
00009|    font-weight: 600;
00010|    color: #475569;
00011|    margin-right: 2px;
00012|  }
00013|  .mon-cell {
00014|    font-size: 0.85rem;
00015|    font-weight: 600;
00016|    color: #0f3d56;
00017|  }
00018|  .investment-total {
00019|    margin-top: 8px;
00020|    padding: 8px 10px;
00021|    background: #f0fdfa;
00022|    border: 1px solid #99f6e4;
00023|    border-radius: 8px;
00024|    font-size: 0.92rem;
00025|  }
00026|  .investment-total .usd-tag {
00027|    font-size: 0.75rem;
00028|    font-weight: 700;
00029|    color: #0f766e;
00030|    background: #ccfbf1;
00031|    padding: 1px 6px;
00032|    border-radius: 4px;
00033|    margin-left: 4px;
00034|  }
00035|</style>
00036|<div class="card">
00037|  <h2 style="margin-top:0;">Detalle de clientes</h2>
00038|  <p class="muted">
00039|    UNE: <strong>{{ une.name_es }}</strong> |
00040|    Periodo: <strong>{{ year }}-{{ month|stringformat:"02d" }}</strong>
00041|  </p>
00042|
00043|  {% if investment_ingresos_total is not None %}
00044|    <p class="investment-total">
00045|      Total Investment (USD):
00046|      <strong>${{ investment_ingresos_total|floatformat:2|unlocalize }}</strong>
00047|      <span class="usd-tag">USD</span>
00048|    </p>
00049|  {% endif %}
00050|  
00051|  <table>
00052|    <thead>
00053|      <tr>
00054|        <th style="text-align:left;">Cliente</th>
00055|        <th>NIT</th>
00056|        <th>Operación</th>
00057|        <th>Contratos previos</th>
00058|        <th>¿Cuenta como nuevo?</th>
00059|        <th title="Moneda original de la operación">Mon.</th>
00060|        <th>Monto</th>
00061|        <th style="text-align:left;">Observación</th>
00062|      </tr>
00063|    </thead>
00064|    <tbody>
00065|      {% for row in rows %}
00066|      <tr>
00067|        <td style="text-align:left;">{{ row.client_name|default:"-" }}</td>
00068|        <td>{{ row.nit|default:"-" }}</td>
00069|        <td>{{ row.operation_code|default:"-" }}</td>
00070|        <td>{{ row.previous_contracts }}</td>
00071|        <td>
00072|          {% if row.counts_as_new %}
00073|            <span class="ok">Sí</span>
00074|          {% else %}
00075|            <span class="bad">No</span>
00076|          {% endif %}
00077|        </td>
00078|        <td class="mon-cell">
00079|          {% if row.currency_code == "USD" or row.currency_code == "US$" or row.currency_code == "$" %}
00080|            USD
00081|          {% elif row.currency_code == "GTQ" or row.currency_code == "Q" or row.currency_code == "QUETZAL" or row.currency_code == "QUETZALES" %}
00082|            Q
00083|          {% else %}
00084|            {{ row.currency_code|default:"-" }}
00085|          {% endif %}
00086|        </td>
00087|        <td>
00088|          {% if row.amount is not None %}
00089|            {% if row.currency_code == "USD" or row.currency_code == "US$" or row.currency_code == "$" %}
00090|              <span class="amt-prefix">$</span>{{ row.amount|floatformat:2|unlocalize }}
00091|            {% elif row.currency_code == "GTQ" or row.currency_code == "Q" or row.currency_code == "QUETZAL" or row.currency_code == "QUETZALES" %}
00092|              <span class="amt-prefix">Q</span>{{ row.amount|floatformat:2|unlocalize }}
00093|            {% else %}
00094|              {{ row.amount|floatformat:2|unlocalize }}
00095|            {% endif %}
00096|          {% else %}
00097|            -
00098|          {% endif %}
00099|        </td>
00100|        <td style="text-align:left;">{{ row.observations|default:"-" }}</td>
00101|      </tr>
00102|      {% empty %}
00103|      <tr>
00104|        <td colspan="8" style="text-align:center;">
00105|          No existen registros importados para esta UNE y periodo.
00106|        </td>
00107|      </tr>
00108|      {% endfor %}
00109|    </tbody>
00110|  </table>
00111|</div>
00112|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZS5odG1sIiAlfQp7JSBsb2FkIGwxMG4gJX0KCnslIGJsb2NrIHRpdGxlICV9RGV0YWxsZSBjbGllbnRlcyBudWV2b3N7JSBlbmRibG9jayAlfQoKeyUgYmxvY2sgY29udGVudCAlfQo8c3R5bGU+CiAgLmFtdC1wcmVmaXggewogICAgZm9udC13ZWlnaHQ6IDYwMDsKICAgIGNvbG9yOiAjNDc1NTY5OwogICAgbWFyZ2luLXJpZ2h0OiAycHg7CiAgfQogIC5tb24tY2VsbCB7CiAgICBmb250LXNpemU6IDAuODVyZW07CiAgICBmb250LXdlaWdodDogNjAwOwogICAgY29sb3I6ICMwZjNkNTY7CiAgfQogIC5pbnZlc3RtZW50LXRvdGFsIHsKICAgIG1hcmdpbi10b3A6IDhweDsKICAgIHBhZGRpbmc6IDhweCAxMHB4OwogICAgYmFja2dyb3VuZDogI2YwZmRmYTsKICAgIGJvcmRlcjogMXB4IHNvbGlkICM5OWY2ZTQ7CiAgICBib3JkZXItcmFkaXVzOiA4cHg7CiAgICBmb250LXNpemU6IDAuOTJyZW07CiAgfQogIC5pbnZlc3RtZW50LXRvdGFsIC51c2QtdGFnIHsKICAgIGZvbnQtc2l6ZTogMC43NXJlbTsKICAgIGZvbnQtd2VpZ2h0OiA3MDA7CiAgICBjb2xvcjogIzBmNzY2ZTsKICAgIGJhY2tncm91bmQ6ICNjY2ZiZjE7CiAgICBwYWRkaW5nOiAxcHggNnB4OwogICAgYm9yZGVyLXJhZGl1czogNHB4OwogICAgbWFyZ2luLWxlZnQ6IDRweDsKICB9Cjwvc3R5bGU+CjxkaXYgY2xhc3M9ImNhcmQiPgogIDxoMiBzdHlsZT0ibWFyZ2luLXRvcDowOyI+RGV0YWxsZSBkZSBjbGllbnRlczwvaDI+CiAgPHAgY2xhc3M9Im11dGVkIj4KICAgIFVORTogPHN0cm9uZz57eyB1bmUubmFtZV9lcyB9fTwvc3Ryb25nPiB8CiAgICBQZXJpb2RvOiA8c3Ryb25nPnt7IHllYXIgfX0te3sgbW9udGh8c3RyaW5nZm9ybWF0OiIwMmQiIH19PC9zdHJvbmc+CiAgPC9wPgoKICB7JSBpZiBpbnZlc3RtZW50X2luZ3Jlc29zX3RvdGFsIGlzIG5vdCBOb25lICV9CiAgICA8cCBjbGFzcz0iaW52ZXN0bWVudC10b3RhbCI+CiAgICAgIFRvdGFsIEludmVzdG1lbnQgKFVTRCk6CiAgICAgIDxzdHJvbmc+JHt7IGludmVzdG1lbnRfaW5ncmVzb3NfdG90YWx8ZmxvYXRmb3JtYXQ6Mnx1bmxvY2FsaXplIH19PC9zdHJvbmc+CiAgICAgIDxzcGFuIGNsYXNzPSJ1c2QtdGFnIj5VU0Q8L3NwYW4+CiAgICA8L3A+CiAgeyUgZW5kaWYgJX0KICAKICA8dGFibGU+CiAgICA8dGhlYWQ+CiAgICAgIDx0cj4KICAgICAgICA8dGggc3R5bGU9InRleHQtYWxpZ246bGVmdDsiPkNsaWVudGU8L3RoPgogICAgICAgIDx0aD5OSVQ8L3RoPgogICAgICAgIDx0aD5PcGVyYWNpw7NuPC90aD4KICAgICAgICA8dGg+Q29udHJhdG9zIHByZXZpb3M8L3RoPgogICAgICAgIDx0aD7Cv0N1ZW50YSBjb21vIG51ZXZvPzwvdGg+CiAgICAgICAgPHRoIHRpdGxlPSJNb25lZGEgb3JpZ2luYWwgZGUgbGEgb3BlcmFjacOzbiI+TW9uLjwvdGg+CiAgICAgICAgPHRoPk1vbnRvPC90aD4KICAgICAgICA8dGggc3R5bGU9InRleHQtYWxpZ246bGVmdDsiPk9ic2VydmFjacOzbjwvdGg+CiAgICAgIDwvdHI+CiAgICA8L3RoZWFkPgogICAgPHRib2R5PgogICAgICB7JSBmb3Igcm93IGluIHJvd3MgJX0KICAgICAgPHRyPgogICAgICAgIDx0ZCBzdHlsZT0idGV4dC1hbGlnbjpsZWZ0OyI+e3sgcm93LmNsaWVudF9uYW1lfGRlZmF1bHQ6Ii0iIH19PC90ZD4KICAgICAgICA8dGQ+e3sgcm93Lm5pdHxkZWZhdWx0OiItIiB9fTwvdGQ+CiAgICAgICAgPHRkPnt7IHJvdy5vcGVyYXRpb25fY29kZXxkZWZhdWx0OiItIiB9fTwvdGQ+CiAgICAgICAgPHRkPnt7IHJvdy5wcmV2aW91c19jb250cmFjdHMgfX08L3RkPgogICAgICAgIDx0ZD4KICAgICAgICAgIHslIGlmIHJvdy5jb3VudHNfYXNfbmV3ICV9CiAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJvayI+U8OtPC9zcGFuPgogICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgICA8c3BhbiBjbGFzcz0iYmFkIj5Obzwvc3Bhbj4KICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgPC90ZD4KICAgICAgICA8dGQgY2xhc3M9Im1vbi1jZWxsIj4KICAgICAgICAgIHslIGlmIHJvdy5jdXJyZW5jeV9jb2RlID09ICJVU0QiIG9yIHJvdy5jdXJyZW5jeV9jb2RlID09ICJVUyQiIG9yIHJvdy5jdXJyZW5jeV9jb2RlID09ICIkIiAlfQogICAgICAgICAgICBVU0QKICAgICAgICAgIHslIGVsaWYgcm93LmN1cnJlbmN5X2NvZGUgPT0gIkdUUSIgb3Igcm93LmN1cnJlbmN5X2NvZGUgPT0gIlEiIG9yIHJvdy5jdXJyZW5jeV9jb2RlID09ICJRVUVUWkFMIiBvciByb3cuY3VycmVuY3lfY29kZSA9PSAiUVVFVFpBTEVTIiAlfQogICAgICAgICAgICBRCiAgICAgICAgICB7JSBlbHNlICV9CiAgICAgICAgICAgIHt7IHJvdy5jdXJyZW5jeV9jb2RlfGRlZmF1bHQ6Ii0iIH19CiAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgIDwvdGQ+CiAgICAgICAgPHRkPgogICAgICAgICAgeyUgaWYgcm93LmFtb3VudCBpcyBub3QgTm9uZSAlfQogICAgICAgICAgICB7JSBpZiByb3cuY3VycmVuY3lfY29kZSA9PSAiVVNEIiBvciByb3cuY3VycmVuY3lfY29kZSA9PSAiVVMkIiBvciByb3cuY3VycmVuY3lfY29kZSA9PSAiJCIgJX0KICAgICAgICAgICAgICA8c3BhbiBjbGFzcz0iYW10LXByZWZpeCI+JDwvc3Bhbj57eyByb3cuYW1vdW50fGZsb2F0Zm9ybWF0OjJ8dW5sb2NhbGl6ZSB9fQogICAgICAgICAgICB7JSBlbGlmIHJvdy5jdXJyZW5jeV9jb2RlID09ICJHVFEiIG9yIHJvdy5jdXJyZW5jeV9jb2RlID09ICJRIiBvciByb3cuY3VycmVuY3lfY29kZSA9PSAiUVVFVFpBTCIgb3Igcm93LmN1cnJlbmN5X2NvZGUgPT0gIlFVRVRaQUxFUyIgJX0KICAgICAgICAgICAgICA8c3BhbiBjbGFzcz0iYW10LXByZWZpeCI+UTwvc3Bhbj57eyByb3cuYW1vdW50fGZsb2F0Zm9ybWF0OjJ8dW5sb2NhbGl6ZSB9fQogICAgICAgICAgICB7JSBlbHNlICV9CiAgICAgICAgICAgICAge3sgcm93LmFtb3VudHxmbG9hdGZvcm1hdDoyfHVubG9jYWxpemUgfX0KICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgIHslIGVsc2UgJX0KICAgICAgICAgICAgLQogICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICA8L3RkPgogICAgICAgIDx0ZCBzdHlsZT0idGV4dC1hbGlnbjpsZWZ0OyI+e3sgcm93Lm9ic2VydmF0aW9uc3xkZWZhdWx0OiItIiB9fTwvdGQ+CiAgICAgIDwvdHI+CiAgICAgIHslIGVtcHR5ICV9CiAgICAgIDx0cj4KICAgICAgICA8dGQgY29sc3Bhbj0iOCIgc3R5bGU9InRleHQtYWxpZ246Y2VudGVyOyI+CiAgICAgICAgICBObyBleGlzdGVuIHJlZ2lzdHJvcyBpbXBvcnRhZG9zIHBhcmEgZXN0YSBVTkUgeSBwZXJpb2RvLgogICAgICAgIDwvdGQ+CiAgICAgIDwvdHI+CiAgICAgIHslIGVuZGZvciAlfQogICAgPC90Ym9keT4KICA8L3RhYmxlPgo8L2Rpdj4KeyUgZW5kYmxvY2sgJX0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgc/dashboard.html
PATH_JSON="templates/pgc/dashboard.html"
FILENAME=dashboard.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=1201
SIZE_BYTES_UTF8=41098
CONTENT_SHA256=8de8f8091b1912f52ed42fec5efb160df2ab9e67c370628500b1e348cdbb89c4
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

{% block title %}Tablero principal PGC{% endblock %}

{% block content %}
<style>
  .group_separator td {
    padding: 0;
    height: 14px;
    border-bottom: none;
    background: #ffffff;
  }

  /*
    Clasifica Sí / No — elegante y legible (daltonismo: frío vs cálido + forma).
    Sí  = verde suave más presente + tipografía casi negra + semibold + sello.
    No  = rosa muy pálido (mayoría) + gris oscuro, sin gritar.
  */
  table.pgc-scoreboard tbody tr.row-clasifica-no td {
    background: #faf6f4;
    color: #4a535c;
    font-weight: 400;
  }
  table.pgc-scoreboard tbody tr.row-clasifica-no td:first-child {
    box-shadow: inset 3px 0 0 #e8d5ce;
  }
  table.pgc-scoreboard tbody tr.row-clasifica-no:hover td {
    background: #f5efec;
  }
  table.pgc-scoreboard tbody tr.row-clasifica-no .clasifica-pill {
    color: #6b7280;
    font-weight: 500;
    letter-spacing: 0.02em;
  }

  table.pgc-scoreboard tbody tr.row-clasifica-si td {
    background: #d3ebe0;
    color: #0c1210;
    font-weight: 600;
    letter-spacing: 0.01em;
  }
  table.pgc-scoreboard tbody tr.row-clasifica-si td:first-child {
    box-shadow: inset 5px 0 0 #2f6f55;
  }
  table.pgc-scoreboard tbody tr.row-clasifica-si:hover td {
    background: #c5e4d4;
  }
  /* Total un poco más marcado en Sí (forma tipográfica, sin bold 700) */
  table.pgc-scoreboard tbody tr.row-clasifica-si td strong {
    font-weight: 600;
    color: #06100c;
  }
  table.pgc-scoreboard tbody tr.row-clasifica-no td strong {
    font-weight: 500;
    color: #4a535c;
  }

  table.pgc-scoreboard .clasifica-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.28rem;
    padding: 0.18rem 0.55rem;
    border-radius: 999px;
    font-size: 0.82rem;
    line-height: 1.2;
    border: 1px solid transparent;
  }
  table.pgc-scoreboard tbody tr.row-clasifica-si .clasifica-pill {
    background: rgba(255, 255, 255, 0.55);
    border-color: rgba(47, 111, 85, 0.35);
    color: #06100c;
    font-weight: 600;
    box-shadow: 0 1px 0 rgba(255, 255, 255, 0.7);
  }
  table.pgc-scoreboard tbody tr.row-clasifica-si .clasifica-pill.ok {
    color: #06100c;
    font-weight: 600;
  }
  table.pgc-scoreboard tbody tr.row-clasifica-no .clasifica-pill.bad {
    color: #6b7280;
    font-weight: 500;
  }
  table.pgc-scoreboard tbody tr.row-clasifica-si .clasifica-mark {
    font-size: 0.72rem;
    opacity: 0.9;
  }
</style>
<div class="card">
    <div class="wcg-report-head" style="margin-top:0;">
      <h2 style="margin:0;">Tablero principal de puntos — {{ selected_mode_label|default:selected_mode }}</h2>
      {% include "includes/module_mark.html" with module="pgc" %}
    </div>
  
    <p class="muted">
        Resumen mensual de puntos por UNE y periodo.
    </p>

    <form method="get" class="filters">
        <div>
            <label for="start_period">Desde</label><br>
            <select id="start_period">
                {% for p in available_periods %}
                    <option
                        value="{{ p.year }}-{{ p.month|stringformat:'02d' }}"
                        data-year="{{ p.year }}"
                        data-month="{{ p.month }}"
                        {% if report_filter.start_year == p.year and report_filter.start_month == p.month %}selected{% endif %}
                    >
                        {{ p.year }}-{{ p.month|stringformat:"02d" }}
                    </option>
                {% endfor %}
            </select>
            <input type="hidden" name="start_year" id="start_year" value="{{ report_filter.start_year }}">
            <input type="hidden" name="start_month" id="start_month" value="{{ report_filter.start_month }}">
        </div>

        <div>
            <label for="month_count">Meses incluidos</label><br>
            <select name="month_count" id="month_count">
                {% for n in month_count_options %}
                    <option value="{{ n }}" {% if report_filter.month_count == n %}selected{% endif %}>
                        {{ n }}
                    </option>
                {% endfor %}
            </select>
        </div>

        <div>
            <label for="mode">Modalidad</label><br>
            <select name="mode" id="mode">
                {% for value, label in mode_choices %}
                    <option value="{{ value }}" {% if selected_mode == value %}selected{% endif %}>
                        {{ label }}
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
        <div style="align-self:end;">
            <button type="button" id="btn-export-4-charts-svg">Exportación 4 charts</button>
            {% csrf_token %}
        </div>
    </form>

    <table class="pgc-scoreboard">
        <thead>
            <tr>
                <th>UNE</th>
                <th>Periodo</th>
                <th>Ingresos</th>
                <th>Clientes nuevos</th>
                <th>Venta cruzada</th>
                <th>Respuesta reqs</th>
                <th>Total</th>
                <th>Clasifica</th>
            </tr>
        </thead>
        <tbody>
          {% for row in rows %}
            {% if row.is_separator %}
              <tr class="group_separator">
                <td colspan="8"></td>
              </tr>
            {% else %}
              <tr class="{% if row.scorecard.is_month_qualified %}row-clasifica-si{% else %}row-clasifica-no{% endif %}">
                <td>{{ row.scorecard.une.name_es }}</td>
                <td>{{ row.scorecard.year }}-{{ row.scorecard.month|stringformat:"02d" }}</td>
                
                <td>{{ row.p_ingresos|floatformat:1 }}</td>
                <td>{{ row.p_clientes|floatformat:1 }}</td>
                <td>{{ row.p_venta_cruzada|floatformat:0 }}</td>
                <td>{{ row.p_respuesta_reqs|floatformat:0 }}</td>
                <td><strong>{{ row.scorecard.total_points|floatformat:1 }}</strong></td>

                <td>
                  {% if row.scorecard.is_month_qualified %}
                    <span class="clasifica-pill ok"><span class="clasifica-mark" aria-hidden="true">✓</span> Sí</span>
                  {% else %}
                    <span class="clasifica-pill bad">No</span>
                  {% endif %}
                </td>
              </tr>
            {% endif %}
          {% empty %}
            <tr>
              <td colspan="8">No hay scorecards para los filtros seleccionados.</td>
            </tr>
          {% endfor %}
        </tbody>
          
    </table>
</div>

<div class="card" style="margin-top:24px;">
  <h3 style="margin-top:0;">Tendencias comparativas</h3>
  <p class="muted">
    Estos gráficos usan el mismo rango de períodos seleccionado en el filtro superior.
  </p>

  <div class="filters" style="margin-bottom:16px;">
    <div>
      <label for="chart_type">Tipo</label><br>
      <select id="chart_type">
        <option value="mixed" selected>Mixto</option>
        <option value="line">Líneas</option>
        <option value="bar">Barras</option>
      </select>
    </div>

    <div>
      <label for="chart_accumulated">Modo</label><br>
      <label style="display:inline-flex; align-items:center; gap:8px; margin-top:6px;">
        <input type="checkbox" id="chart_accumulated">
        Acumulado dentro del rango
      </label>
    </div>

    <div style="min-width:320px;">
      <label>UNEs incluidas</label>
      <div id="chart_une_checklist" style="margin-top:8px; display:flex; flex-wrap:wrap; gap:12px;"></div>
    </div>

    <div style="align-self:end;">
      <button type="button" id="btn-generar-reportes" class="adm-btn adm-btn-primary" style="padding:9px 15px; border-radius:8px; font-weight:600; background:#0f766e; color:#fff; border:none; cursor:pointer;">
        Generar reportes
      </button>
    </div>
  </div>
  
  <div class="card" style="margin-top:12px;">
    <h4 style="margin-top:0; margin-bottom:4px;">Ingresos brutos</h4>
    <p class="muted" style="margin-top:0;">Comparación de cifras reales vs metas por período.</p>
    <div id="plot_ingresos_brutos" style="width:100%; height:420px;"></div>
  </div>

  <div class="card" style="margin-top:16px;">
    <h4 style="margin-top:0; margin-bottom:4px;">Clientes nuevos</h4>
    <p class="muted" style="margin-top:0;">Comparación de cifras reales vs metas por período.</p>
    <div id="plot_clientes_nuevos" style="width:100%; height:420px;"></div>
  </div>

  <div class="card" style="margin-top:16px;">
    <h4 style="margin-top:0; margin-bottom:4px;">Venta cruzada</h4>
    <p class="muted" style="margin-top:0;">Comparación de cifras reales vs metas por período.</p>
    <div id="plot_venta_cruzada" style="width:100%; height:420px;"></div>
  </div>
</div>

{{ chart_payload_json|json_script:"chart-payload-data" }}

<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>

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

        const mode = document.getElementById("mode");

        const params = new URLSearchParams({
            start_year: startYear.value || "",
            start_month: startMonth.value || "",
            month_count: document.getElementById("month_count")?.value || "",
            date_order: dateOrder.value || "asc",
            group_mode: groupMode.value || "une",
            mode: mode?.value || "modo1"
        });

        const url = `{% url 'pgc:dashboard_export_md' %}?` + params.toString();

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

            let filename = "pgc-tablero-principal.md";
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

<script>
  document.addEventListener("DOMContentLoaded", function () {
  const payloadNode = document.getElementById("chart-payload-data");
  if (!payloadNode) return;
  
  let chartPayload = JSON.parse(payloadNode.textContent);
  if (typeof chartPayload === "string") {
    chartPayload = JSON.parse(chartPayload);
  }
  
  if (!chartPayload || !chartPayload.metrics || !chartPayload.unes) {
    console.error("chartPayload inválido:", chartPayload);
    return;
  }
  
  const typeSelect = document.getElementById("chart_type");
  const accumulatedCheckbox = document.getElementById("chart_accumulated");
  const uneChecklist = document.getElementById("chart_une_checklist");

  const metricOrder = [
    "INGRESOS",
    "CLIENTES_NUEVOS",
    "VENTA_CRUZADA"
  ];

  const plotMap = {
    "INGRESOS": "plot_ingresos_brutos",
    "CLIENTES_NUEVOS": "plot_clientes_nuevos",
    "VENTA_CRUZADA": "plot_venta_cruzada"
  };

  function buildUneChecklist() {
    uneChecklist.innerHTML = "";
    chartPayload.unes.forEach(function (une) {
      const label = document.createElement("label");
      label.style.display = "inline-flex";
      label.style.alignItems = "center";
      label.style.gap = "6px";

      const input = document.createElement("input");
      input.type = "checkbox";
      input.name = "chart_une";
      input.value = une.code;
      input.checked = true;
      input.addEventListener("change", renderAllCharts);

      const text = document.createTextNode(une.name_es);

      label.appendChild(input);
      label.appendChild(text);
      uneChecklist.appendChild(label);
    });
  }

  function getSelectedUneCodes() {
    return Array.from(document.querySelectorAll('input[name="chart_une"]:checked'))
      .map(function (input) { return input.value; });
  }

  function accumulateValues(values) {
    let running = 0;
    return values.map(function (value) {
      const safeValue = Number(value || 0);
      running += safeValue;
      return running;
    });
  }

  function buildMetricSeries(metricCode, selectedUneCodes, accumulated) {
    const metric = chartPayload.metrics[metricCode];
  
    if (!metric || !metric.periods) {
      console.error("Métrica faltante o inválida:", metricCode, chartPayload);
      return {
        labels: [],
        realValues: [],
        targetValues: [],
        meta: {
          title: metricCode,
          subtitle: "Sin datos",
          y_axis: "Valor"
        }
      };
    }
  
    const labels = [];
    const realValues = [];
    const targetValues = [];
  
    metric.periods.forEach(function (period) {
      labels.push(period.label);
  
      let realSum = 0;
      let targetSum = 0;
  
      selectedUneCodes.forEach(function (uneCode) {
        const item = period.by_une?.[uneCode];
        if (item) {
          realSum += Number(item.real || 0);
          targetSum += Number(item.target || 0);
        }
      });
  
      realValues.push(realSum);
      targetValues.push(targetSum);
    });
  
    return {
      labels: labels,
      realValues: accumulated ? accumulateValues(realValues) : realValues,
      targetValues: accumulated ? accumulateValues(targetValues) : targetValues,
      meta: metric
    };
  }

  function buildTraces(metricCode, selectedUneCodes, accumulated, chartType) {
    const series = buildMetricSeries(metricCode, selectedUneCodes, accumulated);

    if (chartType === "line") {
      return [
        {
          x: series.labels,
          y: series.targetValues,
          type: "scatter",
          mode: "lines+markers",
          name: "Meta",
          line: { color: "#7f8c8d", width: 3, dash: "dash" },
          marker: { size: 7 }
        },
        {
          x: series.labels,
          y: series.realValues,
          type: "scatter",
          mode: "lines+markers",
          name: "Real",
          line: { color: "#1f77b4", width: 3 },
          marker: { size: 7 }
        }
      ];
    }

    if (chartType === "bar") {
      return [
        {
          x: series.labels,
          y: series.targetValues,
          type: "bar",
          name: "Meta",
          marker: { color: "#b0b7bf" }
        },
        {
          x: series.labels,
          y: series.realValues,
          type: "bar",
          name: "Real",
          marker: { color: "#1f77b4" }
        }
      ];
    }

    
    return [
      {
        x: series.labels,
        y: series.realValues,
        type: "bar",
        name: "Real",
        marker: { color: "#1f77b4" }
      },
      {
        x: series.labels,
        y: series.targetValues,
        type: "scatter",
        mode: "lines",
        name: "Meta",
        line: { color: "#7f8c8d", width: 3, dash: "dash" },
        marker: { size: 7 }
      }
    ];
  }

    
  function buildLayout(metricCode, accumulated) {
    const metric = chartPayload.metrics[metricCode];
    const series = buildMetricSeries(metricCode, getSelectedUneCodes(), accumulated);

    const titleText = accumulated
      ? `${metric.title}<br><sup>${metric.subtitle}. Modo acumulado dentro del rango.</sup>`
      : `${metric.title}<br><sup>${metric.subtitle}. Modo mensual.</sup>`;

    return {
      title: {
        text: titleText,
        font: {
          size: 20,
          color: "#166534"
        }
      },
      barmode: "group",
      margin: { l: 60, r: 24, t: 80, b: 80 },
      legend: {
        orientation: "h",
        yanchor: "top",
        y: -0.2,
        xanchor: "center",
        x: 0.5
      },
      xaxis: {
        title: "Período",
        type: "category",
        categoryorder: "array",
        categoryarray: series.labels,
        tickmode: "array",
        tickvals: series.labels,
        ticktext: series.labels
      },
      yaxis: {
        title: metric.y_axis,
        rangemode: "tozero"
      },
      paper_bgcolor: "white",
      plot_bgcolor: "white"
    };
  }

  function renderChart(metricCode) {
    const selectedUneCodes = getSelectedUneCodes();
    const chartType = typeSelect.value;
    const accumulated = accumulatedCheckbox.checked;

    const traces = buildTraces(metricCode, selectedUneCodes, accumulated, chartType);
    const layout = buildLayout(metricCode, accumulated);

    const config = {
      responsive: true,
      displaylogo: false,
      // Bloquea toda interacción del usuario
      staticPlot: true,          // Desactiva zoom, pan, selección, etc.
      scrollZoom: false,
      doubleClick: false,
      editable: false,
      displayModeBar: false      // Oculta barra de herramientas
    };

    Plotly.react(plotMap[metricCode], traces, layout, config);
  }
    
    
  function renderAllCharts() {
    const selectedUneCodes = getSelectedUneCodes();
    if (!selectedUneCodes.length) {
      metricOrder.forEach(function (metricCode) {
        Plotly.purge(plotMap[metricCode]);
        document.getElementById(plotMap[metricCode]).innerHTML =
          '<div class="muted" style="padding:24px;">Selecciona al menos una UNE.</div>';
      });
      return;
    }

    metricOrder.forEach(renderChart);
  }

  buildUneChecklist();
  typeSelect.addEventListener("change", renderAllCharts);
  accumulatedCheckbox.addEventListener("change", renderAllCharts);
  renderAllCharts();

  // --- Exportación 4 charts: PNG 1920×1080 (TV). ---
  // EXPORT_SVG_VERSION=v16-legend-yaxis-nudge
  // No modifica charts visibles (buildLayout / renderChart).
  // Los 4 charts (FACTORING, LEASING, INSURANCE, GRUPO) usan el MISMO layout.
  //
  // Configuración base (v11, antes del ensayo de fuentes/márgenes v12):
  //   MARGIN T/B/L/R = 155 / 275 / 100 / 80
  //   TITLE / SUBTITLE / AXIS / TICK / LEGEND = 72 / 22 / 24 / 20 / 24
  // Si el ensayo queda mal, restaurar esos valores y EXPORT_SVG_VERSION=v11-bars-navy-blue-png.

  const EXPORT_SVG_VERSION = "v16-legend-yaxis-nudge";
  const EXPORT_SUBTITLE =
    "Real vs meta por período. Cifras acumuladas dentro del rango.";
  const EXPORT_WIDTH = 1920;
  const EXPORT_HEIGHT = 1080;
  const IMAGE_WIDTH = 1920;
  const IMAGE_HEIGHT = 1080;
  // v12: franja blanca superior/inferior ~155 → ~75 (mitad).
  // Inferior: meses/Período/leyenda + ~75 px blancos libres (antes ~155).
  const EXPORT_MARGIN_T = 75;
  const EXPORT_MARGIN_B = 195;
  // v13: margen L = base 100 + ancho de «500».
  // v14–v16: +3× ancho de un dígito («0»).
  const EXPORT_MARGIN_L_BASE = 100;
  const EXPORT_MARGIN_R = 80;
  // v12: título 2.5×; resto de textos 2× (ensayo).
  const EXPORT_TITLE_SIZE = 180;
  const EXPORT_SUBTITLE_SIZE = 44;
  const EXPORT_AXIS_TITLE_SIZE = 48;
  const EXPORT_TICK_SIZE = 40;
  const EXPORT_LEGEND_SIZE = 48;

  function measureExportTextWidth(text, fontSize) {
    try {
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");
      if (!ctx) return Math.round(fontSize * 0.6 * String(text).length);
      // Plotly usa tipografía sans-serif por defecto en estos exports.
      ctx.font = fontSize + "px sans-serif";
      return Math.ceil(ctx.measureText(text).width);
    } catch (err) {
      return Math.round(fontSize * 0.6 * String(text).length);
    }
  }

  const EXPORT_YAXIS_DIGIT_W = measureExportTextWidth("0", EXPORT_TICK_SIZE);
  const EXPORT_MARGIN_L =
    EXPORT_MARGIN_L_BASE +
    measureExportTextWidth("500", EXPORT_TICK_SIZE) +
    3 * EXPORT_YAXIS_DIGIT_W;
  // v14–v16: leyenda baja adicional ≈ 3 × (mitad del ancho de un dígito).
  const EXPORT_LEGEND_NUDGE_PX = 1.5 * EXPORT_YAXIS_DIGIT_W;
  // Colores de marca (exactos). Real = azul navy de relleno; Meta = casi negro (línea).
  const EXPORT_COLOR_TEXT = "#3D3F3F";
  const EXPORT_COLOR_REAL = "#1D284A";
  const EXPORT_COLOR_META = "#010202";

  function getExportIngresosPeriods() {
    const exportBlock = chartPayload.export_ingresos;
    if (exportBlock && Array.isArray(exportBlock.periods) && exportBlock.periods.length) {
      return {
        periods: exportBlock.periods,
        yAxis: exportBlock.y_axis || "Cifras en miles de US$",
      };
    }
    const metric = chartPayload.metrics && chartPayload.metrics.INGRESOS;
    if (!metric || !metric.periods || !metric.periods.length) {
      return { periods: [], yAxis: "Cifras en miles de US$" };
    }
    const last = metric.periods[metric.periods.length - 1];
    const endYear = Number(last.year);
    const endMonth = Number(last.month);
    return {
      periods: metric.periods.filter(function (p) {
        return Number(p.year) === endYear && Number(p.month) >= 1 && Number(p.month) <= endMonth;
      }),
      yAxis: metric.y_axis || "Cifras en miles de US$",
    };
  }

  function buildExportIncomeSeries(periods, selectedUneCodes) {
    const labels = [];
    const realValues = [];
    const targetValues = [];
    periods.forEach(function (period) {
      labels.push(period.label);
      let realSum = 0;
      let targetSum = 0;
      selectedUneCodes.forEach(function (uneCode) {
        const item = period.by_une && period.by_une[uneCode];
        if (item) {
          realSum += Number(item.real || 0);
          targetSum += Number(item.target || 0);
        }
      });
      realValues.push(realSum);
      targetValues.push(targetSum);
    });
    return {
      labels: labels,
      realValues: accumulateValues(realValues),
      targetValues: accumulateValues(targetValues),
    };
  }

  function buildExportIncomeTraces(series) {
    // Real = barras relleno azul #1D284A; Meta = línea casi negra #010202.
    // Array de color por barra: Plotly no puede caer al colorway por omisión.
    const realFill = series.labels.map(function () {
      return EXPORT_COLOR_REAL;
    });
    return [
      {
        x: series.labels,
        y: series.realValues,
        type: "bar",
        name: "Real",
        marker: {
          color: realFill,
          line: { color: EXPORT_COLOR_REAL, width: 0 },
          opacity: 1,
        },
      },
      {
        x: series.labels,
        y: series.targetValues,
        type: "scatter",
        mode: "lines",
        name: "Meta",
        line: { color: EXPORT_COLOR_META, width: 3, dash: "dash" },
        marker: { color: EXPORT_COLOR_META },
      },
    ];
  }

  function buildExportIncomeLayout(title, series, yAxis) {
    // v12: márgenes blancos a la mitad; fuentes ×2.5 / ×2.
    // Subtítulo debajo del título (título ~EXPORT_TITLE_SIZE px + aire).
    const subtitleTopPx = EXPORT_TITLE_SIZE + 28;
    return {
      title: {
        text: "<b>" + title + "</b>",
        font: { size: EXPORT_TITLE_SIZE, color: EXPORT_COLOR_TEXT },
        xref: "paper",
        yref: "paper",
        x: 0.5,
        xanchor: "center",
        y: 1,
        yanchor: "top",
        pad: { t: 10, b: 2, l: 0, r: 0 },
      },
      annotations: [
        {
          text: EXPORT_SUBTITLE,
          xref: "paper",
          yref: "paper",
          x: 0.5,
          y: 1 - subtitleTopPx / IMAGE_HEIGHT,
          xanchor: "center",
          yanchor: "top",
          showarrow: false,
          font: { size: EXPORT_SUBTITLE_SIZE, color: EXPORT_COLOR_TEXT },
        },
      ],
      barmode: "group",
      bargap: 0.28,
      width: IMAGE_WIDTH,
      height: IMAGE_HEIGHT,
      margin: {
        l: EXPORT_MARGIN_L,
        r: EXPORT_MARGIN_R,
        t: EXPORT_MARGIN_T,
        b: EXPORT_MARGIN_B,
        pad: 0,
      },
      legend: {
        orientation: "h",
        xref: "paper",
        yref: "paper",
        x: 0.5,
        xanchor: "center",
        // v7: -0.055 − 1× altura del font (bajo «Período»).
        // v13: −⅓ adicional de la altura del font de la leyenda.
        // v14–v16: − EXPORT_LEGEND_NUDGE_PX (1.5× ancho de un dígito del eje Y).
        y:
          -0.055 -
          EXPORT_LEGEND_SIZE / IMAGE_HEIGHT -
          EXPORT_LEGEND_SIZE / (3 * IMAGE_HEIGHT) -
          EXPORT_LEGEND_NUDGE_PX / IMAGE_HEIGHT,
        yanchor: "top",
        font: { size: EXPORT_LEGEND_SIZE, color: EXPORT_COLOR_TEXT },
        bgcolor: "rgba(255,255,255,0)",
        borderwidth: 0,
        itemsizing: "constant",
        itemwidth: 60,
      },
      xaxis: {
        title: {
          text: "Período",
          font: { size: EXPORT_AXIS_TITLE_SIZE, color: EXPORT_COLOR_TEXT },
          // v8: 10; menor standoff = «Período» más arriba (más cerca de los meses)
          standoff: 4,
        },
        type: "category",
        categoryorder: "array",
        categoryarray: series.labels,
        tickmode: "array",
        tickvals: series.labels,
        ticktext: series.labels,
        tickfont: { size: EXPORT_TICK_SIZE, color: EXPORT_COLOR_TEXT },
        ticklen: 8,
        tickwidth: 1.5,
        linecolor: EXPORT_COLOR_TEXT,
        automargin: false,
        fixedrange: true,
        mirror: false,
      },
      yaxis: {
        title: {
          text: yAxis || "Cifras en miles de US$",
          font: { size: EXPORT_AXIS_TITLE_SIZE, color: EXPORT_COLOR_TEXT },
          standoff: 10,
        },
        rangemode: "tozero",
        tickfont: { size: EXPORT_TICK_SIZE, color: EXPORT_COLOR_TEXT },
        ticklen: 8,
        tickwidth: 1.5,
        linecolor: EXPORT_COLOR_TEXT,
        automargin: false,
        fixedrange: true,
        zeroline: true,
        zerolinecolor: EXPORT_COLOR_TEXT,
        gridcolor: "#e2e8f0",
        gridwidth: 1,
      },
      font: { color: EXPORT_COLOR_TEXT },
      colorway: [EXPORT_COLOR_REAL, EXPORT_COLOR_META],
      paper_bgcolor: "#ffffff",
      plot_bgcolor: "#ffffff",
      showlegend: true,
    };
  }

  function formatExportStamp(date) {
    const yy = String(date.getFullYear()).slice(-2);
    const mm = String(date.getMonth() + 1).padStart(2, "0");
    const hh = String(date.getHours()).padStart(2, "0");
    const mi = String(date.getMinutes()).padStart(2, "0");
    return yy + "-" + mm + " " + hh + "-" + mi;
  }

  function downloadDataUrl(dataUrl, filename) {
    const a = document.createElement("a");
    a.href = dataUrl;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
  }

  function getCsrfToken() {
    const input = document.querySelector("input[name='csrfmiddlewaretoken']");
    if (input && input.value) return input.value;
    const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    return match ? decodeURIComponent(match[1]) : "";
  }

  async function uploadExportPngToServer(dataUrl, filename) {
    const res = await fetch(dataUrl);
    const blob = await res.blob();
    const form = new FormData();
    form.append("file", blob, filename);
    form.append("activate", "1");
    const response = await fetch("{% url 'pgc:tv_charts_upload' %}", {
      method: "POST",
      headers: { "X-CSRFToken": getCsrfToken() },
      body: form,
      credentials: "same-origin",
    });
    let payload = {};
    try {
      payload = await response.json();
    } catch (e) {
      payload = {};
    }
    if (response.status === 403 || response.status === 401) {
      throw new Error("Sin permiso para guardar en el servidor (inicie sesión). La descarga local sí se hizo.");
    }
    if (!response.ok || !payload.ok) {
      throw new Error((payload && payload.error) || ("Error al guardar " + filename + " en el servidor (HTTP " + response.status + ")."));
    }
    return payload;
  }

  function sleep(ms) {
    return new Promise(function (resolve) { setTimeout(resolve, ms); });
  }

  async function exportFourIncomeChartsSvg() {
    const btnExport = document.getElementById("btn-export-4-charts-svg");
    if (!btnExport) return;

    if (typeof Plotly === "undefined" || !Plotly.newPlot || !Plotly.toImage) {
      alert("Plotly no está disponible; no se pueden exportar los PNG.");
      return;
    }

    const source = getExportIngresosPeriods();
    if (!source.periods.length) {
      alert("No hay datos de INGRESOS para exportar (export_ingresos / chartPayload).");
      return;
    }

    const configs = [
      { fileIndex: 1, title: "FACTORING", uneCodes: ["FACTORING"] },
      { fileIndex: 2, title: "LEASING", uneCodes: ["LEASING"] },
      { fileIndex: 3, title: "INSURANCE", uneCodes: ["INSURANCE"] },
      { fileIndex: 4, title: "GRUPO", uneCodes: ["FACTORING", "LEASING", "INSURANCE"] },
    ];

    const stamp = formatExportStamp(new Date());
    const originalText = btnExport.textContent;
    btnExport.disabled = true;
    btnExport.textContent = "Generando...";

    const host = document.createElement("div");
    host.setAttribute("aria-hidden", "true");
    host.style.cssText =
      "position:fixed;left:-10000px;top:0;width:" + IMAGE_WIDTH +
      "px;height:" + IMAGE_HEIGHT + "px;overflow:hidden;pointer-events:none;";
    document.body.appendChild(host);

    let serverSaved = 0;
    try {
      for (let i = 0; i < configs.length; i++) {
        const cfg = configs[i];
        const series = buildExportIncomeSeries(source.periods, cfg.uneCodes);
        if (!series.labels.length) {
          throw new Error("Serie vacía para " + cfg.title);
        }

        const gd = document.createElement("div");
        gd.style.width = IMAGE_WIDTH + "px";
        gd.style.height = IMAGE_HEIGHT + "px";
        host.appendChild(gd);

        await Plotly.newPlot(
          gd,
          buildExportIncomeTraces(series),
          buildExportIncomeLayout(cfg.title, series, source.yAxis),
          {
            staticPlot: true,
            displaylogo: false,
            displayModeBar: false,
            responsive: false,
          }
        );

        const dataUrlPng = await Plotly.toImage(gd, {
          format: "png",
          width: IMAGE_WIDTH,
          height: IMAGE_HEIGHT,
        });
        const filename = "wcg-g" + cfg.fileIndex + " " + stamp + ".png";
        downloadDataUrl(dataUrlPng, filename);
        await uploadExportPngToServer(dataUrlPng, filename);
        serverSaved += 1;

        Plotly.purge(gd);
        gd.remove();
        await sleep(250);
      }
      btnExport.textContent = "Listo (" + serverSaved + " en TV)";
      await sleep(1200);
    } catch (err) {
      console.error(err);
      alert((err && err.message) || "Error al generar la exportación de 4 charts PNG.");
    } finally {
      try {
        host.querySelectorAll("div").forEach(function (el) {
          try { Plotly.purge(el); } catch (e) {}
        });
      } catch (e) {}
      host.remove();
      btnExport.disabled = false;
      btnExport.textContent = originalText;
    }
  }

  const btnFourCharts = document.getElementById("btn-export-4-charts-svg");
  if (btnFourCharts) {
    btnFourCharts.setAttribute("data-export-svg-version", EXPORT_SVG_VERSION);
    btnFourCharts.addEventListener("click", function () {
      exportFourIncomeChartsSvg();
    });
  }

  // --- Generar reportes (modal) ---
  (function initReportModal() {
    const btn = document.getElementById("btn-generar-reportes");
    const modal = document.getElementById("reportes-modal");
    if (!btn || !modal) return;

    const closeBtns = modal.querySelectorAll("[data-reportes-close]");
    const form = document.getElementById("reportes-form");
    const statusEl = document.getElementById("reportes-status");
    const errEl = document.getElementById("reportes-error");
    const generateBtn = document.getElementById("reportes-generate");
    const csrfInput = document.querySelector("#btn-export-4-charts-svg")
      ? document.querySelector('input[name="csrfmiddlewaretoken"]')
      : document.querySelector('input[name="csrfmiddlewaretoken"]');

    function openModal() {
      errEl.textContent = "";
      statusEl.textContent = "";
      modal.style.display = "flex";
      fetch("{% url 'reports:defaults' %}", { credentials: "same-origin" })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (!data || !data.defaults) return;
          Object.keys(data.defaults).forEach(function (key) {
            const input = form.querySelector('input[name="areas"][value="' + key + '"]');
            if (input) input.checked = !!data.defaults[key];
          });
        })
        .catch(function () {});
    }

    function closeModal() {
      modal.style.display = "none";
      generateBtn.disabled = false;
      generateBtn.textContent = "Generar";
    }

    btn.addEventListener("click", openModal);
    closeBtns.forEach(function (el) {
      el.addEventListener("click", closeModal);
    });
    modal.addEventListener("click", function (ev) {
      if (ev.target === modal) closeModal();
    });

    form.addEventListener("submit", async function (ev) {
      ev.preventDefault();
      errEl.textContent = "";
      const checked = Array.from(form.querySelectorAll('input[name="areas"]:checked')).map(function (i) {
        return i.value;
      });
      if (!checked.length) {
        errEl.textContent = "Seleccione al menos un área: Administración, PGC, PGO o B. Riesgo.";
        return;
      }
      generateBtn.disabled = true;
      generateBtn.textContent = "Generando...";
      statusEl.textContent = "Generando reportes…";

      const csrf = (csrfInput && csrfInput.value) ||
        (document.cookie.match(/csrftoken=([^;]+)/) || [])[1] || "";

      try {
        const resp = await fetch("{% url 'reports:generate' %}", {
          method: "POST",
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf
          },
          body: JSON.stringify({ areas: checked })
        });
        if (!resp.ok) {
          let msg = "No se pudieron generar los reportes.";
          try {
            const j = await resp.json();
            if (j && j.error) msg = j.error;
          } catch (e) {}
          throw new Error(msg);
        }
        const blob = await resp.blob();
        let filename = resp.headers.get("X-Report-Filename") || "reportes_wcg.zip";
        const cd = resp.headers.get("Content-Disposition") || "";
        const m = cd.match(/filename=\"([^\"]+)\"/);
        if (m) filename = m[1];
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(url);
        statusEl.textContent = "Descarga iniciada: " + filename;
        generateBtn.textContent = "Generar";
        generateBtn.disabled = false;
      } catch (err) {
        errEl.textContent = (err && err.message) || "Error al generar.";
        statusEl.textContent = "";
        generateBtn.disabled = false;
        generateBtn.textContent = "Generar";
      }
    });
  })();

});
</script>

<div id="reportes-modal" style="display:none; position:fixed; inset:0; z-index:9999; background:rgba(15,23,42,0.45); align-items:center; justify-content:center; padding:16px;">
  <div style="background:#fff; border-radius:12px; max-width:420px; width:100%; box-shadow:0 20px 50px rgba(0,0,0,0.25); padding:22px 24px; border:1px solid #d9e2ec;">
    <h3 style="margin:0 0 6px; color:#0f3d56;">Generar reportes</h3>
    <p class="muted" style="margin:0 0 14px; font-size:0.9rem;">Seleccione una o varias áreas. Se descargará .md (+ .xlsx en resultados) o un .zip si hay varios archivos.</p>
    <form id="reportes-form">
      <label style="display:flex; gap:10px; align-items:center; margin:8px 0; font-weight:600;">
        <input type="checkbox" name="areas" value="admin"> Administración
      </label>
      <label style="display:flex; gap:10px; align-items:center; margin:8px 0; font-weight:600;">
        <input type="checkbox" name="areas" value="pgc" checked> PGC
      </label>
      <label style="display:flex; gap:10px; align-items:center; margin:8px 0; font-weight:600;">
        <input type="checkbox" name="areas" value="pgo"> PGO
      </label>
      <label style="display:flex; gap:10px; align-items:center; margin:8px 0; font-weight:600;">
        <input type="checkbox" name="areas" value="risk"> B. Riesgo
      </label>
      <p id="reportes-error" style="color:#b91c1c; font-size:0.88rem; min-height:1.2em; margin:10px 0 0;"></p>
      <p id="reportes-status" class="muted" style="font-size:0.88rem; min-height:1.2em; margin:4px 0 12px;"></p>
      <div style="display:flex; gap:10px; justify-content:flex-end;">
        <button type="button" data-reportes-close style="padding:8px 14px; border-radius:8px; border:1px solid #94a3b8; background:#f1f5f9; color:#0f172a; cursor:pointer; font-weight:600;">Cancelar</button>
        <button type="submit" id="reportes-generate" style="padding:8px 14px; border-radius:8px; border:none; background:#0f766e; color:#fff; cursor:pointer; font-weight:600;">Generar</button>
      </div>
    </form>
  </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base.html" %}
00002|
00003|{% block title %}Tablero principal PGC{% endblock %}
00004|
00005|{% block content %}
00006|<style>
00007|  .group_separator td {
00008|    padding: 0;
00009|    height: 14px;
00010|    border-bottom: none;
00011|    background: #ffffff;
00012|  }
00013|
00014|  /*
00015|    Clasifica Sí / No — elegante y legible (daltonismo: frío vs cálido + forma).
00016|    Sí  = verde suave más presente + tipografía casi negra + semibold + sello.
00017|    No  = rosa muy pálido (mayoría) + gris oscuro, sin gritar.
00018|  */
00019|  table.pgc-scoreboard tbody tr.row-clasifica-no td {
00020|    background: #faf6f4;
00021|    color: #4a535c;
00022|    font-weight: 400;
00023|  }
00024|  table.pgc-scoreboard tbody tr.row-clasifica-no td:first-child {
00025|    box-shadow: inset 3px 0 0 #e8d5ce;
00026|  }
00027|  table.pgc-scoreboard tbody tr.row-clasifica-no:hover td {
00028|    background: #f5efec;
00029|  }
00030|  table.pgc-scoreboard tbody tr.row-clasifica-no .clasifica-pill {
00031|    color: #6b7280;
00032|    font-weight: 500;
00033|    letter-spacing: 0.02em;
00034|  }
00035|
00036|  table.pgc-scoreboard tbody tr.row-clasifica-si td {
00037|    background: #d3ebe0;
00038|    color: #0c1210;
00039|    font-weight: 600;
00040|    letter-spacing: 0.01em;
00041|  }
00042|  table.pgc-scoreboard tbody tr.row-clasifica-si td:first-child {
00043|    box-shadow: inset 5px 0 0 #2f6f55;
00044|  }
00045|  table.pgc-scoreboard tbody tr.row-clasifica-si:hover td {
00046|    background: #c5e4d4;
00047|  }
00048|  /* Total un poco más marcado en Sí (forma tipográfica, sin bold 700) */
00049|  table.pgc-scoreboard tbody tr.row-clasifica-si td strong {
00050|    font-weight: 600;
00051|    color: #06100c;
00052|  }
00053|  table.pgc-scoreboard tbody tr.row-clasifica-no td strong {
00054|    font-weight: 500;
00055|    color: #4a535c;
00056|  }
00057|
00058|  table.pgc-scoreboard .clasifica-pill {
00059|    display: inline-flex;
00060|    align-items: center;
00061|    gap: 0.28rem;
00062|    padding: 0.18rem 0.55rem;
00063|    border-radius: 999px;
00064|    font-size: 0.82rem;
00065|    line-height: 1.2;
00066|    border: 1px solid transparent;
00067|  }
00068|  table.pgc-scoreboard tbody tr.row-clasifica-si .clasifica-pill {
00069|    background: rgba(255, 255, 255, 0.55);
00070|    border-color: rgba(47, 111, 85, 0.35);
00071|    color: #06100c;
00072|    font-weight: 600;
00073|    box-shadow: 0 1px 0 rgba(255, 255, 255, 0.7);
00074|  }
00075|  table.pgc-scoreboard tbody tr.row-clasifica-si .clasifica-pill.ok {
00076|    color: #06100c;
00077|    font-weight: 600;
00078|  }
00079|  table.pgc-scoreboard tbody tr.row-clasifica-no .clasifica-pill.bad {
00080|    color: #6b7280;
00081|    font-weight: 500;
00082|  }
00083|  table.pgc-scoreboard tbody tr.row-clasifica-si .clasifica-mark {
00084|    font-size: 0.72rem;
00085|    opacity: 0.9;
00086|  }
00087|</style>
00088|<div class="card">
00089|    <div class="wcg-report-head" style="margin-top:0;">
00090|      <h2 style="margin:0;">Tablero principal de puntos — {{ selected_mode_label|default:selected_mode }}</h2>
00091|      {% include "includes/module_mark.html" with module="pgc" %}
00092|    </div>
00093|  
00094|    <p class="muted">
00095|        Resumen mensual de puntos por UNE y periodo.
00096|    </p>
00097|
00098|    <form method="get" class="filters">
00099|        <div>
00100|            <label for="start_period">Desde</label><br>
00101|            <select id="start_period">
00102|                {% for p in available_periods %}
00103|                    <option
00104|                        value="{{ p.year }}-{{ p.month|stringformat:'02d' }}"
00105|                        data-year="{{ p.year }}"
00106|                        data-month="{{ p.month }}"
00107|                        {% if report_filter.start_year == p.year and report_filter.start_month == p.month %}selected{% endif %}
00108|                    >
00109|                        {{ p.year }}-{{ p.month|stringformat:"02d" }}
00110|                    </option>
00111|                {% endfor %}
00112|            </select>
00113|            <input type="hidden" name="start_year" id="start_year" value="{{ report_filter.start_year }}">
00114|            <input type="hidden" name="start_month" id="start_month" value="{{ report_filter.start_month }}">
00115|        </div>
00116|
00117|        <div>
00118|            <label for="month_count">Meses incluidos</label><br>
00119|            <select name="month_count" id="month_count">
00120|                {% for n in month_count_options %}
00121|                    <option value="{{ n }}" {% if report_filter.month_count == n %}selected{% endif %}>
00122|                        {{ n }}
00123|                    </option>
00124|                {% endfor %}
00125|            </select>
00126|        </div>
00127|
00128|        <div>
00129|            <label for="mode">Modalidad</label><br>
00130|            <select name="mode" id="mode">
00131|                {% for value, label in mode_choices %}
00132|                    <option value="{{ value }}" {% if selected_mode == value %}selected{% endif %}>
00133|                        {{ label }}
00134|                    </option>
00135|                {% endfor %}
00136|            </select>
00137|        </div>
00138|      
00139|        <div>
00140|          <label for="sort">Sort</label><br>
00141|          <select id="sort">
00142|            <option value="unes"
00143|              {% if report_sort.group_mode == "une" %}selected{% endif %}>
00144|              UNEs
00145|            </option>
00146|            <option value="fechas_asc"
00147|              {% if report_sort.group_mode == "period" and report_sort.date_order == "asc" %}selected{% endif %}>
00148|              Fechas ascendentes
00149|            </option>
00150|            <option value="fechas_desc"
00151|              {% if report_sort.group_mode == "period" and report_sort.date_order == "desc" %}selected{% endif %}>
00152|              Fechas descendentes
00153|            </option>
00154|          </select>
00155|          <input type="hidden" name="date_order" id="date_order"
00156|                 value="{% if report_sort.group_mode == 'period' and report_sort.date_order == 'desc' %}desc{% else %}asc{% endif %}">
00157|          <input type="hidden" name="group_mode" id="group_mode"
00158|                 value="{% if report_sort.group_mode == 'period' %}period{% else %}une{% endif %}">
00159|        </div>
00160|      
00161|        <div style="align-self:end;">
00162|            <button type="button" id="btn-export-md">.md export</button>
00163|        </div>
00164|        <div style="align-self:end;">
00165|            <button type="button" id="btn-export-4-charts-svg">Exportación 4 charts</button>
00166|            {% csrf_token %}
00167|        </div>
00168|    </form>
00169|
00170|    <table class="pgc-scoreboard">
00171|        <thead>
00172|            <tr>
00173|                <th>UNE</th>
00174|                <th>Periodo</th>
00175|                <th>Ingresos</th>
00176|                <th>Clientes nuevos</th>
00177|                <th>Venta cruzada</th>
00178|                <th>Respuesta reqs</th>
00179|                <th>Total</th>
00180|                <th>Clasifica</th>
00181|            </tr>
00182|        </thead>
00183|        <tbody>
00184|          {% for row in rows %}
00185|            {% if row.is_separator %}
00186|              <tr class="group_separator">
00187|                <td colspan="8"></td>
00188|              </tr>
00189|            {% else %}
00190|              <tr class="{% if row.scorecard.is_month_qualified %}row-clasifica-si{% else %}row-clasifica-no{% endif %}">
00191|                <td>{{ row.scorecard.une.name_es }}</td>
00192|                <td>{{ row.scorecard.year }}-{{ row.scorecard.month|stringformat:"02d" }}</td>
00193|                
00194|                <td>{{ row.p_ingresos|floatformat:1 }}</td>
00195|                <td>{{ row.p_clientes|floatformat:1 }}</td>
00196|                <td>{{ row.p_venta_cruzada|floatformat:0 }}</td>
00197|                <td>{{ row.p_respuesta_reqs|floatformat:0 }}</td>
00198|                <td><strong>{{ row.scorecard.total_points|floatformat:1 }}</strong></td>
00199|
00200|                <td>
00201|                  {% if row.scorecard.is_month_qualified %}
00202|                    <span class="clasifica-pill ok"><span class="clasifica-mark" aria-hidden="true">✓</span> Sí</span>
00203|                  {% else %}
00204|                    <span class="clasifica-pill bad">No</span>
00205|                  {% endif %}
00206|                </td>
00207|              </tr>
00208|            {% endif %}
00209|          {% empty %}
00210|            <tr>
00211|              <td colspan="8">No hay scorecards para los filtros seleccionados.</td>
00212|            </tr>
00213|          {% endfor %}
00214|        </tbody>
00215|          
00216|    </table>
00217|</div>
00218|
00219|<div class="card" style="margin-top:24px;">
00220|  <h3 style="margin-top:0;">Tendencias comparativas</h3>
00221|  <p class="muted">
00222|    Estos gráficos usan el mismo rango de períodos seleccionado en el filtro superior.
00223|  </p>
00224|
00225|  <div class="filters" style="margin-bottom:16px;">
00226|    <div>
00227|      <label for="chart_type">Tipo</label><br>
00228|      <select id="chart_type">
00229|        <option value="mixed" selected>Mixto</option>
00230|        <option value="line">Líneas</option>
00231|        <option value="bar">Barras</option>
00232|      </select>
00233|    </div>
00234|
00235|    <div>
00236|      <label for="chart_accumulated">Modo</label><br>
00237|      <label style="display:inline-flex; align-items:center; gap:8px; margin-top:6px;">
00238|        <input type="checkbox" id="chart_accumulated">
00239|        Acumulado dentro del rango
00240|      </label>
00241|    </div>
00242|
00243|    <div style="min-width:320px;">
00244|      <label>UNEs incluidas</label>
00245|      <div id="chart_une_checklist" style="margin-top:8px; display:flex; flex-wrap:wrap; gap:12px;"></div>
00246|    </div>
00247|
00248|    <div style="align-self:end;">
00249|      <button type="button" id="btn-generar-reportes" class="adm-btn adm-btn-primary" style="padding:9px 15px; border-radius:8px; font-weight:600; background:#0f766e; color:#fff; border:none; cursor:pointer;">
00250|        Generar reportes
00251|      </button>
00252|    </div>
00253|  </div>
00254|  
00255|  <div class="card" style="margin-top:12px;">
00256|    <h4 style="margin-top:0; margin-bottom:4px;">Ingresos brutos</h4>
00257|    <p class="muted" style="margin-top:0;">Comparación de cifras reales vs metas por período.</p>
00258|    <div id="plot_ingresos_brutos" style="width:100%; height:420px;"></div>
00259|  </div>
00260|
00261|  <div class="card" style="margin-top:16px;">
00262|    <h4 style="margin-top:0; margin-bottom:4px;">Clientes nuevos</h4>
00263|    <p class="muted" style="margin-top:0;">Comparación de cifras reales vs metas por período.</p>
00264|    <div id="plot_clientes_nuevos" style="width:100%; height:420px;"></div>
00265|  </div>
00266|
00267|  <div class="card" style="margin-top:16px;">
00268|    <h4 style="margin-top:0; margin-bottom:4px;">Venta cruzada</h4>
00269|    <p class="muted" style="margin-top:0;">Comparación de cifras reales vs metas por período.</p>
00270|    <div id="plot_venta_cruzada" style="width:100%; height:420px;"></div>
00271|  </div>
00272|</div>
00273|
00274|{{ chart_payload_json|json_script:"chart-payload-data" }}
00275|
00276|<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
00277|
00278|<script>
00279|document.addEventListener("DOMContentLoaded", function () {
00280|    const startPeriod = document.getElementById("start_period");
00281|    const startYear = document.getElementById("start_year");
00282|    const startMonth = document.getElementById("start_month");
00283|    const sort = document.getElementById("sort");
00284|    const dateOrder = document.getElementById("date_order");
00285|    const groupMode = document.getElementById("group_mode");
00286|    const btn = document.getElementById("btn-export-md");
00287|
00288|    function syncPeriodFields() {
00289|        if (!startPeriod) return;
00290|        const option = startPeriod.options[startPeriod.selectedIndex];
00291|        if (!option) return;
00292|        startYear.value = option.dataset.year || "";
00293|        startMonth.value = option.dataset.month || "";
00294|    }
00295|
00296|    function syncSortFields() {
00297|        if (!sort) return;
00298|        if (sort.value === "unes") {
00299|            groupMode.value = "une";
00300|            dateOrder.value = "asc";
00301|        } else if (sort.value === "fechas_desc") {
00302|            groupMode.value = "period";
00303|            dateOrder.value = "desc";
00304|        } else {
00305|            groupMode.value = "period";
00306|            dateOrder.value = "asc";
00307|        }
00308|    }
00309|
00310|
00311|    const filterForm = document.querySelector("form.filters");
00312|    function applyFilters() {
00313|        if (typeof syncPeriodFields === "function") syncPeriodFields();
00314|        if (typeof syncSortFields === "function") syncSortFields();
00315|        if (filterForm) filterForm.submit();
00316|    }
00317|
00318|    if (startPeriod) {
00319|        startPeriod.addEventListener("change", applyFilters);
00320|        syncPeriodFields();
00321|    }
00322|
00323|    if (sort) {
00324|        sort.addEventListener("change", applyFilters);
00325|        syncSortFields();
00326|    }
00327|
00328|    ["month_count", "mode", "start_year", "start_month", "year", "month", "une"].forEach(function (id) {
00329|        const el = document.getElementById(id);
00330|        if (el && el.tagName === "SELECT") {
00331|            el.addEventListener("change", applyFilters);
00332|        }
00333|    });
00334|
00335|    if (!btn) return;
00336|
00337|    btn.addEventListener("click", async function () {
00338|        syncPeriodFields();
00339|        syncSortFields();
00340|
00341|        const mode = document.getElementById("mode");
00342|
00343|        const params = new URLSearchParams({
00344|            start_year: startYear.value || "",
00345|            start_month: startMonth.value || "",
00346|            month_count: document.getElementById("month_count")?.value || "",
00347|            date_order: dateOrder.value || "asc",
00348|            group_mode: groupMode.value || "une",
00349|            mode: mode?.value || "modo1"
00350|        });
00351|
00352|        const url = `{% url 'pgc:dashboard_export_md' %}?` + params.toString();
00353|
00354|        btn.disabled = true;
00355|        const originalText = btn.textContent;
00356|        btn.textContent = "Generando...";
00357|
00358|        try {
00359|            const response = await fetch(url, {
00360|                method: "GET",
00361|                headers: {
00362|                    "X-Requested-With": "XMLHttpRequest"
00363|                }
00364|            });
00365|
00366|            if (!response.ok) {
00367|                throw new Error("No se pudo generar el archivo Markdown.");
00368|            }
00369|
00370|            const blob = await response.blob();
00371|
00372|            let filename = "pgc-tablero-principal.md";
00373|            const disposition = response.headers.get("Content-Disposition");
00374|            if (disposition) {
00375|                const utf8Match = disposition.match(/filename\*=UTF-8''([^;]+)/i);
00376|                const asciiMatch = disposition.match(/filename="([^"]+)"/i);
00377|
00378|                if (utf8Match && utf8Match[1]) {
00379|                    filename = decodeURIComponent(utf8Match[1]);
00380|                } else if (asciiMatch && asciiMatch[1]) {
00381|                    filename = asciiMatch[1];
00382|                }
00383|            }
00384|
00385|            const objectUrl = window.URL.createObjectURL(blob);
00386|            const a = document.createElement("a");
00387|            a.href = objectUrl;
00388|            a.download = filename;
00389|            document.body.appendChild(a);
00390|            a.click();
00391|            a.remove();
00392|            window.URL.revokeObjectURL(objectUrl);
00393|        } catch (error) {
00394|            alert(error.message || "Error generando la exportación.");
00395|        } finally {
00396|            btn.disabled = false;
00397|            btn.textContent = originalText;
00398|        }
00399|    });
00400|});
00401|</script>
00402|
00403|<script>
00404|  document.addEventListener("DOMContentLoaded", function () {
00405|  const payloadNode = document.getElementById("chart-payload-data");
00406|  if (!payloadNode) return;
00407|  
00408|  let chartPayload = JSON.parse(payloadNode.textContent);
00409|  if (typeof chartPayload === "string") {
00410|    chartPayload = JSON.parse(chartPayload);
00411|  }
00412|  
00413|  if (!chartPayload || !chartPayload.metrics || !chartPayload.unes) {
00414|    console.error("chartPayload inválido:", chartPayload);
00415|    return;
00416|  }
00417|  
00418|  const typeSelect = document.getElementById("chart_type");
00419|  const accumulatedCheckbox = document.getElementById("chart_accumulated");
00420|  const uneChecklist = document.getElementById("chart_une_checklist");
00421|
00422|  const metricOrder = [
00423|    "INGRESOS",
00424|    "CLIENTES_NUEVOS",
00425|    "VENTA_CRUZADA"
00426|  ];
00427|
00428|  const plotMap = {
00429|    "INGRESOS": "plot_ingresos_brutos",
00430|    "CLIENTES_NUEVOS": "plot_clientes_nuevos",
00431|    "VENTA_CRUZADA": "plot_venta_cruzada"
00432|  };
00433|
00434|  function buildUneChecklist() {
00435|    uneChecklist.innerHTML = "";
00436|    chartPayload.unes.forEach(function (une) {
00437|      const label = document.createElement("label");
00438|      label.style.display = "inline-flex";
00439|      label.style.alignItems = "center";
00440|      label.style.gap = "6px";
00441|
00442|      const input = document.createElement("input");
00443|      input.type = "checkbox";
00444|      input.name = "chart_une";
00445|      input.value = une.code;
00446|      input.checked = true;
00447|      input.addEventListener("change", renderAllCharts);
00448|
00449|      const text = document.createTextNode(une.name_es);
00450|
00451|      label.appendChild(input);
00452|      label.appendChild(text);
00453|      uneChecklist.appendChild(label);
00454|    });
00455|  }
00456|
00457|  function getSelectedUneCodes() {
00458|    return Array.from(document.querySelectorAll('input[name="chart_une"]:checked'))
00459|      .map(function (input) { return input.value; });
00460|  }
00461|
00462|  function accumulateValues(values) {
00463|    let running = 0;
00464|    return values.map(function (value) {
00465|      const safeValue = Number(value || 0);
00466|      running += safeValue;
00467|      return running;
00468|    });
00469|  }
00470|
00471|  function buildMetricSeries(metricCode, selectedUneCodes, accumulated) {
00472|    const metric = chartPayload.metrics[metricCode];
00473|  
00474|    if (!metric || !metric.periods) {
00475|      console.error("Métrica faltante o inválida:", metricCode, chartPayload);
00476|      return {
00477|        labels: [],
00478|        realValues: [],
00479|        targetValues: [],
00480|        meta: {
00481|          title: metricCode,
00482|          subtitle: "Sin datos",
00483|          y_axis: "Valor"
00484|        }
00485|      };
00486|    }
00487|  
00488|    const labels = [];
00489|    const realValues = [];
00490|    const targetValues = [];
00491|  
00492|    metric.periods.forEach(function (period) {
00493|      labels.push(period.label);
00494|  
00495|      let realSum = 0;
00496|      let targetSum = 0;
00497|  
00498|      selectedUneCodes.forEach(function (uneCode) {
00499|        const item = period.by_une?.[uneCode];
00500|        if (item) {
00501|          realSum += Number(item.real || 0);
00502|          targetSum += Number(item.target || 0);
00503|        }
00504|      });
00505|  
00506|      realValues.push(realSum);
00507|      targetValues.push(targetSum);
00508|    });
00509|  
00510|    return {
00511|      labels: labels,
00512|      realValues: accumulated ? accumulateValues(realValues) : realValues,
00513|      targetValues: accumulated ? accumulateValues(targetValues) : targetValues,
00514|      meta: metric
00515|    };
00516|  }
00517|
00518|  function buildTraces(metricCode, selectedUneCodes, accumulated, chartType) {
00519|    const series = buildMetricSeries(metricCode, selectedUneCodes, accumulated);
00520|
00521|    if (chartType === "line") {
00522|      return [
00523|        {
00524|          x: series.labels,
00525|          y: series.targetValues,
00526|          type: "scatter",
00527|          mode: "lines+markers",
00528|          name: "Meta",
00529|          line: { color: "#7f8c8d", width: 3, dash: "dash" },
00530|          marker: { size: 7 }
00531|        },
00532|        {
00533|          x: series.labels,
00534|          y: series.realValues,
00535|          type: "scatter",
00536|          mode: "lines+markers",
00537|          name: "Real",
00538|          line: { color: "#1f77b4", width: 3 },
00539|          marker: { size: 7 }
00540|        }
00541|      ];
00542|    }
00543|
00544|    if (chartType === "bar") {
00545|      return [
00546|        {
00547|          x: series.labels,
00548|          y: series.targetValues,
00549|          type: "bar",
00550|          name: "Meta",
00551|          marker: { color: "#b0b7bf" }
00552|        },
00553|        {
00554|          x: series.labels,
00555|          y: series.realValues,
00556|          type: "bar",
00557|          name: "Real",
00558|          marker: { color: "#1f77b4" }
00559|        }
00560|      ];
00561|    }
00562|
00563|    
00564|    return [
00565|      {
00566|        x: series.labels,
00567|        y: series.realValues,
00568|        type: "bar",
00569|        name: "Real",
00570|        marker: { color: "#1f77b4" }
00571|      },
00572|      {
00573|        x: series.labels,
00574|        y: series.targetValues,
00575|        type: "scatter",
00576|        mode: "lines",
00577|        name: "Meta",
00578|        line: { color: "#7f8c8d", width: 3, dash: "dash" },
00579|        marker: { size: 7 }
00580|      }
00581|    ];
00582|  }
00583|
00584|    
00585|  function buildLayout(metricCode, accumulated) {
00586|    const metric = chartPayload.metrics[metricCode];
00587|    const series = buildMetricSeries(metricCode, getSelectedUneCodes(), accumulated);
00588|
00589|    const titleText = accumulated
00590|      ? `${metric.title}<br><sup>${metric.subtitle}. Modo acumulado dentro del rango.</sup>`
00591|      : `${metric.title}<br><sup>${metric.subtitle}. Modo mensual.</sup>`;
00592|
00593|    return {
00594|      title: {
00595|        text: titleText,
00596|        font: {
00597|          size: 20,
00598|          color: "#166534"
00599|        }
00600|      },
00601|      barmode: "group",
00602|      margin: { l: 60, r: 24, t: 80, b: 80 },
00603|      legend: {
00604|        orientation: "h",
00605|        yanchor: "top",
00606|        y: -0.2,
00607|        xanchor: "center",
00608|        x: 0.5
00609|      },
00610|      xaxis: {
00611|        title: "Período",
00612|        type: "category",
00613|        categoryorder: "array",
00614|        categoryarray: series.labels,
00615|        tickmode: "array",
00616|        tickvals: series.labels,
00617|        ticktext: series.labels
00618|      },
00619|      yaxis: {
00620|        title: metric.y_axis,
00621|        rangemode: "tozero"
00622|      },
00623|      paper_bgcolor: "white",
00624|      plot_bgcolor: "white"
00625|    };
00626|  }
00627|
00628|  function renderChart(metricCode) {
00629|    const selectedUneCodes = getSelectedUneCodes();
00630|    const chartType = typeSelect.value;
00631|    const accumulated = accumulatedCheckbox.checked;
00632|
00633|    const traces = buildTraces(metricCode, selectedUneCodes, accumulated, chartType);
00634|    const layout = buildLayout(metricCode, accumulated);
00635|
00636|    const config = {
00637|      responsive: true,
00638|      displaylogo: false,
00639|      // Bloquea toda interacción del usuario
00640|      staticPlot: true,          // Desactiva zoom, pan, selección, etc.
00641|      scrollZoom: false,
00642|      doubleClick: false,
00643|      editable: false,
00644|      displayModeBar: false      // Oculta barra de herramientas
00645|    };
00646|
00647|    Plotly.react(plotMap[metricCode], traces, layout, config);
00648|  }
00649|    
00650|    
00651|  function renderAllCharts() {
00652|    const selectedUneCodes = getSelectedUneCodes();
00653|    if (!selectedUneCodes.length) {
00654|      metricOrder.forEach(function (metricCode) {
00655|        Plotly.purge(plotMap[metricCode]);
00656|        document.getElementById(plotMap[metricCode]).innerHTML =
00657|          '<div class="muted" style="padding:24px;">Selecciona al menos una UNE.</div>';
00658|      });
00659|      return;
00660|    }
00661|
00662|    metricOrder.forEach(renderChart);
00663|  }
00664|
00665|  buildUneChecklist();
00666|  typeSelect.addEventListener("change", renderAllCharts);
00667|  accumulatedCheckbox.addEventListener("change", renderAllCharts);
00668|  renderAllCharts();
00669|
00670|  // --- Exportación 4 charts: PNG 1920×1080 (TV). ---
00671|  // EXPORT_SVG_VERSION=v16-legend-yaxis-nudge
00672|  // No modifica charts visibles (buildLayout / renderChart).
00673|  // Los 4 charts (FACTORING, LEASING, INSURANCE, GRUPO) usan el MISMO layout.
00674|  //
00675|  // Configuración base (v11, antes del ensayo de fuentes/márgenes v12):
00676|  //   MARGIN T/B/L/R = 155 / 275 / 100 / 80
00677|  //   TITLE / SUBTITLE / AXIS / TICK / LEGEND = 72 / 22 / 24 / 20 / 24
00678|  // Si el ensayo queda mal, restaurar esos valores y EXPORT_SVG_VERSION=v11-bars-navy-blue-png.
00679|
00680|  const EXPORT_SVG_VERSION = "v16-legend-yaxis-nudge";
00681|  const EXPORT_SUBTITLE =
00682|    "Real vs meta por período. Cifras acumuladas dentro del rango.";
00683|  const EXPORT_WIDTH = 1920;
00684|  const EXPORT_HEIGHT = 1080;
00685|  const IMAGE_WIDTH = 1920;
00686|  const IMAGE_HEIGHT = 1080;
00687|  // v12: franja blanca superior/inferior ~155 → ~75 (mitad).
00688|  // Inferior: meses/Período/leyenda + ~75 px blancos libres (antes ~155).
00689|  const EXPORT_MARGIN_T = 75;
00690|  const EXPORT_MARGIN_B = 195;
00691|  // v13: margen L = base 100 + ancho de «500».
00692|  // v14–v16: +3× ancho de un dígito («0»).
00693|  const EXPORT_MARGIN_L_BASE = 100;
00694|  const EXPORT_MARGIN_R = 80;
00695|  // v12: título 2.5×; resto de textos 2× (ensayo).
00696|  const EXPORT_TITLE_SIZE = 180;
00697|  const EXPORT_SUBTITLE_SIZE = 44;
00698|  const EXPORT_AXIS_TITLE_SIZE = 48;
00699|  const EXPORT_TICK_SIZE = 40;
00700|  const EXPORT_LEGEND_SIZE = 48;
00701|
00702|  function measureExportTextWidth(text, fontSize) {
00703|    try {
00704|      const canvas = document.createElement("canvas");
00705|      const ctx = canvas.getContext("2d");
00706|      if (!ctx) return Math.round(fontSize * 0.6 * String(text).length);
00707|      // Plotly usa tipografía sans-serif por defecto en estos exports.
00708|      ctx.font = fontSize + "px sans-serif";
00709|      return Math.ceil(ctx.measureText(text).width);
00710|    } catch (err) {
00711|      return Math.round(fontSize * 0.6 * String(text).length);
00712|    }
00713|  }
00714|
00715|  const EXPORT_YAXIS_DIGIT_W = measureExportTextWidth("0", EXPORT_TICK_SIZE);
00716|  const EXPORT_MARGIN_L =
00717|    EXPORT_MARGIN_L_BASE +
00718|    measureExportTextWidth("500", EXPORT_TICK_SIZE) +
00719|    3 * EXPORT_YAXIS_DIGIT_W;
00720|  // v14–v16: leyenda baja adicional ≈ 3 × (mitad del ancho de un dígito).
00721|  const EXPORT_LEGEND_NUDGE_PX = 1.5 * EXPORT_YAXIS_DIGIT_W;
00722|  // Colores de marca (exactos). Real = azul navy de relleno; Meta = casi negro (línea).
00723|  const EXPORT_COLOR_TEXT = "#3D3F3F";
00724|  const EXPORT_COLOR_REAL = "#1D284A";
00725|  const EXPORT_COLOR_META = "#010202";
00726|
00727|  function getExportIngresosPeriods() {
00728|    const exportBlock = chartPayload.export_ingresos;
00729|    if (exportBlock && Array.isArray(exportBlock.periods) && exportBlock.periods.length) {
00730|      return {
00731|        periods: exportBlock.periods,
00732|        yAxis: exportBlock.y_axis || "Cifras en miles de US$",
00733|      };
00734|    }
00735|    const metric = chartPayload.metrics && chartPayload.metrics.INGRESOS;
00736|    if (!metric || !metric.periods || !metric.periods.length) {
00737|      return { periods: [], yAxis: "Cifras en miles de US$" };
00738|    }
00739|    const last = metric.periods[metric.periods.length - 1];
00740|    const endYear = Number(last.year);
00741|    const endMonth = Number(last.month);
00742|    return {
00743|      periods: metric.periods.filter(function (p) {
00744|        return Number(p.year) === endYear && Number(p.month) >= 1 && Number(p.month) <= endMonth;
00745|      }),
00746|      yAxis: metric.y_axis || "Cifras en miles de US$",
00747|    };
00748|  }
00749|
00750|  function buildExportIncomeSeries(periods, selectedUneCodes) {
00751|    const labels = [];
00752|    const realValues = [];
00753|    const targetValues = [];
00754|    periods.forEach(function (period) {
00755|      labels.push(period.label);
00756|      let realSum = 0;
00757|      let targetSum = 0;
00758|      selectedUneCodes.forEach(function (uneCode) {
00759|        const item = period.by_une && period.by_une[uneCode];
00760|        if (item) {
00761|          realSum += Number(item.real || 0);
00762|          targetSum += Number(item.target || 0);
00763|        }
00764|      });
00765|      realValues.push(realSum);
00766|      targetValues.push(targetSum);
00767|    });
00768|    return {
00769|      labels: labels,
00770|      realValues: accumulateValues(realValues),
00771|      targetValues: accumulateValues(targetValues),
00772|    };
00773|  }
00774|
00775|  function buildExportIncomeTraces(series) {
00776|    // Real = barras relleno azul #1D284A; Meta = línea casi negra #010202.
00777|    // Array de color por barra: Plotly no puede caer al colorway por omisión.
00778|    const realFill = series.labels.map(function () {
00779|      return EXPORT_COLOR_REAL;
00780|    });
00781|    return [
00782|      {
00783|        x: series.labels,
00784|        y: series.realValues,
00785|        type: "bar",
00786|        name: "Real",
00787|        marker: {
00788|          color: realFill,
00789|          line: { color: EXPORT_COLOR_REAL, width: 0 },
00790|          opacity: 1,
00791|        },
00792|      },
00793|      {
00794|        x: series.labels,
00795|        y: series.targetValues,
00796|        type: "scatter",
00797|        mode: "lines",
00798|        name: "Meta",
00799|        line: { color: EXPORT_COLOR_META, width: 3, dash: "dash" },
00800|        marker: { color: EXPORT_COLOR_META },
00801|      },
00802|    ];
00803|  }
00804|
00805|  function buildExportIncomeLayout(title, series, yAxis) {
00806|    // v12: márgenes blancos a la mitad; fuentes ×2.5 / ×2.
00807|    // Subtítulo debajo del título (título ~EXPORT_TITLE_SIZE px + aire).
00808|    const subtitleTopPx = EXPORT_TITLE_SIZE + 28;
00809|    return {
00810|      title: {
00811|        text: "<b>" + title + "</b>",
00812|        font: { size: EXPORT_TITLE_SIZE, color: EXPORT_COLOR_TEXT },
00813|        xref: "paper",
00814|        yref: "paper",
00815|        x: 0.5,
00816|        xanchor: "center",
00817|        y: 1,
00818|        yanchor: "top",
00819|        pad: { t: 10, b: 2, l: 0, r: 0 },
00820|      },
00821|      annotations: [
00822|        {
00823|          text: EXPORT_SUBTITLE,
00824|          xref: "paper",
00825|          yref: "paper",
00826|          x: 0.5,
00827|          y: 1 - subtitleTopPx / IMAGE_HEIGHT,
00828|          xanchor: "center",
00829|          yanchor: "top",
00830|          showarrow: false,
00831|          font: { size: EXPORT_SUBTITLE_SIZE, color: EXPORT_COLOR_TEXT },
00832|        },
00833|      ],
00834|      barmode: "group",
00835|      bargap: 0.28,
00836|      width: IMAGE_WIDTH,
00837|      height: IMAGE_HEIGHT,
00838|      margin: {
00839|        l: EXPORT_MARGIN_L,
00840|        r: EXPORT_MARGIN_R,
00841|        t: EXPORT_MARGIN_T,
00842|        b: EXPORT_MARGIN_B,
00843|        pad: 0,
00844|      },
00845|      legend: {
00846|        orientation: "h",
00847|        xref: "paper",
00848|        yref: "paper",
00849|        x: 0.5,
00850|        xanchor: "center",
00851|        // v7: -0.055 − 1× altura del font (bajo «Período»).
00852|        // v13: −⅓ adicional de la altura del font de la leyenda.
00853|        // v14–v16: − EXPORT_LEGEND_NUDGE_PX (1.5× ancho de un dígito del eje Y).
00854|        y:
00855|          -0.055 -
00856|          EXPORT_LEGEND_SIZE / IMAGE_HEIGHT -
00857|          EXPORT_LEGEND_SIZE / (3 * IMAGE_HEIGHT) -
00858|          EXPORT_LEGEND_NUDGE_PX / IMAGE_HEIGHT,
00859|        yanchor: "top",
00860|        font: { size: EXPORT_LEGEND_SIZE, color: EXPORT_COLOR_TEXT },
00861|        bgcolor: "rgba(255,255,255,0)",
00862|        borderwidth: 0,
00863|        itemsizing: "constant",
00864|        itemwidth: 60,
00865|      },
00866|      xaxis: {
00867|        title: {
00868|          text: "Período",
00869|          font: { size: EXPORT_AXIS_TITLE_SIZE, color: EXPORT_COLOR_TEXT },
00870|          // v8: 10; menor standoff = «Período» más arriba (más cerca de los meses)
00871|          standoff: 4,
00872|        },
00873|        type: "category",
00874|        categoryorder: "array",
00875|        categoryarray: series.labels,
00876|        tickmode: "array",
00877|        tickvals: series.labels,
00878|        ticktext: series.labels,
00879|        tickfont: { size: EXPORT_TICK_SIZE, color: EXPORT_COLOR_TEXT },
00880|        ticklen: 8,
00881|        tickwidth: 1.5,
00882|        linecolor: EXPORT_COLOR_TEXT,
00883|        automargin: false,
00884|        fixedrange: true,
00885|        mirror: false,
00886|      },
00887|      yaxis: {
00888|        title: {
00889|          text: yAxis || "Cifras en miles de US$",
00890|          font: { size: EXPORT_AXIS_TITLE_SIZE, color: EXPORT_COLOR_TEXT },
00891|          standoff: 10,
00892|        },
00893|        rangemode: "tozero",
00894|        tickfont: { size: EXPORT_TICK_SIZE, color: EXPORT_COLOR_TEXT },
00895|        ticklen: 8,
00896|        tickwidth: 1.5,
00897|        linecolor: EXPORT_COLOR_TEXT,
00898|        automargin: false,
00899|        fixedrange: true,
00900|        zeroline: true,
00901|        zerolinecolor: EXPORT_COLOR_TEXT,
00902|        gridcolor: "#e2e8f0",
00903|        gridwidth: 1,
00904|      },
00905|      font: { color: EXPORT_COLOR_TEXT },
00906|      colorway: [EXPORT_COLOR_REAL, EXPORT_COLOR_META],
00907|      paper_bgcolor: "#ffffff",
00908|      plot_bgcolor: "#ffffff",
00909|      showlegend: true,
00910|    };
00911|  }
00912|
00913|  function formatExportStamp(date) {
00914|    const yy = String(date.getFullYear()).slice(-2);
00915|    const mm = String(date.getMonth() + 1).padStart(2, "0");
00916|    const hh = String(date.getHours()).padStart(2, "0");
00917|    const mi = String(date.getMinutes()).padStart(2, "0");
00918|    return yy + "-" + mm + " " + hh + "-" + mi;
00919|  }
00920|
00921|  function downloadDataUrl(dataUrl, filename) {
00922|    const a = document.createElement("a");
00923|    a.href = dataUrl;
00924|    a.download = filename;
00925|    document.body.appendChild(a);
00926|    a.click();
00927|    a.remove();
00928|  }
00929|
00930|  function getCsrfToken() {
00931|    const input = document.querySelector("input[name='csrfmiddlewaretoken']");
00932|    if (input && input.value) return input.value;
00933|    const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
00934|    return match ? decodeURIComponent(match[1]) : "";
00935|  }
00936|
00937|  async function uploadExportPngToServer(dataUrl, filename) {
00938|    const res = await fetch(dataUrl);
00939|    const blob = await res.blob();
00940|    const form = new FormData();
00941|    form.append("file", blob, filename);
00942|    form.append("activate", "1");
00943|    const response = await fetch("{% url 'pgc:tv_charts_upload' %}", {
00944|      method: "POST",
00945|      headers: { "X-CSRFToken": getCsrfToken() },
00946|      body: form,
00947|      credentials: "same-origin",
00948|    });
00949|    let payload = {};
00950|    try {
00951|      payload = await response.json();
00952|    } catch (e) {
00953|      payload = {};
00954|    }
00955|    if (response.status === 403 || response.status === 401) {
00956|      throw new Error("Sin permiso para guardar en el servidor (inicie sesión). La descarga local sí se hizo.");
00957|    }
00958|    if (!response.ok || !payload.ok) {
00959|      throw new Error((payload && payload.error) || ("Error al guardar " + filename + " en el servidor (HTTP " + response.status + ")."));
00960|    }
00961|    return payload;
00962|  }
00963|
00964|  function sleep(ms) {
00965|    return new Promise(function (resolve) { setTimeout(resolve, ms); });
00966|  }
00967|
00968|  async function exportFourIncomeChartsSvg() {
00969|    const btnExport = document.getElementById("btn-export-4-charts-svg");
00970|    if (!btnExport) return;
00971|
00972|    if (typeof Plotly === "undefined" || !Plotly.newPlot || !Plotly.toImage) {
00973|      alert("Plotly no está disponible; no se pueden exportar los PNG.");
00974|      return;
00975|    }
00976|
00977|    const source = getExportIngresosPeriods();
00978|    if (!source.periods.length) {
00979|      alert("No hay datos de INGRESOS para exportar (export_ingresos / chartPayload).");
00980|      return;
00981|    }
00982|
00983|    const configs = [
00984|      { fileIndex: 1, title: "FACTORING", uneCodes: ["FACTORING"] },
00985|      { fileIndex: 2, title: "LEASING", uneCodes: ["LEASING"] },
00986|      { fileIndex: 3, title: "INSURANCE", uneCodes: ["INSURANCE"] },
00987|      { fileIndex: 4, title: "GRUPO", uneCodes: ["FACTORING", "LEASING", "INSURANCE"] },
00988|    ];
00989|
00990|    const stamp = formatExportStamp(new Date());
00991|    const originalText = btnExport.textContent;
00992|    btnExport.disabled = true;
00993|    btnExport.textContent = "Generando...";
00994|
00995|    const host = document.createElement("div");
00996|    host.setAttribute("aria-hidden", "true");
00997|    host.style.cssText =
00998|      "position:fixed;left:-10000px;top:0;width:" + IMAGE_WIDTH +
00999|      "px;height:" + IMAGE_HEIGHT + "px;overflow:hidden;pointer-events:none;";
01000|    document.body.appendChild(host);
01001|
01002|    let serverSaved = 0;
01003|    try {
01004|      for (let i = 0; i < configs.length; i++) {
01005|        const cfg = configs[i];
01006|        const series = buildExportIncomeSeries(source.periods, cfg.uneCodes);
01007|        if (!series.labels.length) {
01008|          throw new Error("Serie vacía para " + cfg.title);
01009|        }
01010|
01011|        const gd = document.createElement("div");
01012|        gd.style.width = IMAGE_WIDTH + "px";
01013|        gd.style.height = IMAGE_HEIGHT + "px";
01014|        host.appendChild(gd);
01015|
01016|        await Plotly.newPlot(
01017|          gd,
01018|          buildExportIncomeTraces(series),
01019|          buildExportIncomeLayout(cfg.title, series, source.yAxis),
01020|          {
01021|            staticPlot: true,
01022|            displaylogo: false,
01023|            displayModeBar: false,
01024|            responsive: false,
01025|          }
01026|        );
01027|
01028|        const dataUrlPng = await Plotly.toImage(gd, {
01029|          format: "png",
01030|          width: IMAGE_WIDTH,
01031|          height: IMAGE_HEIGHT,
01032|        });
01033|        const filename = "wcg-g" + cfg.fileIndex + " " + stamp + ".png";
01034|        downloadDataUrl(dataUrlPng, filename);
01035|        await uploadExportPngToServer(dataUrlPng, filename);
01036|        serverSaved += 1;
01037|
01038|        Plotly.purge(gd);
01039|        gd.remove();
01040|        await sleep(250);
01041|      }
01042|      btnExport.textContent = "Listo (" + serverSaved + " en TV)";
01043|      await sleep(1200);
01044|    } catch (err) {
01045|      console.error(err);
01046|      alert((err && err.message) || "Error al generar la exportación de 4 charts PNG.");
01047|    } finally {
01048|      try {
01049|        host.querySelectorAll("div").forEach(function (el) {
01050|          try { Plotly.purge(el); } catch (e) {}
01051|        });
01052|      } catch (e) {}
01053|      host.remove();
01054|      btnExport.disabled = false;
01055|      btnExport.textContent = originalText;
01056|    }
01057|  }
01058|
01059|  const btnFourCharts = document.getElementById("btn-export-4-charts-svg");
01060|  if (btnFourCharts) {
01061|    btnFourCharts.setAttribute("data-export-svg-version", EXPORT_SVG_VERSION);
01062|    btnFourCharts.addEventListener("click", function () {
01063|      exportFourIncomeChartsSvg();
01064|    });
01065|  }
01066|
01067|  // --- Generar reportes (modal) ---
01068|  (function initReportModal() {
01069|    const btn = document.getElementById("btn-generar-reportes");
01070|    const modal = document.getElementById("reportes-modal");
01071|    if (!btn || !modal) return;
01072|
01073|    const closeBtns = modal.querySelectorAll("[data-reportes-close]");
01074|    const form = document.getElementById("reportes-form");
01075|    const statusEl = document.getElementById("reportes-status");
01076|    const errEl = document.getElementById("reportes-error");
01077|    const generateBtn = document.getElementById("reportes-generate");
01078|    const csrfInput = document.querySelector("#btn-export-4-charts-svg")
01079|      ? document.querySelector('input[name="csrfmiddlewaretoken"]')
01080|      : document.querySelector('input[name="csrfmiddlewaretoken"]');
01081|
01082|    function openModal() {
01083|      errEl.textContent = "";
01084|      statusEl.textContent = "";
01085|      modal.style.display = "flex";
01086|      fetch("{% url 'reports:defaults' %}", { credentials: "same-origin" })
01087|        .then(function (r) { return r.json(); })
01088|        .then(function (data) {
01089|          if (!data || !data.defaults) return;
01090|          Object.keys(data.defaults).forEach(function (key) {
01091|            const input = form.querySelector('input[name="areas"][value="' + key + '"]');
01092|            if (input) input.checked = !!data.defaults[key];
01093|          });
01094|        })
01095|        .catch(function () {});
01096|    }
01097|
01098|    function closeModal() {
01099|      modal.style.display = "none";
01100|      generateBtn.disabled = false;
01101|      generateBtn.textContent = "Generar";
01102|    }
01103|
01104|    btn.addEventListener("click", openModal);
01105|    closeBtns.forEach(function (el) {
01106|      el.addEventListener("click", closeModal);
01107|    });
01108|    modal.addEventListener("click", function (ev) {
01109|      if (ev.target === modal) closeModal();
01110|    });
01111|
01112|    form.addEventListener("submit", async function (ev) {
01113|      ev.preventDefault();
01114|      errEl.textContent = "";
01115|      const checked = Array.from(form.querySelectorAll('input[name="areas"]:checked')).map(function (i) {
01116|        return i.value;
01117|      });
01118|      if (!checked.length) {
01119|        errEl.textContent = "Seleccione al menos un área: Administración, PGC, PGO o B. Riesgo.";
01120|        return;
01121|      }
01122|      generateBtn.disabled = true;
01123|      generateBtn.textContent = "Generando...";
01124|      statusEl.textContent = "Generando reportes…";
01125|
01126|      const csrf = (csrfInput && csrfInput.value) ||
01127|        (document.cookie.match(/csrftoken=([^;]+)/) || [])[1] || "";
01128|
01129|      try {
01130|        const resp = await fetch("{% url 'reports:generate' %}", {
01131|          method: "POST",
01132|          credentials: "same-origin",
01133|          headers: {
01134|            "Content-Type": "application/json",
01135|            "X-CSRFToken": csrf
01136|          },
01137|          body: JSON.stringify({ areas: checked })
01138|        });
01139|        if (!resp.ok) {
01140|          let msg = "No se pudieron generar los reportes.";
01141|          try {
01142|            const j = await resp.json();
01143|            if (j && j.error) msg = j.error;
01144|          } catch (e) {}
01145|          throw new Error(msg);
01146|        }
01147|        const blob = await resp.blob();
01148|        let filename = resp.headers.get("X-Report-Filename") || "reportes_wcg.zip";
01149|        const cd = resp.headers.get("Content-Disposition") || "";
01150|        const m = cd.match(/filename=\"([^\"]+)\"/);
01151|        if (m) filename = m[1];
01152|        const url = URL.createObjectURL(blob);
01153|        const a = document.createElement("a");
01154|        a.href = url;
01155|        a.download = filename;
01156|        document.body.appendChild(a);
01157|        a.click();
01158|        a.remove();
01159|        URL.revokeObjectURL(url);
01160|        statusEl.textContent = "Descarga iniciada: " + filename;
01161|        generateBtn.textContent = "Generar";
01162|        generateBtn.disabled = false;
01163|      } catch (err) {
01164|        errEl.textContent = (err && err.message) || "Error al generar.";
01165|        statusEl.textContent = "";
01166|        generateBtn.disabled = false;
01167|        generateBtn.textContent = "Generar";
01168|      }
01169|    });
01170|  })();
01171|
01172|});
01173|</script>
01174|
01175|<div id="reportes-modal" style="display:none; position:fixed; inset:0; z-index:9999; background:rgba(15,23,42,0.45); align-items:center; justify-content:center; padding:16px;">
01176|  <div style="background:#fff; border-radius:12px; max-width:420px; width:100%; box-shadow:0 20px 50px rgba(0,0,0,0.25); padding:22px 24px; border:1px solid #d9e2ec;">
01177|    <h3 style="margin:0 0 6px; color:#0f3d56;">Generar reportes</h3>
01178|    <p class="muted" style="margin:0 0 14px; font-size:0.9rem;">Seleccione una o varias áreas. Se descargará .md (+ .xlsx en resultados) o un .zip si hay varios archivos.</p>
01179|    <form id="reportes-form">
01180|      <label style="display:flex; gap:10px; align-items:center; margin:8px 0; font-weight:600;">
01181|        <input type="checkbox" name="areas" value="admin"> Administración
01182|      </label>
01183|      <label style="display:flex; gap:10px; align-items:center; margin:8px 0; font-weight:600;">
01184|        <input type="checkbox" name="areas" value="pgc" checked> PGC
01185|      </label>
01186|      <label style="display:flex; gap:10px; align-items:center; margin:8px 0; font-weight:600;">
01187|        <input type="checkbox" name="areas" value="pgo"> PGO
01188|      </label>
01189|      <label style="display:flex; gap:10px; align-items:center; margin:8px 0; font-weight:600;">
01190|        <input type="checkbox" name="areas" value="risk"> B. Riesgo
01191|      </label>
01192|      <p id="reportes-error" style="color:#b91c1c; font-size:0.88rem; min-height:1.2em; margin:10px 0 0;"></p>
01193|      <p id="reportes-status" class="muted" style="font-size:0.88rem; min-height:1.2em; margin:4px 0 12px;"></p>
01194|      <div style="display:flex; gap:10px; justify-content:flex-end;">
01195|        <button type="button" data-reportes-close style="padding:8px 14px; border-radius:8px; border:1px solid #94a3b8; background:#f1f5f9; color:#0f172a; cursor:pointer; font-weight:600;">Cancelar</button>
01196|        <button type="submit" id="reportes-generate" style="padding:8px 14px; border-radius:8px; border:none; background:#0f766e; color:#fff; cursor:pointer; font-weight:600;">Generar</button>
01197|      </div>
01198|    </form>
01199|  </div>
01200|</div>
01201|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZS5odG1sIiAlfQoKeyUgYmxvY2sgdGl0bGUgJX1UYWJsZXJvIHByaW5jaXBhbCBQR0N7JSBlbmRibG9jayAlfQoKeyUgYmxvY2sgY29udGVudCAlfQo8c3R5bGU+CiAgLmdyb3VwX3NlcGFyYXRvciB0ZCB7CiAgICBwYWRkaW5nOiAwOwogICAgaGVpZ2h0OiAxNHB4OwogICAgYm9yZGVyLWJvdHRvbTogbm9uZTsKICAgIGJhY2tncm91bmQ6ICNmZmZmZmY7CiAgfQoKICAvKgogICAgQ2xhc2lmaWNhIFPDrSAvIE5vIOKAlCBlbGVnYW50ZSB5IGxlZ2libGUgKGRhbHRvbmlzbW86IGZyw61vIHZzIGPDoWxpZG8gKyBmb3JtYSkuCiAgICBTw60gID0gdmVyZGUgc3VhdmUgbcOhcyBwcmVzZW50ZSArIHRpcG9ncmFmw61hIGNhc2kgbmVncmEgKyBzZW1pYm9sZCArIHNlbGxvLgogICAgTm8gID0gcm9zYSBtdXkgcMOhbGlkbyAobWF5b3LDrWEpICsgZ3JpcyBvc2N1cm8sIHNpbiBncml0YXIuCiAgKi8KICB0YWJsZS5wZ2Mtc2NvcmVib2FyZCB0Ym9keSB0ci5yb3ctY2xhc2lmaWNhLW5vIHRkIHsKICAgIGJhY2tncm91bmQ6ICNmYWY2ZjQ7CiAgICBjb2xvcjogIzRhNTM1YzsKICAgIGZvbnQtd2VpZ2h0OiA0MDA7CiAgfQogIHRhYmxlLnBnYy1zY29yZWJvYXJkIHRib2R5IHRyLnJvdy1jbGFzaWZpY2Etbm8gdGQ6Zmlyc3QtY2hpbGQgewogICAgYm94LXNoYWRvdzogaW5zZXQgM3B4IDAgMCAjZThkNWNlOwogIH0KICB0YWJsZS5wZ2Mtc2NvcmVib2FyZCB0Ym9keSB0ci5yb3ctY2xhc2lmaWNhLW5vOmhvdmVyIHRkIHsKICAgIGJhY2tncm91bmQ6ICNmNWVmZWM7CiAgfQogIHRhYmxlLnBnYy1zY29yZWJvYXJkIHRib2R5IHRyLnJvdy1jbGFzaWZpY2Etbm8gLmNsYXNpZmljYS1waWxsIHsKICAgIGNvbG9yOiAjNmI3MjgwOwogICAgZm9udC13ZWlnaHQ6IDUwMDsKICAgIGxldHRlci1zcGFjaW5nOiAwLjAyZW07CiAgfQoKICB0YWJsZS5wZ2Mtc2NvcmVib2FyZCB0Ym9keSB0ci5yb3ctY2xhc2lmaWNhLXNpIHRkIHsKICAgIGJhY2tncm91bmQ6ICNkM2ViZTA7CiAgICBjb2xvcjogIzBjMTIxMDsKICAgIGZvbnQtd2VpZ2h0OiA2MDA7CiAgICBsZXR0ZXItc3BhY2luZzogMC4wMWVtOwogIH0KICB0YWJsZS5wZ2Mtc2NvcmVib2FyZCB0Ym9keSB0ci5yb3ctY2xhc2lmaWNhLXNpIHRkOmZpcnN0LWNoaWxkIHsKICAgIGJveC1zaGFkb3c6IGluc2V0IDVweCAwIDAgIzJmNmY1NTsKICB9CiAgdGFibGUucGdjLXNjb3JlYm9hcmQgdGJvZHkgdHIucm93LWNsYXNpZmljYS1zaTpob3ZlciB0ZCB7CiAgICBiYWNrZ3JvdW5kOiAjYzVlNGQ0OwogIH0KICAvKiBUb3RhbCB1biBwb2NvIG3DoXMgbWFyY2FkbyBlbiBTw60gKGZvcm1hIHRpcG9ncsOhZmljYSwgc2luIGJvbGQgNzAwKSAqLwogIHRhYmxlLnBnYy1zY29yZWJvYXJkIHRib2R5IHRyLnJvdy1jbGFzaWZpY2Etc2kgdGQgc3Ryb25nIHsKICAgIGZvbnQtd2VpZ2h0OiA2MDA7CiAgICBjb2xvcjogIzA2MTAwYzsKICB9CiAgdGFibGUucGdjLXNjb3JlYm9hcmQgdGJvZHkgdHIucm93LWNsYXNpZmljYS1ubyB0ZCBzdHJvbmcgewogICAgZm9udC13ZWlnaHQ6IDUwMDsKICAgIGNvbG9yOiAjNGE1MzVjOwogIH0KCiAgdGFibGUucGdjLXNjb3JlYm9hcmQgLmNsYXNpZmljYS1waWxsIHsKICAgIGRpc3BsYXk6IGlubGluZS1mbGV4OwogICAgYWxpZ24taXRlbXM6IGNlbnRlcjsKICAgIGdhcDogMC4yOHJlbTsKICAgIHBhZGRpbmc6IDAuMThyZW0gMC41NXJlbTsKICAgIGJvcmRlci1yYWRpdXM6IDk5OXB4OwogICAgZm9udC1zaXplOiAwLjgycmVtOwogICAgbGluZS1oZWlnaHQ6IDEuMjsKICAgIGJvcmRlcjogMXB4IHNvbGlkIHRyYW5zcGFyZW50OwogIH0KICB0YWJsZS5wZ2Mtc2NvcmVib2FyZCB0Ym9keSB0ci5yb3ctY2xhc2lmaWNhLXNpIC5jbGFzaWZpY2EtcGlsbCB7CiAgICBiYWNrZ3JvdW5kOiByZ2JhKDI1NSwgMjU1LCAyNTUsIDAuNTUpOwogICAgYm9yZGVyLWNvbG9yOiByZ2JhKDQ3LCAxMTEsIDg1LCAwLjM1KTsKICAgIGNvbG9yOiAjMDYxMDBjOwogICAgZm9udC13ZWlnaHQ6IDYwMDsKICAgIGJveC1zaGFkb3c6IDAgMXB4IDAgcmdiYSgyNTUsIDI1NSwgMjU1LCAwLjcpOwogIH0KICB0YWJsZS5wZ2Mtc2NvcmVib2FyZCB0Ym9keSB0ci5yb3ctY2xhc2lmaWNhLXNpIC5jbGFzaWZpY2EtcGlsbC5vayB7CiAgICBjb2xvcjogIzA2MTAwYzsKICAgIGZvbnQtd2VpZ2h0OiA2MDA7CiAgfQogIHRhYmxlLnBnYy1zY29yZWJvYXJkIHRib2R5IHRyLnJvdy1jbGFzaWZpY2Etbm8gLmNsYXNpZmljYS1waWxsLmJhZCB7CiAgICBjb2xvcjogIzZiNzI4MDsKICAgIGZvbnQtd2VpZ2h0OiA1MDA7CiAgfQogIHRhYmxlLnBnYy1zY29yZWJvYXJkIHRib2R5IHRyLnJvdy1jbGFzaWZpY2Etc2kgLmNsYXNpZmljYS1tYXJrIHsKICAgIGZvbnQtc2l6ZTogMC43MnJlbTsKICAgIG9wYWNpdHk6IDAuOTsKICB9Cjwvc3R5bGU+CjxkaXYgY2xhc3M9ImNhcmQiPgogICAgPGRpdiBjbGFzcz0id2NnLXJlcG9ydC1oZWFkIiBzdHlsZT0ibWFyZ2luLXRvcDowOyI+CiAgICAgIDxoMiBzdHlsZT0ibWFyZ2luOjA7Ij5UYWJsZXJvIHByaW5jaXBhbCBkZSBwdW50b3Mg4oCUIHt7IHNlbGVjdGVkX21vZGVfbGFiZWx8ZGVmYXVsdDpzZWxlY3RlZF9tb2RlIH19PC9oMj4KICAgICAgeyUgaW5jbHVkZSAiaW5jbHVkZXMvbW9kdWxlX21hcmsuaHRtbCIgd2l0aCBtb2R1bGU9InBnYyIgJX0KICAgIDwvZGl2PgogIAogICAgPHAgY2xhc3M9Im11dGVkIj4KICAgICAgICBSZXN1bWVuIG1lbnN1YWwgZGUgcHVudG9zIHBvciBVTkUgeSBwZXJpb2RvLgogICAgPC9wPgoKICAgIDxmb3JtIG1ldGhvZD0iZ2V0IiBjbGFzcz0iZmlsdGVycyI+CiAgICAgICAgPGRpdj4KICAgICAgICAgICAgPGxhYmVsIGZvcj0ic3RhcnRfcGVyaW9kIj5EZXNkZTwvbGFiZWw+PGJyPgogICAgICAgICAgICA8c2VsZWN0IGlkPSJzdGFydF9wZXJpb2QiPgogICAgICAgICAgICAgICAgeyUgZm9yIHAgaW4gYXZhaWxhYmxlX3BlcmlvZHMgJX0KICAgICAgICAgICAgICAgICAgICA8b3B0aW9uCiAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlPSJ7eyBwLnllYXIgfX0te3sgcC5tb250aHxzdHJpbmdmb3JtYXQ6JzAyZCcgfX0iCiAgICAgICAgICAgICAgICAgICAgICAgIGRhdGEteWVhcj0ie3sgcC55ZWFyIH19IgogICAgICAgICAgICAgICAgICAgICAgICBkYXRhLW1vbnRoPSJ7eyBwLm1vbnRoIH19IgogICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiByZXBvcnRfZmlsdGVyLnN0YXJ0X3llYXIgPT0gcC55ZWFyIGFuZCByZXBvcnRfZmlsdGVyLnN0YXJ0X21vbnRoID09IHAubW9udGggJX1zZWxlY3RlZHslIGVuZGlmICV9CiAgICAgICAgICAgICAgICAgICAgPgogICAgICAgICAgICAgICAgICAgICAgICB7eyBwLnllYXIgfX0te3sgcC5tb250aHxzdHJpbmdmb3JtYXQ6IjAyZCIgfX0KICAgICAgICAgICAgICAgICAgICA8L29wdGlvbj4KICAgICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICA8L3NlbGVjdD4KICAgICAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ic3RhcnRfeWVhciIgaWQ9InN0YXJ0X3llYXIiIHZhbHVlPSJ7eyByZXBvcnRfZmlsdGVyLnN0YXJ0X3llYXIgfX0iPgogICAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJzdGFydF9tb250aCIgaWQ9InN0YXJ0X21vbnRoIiB2YWx1ZT0ie3sgcmVwb3J0X2ZpbHRlci5zdGFydF9tb250aCB9fSI+CiAgICAgICAgPC9kaXY+CgogICAgICAgIDxkaXY+CiAgICAgICAgICAgIDxsYWJlbCBmb3I9Im1vbnRoX2NvdW50Ij5NZXNlcyBpbmNsdWlkb3M8L2xhYmVsPjxicj4KICAgICAgICAgICAgPHNlbGVjdCBuYW1lPSJtb250aF9jb3VudCIgaWQ9Im1vbnRoX2NvdW50Ij4KICAgICAgICAgICAgICAgIHslIGZvciBuIGluIG1vbnRoX2NvdW50X29wdGlvbnMgJX0KICAgICAgICAgICAgICAgICAgICA8b3B0aW9uIHZhbHVlPSJ7eyBuIH19IiB7JSBpZiByZXBvcnRfZmlsdGVyLm1vbnRoX2NvdW50ID09IG4gJX1zZWxlY3RlZHslIGVuZGlmICV9PgogICAgICAgICAgICAgICAgICAgICAgICB7eyBuIH19CiAgICAgICAgICAgICAgICAgICAgPC9vcHRpb24+CiAgICAgICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgICAgPC9zZWxlY3Q+CiAgICAgICAgPC9kaXY+CgogICAgICAgIDxkaXY+CiAgICAgICAgICAgIDxsYWJlbCBmb3I9Im1vZGUiPk1vZGFsaWRhZDwvbGFiZWw+PGJyPgogICAgICAgICAgICA8c2VsZWN0IG5hbWU9Im1vZGUiIGlkPSJtb2RlIj4KICAgICAgICAgICAgICAgIHslIGZvciB2YWx1ZSwgbGFiZWwgaW4gbW9kZV9jaG9pY2VzICV9CiAgICAgICAgICAgICAgICAgICAgPG9wdGlvbiB2YWx1ZT0ie3sgdmFsdWUgfX0iIHslIGlmIHNlbGVjdGVkX21vZGUgPT0gdmFsdWUgJX1zZWxlY3RlZHslIGVuZGlmICV9PgogICAgICAgICAgICAgICAgICAgICAgICB7eyBsYWJlbCB9fQogICAgICAgICAgICAgICAgICAgIDwvb3B0aW9uPgogICAgICAgICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgICAgIDwvc2VsZWN0PgogICAgICAgIDwvZGl2PgogICAgICAKICAgICAgICA8ZGl2PgogICAgICAgICAgPGxhYmVsIGZvcj0ic29ydCI+U29ydDwvbGFiZWw+PGJyPgogICAgICAgICAgPHNlbGVjdCBpZD0ic29ydCI+CiAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9InVuZXMiCiAgICAgICAgICAgICAgeyUgaWYgcmVwb3J0X3NvcnQuZ3JvdXBfbW9kZSA9PSAidW5lIiAlfXNlbGVjdGVkeyUgZW5kaWYgJX0+CiAgICAgICAgICAgICAgVU5FcwogICAgICAgICAgICA8L29wdGlvbj4KICAgICAgICAgICAgPG9wdGlvbiB2YWx1ZT0iZmVjaGFzX2FzYyIKICAgICAgICAgICAgICB7JSBpZiByZXBvcnRfc29ydC5ncm91cF9tb2RlID09ICJwZXJpb2QiIGFuZCByZXBvcnRfc29ydC5kYXRlX29yZGVyID09ICJhc2MiICV9c2VsZWN0ZWR7JSBlbmRpZiAlfT4KICAgICAgICAgICAgICBGZWNoYXMgYXNjZW5kZW50ZXMKICAgICAgICAgICAgPC9vcHRpb24+CiAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9ImZlY2hhc19kZXNjIgogICAgICAgICAgICAgIHslIGlmIHJlcG9ydF9zb3J0Lmdyb3VwX21vZGUgPT0gInBlcmlvZCIgYW5kIHJlcG9ydF9zb3J0LmRhdGVfb3JkZXIgPT0gImRlc2MiICV9c2VsZWN0ZWR7JSBlbmRpZiAlfT4KICAgICAgICAgICAgICBGZWNoYXMgZGVzY2VuZGVudGVzCiAgICAgICAgICAgIDwvb3B0aW9uPgogICAgICAgICAgPC9zZWxlY3Q+CiAgICAgICAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJkYXRlX29yZGVyIiBpZD0iZGF0ZV9vcmRlciIKICAgICAgICAgICAgICAgICB2YWx1ZT0ieyUgaWYgcmVwb3J0X3NvcnQuZ3JvdXBfbW9kZSA9PSAncGVyaW9kJyBhbmQgcmVwb3J0X3NvcnQuZGF0ZV9vcmRlciA9PSAnZGVzYycgJX1kZXNjeyUgZWxzZSAlfWFzY3slIGVuZGlmICV9Ij4KICAgICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9Imdyb3VwX21vZGUiIGlkPSJncm91cF9tb2RlIgogICAgICAgICAgICAgICAgIHZhbHVlPSJ7JSBpZiByZXBvcnRfc29ydC5ncm91cF9tb2RlID09ICdwZXJpb2QnICV9cGVyaW9keyUgZWxzZSAlfXVuZXslIGVuZGlmICV9Ij4KICAgICAgICA8L2Rpdj4KICAgICAgCiAgICAgICAgPGRpdiBzdHlsZT0iYWxpZ24tc2VsZjplbmQ7Ij4KICAgICAgICAgICAgPGJ1dHRvbiB0eXBlPSJidXR0b24iIGlkPSJidG4tZXhwb3J0LW1kIj4ubWQgZXhwb3J0PC9idXR0b24+CiAgICAgICAgPC9kaXY+CiAgICAgICAgPGRpdiBzdHlsZT0iYWxpZ24tc2VsZjplbmQ7Ij4KICAgICAgICAgICAgPGJ1dHRvbiB0eXBlPSJidXR0b24iIGlkPSJidG4tZXhwb3J0LTQtY2hhcnRzLXN2ZyI+RXhwb3J0YWNpw7NuIDQgY2hhcnRzPC9idXR0b24+CiAgICAgICAgICAgIHslIGNzcmZfdG9rZW4gJX0KICAgICAgICA8L2Rpdj4KICAgIDwvZm9ybT4KCiAgICA8dGFibGUgY2xhc3M9InBnYy1zY29yZWJvYXJkIj4KICAgICAgICA8dGhlYWQ+CiAgICAgICAgICAgIDx0cj4KICAgICAgICAgICAgICAgIDx0aD5VTkU8L3RoPgogICAgICAgICAgICAgICAgPHRoPlBlcmlvZG88L3RoPgogICAgICAgICAgICAgICAgPHRoPkluZ3Jlc29zPC90aD4KICAgICAgICAgICAgICAgIDx0aD5DbGllbnRlcyBudWV2b3M8L3RoPgogICAgICAgICAgICAgICAgPHRoPlZlbnRhIGNydXphZGE8L3RoPgogICAgICAgICAgICAgICAgPHRoPlJlc3B1ZXN0YSByZXFzPC90aD4KICAgICAgICAgICAgICAgIDx0aD5Ub3RhbDwvdGg+CiAgICAgICAgICAgICAgICA8dGg+Q2xhc2lmaWNhPC90aD4KICAgICAgICAgICAgPC90cj4KICAgICAgICA8L3RoZWFkPgogICAgICAgIDx0Ym9keT4KICAgICAgICAgIHslIGZvciByb3cgaW4gcm93cyAlfQogICAgICAgICAgICB7JSBpZiByb3cuaXNfc2VwYXJhdG9yICV9CiAgICAgICAgICAgICAgPHRyIGNsYXNzPSJncm91cF9zZXBhcmF0b3IiPgogICAgICAgICAgICAgICAgPHRkIGNvbHNwYW49IjgiPjwvdGQ+CiAgICAgICAgICAgICAgPC90cj4KICAgICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgICAgIDx0ciBjbGFzcz0ieyUgaWYgcm93LnNjb3JlY2FyZC5pc19tb250aF9xdWFsaWZpZWQgJX1yb3ctY2xhc2lmaWNhLXNpeyUgZWxzZSAlfXJvdy1jbGFzaWZpY2Etbm97JSBlbmRpZiAlfSI+CiAgICAgICAgICAgICAgICA8dGQ+e3sgcm93LnNjb3JlY2FyZC51bmUubmFtZV9lcyB9fTwvdGQ+CiAgICAgICAgICAgICAgICA8dGQ+e3sgcm93LnNjb3JlY2FyZC55ZWFyIH19LXt7IHJvdy5zY29yZWNhcmQubW9udGh8c3RyaW5nZm9ybWF0OiIwMmQiIH19PC90ZD4KICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgPHRkPnt7IHJvdy5wX2luZ3Jlc29zfGZsb2F0Zm9ybWF0OjEgfX08L3RkPgogICAgICAgICAgICAgICAgPHRkPnt7IHJvdy5wX2NsaWVudGVzfGZsb2F0Zm9ybWF0OjEgfX08L3RkPgogICAgICAgICAgICAgICAgPHRkPnt7IHJvdy5wX3ZlbnRhX2NydXphZGF8ZmxvYXRmb3JtYXQ6MCB9fTwvdGQ+CiAgICAgICAgICAgICAgICA8dGQ+e3sgcm93LnBfcmVzcHVlc3RhX3JlcXN8ZmxvYXRmb3JtYXQ6MCB9fTwvdGQ+CiAgICAgICAgICAgICAgICA8dGQ+PHN0cm9uZz57eyByb3cuc2NvcmVjYXJkLnRvdGFsX3BvaW50c3xmbG9hdGZvcm1hdDoxIH19PC9zdHJvbmc+PC90ZD4KCiAgICAgICAgICAgICAgICA8dGQ+CiAgICAgICAgICAgICAgICAgIHslIGlmIHJvdy5zY29yZWNhcmQuaXNfbW9udGhfcXVhbGlmaWVkICV9CiAgICAgICAgICAgICAgICAgICAgPHNwYW4gY2xhc3M9ImNsYXNpZmljYS1waWxsIG9rIj48c3BhbiBjbGFzcz0iY2xhc2lmaWNhLW1hcmsiIGFyaWEtaGlkZGVuPSJ0cnVlIj7inJM8L3NwYW4+IFPDrTwvc3Bhbj4KICAgICAgICAgICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJjbGFzaWZpY2EtcGlsbCBiYWQiPk5vPC9zcGFuPgogICAgICAgICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgICAgICAgPC90ZD4KICAgICAgICAgICAgICA8L3RyPgogICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgeyUgZW1wdHkgJX0KICAgICAgICAgICAgPHRyPgogICAgICAgICAgICAgIDx0ZCBjb2xzcGFuPSI4Ij5ObyBoYXkgc2NvcmVjYXJkcyBwYXJhIGxvcyBmaWx0cm9zIHNlbGVjY2lvbmFkb3MuPC90ZD4KICAgICAgICAgICAgPC90cj4KICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgIDwvdGJvZHk+CiAgICAgICAgICAKICAgIDwvdGFibGU+CjwvZGl2PgoKPGRpdiBjbGFzcz0iY2FyZCIgc3R5bGU9Im1hcmdpbi10b3A6MjRweDsiPgogIDxoMyBzdHlsZT0ibWFyZ2luLXRvcDowOyI+VGVuZGVuY2lhcyBjb21wYXJhdGl2YXM8L2gzPgogIDxwIGNsYXNzPSJtdXRlZCI+CiAgICBFc3RvcyBncsOhZmljb3MgdXNhbiBlbCBtaXNtbyByYW5nbyBkZSBwZXLDrW9kb3Mgc2VsZWNjaW9uYWRvIGVuIGVsIGZpbHRybyBzdXBlcmlvci4KICA8L3A+CgogIDxkaXYgY2xhc3M9ImZpbHRlcnMiIHN0eWxlPSJtYXJnaW4tYm90dG9tOjE2cHg7Ij4KICAgIDxkaXY+CiAgICAgIDxsYWJlbCBmb3I9ImNoYXJ0X3R5cGUiPlRpcG88L2xhYmVsPjxicj4KICAgICAgPHNlbGVjdCBpZD0iY2hhcnRfdHlwZSI+CiAgICAgICAgPG9wdGlvbiB2YWx1ZT0ibWl4ZWQiIHNlbGVjdGVkPk1peHRvPC9vcHRpb24+CiAgICAgICAgPG9wdGlvbiB2YWx1ZT0ibGluZSI+TMOtbmVhczwvb3B0aW9uPgogICAgICAgIDxvcHRpb24gdmFsdWU9ImJhciI+QmFycmFzPC9vcHRpb24+CiAgICAgIDwvc2VsZWN0PgogICAgPC9kaXY+CgogICAgPGRpdj4KICAgICAgPGxhYmVsIGZvcj0iY2hhcnRfYWNjdW11bGF0ZWQiPk1vZG88L2xhYmVsPjxicj4KICAgICAgPGxhYmVsIHN0eWxlPSJkaXNwbGF5OmlubGluZS1mbGV4OyBhbGlnbi1pdGVtczpjZW50ZXI7IGdhcDo4cHg7IG1hcmdpbi10b3A6NnB4OyI+CiAgICAgICAgPGlucHV0IHR5cGU9ImNoZWNrYm94IiBpZD0iY2hhcnRfYWNjdW11bGF0ZWQiPgogICAgICAgIEFjdW11bGFkbyBkZW50cm8gZGVsIHJhbmdvCiAgICAgIDwvbGFiZWw+CiAgICA8L2Rpdj4KCiAgICA8ZGl2IHN0eWxlPSJtaW4td2lkdGg6MzIwcHg7Ij4KICAgICAgPGxhYmVsPlVORXMgaW5jbHVpZGFzPC9sYWJlbD4KICAgICAgPGRpdiBpZD0iY2hhcnRfdW5lX2NoZWNrbGlzdCIgc3R5bGU9Im1hcmdpbi10b3A6OHB4OyBkaXNwbGF5OmZsZXg7IGZsZXgtd3JhcDp3cmFwOyBnYXA6MTJweDsiPjwvZGl2PgogICAgPC9kaXY+CgogICAgPGRpdiBzdHlsZT0iYWxpZ24tc2VsZjplbmQ7Ij4KICAgICAgPGJ1dHRvbiB0eXBlPSJidXR0b24iIGlkPSJidG4tZ2VuZXJhci1yZXBvcnRlcyIgY2xhc3M9ImFkbS1idG4gYWRtLWJ0bi1wcmltYXJ5IiBzdHlsZT0icGFkZGluZzo5cHggMTVweDsgYm9yZGVyLXJhZGl1czo4cHg7IGZvbnQtd2VpZ2h0OjYwMDsgYmFja2dyb3VuZDojMGY3NjZlOyBjb2xvcjojZmZmOyBib3JkZXI6bm9uZTsgY3Vyc29yOnBvaW50ZXI7Ij4KICAgICAgICBHZW5lcmFyIHJlcG9ydGVzCiAgICAgIDwvYnV0dG9uPgogICAgPC9kaXY+CiAgPC9kaXY+CiAgCiAgPGRpdiBjbGFzcz0iY2FyZCIgc3R5bGU9Im1hcmdpbi10b3A6MTJweDsiPgogICAgPGg0IHN0eWxlPSJtYXJnaW4tdG9wOjA7IG1hcmdpbi1ib3R0b206NHB4OyI+SW5ncmVzb3MgYnJ1dG9zPC9oND4KICAgIDxwIGNsYXNzPSJtdXRlZCIgc3R5bGU9Im1hcmdpbi10b3A6MDsiPkNvbXBhcmFjacOzbiBkZSBjaWZyYXMgcmVhbGVzIHZzIG1ldGFzIHBvciBwZXLDrW9kby48L3A+CiAgICA8ZGl2IGlkPSJwbG90X2luZ3Jlc29zX2JydXRvcyIgc3R5bGU9IndpZHRoOjEwMCU7IGhlaWdodDo0MjBweDsiPjwvZGl2PgogIDwvZGl2PgoKICA8ZGl2IGNsYXNzPSJjYXJkIiBzdHlsZT0ibWFyZ2luLXRvcDoxNnB4OyI+CiAgICA8aDQgc3R5bGU9Im1hcmdpbi10b3A6MDsgbWFyZ2luLWJvdHRvbTo0cHg7Ij5DbGllbnRlcyBudWV2b3M8L2g0PgogICAgPHAgY2xhc3M9Im11dGVkIiBzdHlsZT0ibWFyZ2luLXRvcDowOyI+Q29tcGFyYWNpw7NuIGRlIGNpZnJhcyByZWFsZXMgdnMgbWV0YXMgcG9yIHBlcsOtb2RvLjwvcD4KICAgIDxkaXYgaWQ9InBsb3RfY2xpZW50ZXNfbnVldm9zIiBzdHlsZT0id2lkdGg6MTAwJTsgaGVpZ2h0OjQyMHB4OyI+PC9kaXY+CiAgPC9kaXY+CgogIDxkaXYgY2xhc3M9ImNhcmQiIHN0eWxlPSJtYXJnaW4tdG9wOjE2cHg7Ij4KICAgIDxoNCBzdHlsZT0ibWFyZ2luLXRvcDowOyBtYXJnaW4tYm90dG9tOjRweDsiPlZlbnRhIGNydXphZGE8L2g0PgogICAgPHAgY2xhc3M9Im11dGVkIiBzdHlsZT0ibWFyZ2luLXRvcDowOyI+Q29tcGFyYWNpw7NuIGRlIGNpZnJhcyByZWFsZXMgdnMgbWV0YXMgcG9yIHBlcsOtb2RvLjwvcD4KICAgIDxkaXYgaWQ9InBsb3RfdmVudGFfY3J1emFkYSIgc3R5bGU9IndpZHRoOjEwMCU7IGhlaWdodDo0MjBweDsiPjwvZGl2PgogIDwvZGl2Pgo8L2Rpdj4KCnt7IGNoYXJ0X3BheWxvYWRfanNvbnxqc29uX3NjcmlwdDoiY2hhcnQtcGF5bG9hZC1kYXRhIiB9fQoKPHNjcmlwdCBzcmM9Imh0dHBzOi8vY2RuLnBsb3QubHkvcGxvdGx5LTIuMzUuMi5taW4uanMiPjwvc2NyaXB0PgoKPHNjcmlwdD4KZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcigiRE9NQ29udGVudExvYWRlZCIsIGZ1bmN0aW9uICgpIHsKICAgIGNvbnN0IHN0YXJ0UGVyaW9kID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoInN0YXJ0X3BlcmlvZCIpOwogICAgY29uc3Qgc3RhcnRZZWFyID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoInN0YXJ0X3llYXIiKTsKICAgIGNvbnN0IHN0YXJ0TW9udGggPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgic3RhcnRfbW9udGgiKTsKICAgIGNvbnN0IHNvcnQgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgic29ydCIpOwogICAgY29uc3QgZGF0ZU9yZGVyID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImRhdGVfb3JkZXIiKTsKICAgIGNvbnN0IGdyb3VwTW9kZSA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJncm91cF9tb2RlIik7CiAgICBjb25zdCBidG4gPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuLWV4cG9ydC1tZCIpOwoKICAgIGZ1bmN0aW9uIHN5bmNQZXJpb2RGaWVsZHMoKSB7CiAgICAgICAgaWYgKCFzdGFydFBlcmlvZCkgcmV0dXJuOwogICAgICAgIGNvbnN0IG9wdGlvbiA9IHN0YXJ0UGVyaW9kLm9wdGlvbnNbc3RhcnRQZXJpb2Quc2VsZWN0ZWRJbmRleF07CiAgICAgICAgaWYgKCFvcHRpb24pIHJldHVybjsKICAgICAgICBzdGFydFllYXIudmFsdWUgPSBvcHRpb24uZGF0YXNldC55ZWFyIHx8ICIiOwogICAgICAgIHN0YXJ0TW9udGgudmFsdWUgPSBvcHRpb24uZGF0YXNldC5tb250aCB8fCAiIjsKICAgIH0KCiAgICBmdW5jdGlvbiBzeW5jU29ydEZpZWxkcygpIHsKICAgICAgICBpZiAoIXNvcnQpIHJldHVybjsKICAgICAgICBpZiAoc29ydC52YWx1ZSA9PT0gInVuZXMiKSB7CiAgICAgICAgICAgIGdyb3VwTW9kZS52YWx1ZSA9ICJ1bmUiOwogICAgICAgICAgICBkYXRlT3JkZXIudmFsdWUgPSAiYXNjIjsKICAgICAgICB9IGVsc2UgaWYgKHNvcnQudmFsdWUgPT09ICJmZWNoYXNfZGVzYyIpIHsKICAgICAgICAgICAgZ3JvdXBNb2RlLnZhbHVlID0gInBlcmlvZCI7CiAgICAgICAgICAgIGRhdGVPcmRlci52YWx1ZSA9ICJkZXNjIjsKICAgICAgICB9IGVsc2UgewogICAgICAgICAgICBncm91cE1vZGUudmFsdWUgPSAicGVyaW9kIjsKICAgICAgICAgICAgZGF0ZU9yZGVyLnZhbHVlID0gImFzYyI7CiAgICAgICAgfQogICAgfQoKCiAgICBjb25zdCBmaWx0ZXJGb3JtID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcigiZm9ybS5maWx0ZXJzIik7CiAgICBmdW5jdGlvbiBhcHBseUZpbHRlcnMoKSB7CiAgICAgICAgaWYgKHR5cGVvZiBzeW5jUGVyaW9kRmllbGRzID09PSAiZnVuY3Rpb24iKSBzeW5jUGVyaW9kRmllbGRzKCk7CiAgICAgICAgaWYgKHR5cGVvZiBzeW5jU29ydEZpZWxkcyA9PT0gImZ1bmN0aW9uIikgc3luY1NvcnRGaWVsZHMoKTsKICAgICAgICBpZiAoZmlsdGVyRm9ybSkgZmlsdGVyRm9ybS5zdWJtaXQoKTsKICAgIH0KCiAgICBpZiAoc3RhcnRQZXJpb2QpIHsKICAgICAgICBzdGFydFBlcmlvZC5hZGRFdmVudExpc3RlbmVyKCJjaGFuZ2UiLCBhcHBseUZpbHRlcnMpOwogICAgICAgIHN5bmNQZXJpb2RGaWVsZHMoKTsKICAgIH0KCiAgICBpZiAoc29ydCkgewogICAgICAgIHNvcnQuYWRkRXZlbnRMaXN0ZW5lcigiY2hhbmdlIiwgYXBwbHlGaWx0ZXJzKTsKICAgICAgICBzeW5jU29ydEZpZWxkcygpOwogICAgfQoKICAgIFsibW9udGhfY291bnQiLCAibW9kZSIsICJzdGFydF95ZWFyIiwgInN0YXJ0X21vbnRoIiwgInllYXIiLCAibW9udGgiLCAidW5lIl0uZm9yRWFjaChmdW5jdGlvbiAoaWQpIHsKICAgICAgICBjb25zdCBlbCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKGlkKTsKICAgICAgICBpZiAoZWwgJiYgZWwudGFnTmFtZSA9PT0gIlNFTEVDVCIpIHsKICAgICAgICAgICAgZWwuYWRkRXZlbnRMaXN0ZW5lcigiY2hhbmdlIiwgYXBwbHlGaWx0ZXJzKTsKICAgICAgICB9CiAgICB9KTsKCiAgICBpZiAoIWJ0bikgcmV0dXJuOwoKICAgIGJ0bi5hZGRFdmVudExpc3RlbmVyKCJjbGljayIsIGFzeW5jIGZ1bmN0aW9uICgpIHsKICAgICAgICBzeW5jUGVyaW9kRmllbGRzKCk7CiAgICAgICAgc3luY1NvcnRGaWVsZHMoKTsKCiAgICAgICAgY29uc3QgbW9kZSA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJtb2RlIik7CgogICAgICAgIGNvbnN0IHBhcmFtcyA9IG5ldyBVUkxTZWFyY2hQYXJhbXMoewogICAgICAgICAgICBzdGFydF95ZWFyOiBzdGFydFllYXIudmFsdWUgfHwgIiIsCiAgICAgICAgICAgIHN0YXJ0X21vbnRoOiBzdGFydE1vbnRoLnZhbHVlIHx8ICIiLAogICAgICAgICAgICBtb250aF9jb3VudDogZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoIm1vbnRoX2NvdW50Iik/LnZhbHVlIHx8ICIiLAogICAgICAgICAgICBkYXRlX29yZGVyOiBkYXRlT3JkZXIudmFsdWUgfHwgImFzYyIsCiAgICAgICAgICAgIGdyb3VwX21vZGU6IGdyb3VwTW9kZS52YWx1ZSB8fCAidW5lIiwKICAgICAgICAgICAgbW9kZTogbW9kZT8udmFsdWUgfHwgIm1vZG8xIgogICAgICAgIH0pOwoKICAgICAgICBjb25zdCB1cmwgPSBgeyUgdXJsICdwZ2M6ZGFzaGJvYXJkX2V4cG9ydF9tZCcgJX0/YCArIHBhcmFtcy50b1N0cmluZygpOwoKICAgICAgICBidG4uZGlzYWJsZWQgPSB0cnVlOwogICAgICAgIGNvbnN0IG9yaWdpbmFsVGV4dCA9IGJ0bi50ZXh0Q29udGVudDsKICAgICAgICBidG4udGV4dENvbnRlbnQgPSAiR2VuZXJhbmRvLi4uIjsKCiAgICAgICAgdHJ5IHsKICAgICAgICAgICAgY29uc3QgcmVzcG9uc2UgPSBhd2FpdCBmZXRjaCh1cmwsIHsKICAgICAgICAgICAgICAgIG1ldGhvZDogIkdFVCIsCiAgICAgICAgICAgICAgICBoZWFkZXJzOiB7CiAgICAgICAgICAgICAgICAgICAgIlgtUmVxdWVzdGVkLVdpdGgiOiAiWE1MSHR0cFJlcXVlc3QiCiAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgIH0pOwoKICAgICAgICAgICAgaWYgKCFyZXNwb25zZS5vaykgewogICAgICAgICAgICAgICAgdGhyb3cgbmV3IEVycm9yKCJObyBzZSBwdWRvIGdlbmVyYXIgZWwgYXJjaGl2byBNYXJrZG93bi4iKTsKICAgICAgICAgICAgfQoKICAgICAgICAgICAgY29uc3QgYmxvYiA9IGF3YWl0IHJlc3BvbnNlLmJsb2IoKTsKCiAgICAgICAgICAgIGxldCBmaWxlbmFtZSA9ICJwZ2MtdGFibGVyby1wcmluY2lwYWwubWQiOwogICAgICAgICAgICBjb25zdCBkaXNwb3NpdGlvbiA9IHJlc3BvbnNlLmhlYWRlcnMuZ2V0KCJDb250ZW50LURpc3Bvc2l0aW9uIik7CiAgICAgICAgICAgIGlmIChkaXNwb3NpdGlvbikgewogICAgICAgICAgICAgICAgY29uc3QgdXRmOE1hdGNoID0gZGlzcG9zaXRpb24ubWF0Y2goL2ZpbGVuYW1lXCo9VVRGLTgnJyhbXjtdKykvaSk7CiAgICAgICAgICAgICAgICBjb25zdCBhc2NpaU1hdGNoID0gZGlzcG9zaXRpb24ubWF0Y2goL2ZpbGVuYW1lPSIoW14iXSspIi9pKTsKCiAgICAgICAgICAgICAgICBpZiAodXRmOE1hdGNoICYmIHV0ZjhNYXRjaFsxXSkgewogICAgICAgICAgICAgICAgICAgIGZpbGVuYW1lID0gZGVjb2RlVVJJQ29tcG9uZW50KHV0ZjhNYXRjaFsxXSk7CiAgICAgICAgICAgICAgICB9IGVsc2UgaWYgKGFzY2lpTWF0Y2ggJiYgYXNjaWlNYXRjaFsxXSkgewogICAgICAgICAgICAgICAgICAgIGZpbGVuYW1lID0gYXNjaWlNYXRjaFsxXTsKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgfQoKICAgICAgICAgICAgY29uc3Qgb2JqZWN0VXJsID0gd2luZG93LlVSTC5jcmVhdGVPYmplY3RVUkwoYmxvYik7CiAgICAgICAgICAgIGNvbnN0IGEgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCJhIik7CiAgICAgICAgICAgIGEuaHJlZiA9IG9iamVjdFVybDsKICAgICAgICAgICAgYS5kb3dubG9hZCA9IGZpbGVuYW1lOwogICAgICAgICAgICBkb2N1bWVudC5ib2R5LmFwcGVuZENoaWxkKGEpOwogICAgICAgICAgICBhLmNsaWNrKCk7CiAgICAgICAgICAgIGEucmVtb3ZlKCk7CiAgICAgICAgICAgIHdpbmRvdy5VUkwucmV2b2tlT2JqZWN0VVJMKG9iamVjdFVybCk7CiAgICAgICAgfSBjYXRjaCAoZXJyb3IpIHsKICAgICAgICAgICAgYWxlcnQoZXJyb3IubWVzc2FnZSB8fCAiRXJyb3IgZ2VuZXJhbmRvIGxhIGV4cG9ydGFjacOzbi4iKTsKICAgICAgICB9IGZpbmFsbHkgewogICAgICAgICAgICBidG4uZGlzYWJsZWQgPSBmYWxzZTsKICAgICAgICAgICAgYnRuLnRleHRDb250ZW50ID0gb3JpZ2luYWxUZXh0OwogICAgICAgIH0KICAgIH0pOwp9KTsKPC9zY3JpcHQ+Cgo8c2NyaXB0PgogIGRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoIkRPTUNvbnRlbnRMb2FkZWQiLCBmdW5jdGlvbiAoKSB7CiAgY29uc3QgcGF5bG9hZE5vZGUgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiY2hhcnQtcGF5bG9hZC1kYXRhIik7CiAgaWYgKCFwYXlsb2FkTm9kZSkgcmV0dXJuOwogIAogIGxldCBjaGFydFBheWxvYWQgPSBKU09OLnBhcnNlKHBheWxvYWROb2RlLnRleHRDb250ZW50KTsKICBpZiAodHlwZW9mIGNoYXJ0UGF5bG9hZCA9PT0gInN0cmluZyIpIHsKICAgIGNoYXJ0UGF5bG9hZCA9IEpTT04ucGFyc2UoY2hhcnRQYXlsb2FkKTsKICB9CiAgCiAgaWYgKCFjaGFydFBheWxvYWQgfHwgIWNoYXJ0UGF5bG9hZC5tZXRyaWNzIHx8ICFjaGFydFBheWxvYWQudW5lcykgewogICAgY29uc29sZS5lcnJvcigiY2hhcnRQYXlsb2FkIGludsOhbGlkbzoiLCBjaGFydFBheWxvYWQpOwogICAgcmV0dXJuOwogIH0KICAKICBjb25zdCB0eXBlU2VsZWN0ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImNoYXJ0X3R5cGUiKTsKICBjb25zdCBhY2N1bXVsYXRlZENoZWNrYm94ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImNoYXJ0X2FjY3VtdWxhdGVkIik7CiAgY29uc3QgdW5lQ2hlY2tsaXN0ID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImNoYXJ0X3VuZV9jaGVja2xpc3QiKTsKCiAgY29uc3QgbWV0cmljT3JkZXIgPSBbCiAgICAiSU5HUkVTT1MiLAogICAgIkNMSUVOVEVTX05VRVZPUyIsCiAgICAiVkVOVEFfQ1JVWkFEQSIKICBdOwoKICBjb25zdCBwbG90TWFwID0gewogICAgIklOR1JFU09TIjogInBsb3RfaW5ncmVzb3NfYnJ1dG9zIiwKICAgICJDTElFTlRFU19OVUVWT1MiOiAicGxvdF9jbGllbnRlc19udWV2b3MiLAogICAgIlZFTlRBX0NSVVpBREEiOiAicGxvdF92ZW50YV9jcnV6YWRhIgogIH07CgogIGZ1bmN0aW9uIGJ1aWxkVW5lQ2hlY2tsaXN0KCkgewogICAgdW5lQ2hlY2tsaXN0LmlubmVySFRNTCA9ICIiOwogICAgY2hhcnRQYXlsb2FkLnVuZXMuZm9yRWFjaChmdW5jdGlvbiAodW5lKSB7CiAgICAgIGNvbnN0IGxhYmVsID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgibGFiZWwiKTsKICAgICAgbGFiZWwuc3R5bGUuZGlzcGxheSA9ICJpbmxpbmUtZmxleCI7CiAgICAgIGxhYmVsLnN0eWxlLmFsaWduSXRlbXMgPSAiY2VudGVyIjsKICAgICAgbGFiZWwuc3R5bGUuZ2FwID0gIjZweCI7CgogICAgICBjb25zdCBpbnB1dCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoImlucHV0Iik7CiAgICAgIGlucHV0LnR5cGUgPSAiY2hlY2tib3giOwogICAgICBpbnB1dC5uYW1lID0gImNoYXJ0X3VuZSI7CiAgICAgIGlucHV0LnZhbHVlID0gdW5lLmNvZGU7CiAgICAgIGlucHV0LmNoZWNrZWQgPSB0cnVlOwogICAgICBpbnB1dC5hZGRFdmVudExpc3RlbmVyKCJjaGFuZ2UiLCByZW5kZXJBbGxDaGFydHMpOwoKICAgICAgY29uc3QgdGV4dCA9IGRvY3VtZW50LmNyZWF0ZVRleHROb2RlKHVuZS5uYW1lX2VzKTsKCiAgICAgIGxhYmVsLmFwcGVuZENoaWxkKGlucHV0KTsKICAgICAgbGFiZWwuYXBwZW5kQ2hpbGQodGV4dCk7CiAgICAgIHVuZUNoZWNrbGlzdC5hcHBlbmRDaGlsZChsYWJlbCk7CiAgICB9KTsKICB9CgogIGZ1bmN0aW9uIGdldFNlbGVjdGVkVW5lQ29kZXMoKSB7CiAgICByZXR1cm4gQXJyYXkuZnJvbShkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKCdpbnB1dFtuYW1lPSJjaGFydF91bmUiXTpjaGVja2VkJykpCiAgICAgIC5tYXAoZnVuY3Rpb24gKGlucHV0KSB7IHJldHVybiBpbnB1dC52YWx1ZTsgfSk7CiAgfQoKICBmdW5jdGlvbiBhY2N1bXVsYXRlVmFsdWVzKHZhbHVlcykgewogICAgbGV0IHJ1bm5pbmcgPSAwOwogICAgcmV0dXJuIHZhbHVlcy5tYXAoZnVuY3Rpb24gKHZhbHVlKSB7CiAgICAgIGNvbnN0IHNhZmVWYWx1ZSA9IE51bWJlcih2YWx1ZSB8fCAwKTsKICAgICAgcnVubmluZyArPSBzYWZlVmFsdWU7CiAgICAgIHJldHVybiBydW5uaW5nOwogICAgfSk7CiAgfQoKICBmdW5jdGlvbiBidWlsZE1ldHJpY1NlcmllcyhtZXRyaWNDb2RlLCBzZWxlY3RlZFVuZUNvZGVzLCBhY2N1bXVsYXRlZCkgewogICAgY29uc3QgbWV0cmljID0gY2hhcnRQYXlsb2FkLm1ldHJpY3NbbWV0cmljQ29kZV07CiAgCiAgICBpZiAoIW1ldHJpYyB8fCAhbWV0cmljLnBlcmlvZHMpIHsKICAgICAgY29uc29sZS5lcnJvcigiTcOpdHJpY2EgZmFsdGFudGUgbyBpbnbDoWxpZGE6IiwgbWV0cmljQ29kZSwgY2hhcnRQYXlsb2FkKTsKICAgICAgcmV0dXJuIHsKICAgICAgICBsYWJlbHM6IFtdLAogICAgICAgIHJlYWxWYWx1ZXM6IFtdLAogICAgICAgIHRhcmdldFZhbHVlczogW10sCiAgICAgICAgbWV0YTogewogICAgICAgICAgdGl0bGU6IG1ldHJpY0NvZGUsCiAgICAgICAgICBzdWJ0aXRsZTogIlNpbiBkYXRvcyIsCiAgICAgICAgICB5X2F4aXM6ICJWYWxvciIKICAgICAgICB9CiAgICAgIH07CiAgICB9CiAgCiAgICBjb25zdCBsYWJlbHMgPSBbXTsKICAgIGNvbnN0IHJlYWxWYWx1ZXMgPSBbXTsKICAgIGNvbnN0IHRhcmdldFZhbHVlcyA9IFtdOwogIAogICAgbWV0cmljLnBlcmlvZHMuZm9yRWFjaChmdW5jdGlvbiAocGVyaW9kKSB7CiAgICAgIGxhYmVscy5wdXNoKHBlcmlvZC5sYWJlbCk7CiAgCiAgICAgIGxldCByZWFsU3VtID0gMDsKICAgICAgbGV0IHRhcmdldFN1bSA9IDA7CiAgCiAgICAgIHNlbGVjdGVkVW5lQ29kZXMuZm9yRWFjaChmdW5jdGlvbiAodW5lQ29kZSkgewogICAgICAgIGNvbnN0IGl0ZW0gPSBwZXJpb2QuYnlfdW5lPy5bdW5lQ29kZV07CiAgICAgICAgaWYgKGl0ZW0pIHsKICAgICAgICAgIHJlYWxTdW0gKz0gTnVtYmVyKGl0ZW0ucmVhbCB8fCAwKTsKICAgICAgICAgIHRhcmdldFN1bSArPSBOdW1iZXIoaXRlbS50YXJnZXQgfHwgMCk7CiAgICAgICAgfQogICAgICB9KTsKICAKICAgICAgcmVhbFZhbHVlcy5wdXNoKHJlYWxTdW0pOwogICAgICB0YXJnZXRWYWx1ZXMucHVzaCh0YXJnZXRTdW0pOwogICAgfSk7CiAgCiAgICByZXR1cm4gewogICAgICBsYWJlbHM6IGxhYmVscywKICAgICAgcmVhbFZhbHVlczogYWNjdW11bGF0ZWQgPyBhY2N1bXVsYXRlVmFsdWVzKHJlYWxWYWx1ZXMpIDogcmVhbFZhbHVlcywKICAgICAgdGFyZ2V0VmFsdWVzOiBhY2N1bXVsYXRlZCA/IGFjY3VtdWxhdGVWYWx1ZXModGFyZ2V0VmFsdWVzKSA6IHRhcmdldFZhbHVlcywKICAgICAgbWV0YTogbWV0cmljCiAgICB9OwogIH0KCiAgZnVuY3Rpb24gYnVpbGRUcmFjZXMobWV0cmljQ29kZSwgc2VsZWN0ZWRVbmVDb2RlcywgYWNjdW11bGF0ZWQsIGNoYXJ0VHlwZSkgewogICAgY29uc3Qgc2VyaWVzID0gYnVpbGRNZXRyaWNTZXJpZXMobWV0cmljQ29kZSwgc2VsZWN0ZWRVbmVDb2RlcywgYWNjdW11bGF0ZWQpOwoKICAgIGlmIChjaGFydFR5cGUgPT09ICJsaW5lIikgewogICAgICByZXR1cm4gWwogICAgICAgIHsKICAgICAgICAgIHg6IHNlcmllcy5sYWJlbHMsCiAgICAgICAgICB5OiBzZXJpZXMudGFyZ2V0VmFsdWVzLAogICAgICAgICAgdHlwZTogInNjYXR0ZXIiLAogICAgICAgICAgbW9kZTogImxpbmVzK21hcmtlcnMiLAogICAgICAgICAgbmFtZTogIk1ldGEiLAogICAgICAgICAgbGluZTogeyBjb2xvcjogIiM3ZjhjOGQiLCB3aWR0aDogMywgZGFzaDogImRhc2giIH0sCiAgICAgICAgICBtYXJrZXI6IHsgc2l6ZTogNyB9CiAgICAgICAgfSwKICAgICAgICB7CiAgICAgICAgICB4OiBzZXJpZXMubGFiZWxzLAogICAgICAgICAgeTogc2VyaWVzLnJlYWxWYWx1ZXMsCiAgICAgICAgICB0eXBlOiAic2NhdHRlciIsCiAgICAgICAgICBtb2RlOiAibGluZXMrbWFya2VycyIsCiAgICAgICAgICBuYW1lOiAiUmVhbCIsCiAgICAgICAgICBsaW5lOiB7IGNvbG9yOiAiIzFmNzdiNCIsIHdpZHRoOiAzIH0sCiAgICAgICAgICBtYXJrZXI6IHsgc2l6ZTogNyB9CiAgICAgICAgfQogICAgICBdOwogICAgfQoKICAgIGlmIChjaGFydFR5cGUgPT09ICJiYXIiKSB7CiAgICAgIHJldHVybiBbCiAgICAgICAgewogICAgICAgICAgeDogc2VyaWVzLmxhYmVscywKICAgICAgICAgIHk6IHNlcmllcy50YXJnZXRWYWx1ZXMsCiAgICAgICAgICB0eXBlOiAiYmFyIiwKICAgICAgICAgIG5hbWU6ICJNZXRhIiwKICAgICAgICAgIG1hcmtlcjogeyBjb2xvcjogIiNiMGI3YmYiIH0KICAgICAgICB9LAogICAgICAgIHsKICAgICAgICAgIHg6IHNlcmllcy5sYWJlbHMsCiAgICAgICAgICB5OiBzZXJpZXMucmVhbFZhbHVlcywKICAgICAgICAgIHR5cGU6ICJiYXIiLAogICAgICAgICAgbmFtZTogIlJlYWwiLAogICAgICAgICAgbWFya2VyOiB7IGNvbG9yOiAiIzFmNzdiNCIgfQogICAgICAgIH0KICAgICAgXTsKICAgIH0KCiAgICAKICAgIHJldHVybiBbCiAgICAgIHsKICAgICAgICB4OiBzZXJpZXMubGFiZWxzLAogICAgICAgIHk6IHNlcmllcy5yZWFsVmFsdWVzLAogICAgICAgIHR5cGU6ICJiYXIiLAogICAgICAgIG5hbWU6ICJSZWFsIiwKICAgICAgICBtYXJrZXI6IHsgY29sb3I6ICIjMWY3N2I0IiB9CiAgICAgIH0sCiAgICAgIHsKICAgICAgICB4OiBzZXJpZXMubGFiZWxzLAogICAgICAgIHk6IHNlcmllcy50YXJnZXRWYWx1ZXMsCiAgICAgICAgdHlwZTogInNjYXR0ZXIiLAogICAgICAgIG1vZGU6ICJsaW5lcyIsCiAgICAgICAgbmFtZTogIk1ldGEiLAogICAgICAgIGxpbmU6IHsgY29sb3I6ICIjN2Y4YzhkIiwgd2lkdGg6IDMsIGRhc2g6ICJkYXNoIiB9LAogICAgICAgIG1hcmtlcjogeyBzaXplOiA3IH0KICAgICAgfQogICAgXTsKICB9CgogICAgCiAgZnVuY3Rpb24gYnVpbGRMYXlvdXQobWV0cmljQ29kZSwgYWNjdW11bGF0ZWQpIHsKICAgIGNvbnN0IG1ldHJpYyA9IGNoYXJ0UGF5bG9hZC5tZXRyaWNzW21ldHJpY0NvZGVdOwogICAgY29uc3Qgc2VyaWVzID0gYnVpbGRNZXRyaWNTZXJpZXMobWV0cmljQ29kZSwgZ2V0U2VsZWN0ZWRVbmVDb2RlcygpLCBhY2N1bXVsYXRlZCk7CgogICAgY29uc3QgdGl0bGVUZXh0ID0gYWNjdW11bGF0ZWQKICAgICAgPyBgJHttZXRyaWMudGl0bGV9PGJyPjxzdXA+JHttZXRyaWMuc3VidGl0bGV9LiBNb2RvIGFjdW11bGFkbyBkZW50cm8gZGVsIHJhbmdvLjwvc3VwPmAKICAgICAgOiBgJHttZXRyaWMudGl0bGV9PGJyPjxzdXA+JHttZXRyaWMuc3VidGl0bGV9LiBNb2RvIG1lbnN1YWwuPC9zdXA+YDsKCiAgICByZXR1cm4gewogICAgICB0aXRsZTogewogICAgICAgIHRleHQ6IHRpdGxlVGV4dCwKICAgICAgICBmb250OiB7CiAgICAgICAgICBzaXplOiAyMCwKICAgICAgICAgIGNvbG9yOiAiIzE2NjUzNCIKICAgICAgICB9CiAgICAgIH0sCiAgICAgIGJhcm1vZGU6ICJncm91cCIsCiAgICAgIG1hcmdpbjogeyBsOiA2MCwgcjogMjQsIHQ6IDgwLCBiOiA4MCB9LAogICAgICBsZWdlbmQ6IHsKICAgICAgICBvcmllbnRhdGlvbjogImgiLAogICAgICAgIHlhbmNob3I6ICJ0b3AiLAogICAgICAgIHk6IC0wLjIsCiAgICAgICAgeGFuY2hvcjogImNlbnRlciIsCiAgICAgICAgeDogMC41CiAgICAgIH0sCiAgICAgIHhheGlzOiB7CiAgICAgICAgdGl0bGU6ICJQZXLDrW9kbyIsCiAgICAgICAgdHlwZTogImNhdGVnb3J5IiwKICAgICAgICBjYXRlZ29yeW9yZGVyOiAiYXJyYXkiLAogICAgICAgIGNhdGVnb3J5YXJyYXk6IHNlcmllcy5sYWJlbHMsCiAgICAgICAgdGlja21vZGU6ICJhcnJheSIsCiAgICAgICAgdGlja3ZhbHM6IHNlcmllcy5sYWJlbHMsCiAgICAgICAgdGlja3RleHQ6IHNlcmllcy5sYWJlbHMKICAgICAgfSwKICAgICAgeWF4aXM6IHsKICAgICAgICB0aXRsZTogbWV0cmljLnlfYXhpcywKICAgICAgICByYW5nZW1vZGU6ICJ0b3plcm8iCiAgICAgIH0sCiAgICAgIHBhcGVyX2JnY29sb3I6ICJ3aGl0ZSIsCiAgICAgIHBsb3RfYmdjb2xvcjogIndoaXRlIgogICAgfTsKICB9CgogIGZ1bmN0aW9uIHJlbmRlckNoYXJ0KG1ldHJpY0NvZGUpIHsKICAgIGNvbnN0IHNlbGVjdGVkVW5lQ29kZXMgPSBnZXRTZWxlY3RlZFVuZUNvZGVzKCk7CiAgICBjb25zdCBjaGFydFR5cGUgPSB0eXBlU2VsZWN0LnZhbHVlOwogICAgY29uc3QgYWNjdW11bGF0ZWQgPSBhY2N1bXVsYXRlZENoZWNrYm94LmNoZWNrZWQ7CgogICAgY29uc3QgdHJhY2VzID0gYnVpbGRUcmFjZXMobWV0cmljQ29kZSwgc2VsZWN0ZWRVbmVDb2RlcywgYWNjdW11bGF0ZWQsIGNoYXJ0VHlwZSk7CiAgICBjb25zdCBsYXlvdXQgPSBidWlsZExheW91dChtZXRyaWNDb2RlLCBhY2N1bXVsYXRlZCk7CgogICAgY29uc3QgY29uZmlnID0gewogICAgICByZXNwb25zaXZlOiB0cnVlLAogICAgICBkaXNwbGF5bG9nbzogZmFsc2UsCiAgICAgIC8vIEJsb3F1ZWEgdG9kYSBpbnRlcmFjY2nDs24gZGVsIHVzdWFyaW8KICAgICAgc3RhdGljUGxvdDogdHJ1ZSwgICAgICAgICAgLy8gRGVzYWN0aXZhIHpvb20sIHBhbiwgc2VsZWNjacOzbiwgZXRjLgogICAgICBzY3JvbGxab29tOiBmYWxzZSwKICAgICAgZG91YmxlQ2xpY2s6IGZhbHNlLAogICAgICBlZGl0YWJsZTogZmFsc2UsCiAgICAgIGRpc3BsYXlNb2RlQmFyOiBmYWxzZSAgICAgIC8vIE9jdWx0YSBiYXJyYSBkZSBoZXJyYW1pZW50YXMKICAgIH07CgogICAgUGxvdGx5LnJlYWN0KHBsb3RNYXBbbWV0cmljQ29kZV0sIHRyYWNlcywgbGF5b3V0LCBjb25maWcpOwogIH0KICAgIAogICAgCiAgZnVuY3Rpb24gcmVuZGVyQWxsQ2hhcnRzKCkgewogICAgY29uc3Qgc2VsZWN0ZWRVbmVDb2RlcyA9IGdldFNlbGVjdGVkVW5lQ29kZXMoKTsKICAgIGlmICghc2VsZWN0ZWRVbmVDb2Rlcy5sZW5ndGgpIHsKICAgICAgbWV0cmljT3JkZXIuZm9yRWFjaChmdW5jdGlvbiAobWV0cmljQ29kZSkgewogICAgICAgIFBsb3RseS5wdXJnZShwbG90TWFwW21ldHJpY0NvZGVdKTsKICAgICAgICBkb2N1bWVudC5nZXRFbGVtZW50QnlJZChwbG90TWFwW21ldHJpY0NvZGVdKS5pbm5lckhUTUwgPQogICAgICAgICAgJzxkaXYgY2xhc3M9Im11dGVkIiBzdHlsZT0icGFkZGluZzoyNHB4OyI+U2VsZWNjaW9uYSBhbCBtZW5vcyB1bmEgVU5FLjwvZGl2Pic7CiAgICAgIH0pOwogICAgICByZXR1cm47CiAgICB9CgogICAgbWV0cmljT3JkZXIuZm9yRWFjaChyZW5kZXJDaGFydCk7CiAgfQoKICBidWlsZFVuZUNoZWNrbGlzdCgpOwogIHR5cGVTZWxlY3QuYWRkRXZlbnRMaXN0ZW5lcigiY2hhbmdlIiwgcmVuZGVyQWxsQ2hhcnRzKTsKICBhY2N1bXVsYXRlZENoZWNrYm94LmFkZEV2ZW50TGlzdGVuZXIoImNoYW5nZSIsIHJlbmRlckFsbENoYXJ0cyk7CiAgcmVuZGVyQWxsQ2hhcnRzKCk7CgogIC8vIC0tLSBFeHBvcnRhY2nDs24gNCBjaGFydHM6IFBORyAxOTIww5cxMDgwIChUVikuIC0tLQogIC8vIEVYUE9SVF9TVkdfVkVSU0lPTj12MTYtbGVnZW5kLXlheGlzLW51ZGdlCiAgLy8gTm8gbW9kaWZpY2EgY2hhcnRzIHZpc2libGVzIChidWlsZExheW91dCAvIHJlbmRlckNoYXJ0KS4KICAvLyBMb3MgNCBjaGFydHMgKEZBQ1RPUklORywgTEVBU0lORywgSU5TVVJBTkNFLCBHUlVQTykgdXNhbiBlbCBNSVNNTyBsYXlvdXQuCiAgLy8KICAvLyBDb25maWd1cmFjacOzbiBiYXNlICh2MTEsIGFudGVzIGRlbCBlbnNheW8gZGUgZnVlbnRlcy9tw6FyZ2VuZXMgdjEyKToKICAvLyAgIE1BUkdJTiBUL0IvTC9SID0gMTU1IC8gMjc1IC8gMTAwIC8gODAKICAvLyAgIFRJVExFIC8gU1VCVElUTEUgLyBBWElTIC8gVElDSyAvIExFR0VORCA9IDcyIC8gMjIgLyAyNCAvIDIwIC8gMjQKICAvLyBTaSBlbCBlbnNheW8gcXVlZGEgbWFsLCByZXN0YXVyYXIgZXNvcyB2YWxvcmVzIHkgRVhQT1JUX1NWR19WRVJTSU9OPXYxMS1iYXJzLW5hdnktYmx1ZS1wbmcuCgogIGNvbnN0IEVYUE9SVF9TVkdfVkVSU0lPTiA9ICJ2MTYtbGVnZW5kLXlheGlzLW51ZGdlIjsKICBjb25zdCBFWFBPUlRfU1VCVElUTEUgPQogICAgIlJlYWwgdnMgbWV0YSBwb3IgcGVyw61vZG8uIENpZnJhcyBhY3VtdWxhZGFzIGRlbnRybyBkZWwgcmFuZ28uIjsKICBjb25zdCBFWFBPUlRfV0lEVEggPSAxOTIwOwogIGNvbnN0IEVYUE9SVF9IRUlHSFQgPSAxMDgwOwogIGNvbnN0IElNQUdFX1dJRFRIID0gMTkyMDsKICBjb25zdCBJTUFHRV9IRUlHSFQgPSAxMDgwOwogIC8vIHYxMjogZnJhbmphIGJsYW5jYSBzdXBlcmlvci9pbmZlcmlvciB+MTU1IOKGkiB+NzUgKG1pdGFkKS4KICAvLyBJbmZlcmlvcjogbWVzZXMvUGVyw61vZG8vbGV5ZW5kYSArIH43NSBweCBibGFuY29zIGxpYnJlcyAoYW50ZXMgfjE1NSkuCiAgY29uc3QgRVhQT1JUX01BUkdJTl9UID0gNzU7CiAgY29uc3QgRVhQT1JUX01BUkdJTl9CID0gMTk1OwogIC8vIHYxMzogbWFyZ2VuIEwgPSBiYXNlIDEwMCArIGFuY2hvIGRlIMKrNTAwwrsuCiAgLy8gdjE04oCTdjE2OiArM8OXIGFuY2hvIGRlIHVuIGTDrWdpdG8gKMKrMMK7KS4KICBjb25zdCBFWFBPUlRfTUFSR0lOX0xfQkFTRSA9IDEwMDsKICBjb25zdCBFWFBPUlRfTUFSR0lOX1IgPSA4MDsKICAvLyB2MTI6IHTDrXR1bG8gMi41w5c7IHJlc3RvIGRlIHRleHRvcyAyw5cgKGVuc2F5bykuCiAgY29uc3QgRVhQT1JUX1RJVExFX1NJWkUgPSAxODA7CiAgY29uc3QgRVhQT1JUX1NVQlRJVExFX1NJWkUgPSA0NDsKICBjb25zdCBFWFBPUlRfQVhJU19USVRMRV9TSVpFID0gNDg7CiAgY29uc3QgRVhQT1JUX1RJQ0tfU0laRSA9IDQwOwogIGNvbnN0IEVYUE9SVF9MRUdFTkRfU0laRSA9IDQ4OwoKICBmdW5jdGlvbiBtZWFzdXJlRXhwb3J0VGV4dFdpZHRoKHRleHQsIGZvbnRTaXplKSB7CiAgICB0cnkgewogICAgICBjb25zdCBjYW52YXMgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCJjYW52YXMiKTsKICAgICAgY29uc3QgY3R4ID0gY2FudmFzLmdldENvbnRleHQoIjJkIik7CiAgICAgIGlmICghY3R4KSByZXR1cm4gTWF0aC5yb3VuZChmb250U2l6ZSAqIDAuNiAqIFN0cmluZyh0ZXh0KS5sZW5ndGgpOwogICAgICAvLyBQbG90bHkgdXNhIHRpcG9ncmFmw61hIHNhbnMtc2VyaWYgcG9yIGRlZmVjdG8gZW4gZXN0b3MgZXhwb3J0cy4KICAgICAgY3R4LmZvbnQgPSBmb250U2l6ZSArICJweCBzYW5zLXNlcmlmIjsKICAgICAgcmV0dXJuIE1hdGguY2VpbChjdHgubWVhc3VyZVRleHQodGV4dCkud2lkdGgpOwogICAgfSBjYXRjaCAoZXJyKSB7CiAgICAgIHJldHVybiBNYXRoLnJvdW5kKGZvbnRTaXplICogMC42ICogU3RyaW5nKHRleHQpLmxlbmd0aCk7CiAgICB9CiAgfQoKICBjb25zdCBFWFBPUlRfWUFYSVNfRElHSVRfVyA9IG1lYXN1cmVFeHBvcnRUZXh0V2lkdGgoIjAiLCBFWFBPUlRfVElDS19TSVpFKTsKICBjb25zdCBFWFBPUlRfTUFSR0lOX0wgPQogICAgRVhQT1JUX01BUkdJTl9MX0JBU0UgKwogICAgbWVhc3VyZUV4cG9ydFRleHRXaWR0aCgiNTAwIiwgRVhQT1JUX1RJQ0tfU0laRSkgKwogICAgMyAqIEVYUE9SVF9ZQVhJU19ESUdJVF9XOwogIC8vIHYxNOKAk3YxNjogbGV5ZW5kYSBiYWphIGFkaWNpb25hbCDiiYggMyDDlyAobWl0YWQgZGVsIGFuY2hvIGRlIHVuIGTDrWdpdG8pLgogIGNvbnN0IEVYUE9SVF9MRUdFTkRfTlVER0VfUFggPSAxLjUgKiBFWFBPUlRfWUFYSVNfRElHSVRfVzsKICAvLyBDb2xvcmVzIGRlIG1hcmNhIChleGFjdG9zKS4gUmVhbCA9IGF6dWwgbmF2eSBkZSByZWxsZW5vOyBNZXRhID0gY2FzaSBuZWdybyAobMOtbmVhKS4KICBjb25zdCBFWFBPUlRfQ09MT1JfVEVYVCA9ICIjM0QzRjNGIjsKICBjb25zdCBFWFBPUlRfQ09MT1JfUkVBTCA9ICIjMUQyODRBIjsKICBjb25zdCBFWFBPUlRfQ09MT1JfTUVUQSA9ICIjMDEwMjAyIjsKCiAgZnVuY3Rpb24gZ2V0RXhwb3J0SW5ncmVzb3NQZXJpb2RzKCkgewogICAgY29uc3QgZXhwb3J0QmxvY2sgPSBjaGFydFBheWxvYWQuZXhwb3J0X2luZ3Jlc29zOwogICAgaWYgKGV4cG9ydEJsb2NrICYmIEFycmF5LmlzQXJyYXkoZXhwb3J0QmxvY2sucGVyaW9kcykgJiYgZXhwb3J0QmxvY2sucGVyaW9kcy5sZW5ndGgpIHsKICAgICAgcmV0dXJuIHsKICAgICAgICBwZXJpb2RzOiBleHBvcnRCbG9jay5wZXJpb2RzLAogICAgICAgIHlBeGlzOiBleHBvcnRCbG9jay55X2F4aXMgfHwgIkNpZnJhcyBlbiBtaWxlcyBkZSBVUyQiLAogICAgICB9OwogICAgfQogICAgY29uc3QgbWV0cmljID0gY2hhcnRQYXlsb2FkLm1ldHJpY3MgJiYgY2hhcnRQYXlsb2FkLm1ldHJpY3MuSU5HUkVTT1M7CiAgICBpZiAoIW1ldHJpYyB8fCAhbWV0cmljLnBlcmlvZHMgfHwgIW1ldHJpYy5wZXJpb2RzLmxlbmd0aCkgewogICAgICByZXR1cm4geyBwZXJpb2RzOiBbXSwgeUF4aXM6ICJDaWZyYXMgZW4gbWlsZXMgZGUgVVMkIiB9OwogICAgfQogICAgY29uc3QgbGFzdCA9IG1ldHJpYy5wZXJpb2RzW21ldHJpYy5wZXJpb2RzLmxlbmd0aCAtIDFdOwogICAgY29uc3QgZW5kWWVhciA9IE51bWJlcihsYXN0LnllYXIpOwogICAgY29uc3QgZW5kTW9udGggPSBOdW1iZXIobGFzdC5tb250aCk7CiAgICByZXR1cm4gewogICAgICBwZXJpb2RzOiBtZXRyaWMucGVyaW9kcy5maWx0ZXIoZnVuY3Rpb24gKHApIHsKICAgICAgICByZXR1cm4gTnVtYmVyKHAueWVhcikgPT09IGVuZFllYXIgJiYgTnVtYmVyKHAubW9udGgpID49IDEgJiYgTnVtYmVyKHAubW9udGgpIDw9IGVuZE1vbnRoOwogICAgICB9KSwKICAgICAgeUF4aXM6IG1ldHJpYy55X2F4aXMgfHwgIkNpZnJhcyBlbiBtaWxlcyBkZSBVUyQiLAogICAgfTsKICB9CgogIGZ1bmN0aW9uIGJ1aWxkRXhwb3J0SW5jb21lU2VyaWVzKHBlcmlvZHMsIHNlbGVjdGVkVW5lQ29kZXMpIHsKICAgIGNvbnN0IGxhYmVscyA9IFtdOwogICAgY29uc3QgcmVhbFZhbHVlcyA9IFtdOwogICAgY29uc3QgdGFyZ2V0VmFsdWVzID0gW107CiAgICBwZXJpb2RzLmZvckVhY2goZnVuY3Rpb24gKHBlcmlvZCkgewogICAgICBsYWJlbHMucHVzaChwZXJpb2QubGFiZWwpOwogICAgICBsZXQgcmVhbFN1bSA9IDA7CiAgICAgIGxldCB0YXJnZXRTdW0gPSAwOwogICAgICBzZWxlY3RlZFVuZUNvZGVzLmZvckVhY2goZnVuY3Rpb24gKHVuZUNvZGUpIHsKICAgICAgICBjb25zdCBpdGVtID0gcGVyaW9kLmJ5X3VuZSAmJiBwZXJpb2QuYnlfdW5lW3VuZUNvZGVdOwogICAgICAgIGlmIChpdGVtKSB7CiAgICAgICAgICByZWFsU3VtICs9IE51bWJlcihpdGVtLnJlYWwgfHwgMCk7CiAgICAgICAgICB0YXJnZXRTdW0gKz0gTnVtYmVyKGl0ZW0udGFyZ2V0IHx8IDApOwogICAgICAgIH0KICAgICAgfSk7CiAgICAgIHJlYWxWYWx1ZXMucHVzaChyZWFsU3VtKTsKICAgICAgdGFyZ2V0VmFsdWVzLnB1c2godGFyZ2V0U3VtKTsKICAgIH0pOwogICAgcmV0dXJuIHsKICAgICAgbGFiZWxzOiBsYWJlbHMsCiAgICAgIHJlYWxWYWx1ZXM6IGFjY3VtdWxhdGVWYWx1ZXMocmVhbFZhbHVlcyksCiAgICAgIHRhcmdldFZhbHVlczogYWNjdW11bGF0ZVZhbHVlcyh0YXJnZXRWYWx1ZXMpLAogICAgfTsKICB9CgogIGZ1bmN0aW9uIGJ1aWxkRXhwb3J0SW5jb21lVHJhY2VzKHNlcmllcykgewogICAgLy8gUmVhbCA9IGJhcnJhcyByZWxsZW5vIGF6dWwgIzFEMjg0QTsgTWV0YSA9IGzDrW5lYSBjYXNpIG5lZ3JhICMwMTAyMDIuCiAgICAvLyBBcnJheSBkZSBjb2xvciBwb3IgYmFycmE6IFBsb3RseSBubyBwdWVkZSBjYWVyIGFsIGNvbG9yd2F5IHBvciBvbWlzacOzbi4KICAgIGNvbnN0IHJlYWxGaWxsID0gc2VyaWVzLmxhYmVscy5tYXAoZnVuY3Rpb24gKCkgewogICAgICByZXR1cm4gRVhQT1JUX0NPTE9SX1JFQUw7CiAgICB9KTsKICAgIHJldHVybiBbCiAgICAgIHsKICAgICAgICB4OiBzZXJpZXMubGFiZWxzLAogICAgICAgIHk6IHNlcmllcy5yZWFsVmFsdWVzLAogICAgICAgIHR5cGU6ICJiYXIiLAogICAgICAgIG5hbWU6ICJSZWFsIiwKICAgICAgICBtYXJrZXI6IHsKICAgICAgICAgIGNvbG9yOiByZWFsRmlsbCwKICAgICAgICAgIGxpbmU6IHsgY29sb3I6IEVYUE9SVF9DT0xPUl9SRUFMLCB3aWR0aDogMCB9LAogICAgICAgICAgb3BhY2l0eTogMSwKICAgICAgICB9LAogICAgICB9LAogICAgICB7CiAgICAgICAgeDogc2VyaWVzLmxhYmVscywKICAgICAgICB5OiBzZXJpZXMudGFyZ2V0VmFsdWVzLAogICAgICAgIHR5cGU6ICJzY2F0dGVyIiwKICAgICAgICBtb2RlOiAibGluZXMiLAogICAgICAgIG5hbWU6ICJNZXRhIiwKICAgICAgICBsaW5lOiB7IGNvbG9yOiBFWFBPUlRfQ09MT1JfTUVUQSwgd2lkdGg6IDMsIGRhc2g6ICJkYXNoIiB9LAogICAgICAgIG1hcmtlcjogeyBjb2xvcjogRVhQT1JUX0NPTE9SX01FVEEgfSwKICAgICAgfSwKICAgIF07CiAgfQoKICBmdW5jdGlvbiBidWlsZEV4cG9ydEluY29tZUxheW91dCh0aXRsZSwgc2VyaWVzLCB5QXhpcykgewogICAgLy8gdjEyOiBtw6FyZ2VuZXMgYmxhbmNvcyBhIGxhIG1pdGFkOyBmdWVudGVzIMOXMi41IC8gw5cyLgogICAgLy8gU3VidMOtdHVsbyBkZWJham8gZGVsIHTDrXR1bG8gKHTDrXR1bG8gfkVYUE9SVF9USVRMRV9TSVpFIHB4ICsgYWlyZSkuCiAgICBjb25zdCBzdWJ0aXRsZVRvcFB4ID0gRVhQT1JUX1RJVExFX1NJWkUgKyAyODsKICAgIHJldHVybiB7CiAgICAgIHRpdGxlOiB7CiAgICAgICAgdGV4dDogIjxiPiIgKyB0aXRsZSArICI8L2I+IiwKICAgICAgICBmb250OiB7IHNpemU6IEVYUE9SVF9USVRMRV9TSVpFLCBjb2xvcjogRVhQT1JUX0NPTE9SX1RFWFQgfSwKICAgICAgICB4cmVmOiAicGFwZXIiLAogICAgICAgIHlyZWY6ICJwYXBlciIsCiAgICAgICAgeDogMC41LAogICAgICAgIHhhbmNob3I6ICJjZW50ZXIiLAogICAgICAgIHk6IDEsCiAgICAgICAgeWFuY2hvcjogInRvcCIsCiAgICAgICAgcGFkOiB7IHQ6IDEwLCBiOiAyLCBsOiAwLCByOiAwIH0sCiAgICAgIH0sCiAgICAgIGFubm90YXRpb25zOiBbCiAgICAgICAgewogICAgICAgICAgdGV4dDogRVhQT1JUX1NVQlRJVExFLAogICAgICAgICAgeHJlZjogInBhcGVyIiwKICAgICAgICAgIHlyZWY6ICJwYXBlciIsCiAgICAgICAgICB4OiAwLjUsCiAgICAgICAgICB5OiAxIC0gc3VidGl0bGVUb3BQeCAvIElNQUdFX0hFSUdIVCwKICAgICAgICAgIHhhbmNob3I6ICJjZW50ZXIiLAogICAgICAgICAgeWFuY2hvcjogInRvcCIsCiAgICAgICAgICBzaG93YXJyb3c6IGZhbHNlLAogICAgICAgICAgZm9udDogeyBzaXplOiBFWFBPUlRfU1VCVElUTEVfU0laRSwgY29sb3I6IEVYUE9SVF9DT0xPUl9URVhUIH0sCiAgICAgICAgfSwKICAgICAgXSwKICAgICAgYmFybW9kZTogImdyb3VwIiwKICAgICAgYmFyZ2FwOiAwLjI4LAogICAgICB3aWR0aDogSU1BR0VfV0lEVEgsCiAgICAgIGhlaWdodDogSU1BR0VfSEVJR0hULAogICAgICBtYXJnaW46IHsKICAgICAgICBsOiBFWFBPUlRfTUFSR0lOX0wsCiAgICAgICAgcjogRVhQT1JUX01BUkdJTl9SLAogICAgICAgIHQ6IEVYUE9SVF9NQVJHSU5fVCwKICAgICAgICBiOiBFWFBPUlRfTUFSR0lOX0IsCiAgICAgICAgcGFkOiAwLAogICAgICB9LAogICAgICBsZWdlbmQ6IHsKICAgICAgICBvcmllbnRhdGlvbjogImgiLAogICAgICAgIHhyZWY6ICJwYXBlciIsCiAgICAgICAgeXJlZjogInBhcGVyIiwKICAgICAgICB4OiAwLjUsCiAgICAgICAgeGFuY2hvcjogImNlbnRlciIsCiAgICAgICAgLy8gdjc6IC0wLjA1NSDiiJIgMcOXIGFsdHVyYSBkZWwgZm9udCAoYmFqbyDCq1BlcsOtb2RvwrspLgogICAgICAgIC8vIHYxMzog4oiS4oWTIGFkaWNpb25hbCBkZSBsYSBhbHR1cmEgZGVsIGZvbnQgZGUgbGEgbGV5ZW5kYS4KICAgICAgICAvLyB2MTTigJN2MTY6IOKIkiBFWFBPUlRfTEVHRU5EX05VREdFX1BYICgxLjXDlyBhbmNobyBkZSB1biBkw61naXRvIGRlbCBlamUgWSkuCiAgICAgICAgeToKICAgICAgICAgIC0wLjA1NSAtCiAgICAgICAgICBFWFBPUlRfTEVHRU5EX1NJWkUgLyBJTUFHRV9IRUlHSFQgLQogICAgICAgICAgRVhQT1JUX0xFR0VORF9TSVpFIC8gKDMgKiBJTUFHRV9IRUlHSFQpIC0KICAgICAgICAgIEVYUE9SVF9MRUdFTkRfTlVER0VfUFggLyBJTUFHRV9IRUlHSFQsCiAgICAgICAgeWFuY2hvcjogInRvcCIsCiAgICAgICAgZm9udDogeyBzaXplOiBFWFBPUlRfTEVHRU5EX1NJWkUsIGNvbG9yOiBFWFBPUlRfQ09MT1JfVEVYVCB9LAogICAgICAgIGJnY29sb3I6ICJyZ2JhKDI1NSwyNTUsMjU1LDApIiwKICAgICAgICBib3JkZXJ3aWR0aDogMCwKICAgICAgICBpdGVtc2l6aW5nOiAiY29uc3RhbnQiLAogICAgICAgIGl0ZW13aWR0aDogNjAsCiAgICAgIH0sCiAgICAgIHhheGlzOiB7CiAgICAgICAgdGl0bGU6IHsKICAgICAgICAgIHRleHQ6ICJQZXLDrW9kbyIsCiAgICAgICAgICBmb250OiB7IHNpemU6IEVYUE9SVF9BWElTX1RJVExFX1NJWkUsIGNvbG9yOiBFWFBPUlRfQ09MT1JfVEVYVCB9LAogICAgICAgICAgLy8gdjg6IDEwOyBtZW5vciBzdGFuZG9mZiA9IMKrUGVyw61vZG/CuyBtw6FzIGFycmliYSAobcOhcyBjZXJjYSBkZSBsb3MgbWVzZXMpCiAgICAgICAgICBzdGFuZG9mZjogNCwKICAgICAgICB9LAogICAgICAgIHR5cGU6ICJjYXRlZ29yeSIsCiAgICAgICAgY2F0ZWdvcnlvcmRlcjogImFycmF5IiwKICAgICAgICBjYXRlZ29yeWFycmF5OiBzZXJpZXMubGFiZWxzLAogICAgICAgIHRpY2ttb2RlOiAiYXJyYXkiLAogICAgICAgIHRpY2t2YWxzOiBzZXJpZXMubGFiZWxzLAogICAgICAgIHRpY2t0ZXh0OiBzZXJpZXMubGFiZWxzLAogICAgICAgIHRpY2tmb250OiB7IHNpemU6IEVYUE9SVF9USUNLX1NJWkUsIGNvbG9yOiBFWFBPUlRfQ09MT1JfVEVYVCB9LAogICAgICAgIHRpY2tsZW46IDgsCiAgICAgICAgdGlja3dpZHRoOiAxLjUsCiAgICAgICAgbGluZWNvbG9yOiBFWFBPUlRfQ09MT1JfVEVYVCwKICAgICAgICBhdXRvbWFyZ2luOiBmYWxzZSwKICAgICAgICBmaXhlZHJhbmdlOiB0cnVlLAogICAgICAgIG1pcnJvcjogZmFsc2UsCiAgICAgIH0sCiAgICAgIHlheGlzOiB7CiAgICAgICAgdGl0bGU6IHsKICAgICAgICAgIHRleHQ6IHlBeGlzIHx8ICJDaWZyYXMgZW4gbWlsZXMgZGUgVVMkIiwKICAgICAgICAgIGZvbnQ6IHsgc2l6ZTogRVhQT1JUX0FYSVNfVElUTEVfU0laRSwgY29sb3I6IEVYUE9SVF9DT0xPUl9URVhUIH0sCiAgICAgICAgICBzdGFuZG9mZjogMTAsCiAgICAgICAgfSwKICAgICAgICByYW5nZW1vZGU6ICJ0b3plcm8iLAogICAgICAgIHRpY2tmb250OiB7IHNpemU6IEVYUE9SVF9USUNLX1NJWkUsIGNvbG9yOiBFWFBPUlRfQ09MT1JfVEVYVCB9LAogICAgICAgIHRpY2tsZW46IDgsCiAgICAgICAgdGlja3dpZHRoOiAxLjUsCiAgICAgICAgbGluZWNvbG9yOiBFWFBPUlRfQ09MT1JfVEVYVCwKICAgICAgICBhdXRvbWFyZ2luOiBmYWxzZSwKICAgICAgICBmaXhlZHJhbmdlOiB0cnVlLAogICAgICAgIHplcm9saW5lOiB0cnVlLAogICAgICAgIHplcm9saW5lY29sb3I6IEVYUE9SVF9DT0xPUl9URVhULAogICAgICAgIGdyaWRjb2xvcjogIiNlMmU4ZjAiLAogICAgICAgIGdyaWR3aWR0aDogMSwKICAgICAgfSwKICAgICAgZm9udDogeyBjb2xvcjogRVhQT1JUX0NPTE9SX1RFWFQgfSwKICAgICAgY29sb3J3YXk6IFtFWFBPUlRfQ09MT1JfUkVBTCwgRVhQT1JUX0NPTE9SX01FVEFdLAogICAgICBwYXBlcl9iZ2NvbG9yOiAiI2ZmZmZmZiIsCiAgICAgIHBsb3RfYmdjb2xvcjogIiNmZmZmZmYiLAogICAgICBzaG93bGVnZW5kOiB0cnVlLAogICAgfTsKICB9CgogIGZ1bmN0aW9uIGZvcm1hdEV4cG9ydFN0YW1wKGRhdGUpIHsKICAgIGNvbnN0IHl5ID0gU3RyaW5nKGRhdGUuZ2V0RnVsbFllYXIoKSkuc2xpY2UoLTIpOwogICAgY29uc3QgbW0gPSBTdHJpbmcoZGF0ZS5nZXRNb250aCgpICsgMSkucGFkU3RhcnQoMiwgIjAiKTsKICAgIGNvbnN0IGhoID0gU3RyaW5nKGRhdGUuZ2V0SG91cnMoKSkucGFkU3RhcnQoMiwgIjAiKTsKICAgIGNvbnN0IG1pID0gU3RyaW5nKGRhdGUuZ2V0TWludXRlcygpKS5wYWRTdGFydCgyLCAiMCIpOwogICAgcmV0dXJuIHl5ICsgIi0iICsgbW0gKyAiICIgKyBoaCArICItIiArIG1pOwogIH0KCiAgZnVuY3Rpb24gZG93bmxvYWREYXRhVXJsKGRhdGFVcmwsIGZpbGVuYW1lKSB7CiAgICBjb25zdCBhID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgiYSIpOwogICAgYS5ocmVmID0gZGF0YVVybDsKICAgIGEuZG93bmxvYWQgPSBmaWxlbmFtZTsKICAgIGRvY3VtZW50LmJvZHkuYXBwZW5kQ2hpbGQoYSk7CiAgICBhLmNsaWNrKCk7CiAgICBhLnJlbW92ZSgpOwogIH0KCiAgZnVuY3Rpb24gZ2V0Q3NyZlRva2VuKCkgewogICAgY29uc3QgaW5wdXQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCJpbnB1dFtuYW1lPSdjc3JmbWlkZGxld2FyZXRva2VuJ10iKTsKICAgIGlmIChpbnB1dCAmJiBpbnB1dC52YWx1ZSkgcmV0dXJuIGlucHV0LnZhbHVlOwogICAgY29uc3QgbWF0Y2ggPSBkb2N1bWVudC5jb29raWUubWF0Y2goLyg/Ol58O1xzKiljc3JmdG9rZW49KFteO10rKS8pOwogICAgcmV0dXJuIG1hdGNoID8gZGVjb2RlVVJJQ29tcG9uZW50KG1hdGNoWzFdKSA6ICIiOwogIH0KCiAgYXN5bmMgZnVuY3Rpb24gdXBsb2FkRXhwb3J0UG5nVG9TZXJ2ZXIoZGF0YVVybCwgZmlsZW5hbWUpIHsKICAgIGNvbnN0IHJlcyA9IGF3YWl0IGZldGNoKGRhdGFVcmwpOwogICAgY29uc3QgYmxvYiA9IGF3YWl0IHJlcy5ibG9iKCk7CiAgICBjb25zdCBmb3JtID0gbmV3IEZvcm1EYXRhKCk7CiAgICBmb3JtLmFwcGVuZCgiZmlsZSIsIGJsb2IsIGZpbGVuYW1lKTsKICAgIGZvcm0uYXBwZW5kKCJhY3RpdmF0ZSIsICIxIik7CiAgICBjb25zdCByZXNwb25zZSA9IGF3YWl0IGZldGNoKCJ7JSB1cmwgJ3BnYzp0dl9jaGFydHNfdXBsb2FkJyAlfSIsIHsKICAgICAgbWV0aG9kOiAiUE9TVCIsCiAgICAgIGhlYWRlcnM6IHsgIlgtQ1NSRlRva2VuIjogZ2V0Q3NyZlRva2VuKCkgfSwKICAgICAgYm9keTogZm9ybSwKICAgICAgY3JlZGVudGlhbHM6ICJzYW1lLW9yaWdpbiIsCiAgICB9KTsKICAgIGxldCBwYXlsb2FkID0ge307CiAgICB0cnkgewogICAgICBwYXlsb2FkID0gYXdhaXQgcmVzcG9uc2UuanNvbigpOwogICAgfSBjYXRjaCAoZSkgewogICAgICBwYXlsb2FkID0ge307CiAgICB9CiAgICBpZiAocmVzcG9uc2Uuc3RhdHVzID09PSA0MDMgfHwgcmVzcG9uc2Uuc3RhdHVzID09PSA0MDEpIHsKICAgICAgdGhyb3cgbmV3IEVycm9yKCJTaW4gcGVybWlzbyBwYXJhIGd1YXJkYXIgZW4gZWwgc2Vydmlkb3IgKGluaWNpZSBzZXNpw7NuKS4gTGEgZGVzY2FyZ2EgbG9jYWwgc8OtIHNlIGhpem8uIik7CiAgICB9CiAgICBpZiAoIXJlc3BvbnNlLm9rIHx8ICFwYXlsb2FkLm9rKSB7CiAgICAgIHRocm93IG5ldyBFcnJvcigocGF5bG9hZCAmJiBwYXlsb2FkLmVycm9yKSB8fCAoIkVycm9yIGFsIGd1YXJkYXIgIiArIGZpbGVuYW1lICsgIiBlbiBlbCBzZXJ2aWRvciAoSFRUUCAiICsgcmVzcG9uc2Uuc3RhdHVzICsgIikuIikpOwogICAgfQogICAgcmV0dXJuIHBheWxvYWQ7CiAgfQoKICBmdW5jdGlvbiBzbGVlcChtcykgewogICAgcmV0dXJuIG5ldyBQcm9taXNlKGZ1bmN0aW9uIChyZXNvbHZlKSB7IHNldFRpbWVvdXQocmVzb2x2ZSwgbXMpOyB9KTsKICB9CgogIGFzeW5jIGZ1bmN0aW9uIGV4cG9ydEZvdXJJbmNvbWVDaGFydHNTdmcoKSB7CiAgICBjb25zdCBidG5FeHBvcnQgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuLWV4cG9ydC00LWNoYXJ0cy1zdmciKTsKICAgIGlmICghYnRuRXhwb3J0KSByZXR1cm47CgogICAgaWYgKHR5cGVvZiBQbG90bHkgPT09ICJ1bmRlZmluZWQiIHx8ICFQbG90bHkubmV3UGxvdCB8fCAhUGxvdGx5LnRvSW1hZ2UpIHsKICAgICAgYWxlcnQoIlBsb3RseSBubyBlc3TDoSBkaXNwb25pYmxlOyBubyBzZSBwdWVkZW4gZXhwb3J0YXIgbG9zIFBORy4iKTsKICAgICAgcmV0dXJuOwogICAgfQoKICAgIGNvbnN0IHNvdXJjZSA9IGdldEV4cG9ydEluZ3Jlc29zUGVyaW9kcygpOwogICAgaWYgKCFzb3VyY2UucGVyaW9kcy5sZW5ndGgpIHsKICAgICAgYWxlcnQoIk5vIGhheSBkYXRvcyBkZSBJTkdSRVNPUyBwYXJhIGV4cG9ydGFyIChleHBvcnRfaW5ncmVzb3MgLyBjaGFydFBheWxvYWQpLiIpOwogICAgICByZXR1cm47CiAgICB9CgogICAgY29uc3QgY29uZmlncyA9IFsKICAgICAgeyBmaWxlSW5kZXg6IDEsIHRpdGxlOiAiRkFDVE9SSU5HIiwgdW5lQ29kZXM6IFsiRkFDVE9SSU5HIl0gfSwKICAgICAgeyBmaWxlSW5kZXg6IDIsIHRpdGxlOiAiTEVBU0lORyIsIHVuZUNvZGVzOiBbIkxFQVNJTkciXSB9LAogICAgICB7IGZpbGVJbmRleDogMywgdGl0bGU6ICJJTlNVUkFOQ0UiLCB1bmVDb2RlczogWyJJTlNVUkFOQ0UiXSB9LAogICAgICB7IGZpbGVJbmRleDogNCwgdGl0bGU6ICJHUlVQTyIsIHVuZUNvZGVzOiBbIkZBQ1RPUklORyIsICJMRUFTSU5HIiwgIklOU1VSQU5DRSJdIH0sCiAgICBdOwoKICAgIGNvbnN0IHN0YW1wID0gZm9ybWF0RXhwb3J0U3RhbXAobmV3IERhdGUoKSk7CiAgICBjb25zdCBvcmlnaW5hbFRleHQgPSBidG5FeHBvcnQudGV4dENvbnRlbnQ7CiAgICBidG5FeHBvcnQuZGlzYWJsZWQgPSB0cnVlOwogICAgYnRuRXhwb3J0LnRleHRDb250ZW50ID0gIkdlbmVyYW5kby4uLiI7CgogICAgY29uc3QgaG9zdCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoImRpdiIpOwogICAgaG9zdC5zZXRBdHRyaWJ1dGUoImFyaWEtaGlkZGVuIiwgInRydWUiKTsKICAgIGhvc3Quc3R5bGUuY3NzVGV4dCA9CiAgICAgICJwb3NpdGlvbjpmaXhlZDtsZWZ0Oi0xMDAwMHB4O3RvcDowO3dpZHRoOiIgKyBJTUFHRV9XSURUSCArCiAgICAgICJweDtoZWlnaHQ6IiArIElNQUdFX0hFSUdIVCArICJweDtvdmVyZmxvdzpoaWRkZW47cG9pbnRlci1ldmVudHM6bm9uZTsiOwogICAgZG9jdW1lbnQuYm9keS5hcHBlbmRDaGlsZChob3N0KTsKCiAgICBsZXQgc2VydmVyU2F2ZWQgPSAwOwogICAgdHJ5IHsKICAgICAgZm9yIChsZXQgaSA9IDA7IGkgPCBjb25maWdzLmxlbmd0aDsgaSsrKSB7CiAgICAgICAgY29uc3QgY2ZnID0gY29uZmlnc1tpXTsKICAgICAgICBjb25zdCBzZXJpZXMgPSBidWlsZEV4cG9ydEluY29tZVNlcmllcyhzb3VyY2UucGVyaW9kcywgY2ZnLnVuZUNvZGVzKTsKICAgICAgICBpZiAoIXNlcmllcy5sYWJlbHMubGVuZ3RoKSB7CiAgICAgICAgICB0aHJvdyBuZXcgRXJyb3IoIlNlcmllIHZhY8OtYSBwYXJhICIgKyBjZmcudGl0bGUpOwogICAgICAgIH0KCiAgICAgICAgY29uc3QgZ2QgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCJkaXYiKTsKICAgICAgICBnZC5zdHlsZS53aWR0aCA9IElNQUdFX1dJRFRIICsgInB4IjsKICAgICAgICBnZC5zdHlsZS5oZWlnaHQgPSBJTUFHRV9IRUlHSFQgKyAicHgiOwogICAgICAgIGhvc3QuYXBwZW5kQ2hpbGQoZ2QpOwoKICAgICAgICBhd2FpdCBQbG90bHkubmV3UGxvdCgKICAgICAgICAgIGdkLAogICAgICAgICAgYnVpbGRFeHBvcnRJbmNvbWVUcmFjZXMoc2VyaWVzKSwKICAgICAgICAgIGJ1aWxkRXhwb3J0SW5jb21lTGF5b3V0KGNmZy50aXRsZSwgc2VyaWVzLCBzb3VyY2UueUF4aXMpLAogICAgICAgICAgewogICAgICAgICAgICBzdGF0aWNQbG90OiB0cnVlLAogICAgICAgICAgICBkaXNwbGF5bG9nbzogZmFsc2UsCiAgICAgICAgICAgIGRpc3BsYXlNb2RlQmFyOiBmYWxzZSwKICAgICAgICAgICAgcmVzcG9uc2l2ZTogZmFsc2UsCiAgICAgICAgICB9CiAgICAgICAgKTsKCiAgICAgICAgY29uc3QgZGF0YVVybFBuZyA9IGF3YWl0IFBsb3RseS50b0ltYWdlKGdkLCB7CiAgICAgICAgICBmb3JtYXQ6ICJwbmciLAogICAgICAgICAgd2lkdGg6IElNQUdFX1dJRFRILAogICAgICAgICAgaGVpZ2h0OiBJTUFHRV9IRUlHSFQsCiAgICAgICAgfSk7CiAgICAgICAgY29uc3QgZmlsZW5hbWUgPSAid2NnLWciICsgY2ZnLmZpbGVJbmRleCArICIgIiArIHN0YW1wICsgIi5wbmciOwogICAgICAgIGRvd25sb2FkRGF0YVVybChkYXRhVXJsUG5nLCBmaWxlbmFtZSk7CiAgICAgICAgYXdhaXQgdXBsb2FkRXhwb3J0UG5nVG9TZXJ2ZXIoZGF0YVVybFBuZywgZmlsZW5hbWUpOwogICAgICAgIHNlcnZlclNhdmVkICs9IDE7CgogICAgICAgIFBsb3RseS5wdXJnZShnZCk7CiAgICAgICAgZ2QucmVtb3ZlKCk7CiAgICAgICAgYXdhaXQgc2xlZXAoMjUwKTsKICAgICAgfQogICAgICBidG5FeHBvcnQudGV4dENvbnRlbnQgPSAiTGlzdG8gKCIgKyBzZXJ2ZXJTYXZlZCArICIgZW4gVFYpIjsKICAgICAgYXdhaXQgc2xlZXAoMTIwMCk7CiAgICB9IGNhdGNoIChlcnIpIHsKICAgICAgY29uc29sZS5lcnJvcihlcnIpOwogICAgICBhbGVydCgoZXJyICYmIGVyci5tZXNzYWdlKSB8fCAiRXJyb3IgYWwgZ2VuZXJhciBsYSBleHBvcnRhY2nDs24gZGUgNCBjaGFydHMgUE5HLiIpOwogICAgfSBmaW5hbGx5IHsKICAgICAgdHJ5IHsKICAgICAgICBob3N0LnF1ZXJ5U2VsZWN0b3JBbGwoImRpdiIpLmZvckVhY2goZnVuY3Rpb24gKGVsKSB7CiAgICAgICAgICB0cnkgeyBQbG90bHkucHVyZ2UoZWwpOyB9IGNhdGNoIChlKSB7fQogICAgICAgIH0pOwogICAgICB9IGNhdGNoIChlKSB7fQogICAgICBob3N0LnJlbW92ZSgpOwogICAgICBidG5FeHBvcnQuZGlzYWJsZWQgPSBmYWxzZTsKICAgICAgYnRuRXhwb3J0LnRleHRDb250ZW50ID0gb3JpZ2luYWxUZXh0OwogICAgfQogIH0KCiAgY29uc3QgYnRuRm91ckNoYXJ0cyA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJidG4tZXhwb3J0LTQtY2hhcnRzLXN2ZyIpOwogIGlmIChidG5Gb3VyQ2hhcnRzKSB7CiAgICBidG5Gb3VyQ2hhcnRzLnNldEF0dHJpYnV0ZSgiZGF0YS1leHBvcnQtc3ZnLXZlcnNpb24iLCBFWFBPUlRfU1ZHX1ZFUlNJT04pOwogICAgYnRuRm91ckNoYXJ0cy5hZGRFdmVudExpc3RlbmVyKCJjbGljayIsIGZ1bmN0aW9uICgpIHsKICAgICAgZXhwb3J0Rm91ckluY29tZUNoYXJ0c1N2ZygpOwogICAgfSk7CiAgfQoKICAvLyAtLS0gR2VuZXJhciByZXBvcnRlcyAobW9kYWwpIC0tLQogIChmdW5jdGlvbiBpbml0UmVwb3J0TW9kYWwoKSB7CiAgICBjb25zdCBidG4gPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuLWdlbmVyYXItcmVwb3J0ZXMiKTsKICAgIGNvbnN0IG1vZGFsID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoInJlcG9ydGVzLW1vZGFsIik7CiAgICBpZiAoIWJ0biB8fCAhbW9kYWwpIHJldHVybjsKCiAgICBjb25zdCBjbG9zZUJ0bnMgPSBtb2RhbC5xdWVyeVNlbGVjdG9yQWxsKCJbZGF0YS1yZXBvcnRlcy1jbG9zZV0iKTsKICAgIGNvbnN0IGZvcm0gPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgicmVwb3J0ZXMtZm9ybSIpOwogICAgY29uc3Qgc3RhdHVzRWwgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgicmVwb3J0ZXMtc3RhdHVzIik7CiAgICBjb25zdCBlcnJFbCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJyZXBvcnRlcy1lcnJvciIpOwogICAgY29uc3QgZ2VuZXJhdGVCdG4gPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgicmVwb3J0ZXMtZ2VuZXJhdGUiKTsKICAgIGNvbnN0IGNzcmZJbnB1dCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoIiNidG4tZXhwb3J0LTQtY2hhcnRzLXN2ZyIpCiAgICAgID8gZG9jdW1lbnQucXVlcnlTZWxlY3RvcignaW5wdXRbbmFtZT0iY3NyZm1pZGRsZXdhcmV0b2tlbiJdJykKICAgICAgOiBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCdpbnB1dFtuYW1lPSJjc3JmbWlkZGxld2FyZXRva2VuIl0nKTsKCiAgICBmdW5jdGlvbiBvcGVuTW9kYWwoKSB7CiAgICAgIGVyckVsLnRleHRDb250ZW50ID0gIiI7CiAgICAgIHN0YXR1c0VsLnRleHRDb250ZW50ID0gIiI7CiAgICAgIG1vZGFsLnN0eWxlLmRpc3BsYXkgPSAiZmxleCI7CiAgICAgIGZldGNoKCJ7JSB1cmwgJ3JlcG9ydHM6ZGVmYXVsdHMnICV9IiwgeyBjcmVkZW50aWFsczogInNhbWUtb3JpZ2luIiB9KQogICAgICAgIC50aGVuKGZ1bmN0aW9uIChyKSB7IHJldHVybiByLmpzb24oKTsgfSkKICAgICAgICAudGhlbihmdW5jdGlvbiAoZGF0YSkgewogICAgICAgICAgaWYgKCFkYXRhIHx8ICFkYXRhLmRlZmF1bHRzKSByZXR1cm47CiAgICAgICAgICBPYmplY3Qua2V5cyhkYXRhLmRlZmF1bHRzKS5mb3JFYWNoKGZ1bmN0aW9uIChrZXkpIHsKICAgICAgICAgICAgY29uc3QgaW5wdXQgPSBmb3JtLnF1ZXJ5U2VsZWN0b3IoJ2lucHV0W25hbWU9ImFyZWFzIl1bdmFsdWU9IicgKyBrZXkgKyAnIl0nKTsKICAgICAgICAgICAgaWYgKGlucHV0KSBpbnB1dC5jaGVja2VkID0gISFkYXRhLmRlZmF1bHRzW2tleV07CiAgICAgICAgICB9KTsKICAgICAgICB9KQogICAgICAgIC5jYXRjaChmdW5jdGlvbiAoKSB7fSk7CiAgICB9CgogICAgZnVuY3Rpb24gY2xvc2VNb2RhbCgpIHsKICAgICAgbW9kYWwuc3R5bGUuZGlzcGxheSA9ICJub25lIjsKICAgICAgZ2VuZXJhdGVCdG4uZGlzYWJsZWQgPSBmYWxzZTsKICAgICAgZ2VuZXJhdGVCdG4udGV4dENvbnRlbnQgPSAiR2VuZXJhciI7CiAgICB9CgogICAgYnRuLmFkZEV2ZW50TGlzdGVuZXIoImNsaWNrIiwgb3Blbk1vZGFsKTsKICAgIGNsb3NlQnRucy5mb3JFYWNoKGZ1bmN0aW9uIChlbCkgewogICAgICBlbC5hZGRFdmVudExpc3RlbmVyKCJjbGljayIsIGNsb3NlTW9kYWwpOwogICAgfSk7CiAgICBtb2RhbC5hZGRFdmVudExpc3RlbmVyKCJjbGljayIsIGZ1bmN0aW9uIChldikgewogICAgICBpZiAoZXYudGFyZ2V0ID09PSBtb2RhbCkgY2xvc2VNb2RhbCgpOwogICAgfSk7CgogICAgZm9ybS5hZGRFdmVudExpc3RlbmVyKCJzdWJtaXQiLCBhc3luYyBmdW5jdGlvbiAoZXYpIHsKICAgICAgZXYucHJldmVudERlZmF1bHQoKTsKICAgICAgZXJyRWwudGV4dENvbnRlbnQgPSAiIjsKICAgICAgY29uc3QgY2hlY2tlZCA9IEFycmF5LmZyb20oZm9ybS5xdWVyeVNlbGVjdG9yQWxsKCdpbnB1dFtuYW1lPSJhcmVhcyJdOmNoZWNrZWQnKSkubWFwKGZ1bmN0aW9uIChpKSB7CiAgICAgICAgcmV0dXJuIGkudmFsdWU7CiAgICAgIH0pOwogICAgICBpZiAoIWNoZWNrZWQubGVuZ3RoKSB7CiAgICAgICAgZXJyRWwudGV4dENvbnRlbnQgPSAiU2VsZWNjaW9uZSBhbCBtZW5vcyB1biDDoXJlYTogQWRtaW5pc3RyYWNpw7NuLCBQR0MsIFBHTyBvIEIuIFJpZXNnby4iOwogICAgICAgIHJldHVybjsKICAgICAgfQogICAgICBnZW5lcmF0ZUJ0bi5kaXNhYmxlZCA9IHRydWU7CiAgICAgIGdlbmVyYXRlQnRuLnRleHRDb250ZW50ID0gIkdlbmVyYW5kby4uLiI7CiAgICAgIHN0YXR1c0VsLnRleHRDb250ZW50ID0gIkdlbmVyYW5kbyByZXBvcnRlc+KApiI7CgogICAgICBjb25zdCBjc3JmID0gKGNzcmZJbnB1dCAmJiBjc3JmSW5wdXQudmFsdWUpIHx8CiAgICAgICAgKGRvY3VtZW50LmNvb2tpZS5tYXRjaCgvY3NyZnRva2VuPShbXjtdKykvKSB8fCBbXSlbMV0gfHwgIiI7CgogICAgICB0cnkgewogICAgICAgIGNvbnN0IHJlc3AgPSBhd2FpdCBmZXRjaCgieyUgdXJsICdyZXBvcnRzOmdlbmVyYXRlJyAlfSIsIHsKICAgICAgICAgIG1ldGhvZDogIlBPU1QiLAogICAgICAgICAgY3JlZGVudGlhbHM6ICJzYW1lLW9yaWdpbiIsCiAgICAgICAgICBoZWFkZXJzOiB7CiAgICAgICAgICAgICJDb250ZW50LVR5cGUiOiAiYXBwbGljYXRpb24vanNvbiIsCiAgICAgICAgICAgICJYLUNTUkZUb2tlbiI6IGNzcmYKICAgICAgICAgIH0sCiAgICAgICAgICBib2R5OiBKU09OLnN0cmluZ2lmeSh7IGFyZWFzOiBjaGVja2VkIH0pCiAgICAgICAgfSk7CiAgICAgICAgaWYgKCFyZXNwLm9rKSB7CiAgICAgICAgICBsZXQgbXNnID0gIk5vIHNlIHB1ZGllcm9uIGdlbmVyYXIgbG9zIHJlcG9ydGVzLiI7CiAgICAgICAgICB0cnkgewogICAgICAgICAgICBjb25zdCBqID0gYXdhaXQgcmVzcC5qc29uKCk7CiAgICAgICAgICAgIGlmIChqICYmIGouZXJyb3IpIG1zZyA9IGouZXJyb3I7CiAgICAgICAgICB9IGNhdGNoIChlKSB7fQogICAgICAgICAgdGhyb3cgbmV3IEVycm9yKG1zZyk7CiAgICAgICAgfQogICAgICAgIGNvbnN0IGJsb2IgPSBhd2FpdCByZXNwLmJsb2IoKTsKICAgICAgICBsZXQgZmlsZW5hbWUgPSByZXNwLmhlYWRlcnMuZ2V0KCJYLVJlcG9ydC1GaWxlbmFtZSIpIHx8ICJyZXBvcnRlc193Y2cuemlwIjsKICAgICAgICBjb25zdCBjZCA9IHJlc3AuaGVhZGVycy5nZXQoIkNvbnRlbnQtRGlzcG9zaXRpb24iKSB8fCAiIjsKICAgICAgICBjb25zdCBtID0gY2QubWF0Y2goL2ZpbGVuYW1lPVwiKFteXCJdKylcIi8pOwogICAgICAgIGlmIChtKSBmaWxlbmFtZSA9IG1bMV07CiAgICAgICAgY29uc3QgdXJsID0gVVJMLmNyZWF0ZU9iamVjdFVSTChibG9iKTsKICAgICAgICBjb25zdCBhID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgiYSIpOwogICAgICAgIGEuaHJlZiA9IHVybDsKICAgICAgICBhLmRvd25sb2FkID0gZmlsZW5hbWU7CiAgICAgICAgZG9jdW1lbnQuYm9keS5hcHBlbmRDaGlsZChhKTsKICAgICAgICBhLmNsaWNrKCk7CiAgICAgICAgYS5yZW1vdmUoKTsKICAgICAgICBVUkwucmV2b2tlT2JqZWN0VVJMKHVybCk7CiAgICAgICAgc3RhdHVzRWwudGV4dENvbnRlbnQgPSAiRGVzY2FyZ2EgaW5pY2lhZGE6ICIgKyBmaWxlbmFtZTsKICAgICAgICBnZW5lcmF0ZUJ0bi50ZXh0Q29udGVudCA9ICJHZW5lcmFyIjsKICAgICAgICBnZW5lcmF0ZUJ0bi5kaXNhYmxlZCA9IGZhbHNlOwogICAgICB9IGNhdGNoIChlcnIpIHsKICAgICAgICBlcnJFbC50ZXh0Q29udGVudCA9IChlcnIgJiYgZXJyLm1lc3NhZ2UpIHx8ICJFcnJvciBhbCBnZW5lcmFyLiI7CiAgICAgICAgc3RhdHVzRWwudGV4dENvbnRlbnQgPSAiIjsKICAgICAgICBnZW5lcmF0ZUJ0bi5kaXNhYmxlZCA9IGZhbHNlOwogICAgICAgIGdlbmVyYXRlQnRuLnRleHRDb250ZW50ID0gIkdlbmVyYXIiOwogICAgICB9CiAgICB9KTsKICB9KSgpOwoKfSk7Cjwvc2NyaXB0PgoKPGRpdiBpZD0icmVwb3J0ZXMtbW9kYWwiIHN0eWxlPSJkaXNwbGF5Om5vbmU7IHBvc2l0aW9uOmZpeGVkOyBpbnNldDowOyB6LWluZGV4Ojk5OTk7IGJhY2tncm91bmQ6cmdiYSgxNSwyMyw0MiwwLjQ1KTsgYWxpZ24taXRlbXM6Y2VudGVyOyBqdXN0aWZ5LWNvbnRlbnQ6Y2VudGVyOyBwYWRkaW5nOjE2cHg7Ij4KICA8ZGl2IHN0eWxlPSJiYWNrZ3JvdW5kOiNmZmY7IGJvcmRlci1yYWRpdXM6MTJweDsgbWF4LXdpZHRoOjQyMHB4OyB3aWR0aDoxMDAlOyBib3gtc2hhZG93OjAgMjBweCA1MHB4IHJnYmEoMCwwLDAsMC4yNSk7IHBhZGRpbmc6MjJweCAyNHB4OyBib3JkZXI6MXB4IHNvbGlkICNkOWUyZWM7Ij4KICAgIDxoMyBzdHlsZT0ibWFyZ2luOjAgMCA2cHg7IGNvbG9yOiMwZjNkNTY7Ij5HZW5lcmFyIHJlcG9ydGVzPC9oMz4KICAgIDxwIGNsYXNzPSJtdXRlZCIgc3R5bGU9Im1hcmdpbjowIDAgMTRweDsgZm9udC1zaXplOjAuOXJlbTsiPlNlbGVjY2lvbmUgdW5hIG8gdmFyaWFzIMOhcmVhcy4gU2UgZGVzY2FyZ2Fyw6EgLm1kICgrIC54bHN4IGVuIHJlc3VsdGFkb3MpIG8gdW4gLnppcCBzaSBoYXkgdmFyaW9zIGFyY2hpdm9zLjwvcD4KICAgIDxmb3JtIGlkPSJyZXBvcnRlcy1mb3JtIj4KICAgICAgPGxhYmVsIHN0eWxlPSJkaXNwbGF5OmZsZXg7IGdhcDoxMHB4OyBhbGlnbi1pdGVtczpjZW50ZXI7IG1hcmdpbjo4cHggMDsgZm9udC13ZWlnaHQ6NjAwOyI+CiAgICAgICAgPGlucHV0IHR5cGU9ImNoZWNrYm94IiBuYW1lPSJhcmVhcyIgdmFsdWU9ImFkbWluIj4gQWRtaW5pc3RyYWNpw7NuCiAgICAgIDwvbGFiZWw+CiAgICAgIDxsYWJlbCBzdHlsZT0iZGlzcGxheTpmbGV4OyBnYXA6MTBweDsgYWxpZ24taXRlbXM6Y2VudGVyOyBtYXJnaW46OHB4IDA7IGZvbnQtd2VpZ2h0OjYwMDsiPgogICAgICAgIDxpbnB1dCB0eXBlPSJjaGVja2JveCIgbmFtZT0iYXJlYXMiIHZhbHVlPSJwZ2MiIGNoZWNrZWQ+IFBHQwogICAgICA8L2xhYmVsPgogICAgICA8bGFiZWwgc3R5bGU9ImRpc3BsYXk6ZmxleDsgZ2FwOjEwcHg7IGFsaWduLWl0ZW1zOmNlbnRlcjsgbWFyZ2luOjhweCAwOyBmb250LXdlaWdodDo2MDA7Ij4KICAgICAgICA8aW5wdXQgdHlwZT0iY2hlY2tib3giIG5hbWU9ImFyZWFzIiB2YWx1ZT0icGdvIj4gUEdPCiAgICAgIDwvbGFiZWw+CiAgICAgIDxsYWJlbCBzdHlsZT0iZGlzcGxheTpmbGV4OyBnYXA6MTBweDsgYWxpZ24taXRlbXM6Y2VudGVyOyBtYXJnaW46OHB4IDA7IGZvbnQtd2VpZ2h0OjYwMDsiPgogICAgICAgIDxpbnB1dCB0eXBlPSJjaGVja2JveCIgbmFtZT0iYXJlYXMiIHZhbHVlPSJyaXNrIj4gQi4gUmllc2dvCiAgICAgIDwvbGFiZWw+CiAgICAgIDxwIGlkPSJyZXBvcnRlcy1lcnJvciIgc3R5bGU9ImNvbG9yOiNiOTFjMWM7IGZvbnQtc2l6ZTowLjg4cmVtOyBtaW4taGVpZ2h0OjEuMmVtOyBtYXJnaW46MTBweCAwIDA7Ij48L3A+CiAgICAgIDxwIGlkPSJyZXBvcnRlcy1zdGF0dXMiIGNsYXNzPSJtdXRlZCIgc3R5bGU9ImZvbnQtc2l6ZTowLjg4cmVtOyBtaW4taGVpZ2h0OjEuMmVtOyBtYXJnaW46NHB4IDAgMTJweDsiPjwvcD4KICAgICAgPGRpdiBzdHlsZT0iZGlzcGxheTpmbGV4OyBnYXA6MTBweDsganVzdGlmeS1jb250ZW50OmZsZXgtZW5kOyI+CiAgICAgICAgPGJ1dHRvbiB0eXBlPSJidXR0b24iIGRhdGEtcmVwb3J0ZXMtY2xvc2Ugc3R5bGU9InBhZGRpbmc6OHB4IDE0cHg7IGJvcmRlci1yYWRpdXM6OHB4OyBib3JkZXI6MXB4IHNvbGlkICM5NGEzYjg7IGJhY2tncm91bmQ6I2YxZjVmOTsgY29sb3I6IzBmMTcyYTsgY3Vyc29yOnBvaW50ZXI7IGZvbnQtd2VpZ2h0OjYwMDsiPkNhbmNlbGFyPC9idXR0b24+CiAgICAgICAgPGJ1dHRvbiB0eXBlPSJzdWJtaXQiIGlkPSJyZXBvcnRlcy1nZW5lcmF0ZSIgc3R5bGU9InBhZGRpbmc6OHB4IDE0cHg7IGJvcmRlci1yYWRpdXM6OHB4OyBib3JkZXI6bm9uZTsgYmFja2dyb3VuZDojMGY3NjZlOyBjb2xvcjojZmZmOyBjdXJzb3I6cG9pbnRlcjsgZm9udC13ZWlnaHQ6NjAwOyI+R2VuZXJhcjwvYnV0dG9uPgogICAgICA8L2Rpdj4KICAgIDwvZm9ybT4KICA8L2Rpdj4KPC9kaXY+CnslIGVuZGJsb2NrICV9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgc/ingresos.html
PATH_JSON="templates/pgc/ingresos.html"
FILENAME=ingresos.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=305
SIZE_BYTES_UTF8=11026
CONTENT_SHA256=e12971ca1b05f779412e6bafda7d3ee60f458ed05dc379e3d5634a098ab9e849
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

{% block title %}Ingresos vs meta{% endblock %}

{% block content %}
<style>
  .group_separator td {
        padding: 0;
        height: 14px;
        border-bottom: none;
        background: #ffffff;
  }
  .ingresos-metodo-cell {
    font-family: "Arial Narrow", Arial, sans-serif;
    font-size: 0.85rem;
  }
  .ingresos-observacion-cell {
    font-family: "Arial Narrow", Arial, sans-serif;
    font-size: 0.75rem;
  }
  .currency-hint {
    font-size: 0.85rem;
    color: #64748b;
    margin: 0 0 12px;
  }
  .amt-usd::before {
    content: none;
  }
  .tc-badge {
    display: inline-block;
    font-weight: 700;
    font-size: 0.78rem;
    color: #0f766e;
    background: #ccfbf1;
    border: 1px solid #99f6e4;
    border-radius: 4px;
    padding: 1px 6px;
    margin-right: 6px;
    white-space: nowrap;
  }
  .gtq-ref {
    display: block;
    margin-top: 2px;
    font-size: 0.72rem;
    color: #64748b;
    font-weight: 500;
  }
  .usd-official {
    font-variant-numeric: tabular-nums;
  }
  @media (max-width: 720px) {
    .ingresos-col-full { display: none; }
  }
</style>
<div class="card">
  <div class="wcg-report-head" style="margin-top:0;">
    <h2 style="margin:0;">Ingresos vs meta</h2>
    {% include "includes/module_mark.html" with module="pgc" %}
  </div>
  <p class="muted">
    Meta y resultado mensual de ingresos por UNE y periodo.
  </p>
  <p class="currency-hint">Montos oficiales en USD (cifras en miles de US$).</p>

  <form method="get" class="filters">
      <div>
          <label for="start_year">Año inicial</label><br>
          <select name="start_year" id="start_year">
              {% for p in available_periods %}
                  <option value="{{ p.year }}" {% if report_filter.start_year == p.year and report_filter.start_month == p.month %}selected{% endif %}>
                      {{ p.year }}
                  </option>
              {% endfor %}
          </select>
      </div>
  
      <div>
          <label for="start_month">Mes inicial</label><br>
          <select name="start_month" id="start_month">
              {% for p in available_periods %}
                  <option value="{{ p.month }}" {% if report_filter.start_year == p.year and report_filter.start_month == p.month %}selected{% endif %}>
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
        <th>Periodo</th>
        <th title="Meta en USD">Meta USD</th>
        <th title="Real en USD (oficial)">Real USD</th>
        <th title="Diferencia en USD">Dif. USD</th>
        <th>Cumple</th>
        <th class="ingresos-col-full">Método de cálculo</th>
        <th style="text-align:left;">Observación</th>
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
                    <td style="text-align:left;">{{ row.target.une.name_es|default:row.target.une.name_es }}</td>
                    <td>{{ row.target.year }}-{{ row.target.month|stringformat:"02d" }}</td>
                    <td class="usd-official">
                        {% if row.meta is not None %}
                            {% if row.target.une.code == "INSURANCE" %}
                                ${{ row.meta|floatformat:3|unlocalize }}
                            {% else %}
                                ${{ row.meta|floatformat:0|unlocalize }}
                            {% endif %}
                        {% else %}
                            -
                        {% endif %}
                    </td>
                    <td class="usd-official">
                        {% if row.real is not None %}
                            {% if row.target.une.code == "INSURANCE" %}
                                ${{ row.real|floatformat:3|unlocalize }}
                            {% else %}
                                ${{ row.real|floatformat:0|unlocalize }}
                            {% endif %}
                            {% if row.source_gtq is not None %}
                            <span class="gtq-ref" title="Captura manual en GTQ (referencia; el score usa USD)">
                              ref Q{{ row.source_gtq|floatformat:2|unlocalize }}
                            </span>
                            {% endif %}
                        {% else %}
                            -
                        {% endif %}
                    </td>
                    <td class="usd-official">
                        {% if row.diferencia is not None %}
                            {% if row.target.une.code == "INSURANCE" %}
                                ${{ row.diferencia|floatformat:3|unlocalize }}
                            {% else %}
                                ${{ row.diferencia|floatformat:0|unlocalize }}
                            {% endif %}
                        {% else %}
                            -
                        {% endif %}
                    </td>
                    <td>
                        {% if row.cumple %}
                            <span class="ok">Sí</span>
                        {% else %}
                            <span class="bad">No</span>
                        {% endif %}
                    </td>
                    <td class="ingresos-metodo-cell ingresos-col-full">{{ row.metodo }}</td>
                    <td class="ingresos-observacion-cell" style="text-align:left">
                      {% if row.tc_label %}
                        <span class="tc-badge">{{ row.tc_label }}</span>
                      {% endif %}
                      {% if row.observacion_base %}
                        {{ row.observacion_base }}
                      {% elif not row.tc_label %}
                        -
                      {% endif %}
                    </td>
                </tr>
            {% endif %}
        {% empty %}
            <tr>
                <td colspan="8">No hay datos de ingresos para los filtros seleccionados.</td>
            </tr>
        {% endfor %}
    </tbody>
  </table>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
    const startYear  = document.getElementById("start_year");
    const startMonth = document.getElementById("start_month");
    const sort       = document.getElementById("sort");
    const dateOrder  = document.getElementById("date_order");
    const groupMode  = document.getElementById("group_mode");
    const btn        = document.getElementById("btn-export-md");

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
        if (typeof syncSortFields === "function") syncSortFields();
        if (filterForm) filterForm.submit();
    }

    if (sort) {
        sort.addEventListener("change", applyFilters);
        syncSortFields();
    }

    ["month_count", "start_year", "start_month"].forEach(function (id) {
        const el = document.getElementById(id);
        if (el && el.tagName === "SELECT") {
            el.addEventListener("change", applyFilters);
        }
    });

    if (!btn) return;

    btn.addEventListener("click", async function () {
        // Aseguramos que los campos ocultos reflejen el sort actual
        syncSortFields();

        const params = new URLSearchParams({
            start_year:  startYear?.value  || "",
            start_month: startMonth?.value || "",
            month_count: document.getElementById("month_count")?.value || "",
            date_order:  dateOrder?.value  || "asc",
            group_mode:  groupMode?.value  || "une"
        });

        const url = `{% url 'pgc:ingresos_export_md' %}?` + params.toString();

        btn.disabled = true;
        const originalText = btn.textContent;
        btn.textContent = "Generando...";

        try {
            const response = await fetch(url, {
                method: "GET",
                headers: { "Accept": "text/markdown, text/plain, */*" },
            });
            if (!response.ok) throw new Error("HTTP " + response.status);
            const blob = await response.blob();
            const cd = response.headers.get("Content-Disposition") || "";
            let filename = "pgc-ingresos.md";
            const m = /filename=\"?([^\";]+)\"?/i.exec(cd);
            if (m) filename = m[1];
            const a = document.createElement("a");
            a.href = URL.createObjectURL(blob);
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(a.href);
        } catch (err) {
            alert("No se pudo exportar: " + err.message);
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
00004|{% block title %}Ingresos vs meta{% endblock %}
00005|
00006|{% block content %}
00007|<style>
00008|  .group_separator td {
00009|        padding: 0;
00010|        height: 14px;
00011|        border-bottom: none;
00012|        background: #ffffff;
00013|  }
00014|  .ingresos-metodo-cell {
00015|    font-family: "Arial Narrow", Arial, sans-serif;
00016|    font-size: 0.85rem;
00017|  }
00018|  .ingresos-observacion-cell {
00019|    font-family: "Arial Narrow", Arial, sans-serif;
00020|    font-size: 0.75rem;
00021|  }
00022|  .currency-hint {
00023|    font-size: 0.85rem;
00024|    color: #64748b;
00025|    margin: 0 0 12px;
00026|  }
00027|  .amt-usd::before {
00028|    content: none;
00029|  }
00030|  .tc-badge {
00031|    display: inline-block;
00032|    font-weight: 700;
00033|    font-size: 0.78rem;
00034|    color: #0f766e;
00035|    background: #ccfbf1;
00036|    border: 1px solid #99f6e4;
00037|    border-radius: 4px;
00038|    padding: 1px 6px;
00039|    margin-right: 6px;
00040|    white-space: nowrap;
00041|  }
00042|  .gtq-ref {
00043|    display: block;
00044|    margin-top: 2px;
00045|    font-size: 0.72rem;
00046|    color: #64748b;
00047|    font-weight: 500;
00048|  }
00049|  .usd-official {
00050|    font-variant-numeric: tabular-nums;
00051|  }
00052|  @media (max-width: 720px) {
00053|    .ingresos-col-full { display: none; }
00054|  }
00055|</style>
00056|<div class="card">
00057|  <div class="wcg-report-head" style="margin-top:0;">
00058|    <h2 style="margin:0;">Ingresos vs meta</h2>
00059|    {% include "includes/module_mark.html" with module="pgc" %}
00060|  </div>
00061|  <p class="muted">
00062|    Meta y resultado mensual de ingresos por UNE y periodo.
00063|  </p>
00064|  <p class="currency-hint">Montos oficiales en USD (cifras en miles de US$).</p>
00065|
00066|  <form method="get" class="filters">
00067|      <div>
00068|          <label for="start_year">Año inicial</label><br>
00069|          <select name="start_year" id="start_year">
00070|              {% for p in available_periods %}
00071|                  <option value="{{ p.year }}" {% if report_filter.start_year == p.year and report_filter.start_month == p.month %}selected{% endif %}>
00072|                      {{ p.year }}
00073|                  </option>
00074|              {% endfor %}
00075|          </select>
00076|      </div>
00077|  
00078|      <div>
00079|          <label for="start_month">Mes inicial</label><br>
00080|          <select name="start_month" id="start_month">
00081|              {% for p in available_periods %}
00082|                  <option value="{{ p.month }}" {% if report_filter.start_year == p.year and report_filter.start_month == p.month %}selected{% endif %}>
00083|                      {{ p.month|stringformat:"02d" }}
00084|                  </option>
00085|              {% endfor %}
00086|          </select>
00087|      </div>
00088|  
00089|      <div>
00090|          <label for="month_count">Cantidad de meses</label><br>
00091|          <select name="month_count" id="month_count">
00092|              {% for opt in month_count_options %}
00093|                  <option value="{{ opt }}" {% if report_filter.month_count == opt %}selected{% endif %}>
00094|                      {{ opt }}
00095|                  </option>
00096|              {% endfor %}
00097|          </select>
00098|      </div>
00099|  
00100|      <div>
00101|        <label for="sort">Sort</label><br>
00102|        <select id="sort">
00103|          <option value="unes"
00104|            {% if report_sort.group_mode == "une" %}selected{% endif %}>
00105|            UNEs
00106|          </option>
00107|          <option value="fechas_asc"
00108|            {% if report_sort.group_mode == "period" and report_sort.date_order == "asc" %}selected{% endif %}>
00109|            Fechas ascendentes
00110|          </option>
00111|          <option value="fechas_desc"
00112|            {% if report_sort.group_mode == "period" and report_sort.date_order == "desc" %}selected{% endif %}>
00113|            Fechas descendentes
00114|          </option>
00115|        </select>
00116|        <input type="hidden" name="date_order" id="date_order"
00117|               value="{% if report_sort.group_mode == 'period' and report_sort.date_order == 'desc' %}desc{% else %}asc{% endif %}">
00118|        <input type="hidden" name="group_mode" id="group_mode"
00119|               value="{% if report_sort.group_mode == 'period' %}period{% else %}une{% endif %}">
00120|      </div>
00121|  
00122|      <div style="align-self:end;">
00123|          <button type="button" id="btn-export-md">.md export</button>
00124|      </div>
00125|  </form>
00126|  
00127|  <table>
00128|    <thead>
00129|      <tr>
00130|        <th style="text-align:left;">UNE</th>
00131|        <th>Periodo</th>
00132|        <th title="Meta en USD">Meta USD</th>
00133|        <th title="Real en USD (oficial)">Real USD</th>
00134|        <th title="Diferencia en USD">Dif. USD</th>
00135|        <th>Cumple</th>
00136|        <th class="ingresos-col-full">Método de cálculo</th>
00137|        <th style="text-align:left;">Observación</th>
00138|      </tr>
00139|    </thead>
00140|    <tbody>
00141|        {% for row in rows %}
00142|            {% if row.is_separator %}
00143|                <tr class="group_separator">
00144|                    <td colspan="8"></td>
00145|                </tr>
00146|            {% else %}
00147|                <tr>
00148|                    <td style="text-align:left;">{{ row.target.une.name_es|default:row.target.une.name_es }}</td>
00149|                    <td>{{ row.target.year }}-{{ row.target.month|stringformat:"02d" }}</td>
00150|                    <td class="usd-official">
00151|                        {% if row.meta is not None %}
00152|                            {% if row.target.une.code == "INSURANCE" %}
00153|                                ${{ row.meta|floatformat:3|unlocalize }}
00154|                            {% else %}
00155|                                ${{ row.meta|floatformat:0|unlocalize }}
00156|                            {% endif %}
00157|                        {% else %}
00158|                            -
00159|                        {% endif %}
00160|                    </td>
00161|                    <td class="usd-official">
00162|                        {% if row.real is not None %}
00163|                            {% if row.target.une.code == "INSURANCE" %}
00164|                                ${{ row.real|floatformat:3|unlocalize }}
00165|                            {% else %}
00166|                                ${{ row.real|floatformat:0|unlocalize }}
00167|                            {% endif %}
00168|                            {% if row.source_gtq is not None %}
00169|                            <span class="gtq-ref" title="Captura manual en GTQ (referencia; el score usa USD)">
00170|                              ref Q{{ row.source_gtq|floatformat:2|unlocalize }}
00171|                            </span>
00172|                            {% endif %}
00173|                        {% else %}
00174|                            -
00175|                        {% endif %}
00176|                    </td>
00177|                    <td class="usd-official">
00178|                        {% if row.diferencia is not None %}
00179|                            {% if row.target.une.code == "INSURANCE" %}
00180|                                ${{ row.diferencia|floatformat:3|unlocalize }}
00181|                            {% else %}
00182|                                ${{ row.diferencia|floatformat:0|unlocalize }}
00183|                            {% endif %}
00184|                        {% else %}
00185|                            -
00186|                        {% endif %}
00187|                    </td>
00188|                    <td>
00189|                        {% if row.cumple %}
00190|                            <span class="ok">Sí</span>
00191|                        {% else %}
00192|                            <span class="bad">No</span>
00193|                        {% endif %}
00194|                    </td>
00195|                    <td class="ingresos-metodo-cell ingresos-col-full">{{ row.metodo }}</td>
00196|                    <td class="ingresos-observacion-cell" style="text-align:left">
00197|                      {% if row.tc_label %}
00198|                        <span class="tc-badge">{{ row.tc_label }}</span>
00199|                      {% endif %}
00200|                      {% if row.observacion_base %}
00201|                        {{ row.observacion_base }}
00202|                      {% elif not row.tc_label %}
00203|                        -
00204|                      {% endif %}
00205|                    </td>
00206|                </tr>
00207|            {% endif %}
00208|        {% empty %}
00209|            <tr>
00210|                <td colspan="8">No hay datos de ingresos para los filtros seleccionados.</td>
00211|            </tr>
00212|        {% endfor %}
00213|    </tbody>
00214|  </table>
00215|</div>
00216|
00217|<script>
00218|document.addEventListener("DOMContentLoaded", function () {
00219|    const startYear  = document.getElementById("start_year");
00220|    const startMonth = document.getElementById("start_month");
00221|    const sort       = document.getElementById("sort");
00222|    const dateOrder  = document.getElementById("date_order");
00223|    const groupMode  = document.getElementById("group_mode");
00224|    const btn        = document.getElementById("btn-export-md");
00225|
00226|    function syncSortFields() {
00227|        if (!sort) return;
00228|        if (sort.value === "unes") {
00229|            groupMode.value = "une";
00230|            dateOrder.value = "asc";
00231|        } else if (sort.value === "fechas_desc") {
00232|            groupMode.value = "period";
00233|            dateOrder.value = "desc";
00234|        } else {
00235|            groupMode.value = "period";
00236|            dateOrder.value = "asc";
00237|        }
00238|    }
00239|
00240|    const filterForm = document.querySelector("form.filters");
00241|    function applyFilters() {
00242|        if (typeof syncSortFields === "function") syncSortFields();
00243|        if (filterForm) filterForm.submit();
00244|    }
00245|
00246|    if (sort) {
00247|        sort.addEventListener("change", applyFilters);
00248|        syncSortFields();
00249|    }
00250|
00251|    ["month_count", "start_year", "start_month"].forEach(function (id) {
00252|        const el = document.getElementById(id);
00253|        if (el && el.tagName === "SELECT") {
00254|            el.addEventListener("change", applyFilters);
00255|        }
00256|    });
00257|
00258|    if (!btn) return;
00259|
00260|    btn.addEventListener("click", async function () {
00261|        // Aseguramos que los campos ocultos reflejen el sort actual
00262|        syncSortFields();
00263|
00264|        const params = new URLSearchParams({
00265|            start_year:  startYear?.value  || "",
00266|            start_month: startMonth?.value || "",
00267|            month_count: document.getElementById("month_count")?.value || "",
00268|            date_order:  dateOrder?.value  || "asc",
00269|            group_mode:  groupMode?.value  || "une"
00270|        });
00271|
00272|        const url = `{% url 'pgc:ingresos_export_md' %}?` + params.toString();
00273|
00274|        btn.disabled = true;
00275|        const originalText = btn.textContent;
00276|        btn.textContent = "Generando...";
00277|
00278|        try {
00279|            const response = await fetch(url, {
00280|                method: "GET",
00281|                headers: { "Accept": "text/markdown, text/plain, */*" },
00282|            });
00283|            if (!response.ok) throw new Error("HTTP " + response.status);
00284|            const blob = await response.blob();
00285|            const cd = response.headers.get("Content-Disposition") || "";
00286|            let filename = "pgc-ingresos.md";
00287|            const m = /filename=\"?([^\";]+)\"?/i.exec(cd);
00288|            if (m) filename = m[1];
00289|            const a = document.createElement("a");
00290|            a.href = URL.createObjectURL(blob);
00291|            a.download = filename;
00292|            document.body.appendChild(a);
00293|            a.click();
00294|            a.remove();
00295|            URL.revokeObjectURL(a.href);
00296|        } catch (err) {
00297|            alert("No se pudo exportar: " + err.message);
00298|        } finally {
00299|            btn.disabled = false;
00300|            btn.textContent = originalText;
00301|        }
00302|    });
00303|});
00304|</script>
00305|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZS5odG1sIiAlfQp7JSBsb2FkIGwxMG4gJX0KCnslIGJsb2NrIHRpdGxlICV9SW5ncmVzb3MgdnMgbWV0YXslIGVuZGJsb2NrICV9Cgp7JSBibG9jayBjb250ZW50ICV9CjxzdHlsZT4KICAuZ3JvdXBfc2VwYXJhdG9yIHRkIHsKICAgICAgICBwYWRkaW5nOiAwOwogICAgICAgIGhlaWdodDogMTRweDsKICAgICAgICBib3JkZXItYm90dG9tOiBub25lOwogICAgICAgIGJhY2tncm91bmQ6ICNmZmZmZmY7CiAgfQogIC5pbmdyZXNvcy1tZXRvZG8tY2VsbCB7CiAgICBmb250LWZhbWlseTogIkFyaWFsIE5hcnJvdyIsIEFyaWFsLCBzYW5zLXNlcmlmOwogICAgZm9udC1zaXplOiAwLjg1cmVtOwogIH0KICAuaW5ncmVzb3Mtb2JzZXJ2YWNpb24tY2VsbCB7CiAgICBmb250LWZhbWlseTogIkFyaWFsIE5hcnJvdyIsIEFyaWFsLCBzYW5zLXNlcmlmOwogICAgZm9udC1zaXplOiAwLjc1cmVtOwogIH0KICAuY3VycmVuY3ktaGludCB7CiAgICBmb250LXNpemU6IDAuODVyZW07CiAgICBjb2xvcjogIzY0NzQ4YjsKICAgIG1hcmdpbjogMCAwIDEycHg7CiAgfQogIC5hbXQtdXNkOjpiZWZvcmUgewogICAgY29udGVudDogbm9uZTsKICB9CiAgLnRjLWJhZGdlIHsKICAgIGRpc3BsYXk6IGlubGluZS1ibG9jazsKICAgIGZvbnQtd2VpZ2h0OiA3MDA7CiAgICBmb250LXNpemU6IDAuNzhyZW07CiAgICBjb2xvcjogIzBmNzY2ZTsKICAgIGJhY2tncm91bmQ6ICNjY2ZiZjE7CiAgICBib3JkZXI6IDFweCBzb2xpZCAjOTlmNmU0OwogICAgYm9yZGVyLXJhZGl1czogNHB4OwogICAgcGFkZGluZzogMXB4IDZweDsKICAgIG1hcmdpbi1yaWdodDogNnB4OwogICAgd2hpdGUtc3BhY2U6IG5vd3JhcDsKICB9CiAgLmd0cS1yZWYgewogICAgZGlzcGxheTogYmxvY2s7CiAgICBtYXJnaW4tdG9wOiAycHg7CiAgICBmb250LXNpemU6IDAuNzJyZW07CiAgICBjb2xvcjogIzY0NzQ4YjsKICAgIGZvbnQtd2VpZ2h0OiA1MDA7CiAgfQogIC51c2Qtb2ZmaWNpYWwgewogICAgZm9udC12YXJpYW50LW51bWVyaWM6IHRhYnVsYXItbnVtczsKICB9CiAgQG1lZGlhIChtYXgtd2lkdGg6IDcyMHB4KSB7CiAgICAuaW5ncmVzb3MtY29sLWZ1bGwgeyBkaXNwbGF5OiBub25lOyB9CiAgfQo8L3N0eWxlPgo8ZGl2IGNsYXNzPSJjYXJkIj4KICA8ZGl2IGNsYXNzPSJ3Y2ctcmVwb3J0LWhlYWQiIHN0eWxlPSJtYXJnaW4tdG9wOjA7Ij4KICAgIDxoMiBzdHlsZT0ibWFyZ2luOjA7Ij5JbmdyZXNvcyB2cyBtZXRhPC9oMj4KICAgIHslIGluY2x1ZGUgImluY2x1ZGVzL21vZHVsZV9tYXJrLmh0bWwiIHdpdGggbW9kdWxlPSJwZ2MiICV9CiAgPC9kaXY+CiAgPHAgY2xhc3M9Im11dGVkIj4KICAgIE1ldGEgeSByZXN1bHRhZG8gbWVuc3VhbCBkZSBpbmdyZXNvcyBwb3IgVU5FIHkgcGVyaW9kby4KICA8L3A+CiAgPHAgY2xhc3M9ImN1cnJlbmN5LWhpbnQiPk1vbnRvcyBvZmljaWFsZXMgZW4gVVNEIChjaWZyYXMgZW4gbWlsZXMgZGUgVVMkKS48L3A+CgogIDxmb3JtIG1ldGhvZD0iZ2V0IiBjbGFzcz0iZmlsdGVycyI+CiAgICAgIDxkaXY+CiAgICAgICAgICA8bGFiZWwgZm9yPSJzdGFydF95ZWFyIj5Bw7FvIGluaWNpYWw8L2xhYmVsPjxicj4KICAgICAgICAgIDxzZWxlY3QgbmFtZT0ic3RhcnRfeWVhciIgaWQ9InN0YXJ0X3llYXIiPgogICAgICAgICAgICAgIHslIGZvciBwIGluIGF2YWlsYWJsZV9wZXJpb2RzICV9CiAgICAgICAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9Int7IHAueWVhciB9fSIgeyUgaWYgcmVwb3J0X2ZpbHRlci5zdGFydF95ZWFyID09IHAueWVhciBhbmQgcmVwb3J0X2ZpbHRlci5zdGFydF9tb250aCA9PSBwLm1vbnRoICV9c2VsZWN0ZWR7JSBlbmRpZiAlfT4KICAgICAgICAgICAgICAgICAgICAgIHt7IHAueWVhciB9fQogICAgICAgICAgICAgICAgICA8L29wdGlvbj4KICAgICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgIDwvc2VsZWN0PgogICAgICA8L2Rpdj4KICAKICAgICAgPGRpdj4KICAgICAgICAgIDxsYWJlbCBmb3I9InN0YXJ0X21vbnRoIj5NZXMgaW5pY2lhbDwvbGFiZWw+PGJyPgogICAgICAgICAgPHNlbGVjdCBuYW1lPSJzdGFydF9tb250aCIgaWQ9InN0YXJ0X21vbnRoIj4KICAgICAgICAgICAgICB7JSBmb3IgcCBpbiBhdmFpbGFibGVfcGVyaW9kcyAlfQogICAgICAgICAgICAgICAgICA8b3B0aW9uIHZhbHVlPSJ7eyBwLm1vbnRoIH19IiB7JSBpZiByZXBvcnRfZmlsdGVyLnN0YXJ0X3llYXIgPT0gcC55ZWFyIGFuZCByZXBvcnRfZmlsdGVyLnN0YXJ0X21vbnRoID09IHAubW9udGggJX1zZWxlY3RlZHslIGVuZGlmICV9PgogICAgICAgICAgICAgICAgICAgICAge3sgcC5tb250aHxzdHJpbmdmb3JtYXQ6IjAyZCIgfX0KICAgICAgICAgICAgICAgICAgPC9vcHRpb24+CiAgICAgICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgICA8L3NlbGVjdD4KICAgICAgPC9kaXY+CiAgCiAgICAgIDxkaXY+CiAgICAgICAgICA8bGFiZWwgZm9yPSJtb250aF9jb3VudCI+Q2FudGlkYWQgZGUgbWVzZXM8L2xhYmVsPjxicj4KICAgICAgICAgIDxzZWxlY3QgbmFtZT0ibW9udGhfY291bnQiIGlkPSJtb250aF9jb3VudCI+CiAgICAgICAgICAgICAgeyUgZm9yIG9wdCBpbiBtb250aF9jb3VudF9vcHRpb25zICV9CiAgICAgICAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9Int7IG9wdCB9fSIgeyUgaWYgcmVwb3J0X2ZpbHRlci5tb250aF9jb3VudCA9PSBvcHQgJX1zZWxlY3RlZHslIGVuZGlmICV9PgogICAgICAgICAgICAgICAgICAgICAge3sgb3B0IH19CiAgICAgICAgICAgICAgICAgIDwvb3B0aW9uPgogICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgPC9zZWxlY3Q+CiAgICAgIDwvZGl2PgogIAogICAgICA8ZGl2PgogICAgICAgIDxsYWJlbCBmb3I9InNvcnQiPlNvcnQ8L2xhYmVsPjxicj4KICAgICAgICA8c2VsZWN0IGlkPSJzb3J0Ij4KICAgICAgICAgIDxvcHRpb24gdmFsdWU9InVuZXMiCiAgICAgICAgICAgIHslIGlmIHJlcG9ydF9zb3J0Lmdyb3VwX21vZGUgPT0gInVuZSIgJX1zZWxlY3RlZHslIGVuZGlmICV9PgogICAgICAgICAgICBVTkVzCiAgICAgICAgICA8L29wdGlvbj4KICAgICAgICAgIDxvcHRpb24gdmFsdWU9ImZlY2hhc19hc2MiCiAgICAgICAgICAgIHslIGlmIHJlcG9ydF9zb3J0Lmdyb3VwX21vZGUgPT0gInBlcmlvZCIgYW5kIHJlcG9ydF9zb3J0LmRhdGVfb3JkZXIgPT0gImFzYyIgJX1zZWxlY3RlZHslIGVuZGlmICV9PgogICAgICAgICAgICBGZWNoYXMgYXNjZW5kZW50ZXMKICAgICAgICAgIDwvb3B0aW9uPgogICAgICAgICAgPG9wdGlvbiB2YWx1ZT0iZmVjaGFzX2Rlc2MiCiAgICAgICAgICAgIHslIGlmIHJlcG9ydF9zb3J0Lmdyb3VwX21vZGUgPT0gInBlcmlvZCIgYW5kIHJlcG9ydF9zb3J0LmRhdGVfb3JkZXIgPT0gImRlc2MiICV9c2VsZWN0ZWR7JSBlbmRpZiAlfT4KICAgICAgICAgICAgRmVjaGFzIGRlc2NlbmRlbnRlcwogICAgICAgICAgPC9vcHRpb24+CiAgICAgICAgPC9zZWxlY3Q+CiAgICAgICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0iZGF0ZV9vcmRlciIgaWQ9ImRhdGVfb3JkZXIiCiAgICAgICAgICAgICAgIHZhbHVlPSJ7JSBpZiByZXBvcnRfc29ydC5ncm91cF9tb2RlID09ICdwZXJpb2QnIGFuZCByZXBvcnRfc29ydC5kYXRlX29yZGVyID09ICdkZXNjJyAlfWRlc2N7JSBlbHNlICV9YXNjeyUgZW5kaWYgJX0iPgogICAgICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9Imdyb3VwX21vZGUiIGlkPSJncm91cF9tb2RlIgogICAgICAgICAgICAgICB2YWx1ZT0ieyUgaWYgcmVwb3J0X3NvcnQuZ3JvdXBfbW9kZSA9PSAncGVyaW9kJyAlfXBlcmlvZHslIGVsc2UgJX11bmV7JSBlbmRpZiAlfSI+CiAgICAgIDwvZGl2PgogIAogICAgICA8ZGl2IHN0eWxlPSJhbGlnbi1zZWxmOmVuZDsiPgogICAgICAgICAgPGJ1dHRvbiB0eXBlPSJidXR0b24iIGlkPSJidG4tZXhwb3J0LW1kIj4ubWQgZXhwb3J0PC9idXR0b24+CiAgICAgIDwvZGl2PgogIDwvZm9ybT4KICAKICA8dGFibGU+CiAgICA8dGhlYWQ+CiAgICAgIDx0cj4KICAgICAgICA8dGggc3R5bGU9InRleHQtYWxpZ246bGVmdDsiPlVORTwvdGg+CiAgICAgICAgPHRoPlBlcmlvZG88L3RoPgogICAgICAgIDx0aCB0aXRsZT0iTWV0YSBlbiBVU0QiPk1ldGEgVVNEPC90aD4KICAgICAgICA8dGggdGl0bGU9IlJlYWwgZW4gVVNEIChvZmljaWFsKSI+UmVhbCBVU0Q8L3RoPgogICAgICAgIDx0aCB0aXRsZT0iRGlmZXJlbmNpYSBlbiBVU0QiPkRpZi4gVVNEPC90aD4KICAgICAgICA8dGg+Q3VtcGxlPC90aD4KICAgICAgICA8dGggY2xhc3M9ImluZ3Jlc29zLWNvbC1mdWxsIj5Nw6l0b2RvIGRlIGPDoWxjdWxvPC90aD4KICAgICAgICA8dGggc3R5bGU9InRleHQtYWxpZ246bGVmdDsiPk9ic2VydmFjacOzbjwvdGg+CiAgICAgIDwvdHI+CiAgICA8L3RoZWFkPgogICAgPHRib2R5PgogICAgICAgIHslIGZvciByb3cgaW4gcm93cyAlfQogICAgICAgICAgICB7JSBpZiByb3cuaXNfc2VwYXJhdG9yICV9CiAgICAgICAgICAgICAgICA8dHIgY2xhc3M9Imdyb3VwX3NlcGFyYXRvciI+CiAgICAgICAgICAgICAgICAgICAgPHRkIGNvbHNwYW49IjgiPjwvdGQ+CiAgICAgICAgICAgICAgICA8L3RyPgogICAgICAgICAgICB7JSBlbHNlICV9CiAgICAgICAgICAgICAgICA8dHI+CiAgICAgICAgICAgICAgICAgICAgPHRkIHN0eWxlPSJ0ZXh0LWFsaWduOmxlZnQ7Ij57eyByb3cudGFyZ2V0LnVuZS5uYW1lX2VzfGRlZmF1bHQ6cm93LnRhcmdldC51bmUubmFtZV9lcyB9fTwvdGQ+CiAgICAgICAgICAgICAgICAgICAgPHRkPnt7IHJvdy50YXJnZXQueWVhciB9fS17eyByb3cudGFyZ2V0Lm1vbnRofHN0cmluZ2Zvcm1hdDoiMDJkIiB9fTwvdGQ+CiAgICAgICAgICAgICAgICAgICAgPHRkIGNsYXNzPSJ1c2Qtb2ZmaWNpYWwiPgogICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiByb3cubWV0YSBpcyBub3QgTm9uZSAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgaWYgcm93LnRhcmdldC51bmUuY29kZSA9PSAiSU5TVVJBTkNFIiAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICR7eyByb3cubWV0YXxmbG9hdGZvcm1hdDozfHVubG9jYWxpemUgfX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVsc2UgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAke3sgcm93Lm1ldGF8ZmxvYXRmb3JtYXQ6MHx1bmxvY2FsaXplIH19CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgICAgICAgICAgICAgICB7JSBlbHNlICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAtCiAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgICAgICAgICAgPC90ZD4KICAgICAgICAgICAgICAgICAgICA8dGQgY2xhc3M9InVzZC1vZmZpY2lhbCI+CiAgICAgICAgICAgICAgICAgICAgICAgIHslIGlmIHJvdy5yZWFsIGlzIG5vdCBOb25lICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiByb3cudGFyZ2V0LnVuZS5jb2RlID09ICJJTlNVUkFOQ0UiICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgJHt7IHJvdy5yZWFsfGZsb2F0Zm9ybWF0OjN8dW5sb2NhbGl6ZSB9fQogICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICR7eyByb3cucmVhbHxmbG9hdGZvcm1hdDowfHVubG9jYWxpemUgfX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiByb3cuc291cmNlX2d0cSBpcyBub3QgTm9uZSAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHNwYW4gY2xhc3M9Imd0cS1yZWYiIHRpdGxlPSJDYXB0dXJhIG1hbnVhbCBlbiBHVFEgKHJlZmVyZW5jaWE7IGVsIHNjb3JlIHVzYSBVU0QpIj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgcmVmIFF7eyByb3cuc291cmNlX2d0cXxmbG9hdGZvcm1hdDoyfHVubG9jYWxpemUgfX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvc3Bhbj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgICAgICAgICAgICAgIHslIGVsc2UgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIC0KICAgICAgICAgICAgICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgICAgICAgICAgICA8L3RkPgogICAgICAgICAgICAgICAgICAgIDx0ZCBjbGFzcz0idXNkLW9mZmljaWFsIj4KICAgICAgICAgICAgICAgICAgICAgICAgeyUgaWYgcm93LmRpZmVyZW5jaWEgaXMgbm90IE5vbmUgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgIHslIGlmIHJvdy50YXJnZXQudW5lLmNvZGUgPT0gIklOU1VSQU5DRSIgJX0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAke3sgcm93LmRpZmVyZW5jaWF8ZmxvYXRmb3JtYXQ6M3x1bmxvY2FsaXplIH19CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7JSBlbHNlICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgJHt7IHJvdy5kaWZlcmVuY2lhfGZsb2F0Zm9ybWF0OjB8dW5sb2NhbGl6ZSB9fQogICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgICAgICAgICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgLQogICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgICAgICAgICAgIDwvdGQ+CiAgICAgICAgICAgICAgICAgICAgPHRkPgogICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiByb3cuY3VtcGxlICV9CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8c3BhbiBjbGFzcz0ib2siPlPDrTwvc3Bhbj4KICAgICAgICAgICAgICAgICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgPHNwYW4gY2xhc3M9ImJhZCI+Tm88L3NwYW4+CiAgICAgICAgICAgICAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgICAgICAgICAgPC90ZD4KICAgICAgICAgICAgICAgICAgICA8dGQgY2xhc3M9ImluZ3Jlc29zLW1ldG9kby1jZWxsIGluZ3Jlc29zLWNvbC1mdWxsIj57eyByb3cubWV0b2RvIH19PC90ZD4KICAgICAgICAgICAgICAgICAgICA8dGQgY2xhc3M9ImluZ3Jlc29zLW9ic2VydmFjaW9uLWNlbGwiIHN0eWxlPSJ0ZXh0LWFsaWduOmxlZnQiPgogICAgICAgICAgICAgICAgICAgICAgeyUgaWYgcm93LnRjX2xhYmVsICV9CiAgICAgICAgICAgICAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJ0Yy1iYWRnZSI+e3sgcm93LnRjX2xhYmVsIH19PC9zcGFuPgogICAgICAgICAgICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgICAgICAgICAgICAgIHslIGlmIHJvdy5vYnNlcnZhY2lvbl9iYXNlICV9CiAgICAgICAgICAgICAgICAgICAgICAgIHt7IHJvdy5vYnNlcnZhY2lvbl9iYXNlIH19CiAgICAgICAgICAgICAgICAgICAgICB7JSBlbGlmIG5vdCByb3cudGNfbGFiZWwgJX0KICAgICAgICAgICAgICAgICAgICAgICAgLQogICAgICAgICAgICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgICAgICAgICAgICA8L3RkPgogICAgICAgICAgICAgICAgPC90cj4KICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICB7JSBlbXB0eSAlfQogICAgICAgICAgICA8dHI+CiAgICAgICAgICAgICAgICA8dGQgY29sc3Bhbj0iOCI+Tm8gaGF5IGRhdG9zIGRlIGluZ3Jlc29zIHBhcmEgbG9zIGZpbHRyb3Mgc2VsZWNjaW9uYWRvcy48L3RkPgogICAgICAgICAgICA8L3RyPgogICAgICAgIHslIGVuZGZvciAlfQogICAgPC90Ym9keT4KICA8L3RhYmxlPgo8L2Rpdj4KCjxzY3JpcHQ+CmRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoIkRPTUNvbnRlbnRMb2FkZWQiLCBmdW5jdGlvbiAoKSB7CiAgICBjb25zdCBzdGFydFllYXIgID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoInN0YXJ0X3llYXIiKTsKICAgIGNvbnN0IHN0YXJ0TW9udGggPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgic3RhcnRfbW9udGgiKTsKICAgIGNvbnN0IHNvcnQgICAgICAgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgic29ydCIpOwogICAgY29uc3QgZGF0ZU9yZGVyICA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJkYXRlX29yZGVyIik7CiAgICBjb25zdCBncm91cE1vZGUgID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImdyb3VwX21vZGUiKTsKICAgIGNvbnN0IGJ0biAgICAgICAgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiYnRuLWV4cG9ydC1tZCIpOwoKICAgIGZ1bmN0aW9uIHN5bmNTb3J0RmllbGRzKCkgewogICAgICAgIGlmICghc29ydCkgcmV0dXJuOwogICAgICAgIGlmIChzb3J0LnZhbHVlID09PSAidW5lcyIpIHsKICAgICAgICAgICAgZ3JvdXBNb2RlLnZhbHVlID0gInVuZSI7CiAgICAgICAgICAgIGRhdGVPcmRlci52YWx1ZSA9ICJhc2MiOwogICAgICAgIH0gZWxzZSBpZiAoc29ydC52YWx1ZSA9PT0gImZlY2hhc19kZXNjIikgewogICAgICAgICAgICBncm91cE1vZGUudmFsdWUgPSAicGVyaW9kIjsKICAgICAgICAgICAgZGF0ZU9yZGVyLnZhbHVlID0gImRlc2MiOwogICAgICAgIH0gZWxzZSB7CiAgICAgICAgICAgIGdyb3VwTW9kZS52YWx1ZSA9ICJwZXJpb2QiOwogICAgICAgICAgICBkYXRlT3JkZXIudmFsdWUgPSAiYXNjIjsKICAgICAgICB9CiAgICB9CgogICAgY29uc3QgZmlsdGVyRm9ybSA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoImZvcm0uZmlsdGVycyIpOwogICAgZnVuY3Rpb24gYXBwbHlGaWx0ZXJzKCkgewogICAgICAgIGlmICh0eXBlb2Ygc3luY1NvcnRGaWVsZHMgPT09ICJmdW5jdGlvbiIpIHN5bmNTb3J0RmllbGRzKCk7CiAgICAgICAgaWYgKGZpbHRlckZvcm0pIGZpbHRlckZvcm0uc3VibWl0KCk7CiAgICB9CgogICAgaWYgKHNvcnQpIHsKICAgICAgICBzb3J0LmFkZEV2ZW50TGlzdGVuZXIoImNoYW5nZSIsIGFwcGx5RmlsdGVycyk7CiAgICAgICAgc3luY1NvcnRGaWVsZHMoKTsKICAgIH0KCiAgICBbIm1vbnRoX2NvdW50IiwgInN0YXJ0X3llYXIiLCAic3RhcnRfbW9udGgiXS5mb3JFYWNoKGZ1bmN0aW9uIChpZCkgewogICAgICAgIGNvbnN0IGVsID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoaWQpOwogICAgICAgIGlmIChlbCAmJiBlbC50YWdOYW1lID09PSAiU0VMRUNUIikgewogICAgICAgICAgICBlbC5hZGRFdmVudExpc3RlbmVyKCJjaGFuZ2UiLCBhcHBseUZpbHRlcnMpOwogICAgICAgIH0KICAgIH0pOwoKICAgIGlmICghYnRuKSByZXR1cm47CgogICAgYnRuLmFkZEV2ZW50TGlzdGVuZXIoImNsaWNrIiwgYXN5bmMgZnVuY3Rpb24gKCkgewogICAgICAgIC8vIEFzZWd1cmFtb3MgcXVlIGxvcyBjYW1wb3Mgb2N1bHRvcyByZWZsZWplbiBlbCBzb3J0IGFjdHVhbAogICAgICAgIHN5bmNTb3J0RmllbGRzKCk7CgogICAgICAgIGNvbnN0IHBhcmFtcyA9IG5ldyBVUkxTZWFyY2hQYXJhbXMoewogICAgICAgICAgICBzdGFydF95ZWFyOiAgc3RhcnRZZWFyPy52YWx1ZSAgfHwgIiIsCiAgICAgICAgICAgIHN0YXJ0X21vbnRoOiBzdGFydE1vbnRoPy52YWx1ZSB8fCAiIiwKICAgICAgICAgICAgbW9udGhfY291bnQ6IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJtb250aF9jb3VudCIpPy52YWx1ZSB8fCAiIiwKICAgICAgICAgICAgZGF0ZV9vcmRlcjogIGRhdGVPcmRlcj8udmFsdWUgIHx8ICJhc2MiLAogICAgICAgICAgICBncm91cF9tb2RlOiAgZ3JvdXBNb2RlPy52YWx1ZSAgfHwgInVuZSIKICAgICAgICB9KTsKCiAgICAgICAgY29uc3QgdXJsID0gYHslIHVybCAncGdjOmluZ3Jlc29zX2V4cG9ydF9tZCcgJX0/YCArIHBhcmFtcy50b1N0cmluZygpOwoKICAgICAgICBidG4uZGlzYWJsZWQgPSB0cnVlOwogICAgICAgIGNvbnN0IG9yaWdpbmFsVGV4dCA9IGJ0bi50ZXh0Q29udGVudDsKICAgICAgICBidG4udGV4dENvbnRlbnQgPSAiR2VuZXJhbmRvLi4uIjsKCiAgICAgICAgdHJ5IHsKICAgICAgICAgICAgY29uc3QgcmVzcG9uc2UgPSBhd2FpdCBmZXRjaCh1cmwsIHsKICAgICAgICAgICAgICAgIG1ldGhvZDogIkdFVCIsCiAgICAgICAgICAgICAgICBoZWFkZXJzOiB7ICJBY2NlcHQiOiAidGV4dC9tYXJrZG93biwgdGV4dC9wbGFpbiwgKi8qIiB9LAogICAgICAgICAgICB9KTsKICAgICAgICAgICAgaWYgKCFyZXNwb25zZS5vaykgdGhyb3cgbmV3IEVycm9yKCJIVFRQICIgKyByZXNwb25zZS5zdGF0dXMpOwogICAgICAgICAgICBjb25zdCBibG9iID0gYXdhaXQgcmVzcG9uc2UuYmxvYigpOwogICAgICAgICAgICBjb25zdCBjZCA9IHJlc3BvbnNlLmhlYWRlcnMuZ2V0KCJDb250ZW50LURpc3Bvc2l0aW9uIikgfHwgIiI7CiAgICAgICAgICAgIGxldCBmaWxlbmFtZSA9ICJwZ2MtaW5ncmVzb3MubWQiOwogICAgICAgICAgICBjb25zdCBtID0gL2ZpbGVuYW1lPVwiPyhbXlwiO10rKVwiPy9pLmV4ZWMoY2QpOwogICAgICAgICAgICBpZiAobSkgZmlsZW5hbWUgPSBtWzFdOwogICAgICAgICAgICBjb25zdCBhID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgiYSIpOwogICAgICAgICAgICBhLmhyZWYgPSBVUkwuY3JlYXRlT2JqZWN0VVJMKGJsb2IpOwogICAgICAgICAgICBhLmRvd25sb2FkID0gZmlsZW5hbWU7CiAgICAgICAgICAgIGRvY3VtZW50LmJvZHkuYXBwZW5kQ2hpbGQoYSk7CiAgICAgICAgICAgIGEuY2xpY2soKTsKICAgICAgICAgICAgYS5yZW1vdmUoKTsKICAgICAgICAgICAgVVJMLnJldm9rZU9iamVjdFVSTChhLmhyZWYpOwogICAgICAgIH0gY2F0Y2ggKGVycikgewogICAgICAgICAgICBhbGVydCgiTm8gc2UgcHVkbyBleHBvcnRhcjogIiArIGVyci5tZXNzYWdlKTsKICAgICAgICB9IGZpbmFsbHkgewogICAgICAgICAgICBidG4uZGlzYWJsZWQgPSBmYWxzZTsKICAgICAgICAgICAgYnRuLnRleHRDb250ZW50ID0gb3JpZ2luYWxUZXh0OwogICAgICAgIH0KICAgIH0pOwp9KTsKPC9zY3JpcHQ+CnslIGVuZGJsb2NrICV9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgc/pgchome.html
PATH_JSON="templates/pgc/pgchome.html"
FILENAME=pgchome.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=33
SIZE_BYTES_UTF8=1611
CONTENT_SHA256=e407acd422d94b06111dfaddf6519d2238f2b5a9002dca13d1fa9e20ad34baf7
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
{% block title %}PGC — Módulo{% endblock %}
{% block module_nav %}
<nav class="mt-2 d-flex flex-wrap gap-2 small">
    <a href="{% url 'pgc:dashboard' %}">Tablero</a>
    <a href="{% url 'pgc:ingresos' %}">Ingresos vs meta</a>
    <a href="{% url 'pgc:clientes_nuevos' %}">Clientes</a>
    <a href="{% url 'pgc:venta_cruzada' %}">Venta cruzada</a>
    <a href="{% url 'pgc:respuesta_reqs' %}">Respuesta reqs</a>
</nav>
{% endblock %}
{% block content %}
<h1 class="mb-3">PGC — Planeación y cumplimiento</h1>
<p class="text-muted">Módulo existente integrado a WCG One. Las rutas históricas del PGC se mantienen en la raíz del sitio.</p>
<div class="card p-4">
    <h5>Accesos rápidos</h5>
    <div class="d-flex flex-wrap gap-2 mt-2">
        <a class="btn btn-primary" href="{% url 'pgc:dashboard' %}">Ir al tablero PGC</a>
        {% if user.is_superuser %}
        <a class="btn btn-outline-secondary" href="{% url 'pgc:admin_monthly' %}">Administración mensual</a>
        {% endif %}
    </div>
</div>
<div class="card mt-3 p-3 border-warning">
    <h6 class="text-warning">TODO — Integración PGC</h6>
    <ul class="small mb-0">
        <li>Mapear clientes PGC existentes → <code>core.Entidad</code> (script de sincronización)</li>
        <li>Enlazar <code>UnidadNegocio.une_pgc</code> con UNE del scoreboard</li>
        <li>Exponer métricas PGC en dashboard WCG One si se requiere vista unificada</li>
        <li>Migrar templates PGC a <code>base_wcg.html</code> gradualmente (hoy usan <code>base.html</code> legacy)</li>
    </ul>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}PGC — Módulo{% endblock %}
00003|{% block module_nav %}
00004|<nav class="mt-2 d-flex flex-wrap gap-2 small">
00005|    <a href="{% url 'pgc:dashboard' %}">Tablero</a>
00006|    <a href="{% url 'pgc:ingresos' %}">Ingresos vs meta</a>
00007|    <a href="{% url 'pgc:clientes_nuevos' %}">Clientes</a>
00008|    <a href="{% url 'pgc:venta_cruzada' %}">Venta cruzada</a>
00009|    <a href="{% url 'pgc:respuesta_reqs' %}">Respuesta reqs</a>
00010|</nav>
00011|{% endblock %}
00012|{% block content %}
00013|<h1 class="mb-3">PGC — Planeación y cumplimiento</h1>
00014|<p class="text-muted">Módulo existente integrado a WCG One. Las rutas históricas del PGC se mantienen en la raíz del sitio.</p>
00015|<div class="card p-4">
00016|    <h5>Accesos rápidos</h5>
00017|    <div class="d-flex flex-wrap gap-2 mt-2">
00018|        <a class="btn btn-primary" href="{% url 'pgc:dashboard' %}">Ir al tablero PGC</a>
00019|        {% if user.is_superuser %}
00020|        <a class="btn btn-outline-secondary" href="{% url 'pgc:admin_monthly' %}">Administración mensual</a>
00021|        {% endif %}
00022|    </div>
00023|</div>
00024|<div class="card mt-3 p-3 border-warning">
00025|    <h6 class="text-warning">TODO — Integración PGC</h6>
00026|    <ul class="small mb-0">
00027|        <li>Mapear clientes PGC existentes → <code>core.Entidad</code> (script de sincronización)</li>
00028|        <li>Enlazar <code>UnidadNegocio.une_pgc</code> con UNE del scoreboard</li>
00029|        <li>Exponer métricas PGC en dashboard WCG One si se requiere vista unificada</li>
00030|        <li>Migrar templates PGC a <code>base_wcg.html</code> gradualmente (hoy usan <code>base.html</code> legacy)</li>
00031|    </ul>
00032|</div>
00033|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1QR0Mg4oCUIE3Ds2R1bG97JSBlbmRibG9jayAlfQp7JSBibG9jayBtb2R1bGVfbmF2ICV9CjxuYXYgY2xhc3M9Im10LTIgZC1mbGV4IGZsZXgtd3JhcCBnYXAtMiBzbWFsbCI+CiAgICA8YSBocmVmPSJ7JSB1cmwgJ3BnYzpkYXNoYm9hcmQnICV9Ij5UYWJsZXJvPC9hPgogICAgPGEgaHJlZj0ieyUgdXJsICdwZ2M6aW5ncmVzb3MnICV9Ij5JbmdyZXNvcyB2cyBtZXRhPC9hPgogICAgPGEgaHJlZj0ieyUgdXJsICdwZ2M6Y2xpZW50ZXNfbnVldm9zJyAlfSI+Q2xpZW50ZXM8L2E+CiAgICA8YSBocmVmPSJ7JSB1cmwgJ3BnYzp2ZW50YV9jcnV6YWRhJyAlfSI+VmVudGEgY3J1emFkYTwvYT4KICAgIDxhIGhyZWY9InslIHVybCAncGdjOnJlc3B1ZXN0YV9yZXFzJyAlfSI+UmVzcHVlc3RhIHJlcXM8L2E+CjwvbmF2Pgp7JSBlbmRibG9jayAlfQp7JSBibG9jayBjb250ZW50ICV9CjxoMSBjbGFzcz0ibWItMyI+UEdDIOKAlCBQbGFuZWFjacOzbiB5IGN1bXBsaW1pZW50bzwvaDE+CjxwIGNsYXNzPSJ0ZXh0LW11dGVkIj5Nw7NkdWxvIGV4aXN0ZW50ZSBpbnRlZ3JhZG8gYSBXQ0cgT25lLiBMYXMgcnV0YXMgaGlzdMOzcmljYXMgZGVsIFBHQyBzZSBtYW50aWVuZW4gZW4gbGEgcmHDrXogZGVsIHNpdGlvLjwvcD4KPGRpdiBjbGFzcz0iY2FyZCBwLTQiPgogICAgPGg1PkFjY2Vzb3MgcsOhcGlkb3M8L2g1PgogICAgPGRpdiBjbGFzcz0iZC1mbGV4IGZsZXgtd3JhcCBnYXAtMiBtdC0yIj4KICAgICAgICA8YSBjbGFzcz0iYnRuIGJ0bi1wcmltYXJ5IiBocmVmPSJ7JSB1cmwgJ3BnYzpkYXNoYm9hcmQnICV9Ij5JciBhbCB0YWJsZXJvIFBHQzwvYT4KICAgICAgICB7JSBpZiB1c2VyLmlzX3N1cGVydXNlciAlfQogICAgICAgIDxhIGNsYXNzPSJidG4gYnRuLW91dGxpbmUtc2Vjb25kYXJ5IiBocmVmPSJ7JSB1cmwgJ3BnYzphZG1pbl9tb250aGx5JyAlfSI+QWRtaW5pc3RyYWNpw7NuIG1lbnN1YWw8L2E+CiAgICAgICAgeyUgZW5kaWYgJX0KICAgIDwvZGl2Pgo8L2Rpdj4KPGRpdiBjbGFzcz0iY2FyZCBtdC0zIHAtMyBib3JkZXItd2FybmluZyI+CiAgICA8aDYgY2xhc3M9InRleHQtd2FybmluZyI+VE9ETyDigJQgSW50ZWdyYWNpw7NuIFBHQzwvaDY+CiAgICA8dWwgY2xhc3M9InNtYWxsIG1iLTAiPgogICAgICAgIDxsaT5NYXBlYXIgY2xpZW50ZXMgUEdDIGV4aXN0ZW50ZXMg4oaSIDxjb2RlPmNvcmUuRW50aWRhZDwvY29kZT4gKHNjcmlwdCBkZSBzaW5jcm9uaXphY2nDs24pPC9saT4KICAgICAgICA8bGk+RW5sYXphciA8Y29kZT5VbmlkYWROZWdvY2lvLnVuZV9wZ2M8L2NvZGU+IGNvbiBVTkUgZGVsIHNjb3JlYm9hcmQ8L2xpPgogICAgICAgIDxsaT5FeHBvbmVyIG3DqXRyaWNhcyBQR0MgZW4gZGFzaGJvYXJkIFdDRyBPbmUgc2kgc2UgcmVxdWllcmUgdmlzdGEgdW5pZmljYWRhPC9saT4KICAgICAgICA8bGk+TWlncmFyIHRlbXBsYXRlcyBQR0MgYSA8Y29kZT5iYXNlX3djZy5odG1sPC9jb2RlPiBncmFkdWFsbWVudGUgKGhveSB1c2FuIDxjb2RlPmJhc2UuaHRtbDwvY29kZT4gbGVnYWN5KTwvbGk+CiAgICA8L3VsPgo8L2Rpdj4KeyUgZW5kYmxvY2sgJX0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
