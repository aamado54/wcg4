# CONCATENATED .HTML FILES

PART_NUMBER=5
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
PATH_LITERAL=templates/wcgone/crm/entidad_detail.html
PATH_JSON="templates/wcgone/crm/entidad_detail.html"
FILENAME=entidad_detail.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=116
SIZE_BYTES_UTF8=4643
CONTENT_SHA256=be760a43f71618275b50a5385fa4007fcf44c391e21ed4f5f93f29ffe0eb1ebe
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

{% block title %}{{ entidad.nombre }} — CRM — WCG One{% endblock %}

{% block content %}
<div class="mb-2">
  <a href="{% url 'wcgone_crm:entidad_list' %}" class="btn btn-sm btn-outline-secondary">← Volver a clientes</a>
</div>
<div class="d-flex justify-content-between align-items-start mb-3">
  <div>
    <h1 class="h4 fw-semibold mb-1">{{ entidad.nombre }}</h1>
    <p class="text-muted small mb-0">
      {{ entidad.get_tipo_entidad_display }}
      {% if entidad.nit %} · NIT {{ entidad.nit }}{% endif %}
      {% if entidad.ciudad %} · {{ entidad.ciudad }}{% endif %}
    </p>
  </div>
  {% if entidad.activo %}
  <span class="badge text-bg-success">Activo</span>
  {% else %}
  <span class="badge text-bg-secondary">Inactivo</span>
  {% endif %}
</div>

<div class="row g-3">
  <div class="col-lg-4">
    <div class="card border-0 shadow-sm h-100">
      <div class="card-header bg-white fw-semibold">Datos generales</div>
      <div class="card-body small">
        <dl class="row mb-0">
          <dt class="col-5">Comercial</dt><dd class="col-7">{{ entidad.nombre_comercial|default:"—" }}</dd>
          <dt class="col-5">Email</dt><dd class="col-7">{{ entidad.email|default:"—" }}</dd>
          <dt class="col-5">Teléfono</dt><dd class="col-7">{{ entidad.telefono|default:"—" }}</dd>
          <dt class="col-5">Sector</dt><dd class="col-7">{{ entidad.sector_economico|default:"—" }}</dd>
          <dt class="col-5">Riesgo</dt><dd class="col-7">{{ entidad.categoria_riesgo|default:"—" }}</dd>
        </dl>
        {% if entidad.notas %}
        <hr>
        <p class="mb-0 text-muted">{{ entidad.notas }}</p>
        {% endif %}
      </div>
    </div>
  </div>

  <div class="col-lg-8">
    <div class="card border-0 shadow-sm mb-3">
      <div class="card-header bg-white fw-semibold">Contactos</div>
      <div class="table-responsive">
        <table class="table table-sm mb-0">
          <thead><tr><th>Nombre</th><th>Cargo</th><th>Email</th><th>Teléfono</th></tr></thead>
          <tbody>
            {% for c in contactos %}
            <tr><td>{{ c.nombre }}</td><td>{{ c.cargo|default:"—" }}</td><td>{{ c.email|default:"—" }}</td><td>{{ c.telefono_movil|default:"—" }}</td></tr>
            {% empty %}
            <tr><td colspan="4" class="text-muted text-center py-3">Sin contactos.</td></tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>

    <div class="card border-0 shadow-sm mb-3">
      <div class="card-header bg-white fw-semibold">Productos relacionados</div>
      <div class="table-responsive">
        <table class="table table-sm mb-0">
          <thead><tr><th>Producto</th><th>Unidad</th><th>Estado</th><th>Inicio</th></tr></thead>
          <tbody>
            {% for rel in relaciones_producto %}
            <tr>
              <td>{{ rel.producto.nombre }}</td>
              <td>{{ rel.unidad_negocio|default:"—" }}</td>
              <td>{{ rel.estado|default:"—" }}</td>
              <td>{{ rel.fecha_inicio|date:"d/m/Y"|default:"—" }}</td>
            </tr>
            {% empty %}
            <tr><td colspan="4" class="text-muted text-center py-3">Sin productos relacionados.</td></tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>

    <div class="row g-3">
      <div class="col-md-6">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white fw-semibold">Interacciones recientes</div>
          <ul class="list-group list-group-flush small">
            {% for i in interacciones %}
            <li class="list-group-item">
              <strong>{{ i.fecha|date:"d/m/Y" }}</strong> — {{ i.tipo_interaccion }}: {{ i.resumen }}
            </li>
            {% empty %}
            <li class="list-group-item text-muted">Sin interacciones.</li>
            {% endfor %}
          </ul>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card border-0 shadow-sm h-100">
          <div class="card-header bg-white fw-semibold">Tareas abiertas</div>
          <ul class="list-group list-group-flush small">
            {% for t in tareas %}
            <li class="list-group-item">
              {{ t.descripcion|truncatechars:60 }}
              {% if t.fecha_limite %}<span class="text-muted">· {{ t.fecha_limite|date:"d/m/Y" }}</span>{% endif %}
            </li>
            {% empty %}
            <li class="list-group-item text-muted">Sin tareas pendientes.</li>
            {% endfor %}
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "wcgone_base.html" %}
00002|
00003|{% block title %}{{ entidad.nombre }} — CRM — WCG One{% endblock %}
00004|
00005|{% block content %}
00006|<div class="mb-2">
00007|  <a href="{% url 'wcgone_crm:entidad_list' %}" class="btn btn-sm btn-outline-secondary">← Volver a clientes</a>
00008|</div>
00009|<div class="d-flex justify-content-between align-items-start mb-3">
00010|  <div>
00011|    <h1 class="h4 fw-semibold mb-1">{{ entidad.nombre }}</h1>
00012|    <p class="text-muted small mb-0">
00013|      {{ entidad.get_tipo_entidad_display }}
00014|      {% if entidad.nit %} · NIT {{ entidad.nit }}{% endif %}
00015|      {% if entidad.ciudad %} · {{ entidad.ciudad }}{% endif %}
00016|    </p>
00017|  </div>
00018|  {% if entidad.activo %}
00019|  <span class="badge text-bg-success">Activo</span>
00020|  {% else %}
00021|  <span class="badge text-bg-secondary">Inactivo</span>
00022|  {% endif %}
00023|</div>
00024|
00025|<div class="row g-3">
00026|  <div class="col-lg-4">
00027|    <div class="card border-0 shadow-sm h-100">
00028|      <div class="card-header bg-white fw-semibold">Datos generales</div>
00029|      <div class="card-body small">
00030|        <dl class="row mb-0">
00031|          <dt class="col-5">Comercial</dt><dd class="col-7">{{ entidad.nombre_comercial|default:"—" }}</dd>
00032|          <dt class="col-5">Email</dt><dd class="col-7">{{ entidad.email|default:"—" }}</dd>
00033|          <dt class="col-5">Teléfono</dt><dd class="col-7">{{ entidad.telefono|default:"—" }}</dd>
00034|          <dt class="col-5">Sector</dt><dd class="col-7">{{ entidad.sector_economico|default:"—" }}</dd>
00035|          <dt class="col-5">Riesgo</dt><dd class="col-7">{{ entidad.categoria_riesgo|default:"—" }}</dd>
00036|        </dl>
00037|        {% if entidad.notas %}
00038|        <hr>
00039|        <p class="mb-0 text-muted">{{ entidad.notas }}</p>
00040|        {% endif %}
00041|      </div>
00042|    </div>
00043|  </div>
00044|
00045|  <div class="col-lg-8">
00046|    <div class="card border-0 shadow-sm mb-3">
00047|      <div class="card-header bg-white fw-semibold">Contactos</div>
00048|      <div class="table-responsive">
00049|        <table class="table table-sm mb-0">
00050|          <thead><tr><th>Nombre</th><th>Cargo</th><th>Email</th><th>Teléfono</th></tr></thead>
00051|          <tbody>
00052|            {% for c in contactos %}
00053|            <tr><td>{{ c.nombre }}</td><td>{{ c.cargo|default:"—" }}</td><td>{{ c.email|default:"—" }}</td><td>{{ c.telefono_movil|default:"—" }}</td></tr>
00054|            {% empty %}
00055|            <tr><td colspan="4" class="text-muted text-center py-3">Sin contactos.</td></tr>
00056|            {% endfor %}
00057|          </tbody>
00058|        </table>
00059|      </div>
00060|    </div>
00061|
00062|    <div class="card border-0 shadow-sm mb-3">
00063|      <div class="card-header bg-white fw-semibold">Productos relacionados</div>
00064|      <div class="table-responsive">
00065|        <table class="table table-sm mb-0">
00066|          <thead><tr><th>Producto</th><th>Unidad</th><th>Estado</th><th>Inicio</th></tr></thead>
00067|          <tbody>
00068|            {% for rel in relaciones_producto %}
00069|            <tr>
00070|              <td>{{ rel.producto.nombre }}</td>
00071|              <td>{{ rel.unidad_negocio|default:"—" }}</td>
00072|              <td>{{ rel.estado|default:"—" }}</td>
00073|              <td>{{ rel.fecha_inicio|date:"d/m/Y"|default:"—" }}</td>
00074|            </tr>
00075|            {% empty %}
00076|            <tr><td colspan="4" class="text-muted text-center py-3">Sin productos relacionados.</td></tr>
00077|            {% endfor %}
00078|          </tbody>
00079|        </table>
00080|      </div>
00081|    </div>
00082|
00083|    <div class="row g-3">
00084|      <div class="col-md-6">
00085|        <div class="card border-0 shadow-sm h-100">
00086|          <div class="card-header bg-white fw-semibold">Interacciones recientes</div>
00087|          <ul class="list-group list-group-flush small">
00088|            {% for i in interacciones %}
00089|            <li class="list-group-item">
00090|              <strong>{{ i.fecha|date:"d/m/Y" }}</strong> — {{ i.tipo_interaccion }}: {{ i.resumen }}
00091|            </li>
00092|            {% empty %}
00093|            <li class="list-group-item text-muted">Sin interacciones.</li>
00094|            {% endfor %}
00095|          </ul>
00096|        </div>
00097|      </div>
00098|      <div class="col-md-6">
00099|        <div class="card border-0 shadow-sm h-100">
00100|          <div class="card-header bg-white fw-semibold">Tareas abiertas</div>
00101|          <ul class="list-group list-group-flush small">
00102|            {% for t in tareas %}
00103|            <li class="list-group-item">
00104|              {{ t.descripcion|truncatechars:60 }}
00105|              {% if t.fecha_limite %}<span class="text-muted">· {{ t.fecha_limite|date:"d/m/Y" }}</span>{% endif %}
00106|            </li>
00107|            {% empty %}
00108|            <li class="list-group-item text-muted">Sin tareas pendientes.</li>
00109|            {% endfor %}
00110|          </ul>
00111|        </div>
00112|      </div>
00113|    </div>
00114|  </div>
00115|</div>
00116|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAid2Nnb25lX2Jhc2UuaHRtbCIgJX0KCnslIGJsb2NrIHRpdGxlICV9e3sgZW50aWRhZC5ub21icmUgfX0g4oCUIENSTSDigJQgV0NHIE9uZXslIGVuZGJsb2NrICV9Cgp7JSBibG9jayBjb250ZW50ICV9CjxkaXYgY2xhc3M9Im1iLTIiPgogIDxhIGhyZWY9InslIHVybCAnd2Nnb25lX2NybTplbnRpZGFkX2xpc3QnICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1zZWNvbmRhcnkiPuKGkCBWb2x2ZXIgYSBjbGllbnRlczwvYT4KPC9kaXY+CjxkaXYgY2xhc3M9ImQtZmxleCBqdXN0aWZ5LWNvbnRlbnQtYmV0d2VlbiBhbGlnbi1pdGVtcy1zdGFydCBtYi0zIj4KICA8ZGl2PgogICAgPGgxIGNsYXNzPSJoNCBmdy1zZW1pYm9sZCBtYi0xIj57eyBlbnRpZGFkLm5vbWJyZSB9fTwvaDE+CiAgICA8cCBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCBtYi0wIj4KICAgICAge3sgZW50aWRhZC5nZXRfdGlwb19lbnRpZGFkX2Rpc3BsYXkgfX0KICAgICAgeyUgaWYgZW50aWRhZC5uaXQgJX0gwrcgTklUIHt7IGVudGlkYWQubml0IH19eyUgZW5kaWYgJX0KICAgICAgeyUgaWYgZW50aWRhZC5jaXVkYWQgJX0gwrcge3sgZW50aWRhZC5jaXVkYWQgfX17JSBlbmRpZiAlfQogICAgPC9wPgogIDwvZGl2PgogIHslIGlmIGVudGlkYWQuYWN0aXZvICV9CiAgPHNwYW4gY2xhc3M9ImJhZGdlIHRleHQtYmctc3VjY2VzcyI+QWN0aXZvPC9zcGFuPgogIHslIGVsc2UgJX0KICA8c3BhbiBjbGFzcz0iYmFkZ2UgdGV4dC1iZy1zZWNvbmRhcnkiPkluYWN0aXZvPC9zcGFuPgogIHslIGVuZGlmICV9CjwvZGl2PgoKPGRpdiBjbGFzcz0icm93IGctMyI+CiAgPGRpdiBjbGFzcz0iY29sLWxnLTQiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20gaC0xMDAiPgogICAgICA8ZGl2IGNsYXNzPSJjYXJkLWhlYWRlciBiZy13aGl0ZSBmdy1zZW1pYm9sZCI+RGF0b3MgZ2VuZXJhbGVzPC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtYm9keSBzbWFsbCI+CiAgICAgICAgPGRsIGNsYXNzPSJyb3cgbWItMCI+CiAgICAgICAgICA8ZHQgY2xhc3M9ImNvbC01Ij5Db21lcmNpYWw8L2R0PjxkZCBjbGFzcz0iY29sLTciPnt7IGVudGlkYWQubm9tYnJlX2NvbWVyY2lhbHxkZWZhdWx0OiLigJQiIH19PC9kZD4KICAgICAgICAgIDxkdCBjbGFzcz0iY29sLTUiPkVtYWlsPC9kdD48ZGQgY2xhc3M9ImNvbC03Ij57eyBlbnRpZGFkLmVtYWlsfGRlZmF1bHQ6IuKAlCIgfX08L2RkPgogICAgICAgICAgPGR0IGNsYXNzPSJjb2wtNSI+VGVsw6lmb25vPC9kdD48ZGQgY2xhc3M9ImNvbC03Ij57eyBlbnRpZGFkLnRlbGVmb25vfGRlZmF1bHQ6IuKAlCIgfX08L2RkPgogICAgICAgICAgPGR0IGNsYXNzPSJjb2wtNSI+U2VjdG9yPC9kdD48ZGQgY2xhc3M9ImNvbC03Ij57eyBlbnRpZGFkLnNlY3Rvcl9lY29ub21pY298ZGVmYXVsdDoi4oCUIiB9fTwvZGQ+CiAgICAgICAgICA8ZHQgY2xhc3M9ImNvbC01Ij5SaWVzZ288L2R0PjxkZCBjbGFzcz0iY29sLTciPnt7IGVudGlkYWQuY2F0ZWdvcmlhX3JpZXNnb3xkZWZhdWx0OiLigJQiIH19PC9kZD4KICAgICAgICA8L2RsPgogICAgICAgIHslIGlmIGVudGlkYWQubm90YXMgJX0KICAgICAgICA8aHI+CiAgICAgICAgPHAgY2xhc3M9Im1iLTAgdGV4dC1tdXRlZCI+e3sgZW50aWRhZC5ub3RhcyB9fTwvcD4KICAgICAgICB7JSBlbmRpZiAlfQogICAgICA8L2Rpdj4KICAgIDwvZGl2PgogIDwvZGl2PgoKICA8ZGl2IGNsYXNzPSJjb2wtbGctOCI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSBtYi0zIj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIgYmctd2hpdGUgZnctc2VtaWJvbGQiPkNvbnRhY3RvczwvZGl2PgogICAgICA8ZGl2IGNsYXNzPSJ0YWJsZS1yZXNwb25zaXZlIj4KICAgICAgICA8dGFibGUgY2xhc3M9InRhYmxlIHRhYmxlLXNtIG1iLTAiPgogICAgICAgICAgPHRoZWFkPjx0cj48dGg+Tm9tYnJlPC90aD48dGg+Q2FyZ288L3RoPjx0aD5FbWFpbDwvdGg+PHRoPlRlbMOpZm9ubzwvdGg+PC90cj48L3RoZWFkPgogICAgICAgICAgPHRib2R5PgogICAgICAgICAgICB7JSBmb3IgYyBpbiBjb250YWN0b3MgJX0KICAgICAgICAgICAgPHRyPjx0ZD57eyBjLm5vbWJyZSB9fTwvdGQ+PHRkPnt7IGMuY2FyZ298ZGVmYXVsdDoi4oCUIiB9fTwvdGQ+PHRkPnt7IGMuZW1haWx8ZGVmYXVsdDoi4oCUIiB9fTwvdGQ+PHRkPnt7IGMudGVsZWZvbm9fbW92aWx8ZGVmYXVsdDoi4oCUIiB9fTwvdGQ+PC90cj4KICAgICAgICAgICAgeyUgZW1wdHkgJX0KICAgICAgICAgICAgPHRyPjx0ZCBjb2xzcGFuPSI0IiBjbGFzcz0idGV4dC1tdXRlZCB0ZXh0LWNlbnRlciBweS0zIj5TaW4gY29udGFjdG9zLjwvdGQ+PC90cj4KICAgICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgICA8L3Rib2R5PgogICAgICAgIDwvdGFibGU+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20gbWItMyI+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtaGVhZGVyIGJnLXdoaXRlIGZ3LXNlbWlib2xkIj5Qcm9kdWN0b3MgcmVsYWNpb25hZG9zPC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9InRhYmxlLXJlc3BvbnNpdmUiPgogICAgICAgIDx0YWJsZSBjbGFzcz0idGFibGUgdGFibGUtc20gbWItMCI+CiAgICAgICAgICA8dGhlYWQ+PHRyPjx0aD5Qcm9kdWN0bzwvdGg+PHRoPlVuaWRhZDwvdGg+PHRoPkVzdGFkbzwvdGg+PHRoPkluaWNpbzwvdGg+PC90cj48L3RoZWFkPgogICAgICAgICAgPHRib2R5PgogICAgICAgICAgICB7JSBmb3IgcmVsIGluIHJlbGFjaW9uZXNfcHJvZHVjdG8gJX0KICAgICAgICAgICAgPHRyPgogICAgICAgICAgICAgIDx0ZD57eyByZWwucHJvZHVjdG8ubm9tYnJlIH19PC90ZD4KICAgICAgICAgICAgICA8dGQ+e3sgcmVsLnVuaWRhZF9uZWdvY2lvfGRlZmF1bHQ6IuKAlCIgfX08L3RkPgogICAgICAgICAgICAgIDx0ZD57eyByZWwuZXN0YWRvfGRlZmF1bHQ6IuKAlCIgfX08L3RkPgogICAgICAgICAgICAgIDx0ZD57eyByZWwuZmVjaGFfaW5pY2lvfGRhdGU6ImQvbS9ZInxkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgICAgPC90cj4KICAgICAgICAgICAgeyUgZW1wdHkgJX0KICAgICAgICAgICAgPHRyPjx0ZCBjb2xzcGFuPSI0IiBjbGFzcz0idGV4dC1tdXRlZCB0ZXh0LWNlbnRlciBweS0zIj5TaW4gcHJvZHVjdG9zIHJlbGFjaW9uYWRvcy48L3RkPjwvdHI+CiAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgPC90Ym9keT4KICAgICAgICA8L3RhYmxlPgogICAgICA8L2Rpdj4KICAgIDwvZGl2PgoKICAgIDxkaXYgY2xhc3M9InJvdyBnLTMiPgogICAgICA8ZGl2IGNsYXNzPSJjb2wtbWQtNiI+CiAgICAgICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20gaC0xMDAiPgogICAgICAgICAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIgYmctd2hpdGUgZnctc2VtaWJvbGQiPkludGVyYWNjaW9uZXMgcmVjaWVudGVzPC9kaXY+CiAgICAgICAgICA8dWwgY2xhc3M9Imxpc3QtZ3JvdXAgbGlzdC1ncm91cC1mbHVzaCBzbWFsbCI+CiAgICAgICAgICAgIHslIGZvciBpIGluIGludGVyYWNjaW9uZXMgJX0KICAgICAgICAgICAgPGxpIGNsYXNzPSJsaXN0LWdyb3VwLWl0ZW0iPgogICAgICAgICAgICAgIDxzdHJvbmc+e3sgaS5mZWNoYXxkYXRlOiJkL20vWSIgfX08L3N0cm9uZz4g4oCUIHt7IGkudGlwb19pbnRlcmFjY2lvbiB9fToge3sgaS5yZXN1bWVuIH19CiAgICAgICAgICAgIDwvbGk+CiAgICAgICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgICAgIDxsaSBjbGFzcz0ibGlzdC1ncm91cC1pdGVtIHRleHQtbXV0ZWQiPlNpbiBpbnRlcmFjY2lvbmVzLjwvbGk+CiAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgPC91bD4KICAgICAgICA8L2Rpdj4KICAgICAgPC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9ImNvbC1tZC02Ij4KICAgICAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSBoLTEwMCI+CiAgICAgICAgICA8ZGl2IGNsYXNzPSJjYXJkLWhlYWRlciBiZy13aGl0ZSBmdy1zZW1pYm9sZCI+VGFyZWFzIGFiaWVydGFzPC9kaXY+CiAgICAgICAgICA8dWwgY2xhc3M9Imxpc3QtZ3JvdXAgbGlzdC1ncm91cC1mbHVzaCBzbWFsbCI+CiAgICAgICAgICAgIHslIGZvciB0IGluIHRhcmVhcyAlfQogICAgICAgICAgICA8bGkgY2xhc3M9Imxpc3QtZ3JvdXAtaXRlbSI+CiAgICAgICAgICAgICAge3sgdC5kZXNjcmlwY2lvbnx0cnVuY2F0ZWNoYXJzOjYwIH19CiAgICAgICAgICAgICAgeyUgaWYgdC5mZWNoYV9saW1pdGUgJX08c3BhbiBjbGFzcz0idGV4dC1tdXRlZCI+wrcge3sgdC5mZWNoYV9saW1pdGV8ZGF0ZToiZC9tL1kiIH19PC9zcGFuPnslIGVuZGlmICV9CiAgICAgICAgICAgIDwvbGk+CiAgICAgICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgICAgIDxsaSBjbGFzcz0ibGlzdC1ncm91cC1pdGVtIHRleHQtbXV0ZWQiPlNpbiB0YXJlYXMgcGVuZGllbnRlcy48L2xpPgogICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgIDwvdWw+CiAgICAgICAgPC9kaXY+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CiAgPC9kaXY+CjwvZGl2Pgp7JSBlbmRibG9jayAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/wcgone/crm/entidad_list.html
PATH_JSON="templates/wcgone/crm/entidad_list.html"
FILENAME=entidad_list.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=126
SIZE_BYTES_UTF8=5105
CONTENT_SHA256=924339034aa1c0247132903b042a1e6bc4517d3670369277384443e320f66104
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

{% block title %}Clientes — CRM — WCG One{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-2">
  <div class="wcg-report-head">
    <h1 class="h4 fw-semibold mb-0">CRM — Clientes y entidades</h1>
    {% include "includes/module_mark.html" with module="crm" %}
  </div>
  <div class="d-flex gap-1 flex-wrap">
    <a href="{% url 'wcgone_crm:export_entidades' %}{% if export_query %}?{{ export_query }}{% endif %}" class="btn btn-sm btn-outline-primary">Exportar CSV</a>
    <a href="{% url 'wcgone_crm:contacto_list' %}" class="btn btn-sm btn-outline-secondary">Contactos</a>
    <a href="{% url 'wcgone_crm:tarea_list' %}" class="btn btn-sm btn-outline-secondary">Tareas</a>
  </div>
</div>

<div class="card border-0 shadow-sm mb-3">
  <div class="card-body py-2 px-3 small">
    <div class="row g-2">
      <div class="col-md-3"><strong>Total:</strong> {{ summary.total }}</div>
      <div class="col-md-3"><strong>Activas:</strong> {{ summary.activas }}</div>
      <div class="col-md-3"><strong>Inactivas:</strong> {{ summary.inactivas }}</div>
      <div class="col-md-3">
        <strong>Top ciudades:</strong>
        {% for item in summary.por_ciudad %}{{ item.ciudad }} ({{ item.total }}){% if not forloop.last %}, {% endif %}{% empty %}—{% endfor %}
      </div>
    </div>
    {% if summary.por_riesgo %}
    <div class="mt-1 text-muted">
      <strong>Categoría riesgo:</strong>
      {% for item in summary.por_riesgo %}{{ item.categoria_riesgo }} ({{ item.total }}){% if not forloop.last %}, {% endif %}{% endfor %}
    </div>
    {% endif %}
  </div>
</div>

<form method="get" class="row g-2 mb-3">
  <div class="col-md-4">
    <input type="search" name="q" value="{{ request.GET.q }}" class="form-control form-control-sm" placeholder="Buscar nombre o NIT">
  </div>
  <div class="col-md-3">
    <select name="tipo" class="form-select form-select-sm">
      <option value="">Todos los tipos</option>
      {% for value, label in tipo_choices %}
      <option value="{{ value }}"{% if request.GET.tipo == value %} selected{% endif %}>{{ label }}</option>
      {% endfor %}
    </select>
  </div>
  <div class="col-md-2">
    <select name="activo" class="form-select form-select-sm">
      <option value="">Activo / Inactivo</option>
      <option value="1"{% if request.GET.activo == '1' %} selected{% endif %}>Activos</option>
      <option value="0"{% if request.GET.activo == '0' %} selected{% endif %}>Inactivos</option>
    </select>
  </div>
  <div class="col-md-2">
    <button type="submit" class="btn btn-primary btn-sm w-100">Filtrar</button>
  </div>
</form>

{% if not entidades and not request.GET %}
{% include "includes/empty_state.html" with title="Sin clientes registrados" message="Cargue entidades desde Administración → Importación General." %}
{% endif %}

<div class="card border-0 shadow-sm">
  <div class="table-responsive">
    <table class="table table-hover table-wcg mb-0 align-middle">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>NIT</th>
          <th>Tipo</th>
          <th>Ciudad</th>
          <th>Contactos</th>
          <th>Productos</th>
          <th>Estado</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {% for entidad in entidades %}
        <tr>
          <td>{{ entidad.nombre }}</td>
          <td>{{ entidad.nit|default:"—" }}</td>
          <td>{{ entidad.get_tipo_entidad_display }}</td>
          <td>{{ entidad.ciudad|default:"—" }}</td>
          <td>{{ entidad.num_contactos }}</td>
          <td>{{ entidad.num_productos }}</td>
          <td>
            {% if entidad.activo %}
            <span class="badge text-bg-success">Activo</span>
            {% else %}
            <span class="badge text-bg-secondary">Inactivo</span>
            {% endif %}
          </td>
          <td class="text-end">
            <a href="{% url 'wcgone_crm:entidad_detail' entidad.pk %}" class="btn btn-sm btn-outline-primary">Ver</a>
          </td>
        </tr>
        {% empty %}
        <tr>
          <td colspan="8" class="text-center text-muted py-4">
            No hay resultados con los filtros actuales.
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>

{% if is_paginated %}
<nav class="mt-3">
  <ul class="pagination pagination-sm justify-content-center">
    {% if page_obj.has_previous %}
    <li class="page-item"><a class="page-link" href="?page={{ page_obj.previous_page_number }}&q={{ request.GET.q }}&tipo={{ request.GET.tipo }}&activo={{ request.GET.activo }}">Anterior</a></li>
    {% endif %}
    <li class="page-item disabled"><span class="page-link">Pág. {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}</span></li>
    {% if page_obj.has_next %}
    <li class="page-item"><a class="page-link" href="?page={{ page_obj.next_page_number }}&q={{ request.GET.q }}&tipo={{ request.GET.tipo }}&activo={{ request.GET.activo }}">Siguiente</a></li>
    {% endif %}
  </ul>
</nav>
{% endif %}
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "wcgone_base.html" %}
00002|
00003|{% block title %}Clientes — CRM — WCG One{% endblock %}
00004|
00005|{% block content %}
00006|<div class="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-2">
00007|  <div class="wcg-report-head">
00008|    <h1 class="h4 fw-semibold mb-0">CRM — Clientes y entidades</h1>
00009|    {% include "includes/module_mark.html" with module="crm" %}
00010|  </div>
00011|  <div class="d-flex gap-1 flex-wrap">
00012|    <a href="{% url 'wcgone_crm:export_entidades' %}{% if export_query %}?{{ export_query }}{% endif %}" class="btn btn-sm btn-outline-primary">Exportar CSV</a>
00013|    <a href="{% url 'wcgone_crm:contacto_list' %}" class="btn btn-sm btn-outline-secondary">Contactos</a>
00014|    <a href="{% url 'wcgone_crm:tarea_list' %}" class="btn btn-sm btn-outline-secondary">Tareas</a>
00015|  </div>
00016|</div>
00017|
00018|<div class="card border-0 shadow-sm mb-3">
00019|  <div class="card-body py-2 px-3 small">
00020|    <div class="row g-2">
00021|      <div class="col-md-3"><strong>Total:</strong> {{ summary.total }}</div>
00022|      <div class="col-md-3"><strong>Activas:</strong> {{ summary.activas }}</div>
00023|      <div class="col-md-3"><strong>Inactivas:</strong> {{ summary.inactivas }}</div>
00024|      <div class="col-md-3">
00025|        <strong>Top ciudades:</strong>
00026|        {% for item in summary.por_ciudad %}{{ item.ciudad }} ({{ item.total }}){% if not forloop.last %}, {% endif %}{% empty %}—{% endfor %}
00027|      </div>
00028|    </div>
00029|    {% if summary.por_riesgo %}
00030|    <div class="mt-1 text-muted">
00031|      <strong>Categoría riesgo:</strong>
00032|      {% for item in summary.por_riesgo %}{{ item.categoria_riesgo }} ({{ item.total }}){% if not forloop.last %}, {% endif %}{% endfor %}
00033|    </div>
00034|    {% endif %}
00035|  </div>
00036|</div>
00037|
00038|<form method="get" class="row g-2 mb-3">
00039|  <div class="col-md-4">
00040|    <input type="search" name="q" value="{{ request.GET.q }}" class="form-control form-control-sm" placeholder="Buscar nombre o NIT">
00041|  </div>
00042|  <div class="col-md-3">
00043|    <select name="tipo" class="form-select form-select-sm">
00044|      <option value="">Todos los tipos</option>
00045|      {% for value, label in tipo_choices %}
00046|      <option value="{{ value }}"{% if request.GET.tipo == value %} selected{% endif %}>{{ label }}</option>
00047|      {% endfor %}
00048|    </select>
00049|  </div>
00050|  <div class="col-md-2">
00051|    <select name="activo" class="form-select form-select-sm">
00052|      <option value="">Activo / Inactivo</option>
00053|      <option value="1"{% if request.GET.activo == '1' %} selected{% endif %}>Activos</option>
00054|      <option value="0"{% if request.GET.activo == '0' %} selected{% endif %}>Inactivos</option>
00055|    </select>
00056|  </div>
00057|  <div class="col-md-2">
00058|    <button type="submit" class="btn btn-primary btn-sm w-100">Filtrar</button>
00059|  </div>
00060|</form>
00061|
00062|{% if not entidades and not request.GET %}
00063|{% include "includes/empty_state.html" with title="Sin clientes registrados" message="Cargue entidades desde Administración → Importación General." %}
00064|{% endif %}
00065|
00066|<div class="card border-0 shadow-sm">
00067|  <div class="table-responsive">
00068|    <table class="table table-hover table-wcg mb-0 align-middle">
00069|      <thead>
00070|        <tr>
00071|          <th>Nombre</th>
00072|          <th>NIT</th>
00073|          <th>Tipo</th>
00074|          <th>Ciudad</th>
00075|          <th>Contactos</th>
00076|          <th>Productos</th>
00077|          <th>Estado</th>
00078|          <th></th>
00079|        </tr>
00080|      </thead>
00081|      <tbody>
00082|        {% for entidad in entidades %}
00083|        <tr>
00084|          <td>{{ entidad.nombre }}</td>
00085|          <td>{{ entidad.nit|default:"—" }}</td>
00086|          <td>{{ entidad.get_tipo_entidad_display }}</td>
00087|          <td>{{ entidad.ciudad|default:"—" }}</td>
00088|          <td>{{ entidad.num_contactos }}</td>
00089|          <td>{{ entidad.num_productos }}</td>
00090|          <td>
00091|            {% if entidad.activo %}
00092|            <span class="badge text-bg-success">Activo</span>
00093|            {% else %}
00094|            <span class="badge text-bg-secondary">Inactivo</span>
00095|            {% endif %}
00096|          </td>
00097|          <td class="text-end">
00098|            <a href="{% url 'wcgone_crm:entidad_detail' entidad.pk %}" class="btn btn-sm btn-outline-primary">Ver</a>
00099|          </td>
00100|        </tr>
00101|        {% empty %}
00102|        <tr>
00103|          <td colspan="8" class="text-center text-muted py-4">
00104|            No hay resultados con los filtros actuales.
00105|          </td>
00106|        </tr>
00107|        {% endfor %}
00108|      </tbody>
00109|    </table>
00110|  </div>
00111|</div>
00112|
00113|{% if is_paginated %}
00114|<nav class="mt-3">
00115|  <ul class="pagination pagination-sm justify-content-center">
00116|    {% if page_obj.has_previous %}
00117|    <li class="page-item"><a class="page-link" href="?page={{ page_obj.previous_page_number }}&q={{ request.GET.q }}&tipo={{ request.GET.tipo }}&activo={{ request.GET.activo }}">Anterior</a></li>
00118|    {% endif %}
00119|    <li class="page-item disabled"><span class="page-link">Pág. {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}</span></li>
00120|    {% if page_obj.has_next %}
00121|    <li class="page-item"><a class="page-link" href="?page={{ page_obj.next_page_number }}&q={{ request.GET.q }}&tipo={{ request.GET.tipo }}&activo={{ request.GET.activo }}">Siguiente</a></li>
00122|    {% endif %}
00123|  </ul>
00124|</nav>
00125|{% endif %}
00126|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAid2Nnb25lX2Jhc2UuaHRtbCIgJX0KCnslIGJsb2NrIHRpdGxlICV9Q2xpZW50ZXMg4oCUIENSTSDigJQgV0NHIE9uZXslIGVuZGJsb2NrICV9Cgp7JSBibG9jayBjb250ZW50ICV9CjxkaXYgY2xhc3M9ImQtZmxleCBqdXN0aWZ5LWNvbnRlbnQtYmV0d2VlbiBhbGlnbi1pdGVtcy1zdGFydCBtYi0zIGZsZXgtd3JhcCBnYXAtMiI+CiAgPGRpdiBjbGFzcz0id2NnLXJlcG9ydC1oZWFkIj4KICAgIDxoMSBjbGFzcz0iaDQgZnctc2VtaWJvbGQgbWItMCI+Q1JNIOKAlCBDbGllbnRlcyB5IGVudGlkYWRlczwvaDE+CiAgICB7JSBpbmNsdWRlICJpbmNsdWRlcy9tb2R1bGVfbWFyay5odG1sIiB3aXRoIG1vZHVsZT0iY3JtIiAlfQogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImQtZmxleCBnYXAtMSBmbGV4LXdyYXAiPgogICAgPGEgaHJlZj0ieyUgdXJsICd3Y2dvbmVfY3JtOmV4cG9ydF9lbnRpZGFkZXMnICV9eyUgaWYgZXhwb3J0X3F1ZXJ5ICV9P3t7IGV4cG9ydF9xdWVyeSB9fXslIGVuZGlmICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1wcmltYXJ5Ij5FeHBvcnRhciBDU1Y8L2E+CiAgICA8YSBocmVmPSJ7JSB1cmwgJ3djZ29uZV9jcm06Y29udGFjdG9fbGlzdCcgJX0iIGNsYXNzPSJidG4gYnRuLXNtIGJ0bi1vdXRsaW5lLXNlY29uZGFyeSI+Q29udGFjdG9zPC9hPgogICAgPGEgaHJlZj0ieyUgdXJsICd3Y2dvbmVfY3JtOnRhcmVhX2xpc3QnICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1zZWNvbmRhcnkiPlRhcmVhczwvYT4KICA8L2Rpdj4KPC9kaXY+Cgo8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSBtYi0zIj4KICA8ZGl2IGNsYXNzPSJjYXJkLWJvZHkgcHktMiBweC0zIHNtYWxsIj4KICAgIDxkaXYgY2xhc3M9InJvdyBnLTIiPgogICAgICA8ZGl2IGNsYXNzPSJjb2wtbWQtMyI+PHN0cm9uZz5Ub3RhbDo8L3N0cm9uZz4ge3sgc3VtbWFyeS50b3RhbCB9fTwvZGl2PgogICAgICA8ZGl2IGNsYXNzPSJjb2wtbWQtMyI+PHN0cm9uZz5BY3RpdmFzOjwvc3Ryb25nPiB7eyBzdW1tYXJ5LmFjdGl2YXMgfX08L2Rpdj4KICAgICAgPGRpdiBjbGFzcz0iY29sLW1kLTMiPjxzdHJvbmc+SW5hY3RpdmFzOjwvc3Ryb25nPiB7eyBzdW1tYXJ5LmluYWN0aXZhcyB9fTwvZGl2PgogICAgICA8ZGl2IGNsYXNzPSJjb2wtbWQtMyI+CiAgICAgICAgPHN0cm9uZz5Ub3AgY2l1ZGFkZXM6PC9zdHJvbmc+CiAgICAgICAgeyUgZm9yIGl0ZW0gaW4gc3VtbWFyeS5wb3JfY2l1ZGFkICV9e3sgaXRlbS5jaXVkYWQgfX0gKHt7IGl0ZW0udG90YWwgfX0peyUgaWYgbm90IGZvcmxvb3AubGFzdCAlfSwgeyUgZW5kaWYgJX17JSBlbXB0eSAlfeKAlHslIGVuZGZvciAlfQogICAgICA8L2Rpdj4KICAgIDwvZGl2PgogICAgeyUgaWYgc3VtbWFyeS5wb3Jfcmllc2dvICV9CiAgICA8ZGl2IGNsYXNzPSJtdC0xIHRleHQtbXV0ZWQiPgogICAgICA8c3Ryb25nPkNhdGVnb3LDrWEgcmllc2dvOjwvc3Ryb25nPgogICAgICB7JSBmb3IgaXRlbSBpbiBzdW1tYXJ5LnBvcl9yaWVzZ28gJX17eyBpdGVtLmNhdGVnb3JpYV9yaWVzZ28gfX0gKHt7IGl0ZW0udG90YWwgfX0peyUgaWYgbm90IGZvcmxvb3AubGFzdCAlfSwgeyUgZW5kaWYgJX17JSBlbmRmb3IgJX0KICAgIDwvZGl2PgogICAgeyUgZW5kaWYgJX0KICA8L2Rpdj4KPC9kaXY+Cgo8Zm9ybSBtZXRob2Q9ImdldCIgY2xhc3M9InJvdyBnLTIgbWItMyI+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTQiPgogICAgPGlucHV0IHR5cGU9InNlYXJjaCIgbmFtZT0icSIgdmFsdWU9Int7IHJlcXVlc3QuR0VULnEgfX0iIGNsYXNzPSJmb3JtLWNvbnRyb2wgZm9ybS1jb250cm9sLXNtIiBwbGFjZWhvbGRlcj0iQnVzY2FyIG5vbWJyZSBvIE5JVCI+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTMiPgogICAgPHNlbGVjdCBuYW1lPSJ0aXBvIiBjbGFzcz0iZm9ybS1zZWxlY3QgZm9ybS1zZWxlY3Qtc20iPgogICAgICA8b3B0aW9uIHZhbHVlPSIiPlRvZG9zIGxvcyB0aXBvczwvb3B0aW9uPgogICAgICB7JSBmb3IgdmFsdWUsIGxhYmVsIGluIHRpcG9fY2hvaWNlcyAlfQogICAgICA8b3B0aW9uIHZhbHVlPSJ7eyB2YWx1ZSB9fSJ7JSBpZiByZXF1ZXN0LkdFVC50aXBvID09IHZhbHVlICV9IHNlbGVjdGVkeyUgZW5kaWYgJX0+e3sgbGFiZWwgfX08L29wdGlvbj4KICAgICAgeyUgZW5kZm9yICV9CiAgICA8L3NlbGVjdD4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtMiI+CiAgICA8c2VsZWN0IG5hbWU9ImFjdGl2byIgY2xhc3M9ImZvcm0tc2VsZWN0IGZvcm0tc2VsZWN0LXNtIj4KICAgICAgPG9wdGlvbiB2YWx1ZT0iIj5BY3Rpdm8gLyBJbmFjdGl2bzwvb3B0aW9uPgogICAgICA8b3B0aW9uIHZhbHVlPSIxInslIGlmIHJlcXVlc3QuR0VULmFjdGl2byA9PSAnMScgJX0gc2VsZWN0ZWR7JSBlbmRpZiAlfT5BY3Rpdm9zPC9vcHRpb24+CiAgICAgIDxvcHRpb24gdmFsdWU9IjAieyUgaWYgcmVxdWVzdC5HRVQuYWN0aXZvID09ICcwJyAlfSBzZWxlY3RlZHslIGVuZGlmICV9PkluYWN0aXZvczwvb3B0aW9uPgogICAgPC9zZWxlY3Q+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTIiPgogICAgPGJ1dHRvbiB0eXBlPSJzdWJtaXQiIGNsYXNzPSJidG4gYnRuLXByaW1hcnkgYnRuLXNtIHctMTAwIj5GaWx0cmFyPC9idXR0b24+CiAgPC9kaXY+CjwvZm9ybT4KCnslIGlmIG5vdCBlbnRpZGFkZXMgYW5kIG5vdCByZXF1ZXN0LkdFVCAlfQp7JSBpbmNsdWRlICJpbmNsdWRlcy9lbXB0eV9zdGF0ZS5odG1sIiB3aXRoIHRpdGxlPSJTaW4gY2xpZW50ZXMgcmVnaXN0cmFkb3MiIG1lc3NhZ2U9IkNhcmd1ZSBlbnRpZGFkZXMgZGVzZGUgQWRtaW5pc3RyYWNpw7NuIOKGkiBJbXBvcnRhY2nDs24gR2VuZXJhbC4iICV9CnslIGVuZGlmICV9Cgo8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSI+CiAgPGRpdiBjbGFzcz0idGFibGUtcmVzcG9uc2l2ZSI+CiAgICA8dGFibGUgY2xhc3M9InRhYmxlIHRhYmxlLWhvdmVyIHRhYmxlLXdjZyBtYi0wIGFsaWduLW1pZGRsZSI+CiAgICAgIDx0aGVhZD4KICAgICAgICA8dHI+CiAgICAgICAgICA8dGg+Tm9tYnJlPC90aD4KICAgICAgICAgIDx0aD5OSVQ8L3RoPgogICAgICAgICAgPHRoPlRpcG88L3RoPgogICAgICAgICAgPHRoPkNpdWRhZDwvdGg+CiAgICAgICAgICA8dGg+Q29udGFjdG9zPC90aD4KICAgICAgICAgIDx0aD5Qcm9kdWN0b3M8L3RoPgogICAgICAgICAgPHRoPkVzdGFkbzwvdGg+CiAgICAgICAgICA8dGg+PC90aD4KICAgICAgICA8L3RyPgogICAgICA8L3RoZWFkPgogICAgICA8dGJvZHk+CiAgICAgICAgeyUgZm9yIGVudGlkYWQgaW4gZW50aWRhZGVzICV9CiAgICAgICAgPHRyPgogICAgICAgICAgPHRkPnt7IGVudGlkYWQubm9tYnJlIH19PC90ZD4KICAgICAgICAgIDx0ZD57eyBlbnRpZGFkLm5pdHxkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgIDx0ZD57eyBlbnRpZGFkLmdldF90aXBvX2VudGlkYWRfZGlzcGxheSB9fTwvdGQ+CiAgICAgICAgICA8dGQ+e3sgZW50aWRhZC5jaXVkYWR8ZGVmYXVsdDoi4oCUIiB9fTwvdGQ+CiAgICAgICAgICA8dGQ+e3sgZW50aWRhZC5udW1fY29udGFjdG9zIH19PC90ZD4KICAgICAgICAgIDx0ZD57eyBlbnRpZGFkLm51bV9wcm9kdWN0b3MgfX08L3RkPgogICAgICAgICAgPHRkPgogICAgICAgICAgICB7JSBpZiBlbnRpZGFkLmFjdGl2byAlfQogICAgICAgICAgICA8c3BhbiBjbGFzcz0iYmFkZ2UgdGV4dC1iZy1zdWNjZXNzIj5BY3Rpdm88L3NwYW4+CiAgICAgICAgICAgIHslIGVsc2UgJX0KICAgICAgICAgICAgPHNwYW4gY2xhc3M9ImJhZGdlIHRleHQtYmctc2Vjb25kYXJ5Ij5JbmFjdGl2bzwvc3Bhbj4KICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgIDwvdGQ+CiAgICAgICAgICA8dGQgY2xhc3M9InRleHQtZW5kIj4KICAgICAgICAgICAgPGEgaHJlZj0ieyUgdXJsICd3Y2dvbmVfY3JtOmVudGlkYWRfZGV0YWlsJyBlbnRpZGFkLnBrICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1wcmltYXJ5Ij5WZXI8L2E+CiAgICAgICAgICA8L3RkPgogICAgICAgIDwvdHI+CiAgICAgICAgeyUgZW1wdHkgJX0KICAgICAgICA8dHI+CiAgICAgICAgICA8dGQgY29sc3Bhbj0iOCIgY2xhc3M9InRleHQtY2VudGVyIHRleHQtbXV0ZWQgcHktNCI+CiAgICAgICAgICAgIE5vIGhheSByZXN1bHRhZG9zIGNvbiBsb3MgZmlsdHJvcyBhY3R1YWxlcy4KICAgICAgICAgIDwvdGQ+CiAgICAgICAgPC90cj4KICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgPC90Ym9keT4KICAgIDwvdGFibGU+CiAgPC9kaXY+CjwvZGl2PgoKeyUgaWYgaXNfcGFnaW5hdGVkICV9CjxuYXYgY2xhc3M9Im10LTMiPgogIDx1bCBjbGFzcz0icGFnaW5hdGlvbiBwYWdpbmF0aW9uLXNtIGp1c3RpZnktY29udGVudC1jZW50ZXIiPgogICAgeyUgaWYgcGFnZV9vYmouaGFzX3ByZXZpb3VzICV9CiAgICA8bGkgY2xhc3M9InBhZ2UtaXRlbSI+PGEgY2xhc3M9InBhZ2UtbGluayIgaHJlZj0iP3BhZ2U9e3sgcGFnZV9vYmoucHJldmlvdXNfcGFnZV9udW1iZXIgfX0mcT17eyByZXF1ZXN0LkdFVC5xIH19JnRpcG89e3sgcmVxdWVzdC5HRVQudGlwbyB9fSZhY3Rpdm89e3sgcmVxdWVzdC5HRVQuYWN0aXZvIH19Ij5BbnRlcmlvcjwvYT48L2xpPgogICAgeyUgZW5kaWYgJX0KICAgIDxsaSBjbGFzcz0icGFnZS1pdGVtIGRpc2FibGVkIj48c3BhbiBjbGFzcz0icGFnZS1saW5rIj5Qw6FnLiB7eyBwYWdlX29iai5udW1iZXIgfX0gZGUge3sgcGFnZV9vYmoucGFnaW5hdG9yLm51bV9wYWdlcyB9fTwvc3Bhbj48L2xpPgogICAgeyUgaWYgcGFnZV9vYmouaGFzX25leHQgJX0KICAgIDxsaSBjbGFzcz0icGFnZS1pdGVtIj48YSBjbGFzcz0icGFnZS1saW5rIiBocmVmPSI/cGFnZT17eyBwYWdlX29iai5uZXh0X3BhZ2VfbnVtYmVyIH19JnE9e3sgcmVxdWVzdC5HRVQucSB9fSZ0aXBvPXt7IHJlcXVlc3QuR0VULnRpcG8gfX0mYWN0aXZvPXt7IHJlcXVlc3QuR0VULmFjdGl2byB9fSI+U2lndWllbnRlPC9hPjwvbGk+CiAgICB7JSBlbmRpZiAlfQogIDwvdWw+CjwvbmF2Pgp7JSBlbmRpZiAlfQp7JSBlbmRibG9jayAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/wcgone/crm/tarea_list.html
PATH_JSON="templates/wcgone/crm/tarea_list.html"
FILENAME=tarea_list.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=65
SIZE_BYTES_UTF8=2664
CONTENT_SHA256=36c4b1b9fb3c000a36bef0735e45469198f61eea37ed650a16c5d2a39d80b491
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

{% block title %}Tareas — CRM — WCG One{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-2">
  <div class="wcg-report-head">
    <h1 class="h4 fw-semibold mb-0">CRM — Tareas de seguimiento</h1>
    {% include "includes/module_mark.html" with module="crm" %}
  </div>
  <div class="d-flex gap-1">
    <a href="{% url 'wcgone_crm:entidad_list' %}" class="btn btn-sm btn-outline-secondary">← Clientes</a>
    <a href="{% url 'wcgone_crm:contacto_list' %}" class="btn btn-sm btn-outline-secondary">Contactos</a>
  </div>
</div>

<form method="get" class="row g-2 mb-3">
  <div class="col-auto">
    <select name="estado" class="form-select form-select-sm">
      <option value="">Todos los estados</option>
      <option value="pendiente"{% if request.GET.estado == 'pendiente' %} selected{% endif %}>Pendiente</option>
      <option value="en_proceso"{% if request.GET.estado == 'en_proceso' %} selected{% endif %}>En proceso</option>
      <option value="completada"{% if request.GET.estado == 'completada' %} selected{% endif %}>Completada</option>
    </select>
  </div>
  <div class="col-auto form-check align-self-center">
    <input class="form-check-input" type="checkbox" name="pendientes" value="1" id="pendientes"{% if request.GET.pendientes == '1' %} checked{% endif %}>
    <label class="form-check-label small" for="pendientes">Solo pendientes</label>
  </div>
  <div class="col-auto">
    <button type="submit" class="btn btn-primary btn-sm">Filtrar</button>
  </div>
</form>

<div class="card border-0 shadow-sm">
  <div class="table-responsive">
    <table class="table table-hover table-wcg mb-0">
      <thead>
        <tr>
          <th>Descripción</th>
          <th>Entidad</th>
          <th>Estado</th>
          <th>Prioridad</th>
          <th>Límite</th>
          <th>Asignado</th>
        </tr>
      </thead>
      <tbody>
        {% for tarea in tareas %}
        <tr>
          <td>{{ tarea.descripcion|truncatechars:80 }}</td>
          <td><a href="{% url 'wcgone_crm:entidad_detail' tarea.entidad_id %}">{{ tarea.entidad.nombre }}</a></td>
          <td>{{ tarea.estado }}</td>
          <td>{{ tarea.prioridad|default:"—" }}</td>
          <td>{{ tarea.fecha_limite|date:"d/m/Y"|default:"—" }}</td>
          <td>{% if tarea.asignado_a %}{{ tarea.asignado_a.get_username }}{% else %}—{% endif %}</td>
        </tr>
        {% empty %}
        <tr><td colspan="6" class="text-center text-muted py-4">No hay tareas registradas.</td></tr>
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
00003|{% block title %}Tareas — CRM — WCG One{% endblock %}
00004|
00005|{% block content %}
00006|<div class="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-2">
00007|  <div class="wcg-report-head">
00008|    <h1 class="h4 fw-semibold mb-0">CRM — Tareas de seguimiento</h1>
00009|    {% include "includes/module_mark.html" with module="crm" %}
00010|  </div>
00011|  <div class="d-flex gap-1">
00012|    <a href="{% url 'wcgone_crm:entidad_list' %}" class="btn btn-sm btn-outline-secondary">← Clientes</a>
00013|    <a href="{% url 'wcgone_crm:contacto_list' %}" class="btn btn-sm btn-outline-secondary">Contactos</a>
00014|  </div>
00015|</div>
00016|
00017|<form method="get" class="row g-2 mb-3">
00018|  <div class="col-auto">
00019|    <select name="estado" class="form-select form-select-sm">
00020|      <option value="">Todos los estados</option>
00021|      <option value="pendiente"{% if request.GET.estado == 'pendiente' %} selected{% endif %}>Pendiente</option>
00022|      <option value="en_proceso"{% if request.GET.estado == 'en_proceso' %} selected{% endif %}>En proceso</option>
00023|      <option value="completada"{% if request.GET.estado == 'completada' %} selected{% endif %}>Completada</option>
00024|    </select>
00025|  </div>
00026|  <div class="col-auto form-check align-self-center">
00027|    <input class="form-check-input" type="checkbox" name="pendientes" value="1" id="pendientes"{% if request.GET.pendientes == '1' %} checked{% endif %}>
00028|    <label class="form-check-label small" for="pendientes">Solo pendientes</label>
00029|  </div>
00030|  <div class="col-auto">
00031|    <button type="submit" class="btn btn-primary btn-sm">Filtrar</button>
00032|  </div>
00033|</form>
00034|
00035|<div class="card border-0 shadow-sm">
00036|  <div class="table-responsive">
00037|    <table class="table table-hover table-wcg mb-0">
00038|      <thead>
00039|        <tr>
00040|          <th>Descripción</th>
00041|          <th>Entidad</th>
00042|          <th>Estado</th>
00043|          <th>Prioridad</th>
00044|          <th>Límite</th>
00045|          <th>Asignado</th>
00046|        </tr>
00047|      </thead>
00048|      <tbody>
00049|        {% for tarea in tareas %}
00050|        <tr>
00051|          <td>{{ tarea.descripcion|truncatechars:80 }}</td>
00052|          <td><a href="{% url 'wcgone_crm:entidad_detail' tarea.entidad_id %}">{{ tarea.entidad.nombre }}</a></td>
00053|          <td>{{ tarea.estado }}</td>
00054|          <td>{{ tarea.prioridad|default:"—" }}</td>
00055|          <td>{{ tarea.fecha_limite|date:"d/m/Y"|default:"—" }}</td>
00056|          <td>{% if tarea.asignado_a %}{{ tarea.asignado_a.get_username }}{% else %}—{% endif %}</td>
00057|        </tr>
00058|        {% empty %}
00059|        <tr><td colspan="6" class="text-center text-muted py-4">No hay tareas registradas.</td></tr>
00060|        {% endfor %}
00061|      </tbody>
00062|    </table>
00063|  </div>
00064|</div>
00065|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAid2Nnb25lX2Jhc2UuaHRtbCIgJX0KCnslIGJsb2NrIHRpdGxlICV9VGFyZWFzIOKAlCBDUk0g4oCUIFdDRyBPbmV7JSBlbmRibG9jayAlfQoKeyUgYmxvY2sgY29udGVudCAlfQo8ZGl2IGNsYXNzPSJkLWZsZXgganVzdGlmeS1jb250ZW50LWJldHdlZW4gYWxpZ24taXRlbXMtc3RhcnQgbWItMyBmbGV4LXdyYXAgZ2FwLTIiPgogIDxkaXYgY2xhc3M9IndjZy1yZXBvcnQtaGVhZCI+CiAgICA8aDEgY2xhc3M9Img0IGZ3LXNlbWlib2xkIG1iLTAiPkNSTSDigJQgVGFyZWFzIGRlIHNlZ3VpbWllbnRvPC9oMT4KICAgIHslIGluY2x1ZGUgImluY2x1ZGVzL21vZHVsZV9tYXJrLmh0bWwiIHdpdGggbW9kdWxlPSJjcm0iICV9CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iZC1mbGV4IGdhcC0xIj4KICAgIDxhIGhyZWY9InslIHVybCAnd2Nnb25lX2NybTplbnRpZGFkX2xpc3QnICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1zZWNvbmRhcnkiPuKGkCBDbGllbnRlczwvYT4KICAgIDxhIGhyZWY9InslIHVybCAnd2Nnb25lX2NybTpjb250YWN0b19saXN0JyAlfSIgY2xhc3M9ImJ0biBidG4tc20gYnRuLW91dGxpbmUtc2Vjb25kYXJ5Ij5Db250YWN0b3M8L2E+CiAgPC9kaXY+CjwvZGl2PgoKPGZvcm0gbWV0aG9kPSJnZXQiIGNsYXNzPSJyb3cgZy0yIG1iLTMiPgogIDxkaXYgY2xhc3M9ImNvbC1hdXRvIj4KICAgIDxzZWxlY3QgbmFtZT0iZXN0YWRvIiBjbGFzcz0iZm9ybS1zZWxlY3QgZm9ybS1zZWxlY3Qtc20iPgogICAgICA8b3B0aW9uIHZhbHVlPSIiPlRvZG9zIGxvcyBlc3RhZG9zPC9vcHRpb24+CiAgICAgIDxvcHRpb24gdmFsdWU9InBlbmRpZW50ZSJ7JSBpZiByZXF1ZXN0LkdFVC5lc3RhZG8gPT0gJ3BlbmRpZW50ZScgJX0gc2VsZWN0ZWR7JSBlbmRpZiAlfT5QZW5kaWVudGU8L29wdGlvbj4KICAgICAgPG9wdGlvbiB2YWx1ZT0iZW5fcHJvY2VzbyJ7JSBpZiByZXF1ZXN0LkdFVC5lc3RhZG8gPT0gJ2VuX3Byb2Nlc28nICV9IHNlbGVjdGVkeyUgZW5kaWYgJX0+RW4gcHJvY2Vzbzwvb3B0aW9uPgogICAgICA8b3B0aW9uIHZhbHVlPSJjb21wbGV0YWRhInslIGlmIHJlcXVlc3QuR0VULmVzdGFkbyA9PSAnY29tcGxldGFkYScgJX0gc2VsZWN0ZWR7JSBlbmRpZiAlfT5Db21wbGV0YWRhPC9vcHRpb24+CiAgICA8L3NlbGVjdD4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtYXV0byBmb3JtLWNoZWNrIGFsaWduLXNlbGYtY2VudGVyIj4KICAgIDxpbnB1dCBjbGFzcz0iZm9ybS1jaGVjay1pbnB1dCIgdHlwZT0iY2hlY2tib3giIG5hbWU9InBlbmRpZW50ZXMiIHZhbHVlPSIxIiBpZD0icGVuZGllbnRlcyJ7JSBpZiByZXF1ZXN0LkdFVC5wZW5kaWVudGVzID09ICcxJyAlfSBjaGVja2VkeyUgZW5kaWYgJX0+CiAgICA8bGFiZWwgY2xhc3M9ImZvcm0tY2hlY2stbGFiZWwgc21hbGwiIGZvcj0icGVuZGllbnRlcyI+U29sbyBwZW5kaWVudGVzPC9sYWJlbD4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtYXV0byI+CiAgICA8YnV0dG9uIHR5cGU9InN1Ym1pdCIgY2xhc3M9ImJ0biBidG4tcHJpbWFyeSBidG4tc20iPkZpbHRyYXI8L2J1dHRvbj4KICA8L2Rpdj4KPC9mb3JtPgoKPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20iPgogIDxkaXYgY2xhc3M9InRhYmxlLXJlc3BvbnNpdmUiPgogICAgPHRhYmxlIGNsYXNzPSJ0YWJsZSB0YWJsZS1ob3ZlciB0YWJsZS13Y2cgbWItMCI+CiAgICAgIDx0aGVhZD4KICAgICAgICA8dHI+CiAgICAgICAgICA8dGg+RGVzY3JpcGNpw7NuPC90aD4KICAgICAgICAgIDx0aD5FbnRpZGFkPC90aD4KICAgICAgICAgIDx0aD5Fc3RhZG88L3RoPgogICAgICAgICAgPHRoPlByaW9yaWRhZDwvdGg+CiAgICAgICAgICA8dGg+TMOtbWl0ZTwvdGg+CiAgICAgICAgICA8dGg+QXNpZ25hZG88L3RoPgogICAgICAgIDwvdHI+CiAgICAgIDwvdGhlYWQ+CiAgICAgIDx0Ym9keT4KICAgICAgICB7JSBmb3IgdGFyZWEgaW4gdGFyZWFzICV9CiAgICAgICAgPHRyPgogICAgICAgICAgPHRkPnt7IHRhcmVhLmRlc2NyaXBjaW9ufHRydW5jYXRlY2hhcnM6ODAgfX08L3RkPgogICAgICAgICAgPHRkPjxhIGhyZWY9InslIHVybCAnd2Nnb25lX2NybTplbnRpZGFkX2RldGFpbCcgdGFyZWEuZW50aWRhZF9pZCAlfSI+e3sgdGFyZWEuZW50aWRhZC5ub21icmUgfX08L2E+PC90ZD4KICAgICAgICAgIDx0ZD57eyB0YXJlYS5lc3RhZG8gfX08L3RkPgogICAgICAgICAgPHRkPnt7IHRhcmVhLnByaW9yaWRhZHxkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgIDx0ZD57eyB0YXJlYS5mZWNoYV9saW1pdGV8ZGF0ZToiZC9tL1kifGRlZmF1bHQ6IuKAlCIgfX08L3RkPgogICAgICAgICAgPHRkPnslIGlmIHRhcmVhLmFzaWduYWRvX2EgJX17eyB0YXJlYS5hc2lnbmFkb19hLmdldF91c2VybmFtZSB9fXslIGVsc2UgJX3igJR7JSBlbmRpZiAlfTwvdGQ+CiAgICAgICAgPC90cj4KICAgICAgICB7JSBlbXB0eSAlfQogICAgICAgIDx0cj48dGQgY29sc3Bhbj0iNiIgY2xhc3M9InRleHQtY2VudGVyIHRleHQtbXV0ZWQgcHktNCI+Tm8gaGF5IHRhcmVhcyByZWdpc3RyYWRhcy48L3RkPjwvdHI+CiAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgIDwvdGJvZHk+CiAgICA8L3RhYmxlPgogIDwvZGl2Pgo8L2Rpdj4KeyUgZW5kYmxvY2sgJX0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/wcgone/imports/batch_result.html
PATH_JSON="templates/wcgone/imports/batch_result.html"
FILENAME=batch_result.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=94
SIZE_BYTES_UTF8=3397
CONTENT_SHA256=eeea366eda2253134fd557f5d3c0da0ac37a504ae660cdef727f22d6068338d1
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

{% block title %}Resultado importación #{{ batch.pk }} — WCG One{% endblock %}

{% block content %}
<div class="mb-3">
  <h1 class="h4 fw-semibold mb-1">Resultado de importación #{{ batch.pk }}</h1>
  <p class="text-muted small mb-0">{{ batch.archivo_nombre }} · {{ batch.fecha_carga|date:"d/m/Y H:i" }}</p>
</div>

<div class="row g-3 mb-4">
  <div class="col-md-3 col-6">
    <div class="card border-0 shadow-sm text-center">
      <div class="card-body py-3">
        <div class="stat-value">{{ batch.filas_leidas }}</div>
        <div class="text-muted small">Filas leídas</div>
      </div>
    </div>
  </div>
  <div class="col-md-3 col-6">
    <div class="card border-0 shadow-sm text-center">
      <div class="card-body py-3">
        <div class="stat-value text-success">{{ batch.filas_validas }}</div>
        <div class="text-muted small">Filas válidas</div>
      </div>
    </div>
  </div>
  <div class="col-md-3 col-6">
    <div class="card border-0 shadow-sm text-center">
      <div class="card-body py-3">
        <div class="stat-value text-danger">{{ batch.filas_error }}</div>
        <div class="text-muted small">Filas con error</div>
      </div>
    </div>
  </div>
  <div class="col-md-3 col-6">
    <div class="card border-0 shadow-sm text-center">
      <div class="card-body py-3">
        <div class="stat-value" style="font-size:1.1rem;">{{ batch.get_estado_display }}</div>
        <div class="text-muted small">Estado</div>
      </div>
    </div>
  </div>
</div>

<div class="card border-0 shadow-sm mb-3">
  <div class="card-header bg-white fw-semibold">Detalle del lote</div>
  <div class="card-body small">
    <dl class="row mb-0">
      <dt class="col-sm-3">Módulo</dt><dd class="col-sm-9">{{ batch.modulo }}</dd>
      <dt class="col-sm-3">Tipo</dt><dd class="col-sm-9">{{ batch.tipo_importacion }}</dd>
      <dt class="col-sm-3">Usuario</dt><dd class="col-sm-9">{{ batch.usuario|default:"—" }}</dd>
      <dt class="col-sm-3">Resumen</dt><dd class="col-sm-9">{{ batch.observaciones|default:"—" }}</dd>
    </dl>
  </div>
</div>

<div class="card border-0 shadow-sm">
  <div class="card-header bg-white fw-semibold">Errores por fila {% if errores %}({{ errores|length }}){% endif %}</div>
  <div class="table-responsive">
    <table class="table table-sm mb-0">
      <thead>
        <tr>
          <th>Fila</th>
          <th>Campo</th>
          <th>Mensaje</th>
        </tr>
      </thead>
      <tbody>
        {% for err in errores %}
        <tr>
          <td>{{ err.fila_numero }}</td>
          <td>{{ err.campo|default:"—" }}</td>
          <td>{{ err.mensaje_error }}</td>
        </tr>
        {% empty %}
        <tr><td colspan="3" class="text-muted text-center py-3">Sin errores de fila registrados.</td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>

<div class="mt-3">
  <a href="/" class="btn btn-outline-secondary btn-sm">Inicio</a>
  {% if batch.modulo == 'crm' %}
  <a href="{% url 'wcgone_crm:entidad_list' %}" class="btn btn-primary btn-sm">Ver entidades</a>
  {% elif batch.modulo == 'risk' %}
  <a href="{% url 'wcgone_risk:comando_balon' %}" class="btn btn-primary btn-sm">Comando Balón</a>
  {% elif batch.modulo == 'pgo' %}
  <a href="{% url 'wcgone_pgo:ticket_list' %}" class="btn btn-primary btn-sm">Ver tickets</a>
  {% endif %}
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "wcgone_base.html" %}
00002|
00003|{% block title %}Resultado importación #{{ batch.pk }} — WCG One{% endblock %}
00004|
00005|{% block content %}
00006|<div class="mb-3">
00007|  <h1 class="h4 fw-semibold mb-1">Resultado de importación #{{ batch.pk }}</h1>
00008|  <p class="text-muted small mb-0">{{ batch.archivo_nombre }} · {{ batch.fecha_carga|date:"d/m/Y H:i" }}</p>
00009|</div>
00010|
00011|<div class="row g-3 mb-4">
00012|  <div class="col-md-3 col-6">
00013|    <div class="card border-0 shadow-sm text-center">
00014|      <div class="card-body py-3">
00015|        <div class="stat-value">{{ batch.filas_leidas }}</div>
00016|        <div class="text-muted small">Filas leídas</div>
00017|      </div>
00018|    </div>
00019|  </div>
00020|  <div class="col-md-3 col-6">
00021|    <div class="card border-0 shadow-sm text-center">
00022|      <div class="card-body py-3">
00023|        <div class="stat-value text-success">{{ batch.filas_validas }}</div>
00024|        <div class="text-muted small">Filas válidas</div>
00025|      </div>
00026|    </div>
00027|  </div>
00028|  <div class="col-md-3 col-6">
00029|    <div class="card border-0 shadow-sm text-center">
00030|      <div class="card-body py-3">
00031|        <div class="stat-value text-danger">{{ batch.filas_error }}</div>
00032|        <div class="text-muted small">Filas con error</div>
00033|      </div>
00034|    </div>
00035|  </div>
00036|  <div class="col-md-3 col-6">
00037|    <div class="card border-0 shadow-sm text-center">
00038|      <div class="card-body py-3">
00039|        <div class="stat-value" style="font-size:1.1rem;">{{ batch.get_estado_display }}</div>
00040|        <div class="text-muted small">Estado</div>
00041|      </div>
00042|    </div>
00043|  </div>
00044|</div>
00045|
00046|<div class="card border-0 shadow-sm mb-3">
00047|  <div class="card-header bg-white fw-semibold">Detalle del lote</div>
00048|  <div class="card-body small">
00049|    <dl class="row mb-0">
00050|      <dt class="col-sm-3">Módulo</dt><dd class="col-sm-9">{{ batch.modulo }}</dd>
00051|      <dt class="col-sm-3">Tipo</dt><dd class="col-sm-9">{{ batch.tipo_importacion }}</dd>
00052|      <dt class="col-sm-3">Usuario</dt><dd class="col-sm-9">{{ batch.usuario|default:"—" }}</dd>
00053|      <dt class="col-sm-3">Resumen</dt><dd class="col-sm-9">{{ batch.observaciones|default:"—" }}</dd>
00054|    </dl>
00055|  </div>
00056|</div>
00057|
00058|<div class="card border-0 shadow-sm">
00059|  <div class="card-header bg-white fw-semibold">Errores por fila {% if errores %}({{ errores|length }}){% endif %}</div>
00060|  <div class="table-responsive">
00061|    <table class="table table-sm mb-0">
00062|      <thead>
00063|        <tr>
00064|          <th>Fila</th>
00065|          <th>Campo</th>
00066|          <th>Mensaje</th>
00067|        </tr>
00068|      </thead>
00069|      <tbody>
00070|        {% for err in errores %}
00071|        <tr>
00072|          <td>{{ err.fila_numero }}</td>
00073|          <td>{{ err.campo|default:"—" }}</td>
00074|          <td>{{ err.mensaje_error }}</td>
00075|        </tr>
00076|        {% empty %}
00077|        <tr><td colspan="3" class="text-muted text-center py-3">Sin errores de fila registrados.</td></tr>
00078|        {% endfor %}
00079|      </tbody>
00080|    </table>
00081|  </div>
00082|</div>
00083|
00084|<div class="mt-3">
00085|  <a href="/" class="btn btn-outline-secondary btn-sm">Inicio</a>
00086|  {% if batch.modulo == 'crm' %}
00087|  <a href="{% url 'wcgone_crm:entidad_list' %}" class="btn btn-primary btn-sm">Ver entidades</a>
00088|  {% elif batch.modulo == 'risk' %}
00089|  <a href="{% url 'wcgone_risk:comando_balon' %}" class="btn btn-primary btn-sm">Comando Balón</a>
00090|  {% elif batch.modulo == 'pgo' %}
00091|  <a href="{% url 'wcgone_pgo:ticket_list' %}" class="btn btn-primary btn-sm">Ver tickets</a>
00092|  {% endif %}
00093|</div>
00094|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAid2Nnb25lX2Jhc2UuaHRtbCIgJX0KCnslIGJsb2NrIHRpdGxlICV9UmVzdWx0YWRvIGltcG9ydGFjacOzbiAje3sgYmF0Y2gucGsgfX0g4oCUIFdDRyBPbmV7JSBlbmRibG9jayAlfQoKeyUgYmxvY2sgY29udGVudCAlfQo8ZGl2IGNsYXNzPSJtYi0zIj4KICA8aDEgY2xhc3M9Img0IGZ3LXNlbWlib2xkIG1iLTEiPlJlc3VsdGFkbyBkZSBpbXBvcnRhY2nDs24gI3t7IGJhdGNoLnBrIH19PC9oMT4KICA8cCBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCBtYi0wIj57eyBiYXRjaC5hcmNoaXZvX25vbWJyZSB9fSDCtyB7eyBiYXRjaC5mZWNoYV9jYXJnYXxkYXRlOiJkL20vWSBIOmkiIH19PC9wPgo8L2Rpdj4KCjxkaXYgY2xhc3M9InJvdyBnLTMgbWItNCI+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTMgY29sLTYiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20gdGV4dC1jZW50ZXIiPgogICAgICA8ZGl2IGNsYXNzPSJjYXJkLWJvZHkgcHktMyI+CiAgICAgICAgPGRpdiBjbGFzcz0ic3RhdC12YWx1ZSI+e3sgYmF0Y2guZmlsYXNfbGVpZGFzIH19PC9kaXY+CiAgICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+RmlsYXMgbGXDrWRhczwvZGl2PgogICAgICA8L2Rpdj4KICAgIDwvZGl2PgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1tZC0zIGNvbC02Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIHRleHQtY2VudGVyIj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1ib2R5IHB5LTMiPgogICAgICAgIDxkaXYgY2xhc3M9InN0YXQtdmFsdWUgdGV4dC1zdWNjZXNzIj57eyBiYXRjaC5maWxhc192YWxpZGFzIH19PC9kaXY+CiAgICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+RmlsYXMgdsOhbGlkYXM8L2Rpdj4KICAgICAgPC9kaXY+CiAgICA8L2Rpdj4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtMyBjb2wtNiI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSB0ZXh0LWNlbnRlciI+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtYm9keSBweS0zIj4KICAgICAgICA8ZGl2IGNsYXNzPSJzdGF0LXZhbHVlIHRleHQtZGFuZ2VyIj57eyBiYXRjaC5maWxhc19lcnJvciB9fTwvZGl2PgogICAgICAgIDxkaXYgY2xhc3M9InRleHQtbXV0ZWQgc21hbGwiPkZpbGFzIGNvbiBlcnJvcjwvZGl2PgogICAgICA8L2Rpdj4KICAgIDwvZGl2PgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1tZC0zIGNvbC02Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIHRleHQtY2VudGVyIj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1ib2R5IHB5LTMiPgogICAgICAgIDxkaXYgY2xhc3M9InN0YXQtdmFsdWUiIHN0eWxlPSJmb250LXNpemU6MS4xcmVtOyI+e3sgYmF0Y2guZ2V0X2VzdGFkb19kaXNwbGF5IH19PC9kaXY+CiAgICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+RXN0YWRvPC9kaXY+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CiAgPC9kaXY+CjwvZGl2PgoKPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20gbWItMyI+CiAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIgYmctd2hpdGUgZnctc2VtaWJvbGQiPkRldGFsbGUgZGVsIGxvdGU8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjYXJkLWJvZHkgc21hbGwiPgogICAgPGRsIGNsYXNzPSJyb3cgbWItMCI+CiAgICAgIDxkdCBjbGFzcz0iY29sLXNtLTMiPk3Ds2R1bG88L2R0PjxkZCBjbGFzcz0iY29sLXNtLTkiPnt7IGJhdGNoLm1vZHVsbyB9fTwvZGQ+CiAgICAgIDxkdCBjbGFzcz0iY29sLXNtLTMiPlRpcG88L2R0PjxkZCBjbGFzcz0iY29sLXNtLTkiPnt7IGJhdGNoLnRpcG9faW1wb3J0YWNpb24gfX08L2RkPgogICAgICA8ZHQgY2xhc3M9ImNvbC1zbS0zIj5Vc3VhcmlvPC9kdD48ZGQgY2xhc3M9ImNvbC1zbS05Ij57eyBiYXRjaC51c3VhcmlvfGRlZmF1bHQ6IuKAlCIgfX08L2RkPgogICAgICA8ZHQgY2xhc3M9ImNvbC1zbS0zIj5SZXN1bWVuPC9kdD48ZGQgY2xhc3M9ImNvbC1zbS05Ij57eyBiYXRjaC5vYnNlcnZhY2lvbmVzfGRlZmF1bHQ6IuKAlCIgfX08L2RkPgogICAgPC9kbD4KICA8L2Rpdj4KPC9kaXY+Cgo8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSI+CiAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIgYmctd2hpdGUgZnctc2VtaWJvbGQiPkVycm9yZXMgcG9yIGZpbGEgeyUgaWYgZXJyb3JlcyAlfSh7eyBlcnJvcmVzfGxlbmd0aCB9fSl7JSBlbmRpZiAlfTwvZGl2PgogIDxkaXYgY2xhc3M9InRhYmxlLXJlc3BvbnNpdmUiPgogICAgPHRhYmxlIGNsYXNzPSJ0YWJsZSB0YWJsZS1zbSBtYi0wIj4KICAgICAgPHRoZWFkPgogICAgICAgIDx0cj4KICAgICAgICAgIDx0aD5GaWxhPC90aD4KICAgICAgICAgIDx0aD5DYW1wbzwvdGg+CiAgICAgICAgICA8dGg+TWVuc2FqZTwvdGg+CiAgICAgICAgPC90cj4KICAgICAgPC90aGVhZD4KICAgICAgPHRib2R5PgogICAgICAgIHslIGZvciBlcnIgaW4gZXJyb3JlcyAlfQogICAgICAgIDx0cj4KICAgICAgICAgIDx0ZD57eyBlcnIuZmlsYV9udW1lcm8gfX08L3RkPgogICAgICAgICAgPHRkPnt7IGVyci5jYW1wb3xkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgIDx0ZD57eyBlcnIubWVuc2FqZV9lcnJvciB9fTwvdGQ+CiAgICAgICAgPC90cj4KICAgICAgICB7JSBlbXB0eSAlfQogICAgICAgIDx0cj48dGQgY29sc3Bhbj0iMyIgY2xhc3M9InRleHQtbXV0ZWQgdGV4dC1jZW50ZXIgcHktMyI+U2luIGVycm9yZXMgZGUgZmlsYSByZWdpc3RyYWRvcy48L3RkPjwvdHI+CiAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgIDwvdGJvZHk+CiAgICA8L3RhYmxlPgogIDwvZGl2Pgo8L2Rpdj4KCjxkaXYgY2xhc3M9Im10LTMiPgogIDxhIGhyZWY9Ii8iIGNsYXNzPSJidG4gYnRuLW91dGxpbmUtc2Vjb25kYXJ5IGJ0bi1zbSI+SW5pY2lvPC9hPgogIHslIGlmIGJhdGNoLm1vZHVsbyA9PSAnY3JtJyAlfQogIDxhIGhyZWY9InslIHVybCAnd2Nnb25lX2NybTplbnRpZGFkX2xpc3QnICV9IiBjbGFzcz0iYnRuIGJ0bi1wcmltYXJ5IGJ0bi1zbSI+VmVyIGVudGlkYWRlczwvYT4KICB7JSBlbGlmIGJhdGNoLm1vZHVsbyA9PSAncmlzaycgJX0KICA8YSBocmVmPSJ7JSB1cmwgJ3djZ29uZV9yaXNrOmNvbWFuZG9fYmFsb24nICV9IiBjbGFzcz0iYnRuIGJ0bi1wcmltYXJ5IGJ0bi1zbSI+Q29tYW5kbyBCYWzDs248L2E+CiAgeyUgZWxpZiBiYXRjaC5tb2R1bG8gPT0gJ3BnbycgJX0KICA8YSBocmVmPSJ7JSB1cmwgJ3djZ29uZV9wZ286dGlja2V0X2xpc3QnICV9IiBjbGFzcz0iYnRuIGJ0bi1wcmltYXJ5IGJ0bi1zbSI+VmVyIHRpY2tldHM8L2E+CiAgeyUgZW5kaWYgJX0KPC9kaXY+CnslIGVuZGJsb2NrICV9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/wcgone/imports/upload.html
PATH_JSON="templates/wcgone/imports/upload.html"
FILENAME=upload.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=45
SIZE_BYTES_UTF8=1622
CONTENT_SHA256=0c4f44364157df677c3863291e16e5a9d379242f8926b886d7d5140848931fd9
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

{% block title %}{{ titulo }} — WCG One{% endblock %}

{% block content %}
<div class="row justify-content-center">
  <div class="col-lg-8">
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white">
        <h1 class="h5 fw-semibold mb-1">{{ titulo }}</h1>
        <p class="text-muted small mb-0">{{ descripcion }}</p>
      </div>
      <div class="card-body">
        {% if columnas_ejemplo %}
        <p class="small text-muted">
          <strong>Columnas sugeridas:</strong> {{ columnas_ejemplo }}
        </p>
        {% endif %}
        <form method="post" enctype="multipart/form-data" class="mt-3">
          {% csrf_token %}
          {% for field in form %}
          <div class="mb-3">
            <label class="form-label" for="{{ field.id_for_label }}">{{ field.label }}</label>
            {{ field }}
            {% if field.help_text %}
            <div class="form-text">{{ field.help_text }}</div>
            {% endif %}
            {% for error in field.errors %}
            <div class="text-danger small">{{ error }}</div>
            {% endfor %}
          </div>
          {% endfor %}
          {% if form.non_field_errors %}
          <div class="alert alert-danger small">{{ form.non_field_errors }}</div>
          {% endif %}
          <div class="d-flex gap-2">
            <button type="submit" class="btn btn-primary">Importar archivo</button>
            <a href="javascript:history.back()" class="btn btn-outline-secondary">Cancelar</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "wcgone_base.html" %}
00002|
00003|{% block title %}{{ titulo }} — WCG One{% endblock %}
00004|
00005|{% block content %}
00006|<div class="row justify-content-center">
00007|  <div class="col-lg-8">
00008|    <div class="card border-0 shadow-sm">
00009|      <div class="card-header bg-white">
00010|        <h1 class="h5 fw-semibold mb-1">{{ titulo }}</h1>
00011|        <p class="text-muted small mb-0">{{ descripcion }}</p>
00012|      </div>
00013|      <div class="card-body">
00014|        {% if columnas_ejemplo %}
00015|        <p class="small text-muted">
00016|          <strong>Columnas sugeridas:</strong> {{ columnas_ejemplo }}
00017|        </p>
00018|        {% endif %}
00019|        <form method="post" enctype="multipart/form-data" class="mt-3">
00020|          {% csrf_token %}
00021|          {% for field in form %}
00022|          <div class="mb-3">
00023|            <label class="form-label" for="{{ field.id_for_label }}">{{ field.label }}</label>
00024|            {{ field }}
00025|            {% if field.help_text %}
00026|            <div class="form-text">{{ field.help_text }}</div>
00027|            {% endif %}
00028|            {% for error in field.errors %}
00029|            <div class="text-danger small">{{ error }}</div>
00030|            {% endfor %}
00031|          </div>
00032|          {% endfor %}
00033|          {% if form.non_field_errors %}
00034|          <div class="alert alert-danger small">{{ form.non_field_errors }}</div>
00035|          {% endif %}
00036|          <div class="d-flex gap-2">
00037|            <button type="submit" class="btn btn-primary">Importar archivo</button>
00038|            <a href="javascript:history.back()" class="btn btn-outline-secondary">Cancelar</a>
00039|          </div>
00040|        </form>
00041|      </div>
00042|    </div>
00043|  </div>
00044|</div>
00045|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAid2Nnb25lX2Jhc2UuaHRtbCIgJX0KCnslIGJsb2NrIHRpdGxlICV9e3sgdGl0dWxvIH19IOKAlCBXQ0cgT25leyUgZW5kYmxvY2sgJX0KCnslIGJsb2NrIGNvbnRlbnQgJX0KPGRpdiBjbGFzcz0icm93IGp1c3RpZnktY29udGVudC1jZW50ZXIiPgogIDxkaXYgY2xhc3M9ImNvbC1sZy04Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIgYmctd2hpdGUiPgogICAgICAgIDxoMSBjbGFzcz0iaDUgZnctc2VtaWJvbGQgbWItMSI+e3sgdGl0dWxvIH19PC9oMT4KICAgICAgICA8cCBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCBtYi0wIj57eyBkZXNjcmlwY2lvbiB9fTwvcD4KICAgICAgPC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtYm9keSI+CiAgICAgICAgeyUgaWYgY29sdW1uYXNfZWplbXBsbyAlfQogICAgICAgIDxwIGNsYXNzPSJzbWFsbCB0ZXh0LW11dGVkIj4KICAgICAgICAgIDxzdHJvbmc+Q29sdW1uYXMgc3VnZXJpZGFzOjwvc3Ryb25nPiB7eyBjb2x1bW5hc19lamVtcGxvIH19CiAgICAgICAgPC9wPgogICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgPGZvcm0gbWV0aG9kPSJwb3N0IiBlbmN0eXBlPSJtdWx0aXBhcnQvZm9ybS1kYXRhIiBjbGFzcz0ibXQtMyI+CiAgICAgICAgICB7JSBjc3JmX3Rva2VuICV9CiAgICAgICAgICB7JSBmb3IgZmllbGQgaW4gZm9ybSAlfQogICAgICAgICAgPGRpdiBjbGFzcz0ibWItMyI+CiAgICAgICAgICAgIDxsYWJlbCBjbGFzcz0iZm9ybS1sYWJlbCIgZm9yPSJ7eyBmaWVsZC5pZF9mb3JfbGFiZWwgfX0iPnt7IGZpZWxkLmxhYmVsIH19PC9sYWJlbD4KICAgICAgICAgICAge3sgZmllbGQgfX0KICAgICAgICAgICAgeyUgaWYgZmllbGQuaGVscF90ZXh0ICV9CiAgICAgICAgICAgIDxkaXYgY2xhc3M9ImZvcm0tdGV4dCI+e3sgZmllbGQuaGVscF90ZXh0IH19PC9kaXY+CiAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgIHslIGZvciBlcnJvciBpbiBmaWVsZC5lcnJvcnMgJX0KICAgICAgICAgICAgPGRpdiBjbGFzcz0idGV4dC1kYW5nZXIgc21hbGwiPnt7IGVycm9yIH19PC9kaXY+CiAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgPC9kaXY+CiAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgIHslIGlmIGZvcm0ubm9uX2ZpZWxkX2Vycm9ycyAlfQogICAgICAgICAgPGRpdiBjbGFzcz0iYWxlcnQgYWxlcnQtZGFuZ2VyIHNtYWxsIj57eyBmb3JtLm5vbl9maWVsZF9lcnJvcnMgfX08L2Rpdj4KICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICA8ZGl2IGNsYXNzPSJkLWZsZXggZ2FwLTIiPgogICAgICAgICAgICA8YnV0dG9uIHR5cGU9InN1Ym1pdCIgY2xhc3M9ImJ0biBidG4tcHJpbWFyeSI+SW1wb3J0YXIgYXJjaGl2bzwvYnV0dG9uPgogICAgICAgICAgICA8YSBocmVmPSJqYXZhc2NyaXB0Omhpc3RvcnkuYmFjaygpIiBjbGFzcz0iYnRuIGJ0bi1vdXRsaW5lLXNlY29uZGFyeSI+Q2FuY2VsYXI8L2E+CiAgICAgICAgICA8L2Rpdj4KICAgICAgICA8L2Zvcm0+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CiAgPC9kaXY+CjwvZGl2Pgp7JSBlbmRibG9jayAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/wcgone/legacy_pgc1/home.html
PATH_JSON="templates/wcgone/legacy_pgc1/home.html"
FILENAME=home.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=30
SIZE_BYTES_UTF8=920
CONTENT_SHA256=20b4a5ced7e0a0c7f8ac446116fde000699c3d8c483f9f77802b9c8f2239dac4
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
{% extends "wcgone_base.html" %}

{% block title %}PGC — WCG One{% endblock %}

{% block content %}
<div class="row justify-content-center">
  <div class="col-lg-8">
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white">
        <h1 class="h4 fw-semibold mb-0">PGC</h1>
      </div>
      <div class="card-body">
        <p class="text-muted">
          Acceso correcto al módulo PGC.
        </p>
        <p class="small text-muted mb-4">
          Use el siguiente botón para ingresar al tablero operativo actual.
        </p>
        <div class="d-flex gap-2 flex-wrap">
          <a href="https://wcg.lol/tablero/" class="btn btn-primary" target="_blank" rel="noopener noreferrer">
            Ir a PGC
          </a>
          <a href="{% url 'portal:home' %}" class="btn btn-outline-secondary">Inicio WCG One</a>
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "wcgone_base.html" %}
00002|
00003|{% block title %}PGC — WCG One{% endblock %}
00004|
00005|{% block content %}
00006|<div class="row justify-content-center">
00007|  <div class="col-lg-8">
00008|    <div class="card border-0 shadow-sm">
00009|      <div class="card-header bg-white">
00010|        <h1 class="h4 fw-semibold mb-0">PGC</h1>
00011|      </div>
00012|      <div class="card-body">
00013|        <p class="text-muted">
00014|          Acceso correcto al módulo PGC.
00015|        </p>
00016|        <p class="small text-muted mb-4">
00017|          Use el siguiente botón para ingresar al tablero operativo actual.
00018|        </p>
00019|        <div class="d-flex gap-2 flex-wrap">
00020|          <a href="https://wcg.lol/tablero/" class="btn btn-primary" target="_blank" rel="noopener noreferrer">
00021|            Ir a PGC
00022|          </a>
00023|          <a href="{% url 'portal:home' %}" class="btn btn-outline-secondary">Inicio WCG One</a>
00024|        </div>
00025|      </div>
00026|    </div>
00027|  </div>
00028|</div>
00029|{% endblock %}
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAid2Nnb25lX2Jhc2UuaHRtbCIgJX0KCnslIGJsb2NrIHRpdGxlICV9UEdDIOKAlCBXQ0cgT25leyUgZW5kYmxvY2sgJX0KCnslIGJsb2NrIGNvbnRlbnQgJX0KPGRpdiBjbGFzcz0icm93IGp1c3RpZnktY29udGVudC1jZW50ZXIiPgogIDxkaXYgY2xhc3M9ImNvbC1sZy04Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIgYmctd2hpdGUiPgogICAgICAgIDxoMSBjbGFzcz0iaDQgZnctc2VtaWJvbGQgbWItMCI+UEdDPC9oMT4KICAgICAgPC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtYm9keSI+CiAgICAgICAgPHAgY2xhc3M9InRleHQtbXV0ZWQiPgogICAgICAgICAgQWNjZXNvIGNvcnJlY3RvIGFsIG3Ds2R1bG8gUEdDLgogICAgICAgIDwvcD4KICAgICAgICA8cCBjbGFzcz0ic21hbGwgdGV4dC1tdXRlZCBtYi00Ij4KICAgICAgICAgIFVzZSBlbCBzaWd1aWVudGUgYm90w7NuIHBhcmEgaW5ncmVzYXIgYWwgdGFibGVybyBvcGVyYXRpdm8gYWN0dWFsLgogICAgICAgIDwvcD4KICAgICAgICA8ZGl2IGNsYXNzPSJkLWZsZXggZ2FwLTIgZmxleC13cmFwIj4KICAgICAgICAgIDxhIGhyZWY9Imh0dHBzOi8vd2NnLmxvbC90YWJsZXJvLyIgY2xhc3M9ImJ0biBidG4tcHJpbWFyeSIgdGFyZ2V0PSJfYmxhbmsiIHJlbD0ibm9vcGVuZXIgbm9yZWZlcnJlciI+CiAgICAgICAgICAgIElyIGEgUEdDCiAgICAgICAgICA8L2E+CiAgICAgICAgICA8YSBocmVmPSJ7JSB1cmwgJ3BvcnRhbDpob21lJyAlfSIgY2xhc3M9ImJ0biBidG4tb3V0bGluZS1zZWNvbmRhcnkiPkluaWNpbyBXQ0cgT25lPC9hPgogICAgICAgIDwvZGl2PgogICAgICA8L2Rpdj4KICAgIDwvZGl2PgogIDwvZGl2Pgo8L2Rpdj4KeyUgZW5kYmxvY2sgJX0=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/wcgone/pgc/home.html
PATH_JSON="templates/wcgone/pgc/home.html"
FILENAME=home.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=29
SIZE_BYTES_UTF8=1102
CONTENT_SHA256=5ac31d6649f2f32a7a69dfe9855697a19b995727e29aea9b6e32631531ab3824
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

{% block title %}PGC — WCG One{% endblock %}

{% block content %}
<div class="row justify-content-center">
  <div class="col-lg-8">
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white">
        <h1 class="h4 fw-semibold mb-0">Módulo PGC</h1>
      </div>
      <div class="card-body">
        <p class="text-muted">
          El módulo PGC se integra progresivamente a WCG One. En esta etapa opera como
          <strong>placeholder ordenado</strong> mientras se completa la absorción del sistema legado.
        </p>
        <div class="alert alert-info small mb-4">
          El PGC funcional completo sigue disponible en el sistema legado.
          Use el enlace inferior para acceder durante la transición.
        </div>
        <div class="d-flex gap-2 flex-wrap">
          <a href="{% url 'pgc:module_home' %}" class="btn btn-primary">Ir a PGC Legado</a>
          <a href="{% url 'portal:home' %}" class="btn btn-outline-secondary">Volver al inicio</a>
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "wcgone_base.html" %}
00002|
00003|{% block title %}PGC — WCG One{% endblock %}
00004|
00005|{% block content %}
00006|<div class="row justify-content-center">
00007|  <div class="col-lg-8">
00008|    <div class="card border-0 shadow-sm">
00009|      <div class="card-header bg-white">
00010|        <h1 class="h4 fw-semibold mb-0">Módulo PGC</h1>
00011|      </div>
00012|      <div class="card-body">
00013|        <p class="text-muted">
00014|          El módulo PGC se integra progresivamente a WCG One. En esta etapa opera como
00015|          <strong>placeholder ordenado</strong> mientras se completa la absorción del sistema legado.
00016|        </p>
00017|        <div class="alert alert-info small mb-4">
00018|          El PGC funcional completo sigue disponible en el sistema legado.
00019|          Use el enlace inferior para acceder durante la transición.
00020|        </div>
00021|        <div class="d-flex gap-2 flex-wrap">
00022|          <a href="{% url 'pgc:module_home' %}" class="btn btn-primary">Ir a PGC Legado</a>
00023|          <a href="{% url 'portal:home' %}" class="btn btn-outline-secondary">Volver al inicio</a>
00024|        </div>
00025|      </div>
00026|    </div>
00027|  </div>
00028|</div>
00029|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAid2Nnb25lX2Jhc2UuaHRtbCIgJX0KCnslIGJsb2NrIHRpdGxlICV9UEdDIOKAlCBXQ0cgT25leyUgZW5kYmxvY2sgJX0KCnslIGJsb2NrIGNvbnRlbnQgJX0KPGRpdiBjbGFzcz0icm93IGp1c3RpZnktY29udGVudC1jZW50ZXIiPgogIDxkaXYgY2xhc3M9ImNvbC1sZy04Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIgYmctd2hpdGUiPgogICAgICAgIDxoMSBjbGFzcz0iaDQgZnctc2VtaWJvbGQgbWItMCI+TcOzZHVsbyBQR0M8L2gxPgogICAgICA8L2Rpdj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1ib2R5Ij4KICAgICAgICA8cCBjbGFzcz0idGV4dC1tdXRlZCI+CiAgICAgICAgICBFbCBtw7NkdWxvIFBHQyBzZSBpbnRlZ3JhIHByb2dyZXNpdmFtZW50ZSBhIFdDRyBPbmUuIEVuIGVzdGEgZXRhcGEgb3BlcmEgY29tbwogICAgICAgICAgPHN0cm9uZz5wbGFjZWhvbGRlciBvcmRlbmFkbzwvc3Ryb25nPiBtaWVudHJhcyBzZSBjb21wbGV0YSBsYSBhYnNvcmNpw7NuIGRlbCBzaXN0ZW1hIGxlZ2Fkby4KICAgICAgICA8L3A+CiAgICAgICAgPGRpdiBjbGFzcz0iYWxlcnQgYWxlcnQtaW5mbyBzbWFsbCBtYi00Ij4KICAgICAgICAgIEVsIFBHQyBmdW5jaW9uYWwgY29tcGxldG8gc2lndWUgZGlzcG9uaWJsZSBlbiBlbCBzaXN0ZW1hIGxlZ2Fkby4KICAgICAgICAgIFVzZSBlbCBlbmxhY2UgaW5mZXJpb3IgcGFyYSBhY2NlZGVyIGR1cmFudGUgbGEgdHJhbnNpY2nDs24uCiAgICAgICAgPC9kaXY+CiAgICAgICAgPGRpdiBjbGFzcz0iZC1mbGV4IGdhcC0yIGZsZXgtd3JhcCI+CiAgICAgICAgICA8YSBocmVmPSJ7JSB1cmwgJ3BnYzptb2R1bGVfaG9tZScgJX0iIGNsYXNzPSJidG4gYnRuLXByaW1hcnkiPklyIGEgUEdDIExlZ2FkbzwvYT4KICAgICAgICAgIDxhIGhyZWY9InslIHVybCAncG9ydGFsOmhvbWUnICV9IiBjbGFzcz0iYnRuIGJ0bi1vdXRsaW5lLXNlY29uZGFyeSI+Vm9sdmVyIGFsIGluaWNpbzwvYT4KICAgICAgICA8L2Rpdj4KICAgICAgPC9kaXY+CiAgICA8L2Rpdj4KICA8L2Rpdj4KPC9kaXY+CnslIGVuZGJsb2NrICV9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/wcgone/pgo/dashboard.html
PATH_JSON="templates/wcgone/pgo/dashboard.html"
FILENAME=dashboard.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=119
SIZE_BYTES_UTF8=4932
CONTENT_SHA256=6d6ab7907293050bda6675d15a0d4310099ed62f044b138963a8368cc5fa4f83
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

{% block title %}PGO — WCG One{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-2">
  <div class="wcg-report-head">
    <h1 class="h4 fw-semibold mb-0">PGO — Operación y tickets</h1>
    {% include "includes/module_mark.html" with module="pgo" %}
  </div>
  <div class="d-flex gap-1 flex-wrap">
    <a href="{% url 'wcgone_pgo:export_tickets' %}" class="btn btn-sm btn-outline-primary">Exportar CSV</a>
    <a href="{% url 'wcgone_pgo:ticket_list' %}" class="btn btn-sm btn-outline-primary">Ver todos</a>
    <a href="{% url 'wcgone_pgo:resultados' %}" class="btn btn-sm btn-outline-secondary">Resultados</a>
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
      <div class="stat-value text-warning" style="font-size:1.35rem;">{{ tickets_vencidos }}</div><div class="text-muted small">Abiertos SLA vencido</div>
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
  <div class="col-md-6">
    <div class="card border-0 shadow-sm h-100">
      <div class="card-header bg-white fw-semibold small">Por estado</div>
      <ul class="list-group list-group-flush small">
        {% for row in por_estado %}
        <li class="list-group-item d-flex justify-content-between">
          <span>{{ row.estado_normalizado|default:"(sin estado)" }}</span>
          <span class="badge text-bg-secondary">{{ row.total }}</span>
        </li>
        {% empty %}
        <li class="list-group-item text-muted">Sin datos de tickets.</li>
        {% endfor %}
      </ul>
    </div>
  </div>
  <div class="col-md-6">
    <div class="card border-0 shadow-sm h-100">
      <div class="card-header bg-white fw-semibold small">Por prioridad</div>
      <ul class="list-group list-group-flush small">
        {% for row in por_prioridad %}
        <li class="list-group-item d-flex justify-content-between">
          <span>{{ row.prioridad }}</span>
          <span class="badge text-bg-secondary">{{ row.total }}</span>
        </li>
        {% empty %}
        <li class="list-group-item text-muted">Sin prioridades registradas.</li>
        {% endfor %}
      </ul>
    </div>
  </div>
</div>

{% if total_tickets == 0 %}
{% include "includes/empty_state.html" with title="Sin tickets PGO" message="Cargue tickets desde Administración → Importación General." %}
{% endif %}

<div class="card border-0 shadow-sm">
  <div class="card-header bg-white fw-semibold">Tickets recientes</div>
  <div class="table-responsive">
    <table class="table table-hover table-wcg mb-0 small">
      <thead>
        <tr>
          <th>ID</th>
          <th>Título</th>
          <th>Estado</th>
          <th>Prioridad</th>
          <th>Departamento</th>
          <th>Apertura</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {% for ticket in tickets_recientes %}
        <tr>
          <td>{{ ticket.ticket_externo_id|default:ticket.pk }}</td>
          <td>{{ ticket.titulo|truncatechars:50 }}</td>
          <td>{{ ticket.estado_normalizado|default:ticket.estado_raw|default:"—" }}</td>
          <td>{{ ticket.prioridad|default:"—" }}</td>
          <td>{{ ticket.departamento|default:"—" }}</td>
          <td>{{ ticket.fecha_apertura|date:"d/m/Y H:i"|default:"—" }}</td>
          <td class="text-end">
            <a href="{% url 'wcgone_pgo:ticket_detail' ticket.pk %}" class="btn btn-sm btn-outline-primary">Ver</a>
          </td>
        </tr>
        {% empty %}
        <tr><td colspan="7" class="text-center text-muted py-4">No hay tickets registrados.</td></tr>
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
00003|{% block title %}PGO — WCG One{% endblock %}
00004|
00005|{% block content %}
00006|<div class="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-2">
00007|  <div class="wcg-report-head">
00008|    <h1 class="h4 fw-semibold mb-0">PGO — Operación y tickets</h1>
00009|    {% include "includes/module_mark.html" with module="pgo" %}
00010|  </div>
00011|  <div class="d-flex gap-1 flex-wrap">
00012|    <a href="{% url 'wcgone_pgo:export_tickets' %}" class="btn btn-sm btn-outline-primary">Exportar CSV</a>
00013|    <a href="{% url 'wcgone_pgo:ticket_list' %}" class="btn btn-sm btn-outline-primary">Ver todos</a>
00014|    <a href="{% url 'wcgone_pgo:resultados' %}" class="btn btn-sm btn-outline-secondary">Resultados</a>
00015|  </div>
00016|</div>
00017|
00018|<div class="row g-2 mb-3">
00019|  <div class="col-md-2 col-6">
00020|    <div class="card border-0 shadow-sm text-center"><div class="card-body py-2">
00021|      <div class="stat-value" style="font-size:1.35rem;">{{ total_tickets }}</div><div class="text-muted small">Total</div>
00022|    </div></div>
00023|  </div>
00024|  <div class="col-md-2 col-6">
00025|    <div class="card border-0 shadow-sm text-center"><div class="card-body py-2">
00026|      <div class="stat-value" style="font-size:1.35rem;">{{ tickets_abiertos }}</div><div class="text-muted small">Abiertos</div>
00027|    </div></div>
00028|  </div>
00029|  <div class="col-md-2 col-6">
00030|    <div class="card border-0 shadow-sm text-center"><div class="card-body py-2">
00031|      <div class="stat-value" style="font-size:1.35rem;">{{ tickets_cerrados }}</div><div class="text-muted small">Cerrados</div>
00032|    </div></div>
00033|  </div>
00034|  <div class="col-md-2 col-6">
00035|    <div class="card border-0 shadow-sm text-center"><div class="card-body py-2">
00036|      <div class="stat-value text-warning" style="font-size:1.35rem;">{{ tickets_vencidos }}</div><div class="text-muted small">Abiertos SLA vencido</div>
00037|    </div></div>
00038|  </div>
00039|  <div class="col-md-2 col-6">
00040|    <div class="card border-0 shadow-sm text-center"><div class="card-body py-2">
00041|      <div class="stat-value" style="font-size:1.35rem;">{% if tiempo_promedio %}{{ tiempo_promedio|floatformat:1 }}{% else %}—{% endif %}</div>
00042|      <div class="text-muted small">Horas promedio</div>
00043|    </div></div>
00044|  </div>
00045|</div>
00046|
00047|<div class="row g-3 mb-4">
00048|  <div class="col-md-6">
00049|    <div class="card border-0 shadow-sm h-100">
00050|      <div class="card-header bg-white fw-semibold small">Por estado</div>
00051|      <ul class="list-group list-group-flush small">
00052|        {% for row in por_estado %}
00053|        <li class="list-group-item d-flex justify-content-between">
00054|          <span>{{ row.estado_normalizado|default:"(sin estado)" }}</span>
00055|          <span class="badge text-bg-secondary">{{ row.total }}</span>
00056|        </li>
00057|        {% empty %}
00058|        <li class="list-group-item text-muted">Sin datos de tickets.</li>
00059|        {% endfor %}
00060|      </ul>
00061|    </div>
00062|  </div>
00063|  <div class="col-md-6">
00064|    <div class="card border-0 shadow-sm h-100">
00065|      <div class="card-header bg-white fw-semibold small">Por prioridad</div>
00066|      <ul class="list-group list-group-flush small">
00067|        {% for row in por_prioridad %}
00068|        <li class="list-group-item d-flex justify-content-between">
00069|          <span>{{ row.prioridad }}</span>
00070|          <span class="badge text-bg-secondary">{{ row.total }}</span>
00071|        </li>
00072|        {% empty %}
00073|        <li class="list-group-item text-muted">Sin prioridades registradas.</li>
00074|        {% endfor %}
00075|      </ul>
00076|    </div>
00077|  </div>
00078|</div>
00079|
00080|{% if total_tickets == 0 %}
00081|{% include "includes/empty_state.html" with title="Sin tickets PGO" message="Cargue tickets desde Administración → Importación General." %}
00082|{% endif %}
00083|
00084|<div class="card border-0 shadow-sm">
00085|  <div class="card-header bg-white fw-semibold">Tickets recientes</div>
00086|  <div class="table-responsive">
00087|    <table class="table table-hover table-wcg mb-0 small">
00088|      <thead>
00089|        <tr>
00090|          <th>ID</th>
00091|          <th>Título</th>
00092|          <th>Estado</th>
00093|          <th>Prioridad</th>
00094|          <th>Departamento</th>
00095|          <th>Apertura</th>
00096|          <th></th>
00097|        </tr>
00098|      </thead>
00099|      <tbody>
00100|        {% for ticket in tickets_recientes %}
00101|        <tr>
00102|          <td>{{ ticket.ticket_externo_id|default:ticket.pk }}</td>
00103|          <td>{{ ticket.titulo|truncatechars:50 }}</td>
00104|          <td>{{ ticket.estado_normalizado|default:ticket.estado_raw|default:"—" }}</td>
00105|          <td>{{ ticket.prioridad|default:"—" }}</td>
00106|          <td>{{ ticket.departamento|default:"—" }}</td>
00107|          <td>{{ ticket.fecha_apertura|date:"d/m/Y H:i"|default:"—" }}</td>
00108|          <td class="text-end">
00109|            <a href="{% url 'wcgone_pgo:ticket_detail' ticket.pk %}" class="btn btn-sm btn-outline-primary">Ver</a>
00110|          </td>
00111|        </tr>
00112|        {% empty %}
00113|        <tr><td colspan="7" class="text-center text-muted py-4">No hay tickets registrados.</td></tr>
00114|        {% endfor %}
00115|      </tbody>
00116|    </table>
00117|  </div>
00118|</div>
00119|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAid2Nnb25lX2Jhc2UuaHRtbCIgJX0KCnslIGJsb2NrIHRpdGxlICV9UEdPIOKAlCBXQ0cgT25leyUgZW5kYmxvY2sgJX0KCnslIGJsb2NrIGNvbnRlbnQgJX0KPGRpdiBjbGFzcz0iZC1mbGV4IGp1c3RpZnktY29udGVudC1iZXR3ZWVuIGFsaWduLWl0ZW1zLXN0YXJ0IG1iLTMgZmxleC13cmFwIGdhcC0yIj4KICA8ZGl2IGNsYXNzPSJ3Y2ctcmVwb3J0LWhlYWQiPgogICAgPGgxIGNsYXNzPSJoNCBmdy1zZW1pYm9sZCBtYi0wIj5QR08g4oCUIE9wZXJhY2nDs24geSB0aWNrZXRzPC9oMT4KICAgIHslIGluY2x1ZGUgImluY2x1ZGVzL21vZHVsZV9tYXJrLmh0bWwiIHdpdGggbW9kdWxlPSJwZ28iICV9CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iZC1mbGV4IGdhcC0xIGZsZXgtd3JhcCI+CiAgICA8YSBocmVmPSJ7JSB1cmwgJ3djZ29uZV9wZ286ZXhwb3J0X3RpY2tldHMnICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1wcmltYXJ5Ij5FeHBvcnRhciBDU1Y8L2E+CiAgICA8YSBocmVmPSJ7JSB1cmwgJ3djZ29uZV9wZ286dGlja2V0X2xpc3QnICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1wcmltYXJ5Ij5WZXIgdG9kb3M8L2E+CiAgICA8YSBocmVmPSJ7JSB1cmwgJ3djZ29uZV9wZ286cmVzdWx0YWRvcycgJX0iIGNsYXNzPSJidG4gYnRuLXNtIGJ0bi1vdXRsaW5lLXNlY29uZGFyeSI+UmVzdWx0YWRvczwvYT4KICA8L2Rpdj4KPC9kaXY+Cgo8ZGl2IGNsYXNzPSJyb3cgZy0yIG1iLTMiPgogIDxkaXYgY2xhc3M9ImNvbC1tZC0yIGNvbC02Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIHRleHQtY2VudGVyIj48ZGl2IGNsYXNzPSJjYXJkLWJvZHkgcHktMiI+CiAgICAgIDxkaXYgY2xhc3M9InN0YXQtdmFsdWUiIHN0eWxlPSJmb250LXNpemU6MS4zNXJlbTsiPnt7IHRvdGFsX3RpY2tldHMgfX08L2Rpdj48ZGl2IGNsYXNzPSJ0ZXh0LW11dGVkIHNtYWxsIj5Ub3RhbDwvZGl2PgogICAgPC9kaXY+PC9kaXY+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTIgY29sLTYiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20gdGV4dC1jZW50ZXIiPjxkaXYgY2xhc3M9ImNhcmQtYm9keSBweS0yIj4KICAgICAgPGRpdiBjbGFzcz0ic3RhdC12YWx1ZSIgc3R5bGU9ImZvbnQtc2l6ZToxLjM1cmVtOyI+e3sgdGlja2V0c19hYmllcnRvcyB9fTwvZGl2PjxkaXYgY2xhc3M9InRleHQtbXV0ZWQgc21hbGwiPkFiaWVydG9zPC9kaXY+CiAgICA8L2Rpdj48L2Rpdj4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtMiBjb2wtNiI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSB0ZXh0LWNlbnRlciI+PGRpdiBjbGFzcz0iY2FyZC1ib2R5IHB5LTIiPgogICAgICA8ZGl2IGNsYXNzPSJzdGF0LXZhbHVlIiBzdHlsZT0iZm9udC1zaXplOjEuMzVyZW07Ij57eyB0aWNrZXRzX2NlcnJhZG9zIH19PC9kaXY+PGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+Q2VycmFkb3M8L2Rpdj4KICAgIDwvZGl2PjwvZGl2PgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1tZC0yIGNvbC02Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIHRleHQtY2VudGVyIj48ZGl2IGNsYXNzPSJjYXJkLWJvZHkgcHktMiI+CiAgICAgIDxkaXYgY2xhc3M9InN0YXQtdmFsdWUgdGV4dC13YXJuaW5nIiBzdHlsZT0iZm9udC1zaXplOjEuMzVyZW07Ij57eyB0aWNrZXRzX3ZlbmNpZG9zIH19PC9kaXY+PGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+QWJpZXJ0b3MgU0xBIHZlbmNpZG88L2Rpdj4KICAgIDwvZGl2PjwvZGl2PgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1tZC0yIGNvbC02Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIHRleHQtY2VudGVyIj48ZGl2IGNsYXNzPSJjYXJkLWJvZHkgcHktMiI+CiAgICAgIDxkaXYgY2xhc3M9InN0YXQtdmFsdWUiIHN0eWxlPSJmb250LXNpemU6MS4zNXJlbTsiPnslIGlmIHRpZW1wb19wcm9tZWRpbyAlfXt7IHRpZW1wb19wcm9tZWRpb3xmbG9hdGZvcm1hdDoxIH19eyUgZWxzZSAlfeKAlHslIGVuZGlmICV9PC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9InRleHQtbXV0ZWQgc21hbGwiPkhvcmFzIHByb21lZGlvPC9kaXY+CiAgICA8L2Rpdj48L2Rpdj4KICA8L2Rpdj4KPC9kaXY+Cgo8ZGl2IGNsYXNzPSJyb3cgZy0zIG1iLTQiPgogIDxkaXYgY2xhc3M9ImNvbC1tZC02Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIGgtMTAwIj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIgYmctd2hpdGUgZnctc2VtaWJvbGQgc21hbGwiPlBvciBlc3RhZG88L2Rpdj4KICAgICAgPHVsIGNsYXNzPSJsaXN0LWdyb3VwIGxpc3QtZ3JvdXAtZmx1c2ggc21hbGwiPgogICAgICAgIHslIGZvciByb3cgaW4gcG9yX2VzdGFkbyAlfQogICAgICAgIDxsaSBjbGFzcz0ibGlzdC1ncm91cC1pdGVtIGQtZmxleCBqdXN0aWZ5LWNvbnRlbnQtYmV0d2VlbiI+CiAgICAgICAgICA8c3Bhbj57eyByb3cuZXN0YWRvX25vcm1hbGl6YWRvfGRlZmF1bHQ6IihzaW4gZXN0YWRvKSIgfX08L3NwYW4+CiAgICAgICAgICA8c3BhbiBjbGFzcz0iYmFkZ2UgdGV4dC1iZy1zZWNvbmRhcnkiPnt7IHJvdy50b3RhbCB9fTwvc3Bhbj4KICAgICAgICA8L2xpPgogICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgPGxpIGNsYXNzPSJsaXN0LWdyb3VwLWl0ZW0gdGV4dC1tdXRlZCI+U2luIGRhdG9zIGRlIHRpY2tldHMuPC9saT4KICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgPC91bD4KICAgIDwvZGl2PgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1tZC02Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIGgtMTAwIj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIgYmctd2hpdGUgZnctc2VtaWJvbGQgc21hbGwiPlBvciBwcmlvcmlkYWQ8L2Rpdj4KICAgICAgPHVsIGNsYXNzPSJsaXN0LWdyb3VwIGxpc3QtZ3JvdXAtZmx1c2ggc21hbGwiPgogICAgICAgIHslIGZvciByb3cgaW4gcG9yX3ByaW9yaWRhZCAlfQogICAgICAgIDxsaSBjbGFzcz0ibGlzdC1ncm91cC1pdGVtIGQtZmxleCBqdXN0aWZ5LWNvbnRlbnQtYmV0d2VlbiI+CiAgICAgICAgICA8c3Bhbj57eyByb3cucHJpb3JpZGFkIH19PC9zcGFuPgogICAgICAgICAgPHNwYW4gY2xhc3M9ImJhZGdlIHRleHQtYmctc2Vjb25kYXJ5Ij57eyByb3cudG90YWwgfX08L3NwYW4+CiAgICAgICAgPC9saT4KICAgICAgICB7JSBlbXB0eSAlfQogICAgICAgIDxsaSBjbGFzcz0ibGlzdC1ncm91cC1pdGVtIHRleHQtbXV0ZWQiPlNpbiBwcmlvcmlkYWRlcyByZWdpc3RyYWRhcy48L2xpPgogICAgICAgIHslIGVuZGZvciAlfQogICAgICA8L3VsPgogICAgPC9kaXY+CiAgPC9kaXY+CjwvZGl2PgoKeyUgaWYgdG90YWxfdGlja2V0cyA9PSAwICV9CnslIGluY2x1ZGUgImluY2x1ZGVzL2VtcHR5X3N0YXRlLmh0bWwiIHdpdGggdGl0bGU9IlNpbiB0aWNrZXRzIFBHTyIgbWVzc2FnZT0iQ2FyZ3VlIHRpY2tldHMgZGVzZGUgQWRtaW5pc3RyYWNpw7NuIOKGkiBJbXBvcnRhY2nDs24gR2VuZXJhbC4iICV9CnslIGVuZGlmICV9Cgo8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSI+CiAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIgYmctd2hpdGUgZnctc2VtaWJvbGQiPlRpY2tldHMgcmVjaWVudGVzPC9kaXY+CiAgPGRpdiBjbGFzcz0idGFibGUtcmVzcG9uc2l2ZSI+CiAgICA8dGFibGUgY2xhc3M9InRhYmxlIHRhYmxlLWhvdmVyIHRhYmxlLXdjZyBtYi0wIHNtYWxsIj4KICAgICAgPHRoZWFkPgogICAgICAgIDx0cj4KICAgICAgICAgIDx0aD5JRDwvdGg+CiAgICAgICAgICA8dGg+VMOtdHVsbzwvdGg+CiAgICAgICAgICA8dGg+RXN0YWRvPC90aD4KICAgICAgICAgIDx0aD5QcmlvcmlkYWQ8L3RoPgogICAgICAgICAgPHRoPkRlcGFydGFtZW50bzwvdGg+CiAgICAgICAgICA8dGg+QXBlcnR1cmE8L3RoPgogICAgICAgICAgPHRoPjwvdGg+CiAgICAgICAgPC90cj4KICAgICAgPC90aGVhZD4KICAgICAgPHRib2R5PgogICAgICAgIHslIGZvciB0aWNrZXQgaW4gdGlja2V0c19yZWNpZW50ZXMgJX0KICAgICAgICA8dHI+CiAgICAgICAgICA8dGQ+e3sgdGlja2V0LnRpY2tldF9leHRlcm5vX2lkfGRlZmF1bHQ6dGlja2V0LnBrIH19PC90ZD4KICAgICAgICAgIDx0ZD57eyB0aWNrZXQudGl0dWxvfHRydW5jYXRlY2hhcnM6NTAgfX08L3RkPgogICAgICAgICAgPHRkPnt7IHRpY2tldC5lc3RhZG9fbm9ybWFsaXphZG98ZGVmYXVsdDp0aWNrZXQuZXN0YWRvX3Jhd3xkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgIDx0ZD57eyB0aWNrZXQucHJpb3JpZGFkfGRlZmF1bHQ6IuKAlCIgfX08L3RkPgogICAgICAgICAgPHRkPnt7IHRpY2tldC5kZXBhcnRhbWVudG98ZGVmYXVsdDoi4oCUIiB9fTwvdGQ+CiAgICAgICAgICA8dGQ+e3sgdGlja2V0LmZlY2hhX2FwZXJ0dXJhfGRhdGU6ImQvbS9ZIEg6aSJ8ZGVmYXVsdDoi4oCUIiB9fTwvdGQ+CiAgICAgICAgICA8dGQgY2xhc3M9InRleHQtZW5kIj4KICAgICAgICAgICAgPGEgaHJlZj0ieyUgdXJsICd3Y2dvbmVfcGdvOnRpY2tldF9kZXRhaWwnIHRpY2tldC5wayAlfSIgY2xhc3M9ImJ0biBidG4tc20gYnRuLW91dGxpbmUtcHJpbWFyeSI+VmVyPC9hPgogICAgICAgICAgPC90ZD4KICAgICAgICA8L3RyPgogICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgPHRyPjx0ZCBjb2xzcGFuPSI3IiBjbGFzcz0idGV4dC1jZW50ZXIgdGV4dC1tdXRlZCBweS00Ij5ObyBoYXkgdGlja2V0cyByZWdpc3RyYWRvcy48L3RkPjwvdHI+CiAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgIDwvdGJvZHk+CiAgICA8L3RhYmxlPgogIDwvZGl2Pgo8L2Rpdj4KeyUgZW5kYmxvY2sgJX0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/wcgone/pgo/resultados.html
PATH_JSON="templates/wcgone/pgo/resultados.html"
FILENAME=resultados.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=93
SIZE_BYTES_UTF8=4004
CONTENT_SHA256=bb35f8dec53ff90d9b529a8f5b66d19e52504bdf64efeded6bcb539b32a106fc
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

{% block title %}Resultados — PGO — WCG One{% endblock %}

{% block content %}
<style>
  /*
    Mismo patrón visual que PGC (dashboard.html):
    Sí  = cian-azulado; No = ámbar-naranja (distingibles también en daltonismo verde-rojo).
    Fuente de verdad: PgoPeriodScore.clasifica (BooleanField), no se recalcula aquí.
  */
  table.pgo-scoreboard tbody tr.row-clasifica-si td { background: #dff6fb; }
  table.pgo-scoreboard tbody tr.row-clasifica-no td { background: #fde8c8; }
  table.pgo-scoreboard tbody tr.row-clasifica-si td:first-child { box-shadow: inset 5px 0 0 #0284c7; }
  table.pgo-scoreboard tbody tr.row-clasifica-no td:first-child { box-shadow: inset 5px 0 0 #c2410c; }
  table.pgo-scoreboard tbody tr.row-clasifica-si:hover td { background: #cfeef7; }
  table.pgo-scoreboard tbody tr.row-clasifica-no:hover td { background: #fbd9a8; }
</style>

<div class="d-flex justify-content-between align-items-center mb-3">
  <div class="wcg-report-head">
    <h1 class="h4 fw-semibold mb-0">Resultados por período</h1>
    {% include "includes/module_mark.html" with module="pgo" %}
  </div>
  <a href="{% url 'wcgone_pgo:dashboard' %}" class="btn btn-sm btn-outline-secondary">Dashboard</a>
</div>

<form method="get" class="mb-3">
  <div class="input-group input-group-sm" style="max-width: 200px;">
    <input type="text" name="periodo" value="{{ request.GET.periodo }}" class="form-control" placeholder="YYYY-MM">
    <button class="btn btn-primary" type="submit">Filtrar</button>
  </div>
</form>

<div class="row g-3">
  <div class="col-lg-6">
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white fw-semibold">Puntajes por período</div>
      <div class="table-responsive">
        <table class="table table-sm mb-0 pgo-scoreboard">
          <thead><tr><th>Período</th><th>Área</th><th>Unidad</th><th class="text-end">Puntaje</th><th>Clasifica</th></tr></thead>
          <tbody>
            {% for score in scores %}
            <tr class="{% if score.clasifica %}row-clasifica-si{% else %}row-clasifica-no{% endif %}">
              <td>{{ score.periodo }}</td>
              <td>{{ score.area|default:"—" }}</td>
              <td>{{ score.unidad_negocio|default:"—" }}</td>
              <td class="text-end">{{ score.puntaje_total }}</td>
              <td>
                {% if score.clasifica %}
                  <span class="badge text-bg-success">Sí</span>
                {% else %}
                  <span class="badge text-bg-secondary">No</span>
                {% endif %}
              </td>
            </tr>
            {% empty %}
            <tr><td colspan="5" class="text-muted text-center py-3">Sin puntajes calculados.</td></tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
      <div class="card-footer bg-white small text-muted">
        Color de fila según <code>PgoPeriodScore.clasifica</code> (valor almacenado).
        En el código actual no hay comando que calcule ese booleano ni umbral ≥80.
      </div>
    </div>
  </div>
  <div class="col-lg-6">
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white fw-semibold">Agregados mensuales</div>
      <div class="table-responsive">
        <table class="table table-sm mb-0">
          <thead><tr><th>Período</th><th>Unidad</th><th>Recibidos</th><th>Cerrados</th><th>Prom. h</th></tr></thead>
          <tbody>
            {% for agg in aggs %}
            <tr>
              <td>{{ agg.periodo }}</td>
              <td>{{ agg.unidad_negocio }}</td>
              <td>{{ agg.tickets_recibidos }}</td>
              <td>{{ agg.tickets_cerrados }}</td>
              <td>{{ agg.tiempo_promedio_horas }}</td>
            </tr>
            {% empty %}
            <tr><td colspan="5" class="text-muted text-center py-3">Sin agregados mensuales.</td></tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "wcgone_base.html" %}
00002|
00003|{% block title %}Resultados — PGO — WCG One{% endblock %}
00004|
00005|{% block content %}
00006|<style>
00007|  /*
00008|    Mismo patrón visual que PGC (dashboard.html):
00009|    Sí  = cian-azulado; No = ámbar-naranja (distingibles también en daltonismo verde-rojo).
00010|    Fuente de verdad: PgoPeriodScore.clasifica (BooleanField), no se recalcula aquí.
00011|  */
00012|  table.pgo-scoreboard tbody tr.row-clasifica-si td { background: #dff6fb; }
00013|  table.pgo-scoreboard tbody tr.row-clasifica-no td { background: #fde8c8; }
00014|  table.pgo-scoreboard tbody tr.row-clasifica-si td:first-child { box-shadow: inset 5px 0 0 #0284c7; }
00015|  table.pgo-scoreboard tbody tr.row-clasifica-no td:first-child { box-shadow: inset 5px 0 0 #c2410c; }
00016|  table.pgo-scoreboard tbody tr.row-clasifica-si:hover td { background: #cfeef7; }
00017|  table.pgo-scoreboard tbody tr.row-clasifica-no:hover td { background: #fbd9a8; }
00018|</style>
00019|
00020|<div class="d-flex justify-content-between align-items-center mb-3">
00021|  <div class="wcg-report-head">
00022|    <h1 class="h4 fw-semibold mb-0">Resultados por período</h1>
00023|    {% include "includes/module_mark.html" with module="pgo" %}
00024|  </div>
00025|  <a href="{% url 'wcgone_pgo:dashboard' %}" class="btn btn-sm btn-outline-secondary">Dashboard</a>
00026|</div>
00027|
00028|<form method="get" class="mb-3">
00029|  <div class="input-group input-group-sm" style="max-width: 200px;">
00030|    <input type="text" name="periodo" value="{{ request.GET.periodo }}" class="form-control" placeholder="YYYY-MM">
00031|    <button class="btn btn-primary" type="submit">Filtrar</button>
00032|  </div>
00033|</form>
00034|
00035|<div class="row g-3">
00036|  <div class="col-lg-6">
00037|    <div class="card border-0 shadow-sm">
00038|      <div class="card-header bg-white fw-semibold">Puntajes por período</div>
00039|      <div class="table-responsive">
00040|        <table class="table table-sm mb-0 pgo-scoreboard">
00041|          <thead><tr><th>Período</th><th>Área</th><th>Unidad</th><th class="text-end">Puntaje</th><th>Clasifica</th></tr></thead>
00042|          <tbody>
00043|            {% for score in scores %}
00044|            <tr class="{% if score.clasifica %}row-clasifica-si{% else %}row-clasifica-no{% endif %}">
00045|              <td>{{ score.periodo }}</td>
00046|              <td>{{ score.area|default:"—" }}</td>
00047|              <td>{{ score.unidad_negocio|default:"—" }}</td>
00048|              <td class="text-end">{{ score.puntaje_total }}</td>
00049|              <td>
00050|                {% if score.clasifica %}
00051|                  <span class="badge text-bg-success">Sí</span>
00052|                {% else %}
00053|                  <span class="badge text-bg-secondary">No</span>
00054|                {% endif %}
00055|              </td>
00056|            </tr>
00057|            {% empty %}
00058|            <tr><td colspan="5" class="text-muted text-center py-3">Sin puntajes calculados.</td></tr>
00059|            {% endfor %}
00060|          </tbody>
00061|        </table>
00062|      </div>
00063|      <div class="card-footer bg-white small text-muted">
00064|        Color de fila según <code>PgoPeriodScore.clasifica</code> (valor almacenado).
00065|        En el código actual no hay comando que calcule ese booleano ni umbral ≥80.
00066|      </div>
00067|    </div>
00068|  </div>
00069|  <div class="col-lg-6">
00070|    <div class="card border-0 shadow-sm">
00071|      <div class="card-header bg-white fw-semibold">Agregados mensuales</div>
00072|      <div class="table-responsive">
00073|        <table class="table table-sm mb-0">
00074|          <thead><tr><th>Período</th><th>Unidad</th><th>Recibidos</th><th>Cerrados</th><th>Prom. h</th></tr></thead>
00075|          <tbody>
00076|            {% for agg in aggs %}
00077|            <tr>
00078|              <td>{{ agg.periodo }}</td>
00079|              <td>{{ agg.unidad_negocio }}</td>
00080|              <td>{{ agg.tickets_recibidos }}</td>
00081|              <td>{{ agg.tickets_cerrados }}</td>
00082|              <td>{{ agg.tiempo_promedio_horas }}</td>
00083|            </tr>
00084|            {% empty %}
00085|            <tr><td colspan="5" class="text-muted text-center py-3">Sin agregados mensuales.</td></tr>
00086|            {% endfor %}
00087|          </tbody>
00088|        </table>
00089|      </div>
00090|    </div>
00091|  </div>
00092|</div>
00093|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAid2Nnb25lX2Jhc2UuaHRtbCIgJX0KCnslIGJsb2NrIHRpdGxlICV9UmVzdWx0YWRvcyDigJQgUEdPIOKAlCBXQ0cgT25leyUgZW5kYmxvY2sgJX0KCnslIGJsb2NrIGNvbnRlbnQgJX0KPHN0eWxlPgogIC8qCiAgICBNaXNtbyBwYXRyw7NuIHZpc3VhbCBxdWUgUEdDIChkYXNoYm9hcmQuaHRtbCk6CiAgICBTw60gID0gY2lhbi1henVsYWRvOyBObyA9IMOhbWJhci1uYXJhbmphIChkaXN0aW5naWJsZXMgdGFtYmnDqW4gZW4gZGFsdG9uaXNtbyB2ZXJkZS1yb2pvKS4KICAgIEZ1ZW50ZSBkZSB2ZXJkYWQ6IFBnb1BlcmlvZFNjb3JlLmNsYXNpZmljYSAoQm9vbGVhbkZpZWxkKSwgbm8gc2UgcmVjYWxjdWxhIGFxdcOtLgogICovCiAgdGFibGUucGdvLXNjb3JlYm9hcmQgdGJvZHkgdHIucm93LWNsYXNpZmljYS1zaSB0ZCB7IGJhY2tncm91bmQ6ICNkZmY2ZmI7IH0KICB0YWJsZS5wZ28tc2NvcmVib2FyZCB0Ym9keSB0ci5yb3ctY2xhc2lmaWNhLW5vIHRkIHsgYmFja2dyb3VuZDogI2ZkZThjODsgfQogIHRhYmxlLnBnby1zY29yZWJvYXJkIHRib2R5IHRyLnJvdy1jbGFzaWZpY2Etc2kgdGQ6Zmlyc3QtY2hpbGQgeyBib3gtc2hhZG93OiBpbnNldCA1cHggMCAwICMwMjg0Yzc7IH0KICB0YWJsZS5wZ28tc2NvcmVib2FyZCB0Ym9keSB0ci5yb3ctY2xhc2lmaWNhLW5vIHRkOmZpcnN0LWNoaWxkIHsgYm94LXNoYWRvdzogaW5zZXQgNXB4IDAgMCAjYzI0MTBjOyB9CiAgdGFibGUucGdvLXNjb3JlYm9hcmQgdGJvZHkgdHIucm93LWNsYXNpZmljYS1zaTpob3ZlciB0ZCB7IGJhY2tncm91bmQ6ICNjZmVlZjc7IH0KICB0YWJsZS5wZ28tc2NvcmVib2FyZCB0Ym9keSB0ci5yb3ctY2xhc2lmaWNhLW5vOmhvdmVyIHRkIHsgYmFja2dyb3VuZDogI2ZiZDlhODsgfQo8L3N0eWxlPgoKPGRpdiBjbGFzcz0iZC1mbGV4IGp1c3RpZnktY29udGVudC1iZXR3ZWVuIGFsaWduLWl0ZW1zLWNlbnRlciBtYi0zIj4KICA8ZGl2IGNsYXNzPSJ3Y2ctcmVwb3J0LWhlYWQiPgogICAgPGgxIGNsYXNzPSJoNCBmdy1zZW1pYm9sZCBtYi0wIj5SZXN1bHRhZG9zIHBvciBwZXLDrW9kbzwvaDE+CiAgICB7JSBpbmNsdWRlICJpbmNsdWRlcy9tb2R1bGVfbWFyay5odG1sIiB3aXRoIG1vZHVsZT0icGdvIiAlfQogIDwvZGl2PgogIDxhIGhyZWY9InslIHVybCAnd2Nnb25lX3BnbzpkYXNoYm9hcmQnICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1zZWNvbmRhcnkiPkRhc2hib2FyZDwvYT4KPC9kaXY+Cgo8Zm9ybSBtZXRob2Q9ImdldCIgY2xhc3M9Im1iLTMiPgogIDxkaXYgY2xhc3M9ImlucHV0LWdyb3VwIGlucHV0LWdyb3VwLXNtIiBzdHlsZT0ibWF4LXdpZHRoOiAyMDBweDsiPgogICAgPGlucHV0IHR5cGU9InRleHQiIG5hbWU9InBlcmlvZG8iIHZhbHVlPSJ7eyByZXF1ZXN0LkdFVC5wZXJpb2RvIH19IiBjbGFzcz0iZm9ybS1jb250cm9sIiBwbGFjZWhvbGRlcj0iWVlZWS1NTSI+CiAgICA8YnV0dG9uIGNsYXNzPSJidG4gYnRuLXByaW1hcnkiIHR5cGU9InN1Ym1pdCI+RmlsdHJhcjwvYnV0dG9uPgogIDwvZGl2Pgo8L2Zvcm0+Cgo8ZGl2IGNsYXNzPSJyb3cgZy0zIj4KICA8ZGl2IGNsYXNzPSJjb2wtbGctNiI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSI+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtaGVhZGVyIGJnLXdoaXRlIGZ3LXNlbWlib2xkIj5QdW50YWplcyBwb3IgcGVyw61vZG88L2Rpdj4KICAgICAgPGRpdiBjbGFzcz0idGFibGUtcmVzcG9uc2l2ZSI+CiAgICAgICAgPHRhYmxlIGNsYXNzPSJ0YWJsZSB0YWJsZS1zbSBtYi0wIHBnby1zY29yZWJvYXJkIj4KICAgICAgICAgIDx0aGVhZD48dHI+PHRoPlBlcsOtb2RvPC90aD48dGg+w4FyZWE8L3RoPjx0aD5VbmlkYWQ8L3RoPjx0aCBjbGFzcz0idGV4dC1lbmQiPlB1bnRhamU8L3RoPjx0aD5DbGFzaWZpY2E8L3RoPjwvdHI+PC90aGVhZD4KICAgICAgICAgIDx0Ym9keT4KICAgICAgICAgICAgeyUgZm9yIHNjb3JlIGluIHNjb3JlcyAlfQogICAgICAgICAgICA8dHIgY2xhc3M9InslIGlmIHNjb3JlLmNsYXNpZmljYSAlfXJvdy1jbGFzaWZpY2Etc2l7JSBlbHNlICV9cm93LWNsYXNpZmljYS1ub3slIGVuZGlmICV9Ij4KICAgICAgICAgICAgICA8dGQ+e3sgc2NvcmUucGVyaW9kbyB9fTwvdGQ+CiAgICAgICAgICAgICAgPHRkPnt7IHNjb3JlLmFyZWF8ZGVmYXVsdDoi4oCUIiB9fTwvdGQ+CiAgICAgICAgICAgICAgPHRkPnt7IHNjb3JlLnVuaWRhZF9uZWdvY2lvfGRlZmF1bHQ6IuKAlCIgfX08L3RkPgogICAgICAgICAgICAgIDx0ZCBjbGFzcz0idGV4dC1lbmQiPnt7IHNjb3JlLnB1bnRhamVfdG90YWwgfX08L3RkPgogICAgICAgICAgICAgIDx0ZD4KICAgICAgICAgICAgICAgIHslIGlmIHNjb3JlLmNsYXNpZmljYSAlfQogICAgICAgICAgICAgICAgICA8c3BhbiBjbGFzcz0iYmFkZ2UgdGV4dC1iZy1zdWNjZXNzIj5Tw608L3NwYW4+CiAgICAgICAgICAgICAgICB7JSBlbHNlICV9CiAgICAgICAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJiYWRnZSB0ZXh0LWJnLXNlY29uZGFyeSI+Tm88L3NwYW4+CiAgICAgICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgICAgIDwvdGQ+CiAgICAgICAgICAgIDwvdHI+CiAgICAgICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgICAgIDx0cj48dGQgY29sc3Bhbj0iNSIgY2xhc3M9InRleHQtbXV0ZWQgdGV4dC1jZW50ZXIgcHktMyI+U2luIHB1bnRhamVzIGNhbGN1bGFkb3MuPC90ZD48L3RyPgogICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgIDwvdGJvZHk+CiAgICAgICAgPC90YWJsZT4KICAgICAgPC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtZm9vdGVyIGJnLXdoaXRlIHNtYWxsIHRleHQtbXV0ZWQiPgogICAgICAgIENvbG9yIGRlIGZpbGEgc2Vnw7puIDxjb2RlPlBnb1BlcmlvZFNjb3JlLmNsYXNpZmljYTwvY29kZT4gKHZhbG9yIGFsbWFjZW5hZG8pLgogICAgICAgIEVuIGVsIGPDs2RpZ28gYWN0dWFsIG5vIGhheSBjb21hbmRvIHF1ZSBjYWxjdWxlIGVzZSBib29sZWFubyBuaSB1bWJyYWwg4omlODAuCiAgICAgIDwvZGl2PgogICAgPC9kaXY+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLWxnLTYiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20iPgogICAgICA8ZGl2IGNsYXNzPSJjYXJkLWhlYWRlciBiZy13aGl0ZSBmdy1zZW1pYm9sZCI+QWdyZWdhZG9zIG1lbnN1YWxlczwvZGl2PgogICAgICA8ZGl2IGNsYXNzPSJ0YWJsZS1yZXNwb25zaXZlIj4KICAgICAgICA8dGFibGUgY2xhc3M9InRhYmxlIHRhYmxlLXNtIG1iLTAiPgogICAgICAgICAgPHRoZWFkPjx0cj48dGg+UGVyw61vZG88L3RoPjx0aD5VbmlkYWQ8L3RoPjx0aD5SZWNpYmlkb3M8L3RoPjx0aD5DZXJyYWRvczwvdGg+PHRoPlByb20uIGg8L3RoPjwvdHI+PC90aGVhZD4KICAgICAgICAgIDx0Ym9keT4KICAgICAgICAgICAgeyUgZm9yIGFnZyBpbiBhZ2dzICV9CiAgICAgICAgICAgIDx0cj4KICAgICAgICAgICAgICA8dGQ+e3sgYWdnLnBlcmlvZG8gfX08L3RkPgogICAgICAgICAgICAgIDx0ZD57eyBhZ2cudW5pZGFkX25lZ29jaW8gfX08L3RkPgogICAgICAgICAgICAgIDx0ZD57eyBhZ2cudGlja2V0c19yZWNpYmlkb3MgfX08L3RkPgogICAgICAgICAgICAgIDx0ZD57eyBhZ2cudGlja2V0c19jZXJyYWRvcyB9fTwvdGQ+CiAgICAgICAgICAgICAgPHRkPnt7IGFnZy50aWVtcG9fcHJvbWVkaW9faG9yYXMgfX08L3RkPgogICAgICAgICAgICA8L3RyPgogICAgICAgICAgICB7JSBlbXB0eSAlfQogICAgICAgICAgICA8dHI+PHRkIGNvbHNwYW49IjUiIGNsYXNzPSJ0ZXh0LW11dGVkIHRleHQtY2VudGVyIHB5LTMiPlNpbiBhZ3JlZ2Fkb3MgbWVuc3VhbGVzLjwvdGQ+PC90cj4KICAgICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgICA8L3Rib2R5PgogICAgICAgIDwvdGFibGU+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CiAgPC9kaXY+CjwvZGl2Pgp7JSBlbmRibG9jayAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/wcgone/pgo/ticket_detail.html
PATH_JSON="templates/wcgone/pgo/ticket_detail.html"
FILENAME=ticket_detail.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=59
SIZE_BYTES_UTF8=3092
CONTENT_SHA256=5e7a6f78b1ce92e1c4c303a8a1db225f9d554a7b7148358c4d329af8b28a09a3
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

{% block title %}Ticket {{ ticket.ticket_externo_id|default:ticket.pk }} — PGO — WCG One{% endblock %}

{% block content %}
<div class="mb-3">
  <h1 class="h4 fw-semibold mb-1">{{ ticket.titulo }}</h1>
  <p class="text-muted small mb-0">
    ID {{ ticket.ticket_externo_id|default:ticket.pk }}
    {% if ticket.anio_mes %} · Período {{ ticket.anio_mes }}{% endif %}
  </p>
</div>

<div class="row g-3">
  <div class="col-lg-6">
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white fw-semibold">Datos operativos</div>
      <div class="card-body small">
        <dl class="row mb-0">
          <dt class="col-5">Estado (raw)</dt><dd class="col-7">{{ ticket.estado_raw|default:"—" }}</dd>
          <dt class="col-5">Estado normalizado</dt><dd class="col-7">{{ ticket.estado_normalizado|default:"—" }}</dd>
          <dt class="col-5">Prioridad</dt><dd class="col-7">{{ ticket.prioridad|default:"—" }}</dd>
          <dt class="col-5">Departamento</dt><dd class="col-7">{{ ticket.departamento|default:"—" }}</dd>
          <dt class="col-5">Sistema</dt><dd class="col-7">{{ ticket.sistema|default:"—" }}</dd>
          <dt class="col-5">Tipo servicio</dt><dd class="col-7">{{ ticket.tipo_servicio|default:"—" }}</dd>
          <dt class="col-5">Solicitante</dt><dd class="col-7">{{ ticket.usuario_solicita|default:"—" }}</dd>
          <dt class="col-5">Correo</dt><dd class="col-7">{{ ticket.correo_solicita|default:"—" }}</dd>
          <dt class="col-5">Unidad negocio</dt><dd class="col-7">{{ ticket.unidad_negocio|default:"—" }}</dd>
          <dt class="col-5">Responsable</dt><dd class="col-7">{{ ticket.responsable|default:"—" }}</dd>
        </dl>
      </div>
    </div>
  </div>
  <div class="col-lg-6">
    <div class="card border-0 shadow-sm mb-3">
      <div class="card-header bg-white fw-semibold">Tiempos y SLA</div>
      <div class="card-body small">
        <dl class="row mb-0">
          <dt class="col-5">Apertura</dt><dd class="col-7">{{ ticket.fecha_apertura|date:"d/m/Y H:i"|default:"—" }}</dd>
          <dt class="col-5">Cierre</dt><dd class="col-7">{{ ticket.fecha_cierre|date:"d/m/Y H:i"|default:"—" }}</dd>
          <dt class="col-5">Duración (h)</dt><dd class="col-7">{{ ticket.duracion_horas|default:"—" }}</dd>
          <dt class="col-5">SLA (h)</dt><dd class="col-7">{{ ticket.sla_horas|default:"—" }}</dd>
          <dt class="col-5">SLA cumplido</dt>
          <dd class="col-7">
            {% if ticket.sla_cumplido %}<span class="badge text-bg-success">Sí</span>{% else %}<span class="badge text-bg-secondary">No</span>{% endif %}
          </dd>
          <dt class="col-5">Razón cierre</dt><dd class="col-7">{{ ticket.razon_cierre|default:"—" }}</dd>
        </dl>
      </div>
    </div>
    {% if ticket.solucion %}
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white fw-semibold">Solución</div>
      <div class="card-body small">{{ ticket.solucion }}</div>
    </div>
    {% endif %}
  </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "wcgone_base.html" %}
00002|
00003|{% block title %}Ticket {{ ticket.ticket_externo_id|default:ticket.pk }} — PGO — WCG One{% endblock %}
00004|
00005|{% block content %}
00006|<div class="mb-3">
00007|  <h1 class="h4 fw-semibold mb-1">{{ ticket.titulo }}</h1>
00008|  <p class="text-muted small mb-0">
00009|    ID {{ ticket.ticket_externo_id|default:ticket.pk }}
00010|    {% if ticket.anio_mes %} · Período {{ ticket.anio_mes }}{% endif %}
00011|  </p>
00012|</div>
00013|
00014|<div class="row g-3">
00015|  <div class="col-lg-6">
00016|    <div class="card border-0 shadow-sm">
00017|      <div class="card-header bg-white fw-semibold">Datos operativos</div>
00018|      <div class="card-body small">
00019|        <dl class="row mb-0">
00020|          <dt class="col-5">Estado (raw)</dt><dd class="col-7">{{ ticket.estado_raw|default:"—" }}</dd>
00021|          <dt class="col-5">Estado normalizado</dt><dd class="col-7">{{ ticket.estado_normalizado|default:"—" }}</dd>
00022|          <dt class="col-5">Prioridad</dt><dd class="col-7">{{ ticket.prioridad|default:"—" }}</dd>
00023|          <dt class="col-5">Departamento</dt><dd class="col-7">{{ ticket.departamento|default:"—" }}</dd>
00024|          <dt class="col-5">Sistema</dt><dd class="col-7">{{ ticket.sistema|default:"—" }}</dd>
00025|          <dt class="col-5">Tipo servicio</dt><dd class="col-7">{{ ticket.tipo_servicio|default:"—" }}</dd>
00026|          <dt class="col-5">Solicitante</dt><dd class="col-7">{{ ticket.usuario_solicita|default:"—" }}</dd>
00027|          <dt class="col-5">Correo</dt><dd class="col-7">{{ ticket.correo_solicita|default:"—" }}</dd>
00028|          <dt class="col-5">Unidad negocio</dt><dd class="col-7">{{ ticket.unidad_negocio|default:"—" }}</dd>
00029|          <dt class="col-5">Responsable</dt><dd class="col-7">{{ ticket.responsable|default:"—" }}</dd>
00030|        </dl>
00031|      </div>
00032|    </div>
00033|  </div>
00034|  <div class="col-lg-6">
00035|    <div class="card border-0 shadow-sm mb-3">
00036|      <div class="card-header bg-white fw-semibold">Tiempos y SLA</div>
00037|      <div class="card-body small">
00038|        <dl class="row mb-0">
00039|          <dt class="col-5">Apertura</dt><dd class="col-7">{{ ticket.fecha_apertura|date:"d/m/Y H:i"|default:"—" }}</dd>
00040|          <dt class="col-5">Cierre</dt><dd class="col-7">{{ ticket.fecha_cierre|date:"d/m/Y H:i"|default:"—" }}</dd>
00041|          <dt class="col-5">Duración (h)</dt><dd class="col-7">{{ ticket.duracion_horas|default:"—" }}</dd>
00042|          <dt class="col-5">SLA (h)</dt><dd class="col-7">{{ ticket.sla_horas|default:"—" }}</dd>
00043|          <dt class="col-5">SLA cumplido</dt>
00044|          <dd class="col-7">
00045|            {% if ticket.sla_cumplido %}<span class="badge text-bg-success">Sí</span>{% else %}<span class="badge text-bg-secondary">No</span>{% endif %}
00046|          </dd>
00047|          <dt class="col-5">Razón cierre</dt><dd class="col-7">{{ ticket.razon_cierre|default:"—" }}</dd>
00048|        </dl>
00049|      </div>
00050|    </div>
00051|    {% if ticket.solucion %}
00052|    <div class="card border-0 shadow-sm">
00053|      <div class="card-header bg-white fw-semibold">Solución</div>
00054|      <div class="card-body small">{{ ticket.solucion }}</div>
00055|    </div>
00056|    {% endif %}
00057|  </div>
00058|</div>
00059|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAid2Nnb25lX2Jhc2UuaHRtbCIgJX0KCnslIGJsb2NrIHRpdGxlICV9VGlja2V0IHt7IHRpY2tldC50aWNrZXRfZXh0ZXJub19pZHxkZWZhdWx0OnRpY2tldC5wayB9fSDigJQgUEdPIOKAlCBXQ0cgT25leyUgZW5kYmxvY2sgJX0KCnslIGJsb2NrIGNvbnRlbnQgJX0KPGRpdiBjbGFzcz0ibWItMyI+CiAgPGgxIGNsYXNzPSJoNCBmdy1zZW1pYm9sZCBtYi0xIj57eyB0aWNrZXQudGl0dWxvIH19PC9oMT4KICA8cCBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCBtYi0wIj4KICAgIElEIHt7IHRpY2tldC50aWNrZXRfZXh0ZXJub19pZHxkZWZhdWx0OnRpY2tldC5wayB9fQogICAgeyUgaWYgdGlja2V0LmFuaW9fbWVzICV9IMK3IFBlcsOtb2RvIHt7IHRpY2tldC5hbmlvX21lcyB9fXslIGVuZGlmICV9CiAgPC9wPgo8L2Rpdj4KCjxkaXYgY2xhc3M9InJvdyBnLTMiPgogIDxkaXYgY2xhc3M9ImNvbC1sZy02Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIgYmctd2hpdGUgZnctc2VtaWJvbGQiPkRhdG9zIG9wZXJhdGl2b3M8L2Rpdj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1ib2R5IHNtYWxsIj4KICAgICAgICA8ZGwgY2xhc3M9InJvdyBtYi0wIj4KICAgICAgICAgIDxkdCBjbGFzcz0iY29sLTUiPkVzdGFkbyAocmF3KTwvZHQ+PGRkIGNsYXNzPSJjb2wtNyI+e3sgdGlja2V0LmVzdGFkb19yYXd8ZGVmYXVsdDoi4oCUIiB9fTwvZGQ+CiAgICAgICAgICA8ZHQgY2xhc3M9ImNvbC01Ij5Fc3RhZG8gbm9ybWFsaXphZG88L2R0PjxkZCBjbGFzcz0iY29sLTciPnt7IHRpY2tldC5lc3RhZG9fbm9ybWFsaXphZG98ZGVmYXVsdDoi4oCUIiB9fTwvZGQ+CiAgICAgICAgICA8ZHQgY2xhc3M9ImNvbC01Ij5QcmlvcmlkYWQ8L2R0PjxkZCBjbGFzcz0iY29sLTciPnt7IHRpY2tldC5wcmlvcmlkYWR8ZGVmYXVsdDoi4oCUIiB9fTwvZGQ+CiAgICAgICAgICA8ZHQgY2xhc3M9ImNvbC01Ij5EZXBhcnRhbWVudG88L2R0PjxkZCBjbGFzcz0iY29sLTciPnt7IHRpY2tldC5kZXBhcnRhbWVudG98ZGVmYXVsdDoi4oCUIiB9fTwvZGQ+CiAgICAgICAgICA8ZHQgY2xhc3M9ImNvbC01Ij5TaXN0ZW1hPC9kdD48ZGQgY2xhc3M9ImNvbC03Ij57eyB0aWNrZXQuc2lzdGVtYXxkZWZhdWx0OiLigJQiIH19PC9kZD4KICAgICAgICAgIDxkdCBjbGFzcz0iY29sLTUiPlRpcG8gc2VydmljaW88L2R0PjxkZCBjbGFzcz0iY29sLTciPnt7IHRpY2tldC50aXBvX3NlcnZpY2lvfGRlZmF1bHQ6IuKAlCIgfX08L2RkPgogICAgICAgICAgPGR0IGNsYXNzPSJjb2wtNSI+U29saWNpdGFudGU8L2R0PjxkZCBjbGFzcz0iY29sLTciPnt7IHRpY2tldC51c3VhcmlvX3NvbGljaXRhfGRlZmF1bHQ6IuKAlCIgfX08L2RkPgogICAgICAgICAgPGR0IGNsYXNzPSJjb2wtNSI+Q29ycmVvPC9kdD48ZGQgY2xhc3M9ImNvbC03Ij57eyB0aWNrZXQuY29ycmVvX3NvbGljaXRhfGRlZmF1bHQ6IuKAlCIgfX08L2RkPgogICAgICAgICAgPGR0IGNsYXNzPSJjb2wtNSI+VW5pZGFkIG5lZ29jaW88L2R0PjxkZCBjbGFzcz0iY29sLTciPnt7IHRpY2tldC51bmlkYWRfbmVnb2Npb3xkZWZhdWx0OiLigJQiIH19PC9kZD4KICAgICAgICAgIDxkdCBjbGFzcz0iY29sLTUiPlJlc3BvbnNhYmxlPC9kdD48ZGQgY2xhc3M9ImNvbC03Ij57eyB0aWNrZXQucmVzcG9uc2FibGV8ZGVmYXVsdDoi4oCUIiB9fTwvZGQ+CiAgICAgICAgPC9kbD4KICAgICAgPC9kaXY+CiAgICA8L2Rpdj4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbGctNiI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSBtYi0zIj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIgYmctd2hpdGUgZnctc2VtaWJvbGQiPlRpZW1wb3MgeSBTTEE8L2Rpdj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1ib2R5IHNtYWxsIj4KICAgICAgICA8ZGwgY2xhc3M9InJvdyBtYi0wIj4KICAgICAgICAgIDxkdCBjbGFzcz0iY29sLTUiPkFwZXJ0dXJhPC9kdD48ZGQgY2xhc3M9ImNvbC03Ij57eyB0aWNrZXQuZmVjaGFfYXBlcnR1cmF8ZGF0ZToiZC9tL1kgSDppInxkZWZhdWx0OiLigJQiIH19PC9kZD4KICAgICAgICAgIDxkdCBjbGFzcz0iY29sLTUiPkNpZXJyZTwvZHQ+PGRkIGNsYXNzPSJjb2wtNyI+e3sgdGlja2V0LmZlY2hhX2NpZXJyZXxkYXRlOiJkL20vWSBIOmkifGRlZmF1bHQ6IuKAlCIgfX08L2RkPgogICAgICAgICAgPGR0IGNsYXNzPSJjb2wtNSI+RHVyYWNpw7NuIChoKTwvZHQ+PGRkIGNsYXNzPSJjb2wtNyI+e3sgdGlja2V0LmR1cmFjaW9uX2hvcmFzfGRlZmF1bHQ6IuKAlCIgfX08L2RkPgogICAgICAgICAgPGR0IGNsYXNzPSJjb2wtNSI+U0xBIChoKTwvZHQ+PGRkIGNsYXNzPSJjb2wtNyI+e3sgdGlja2V0LnNsYV9ob3Jhc3xkZWZhdWx0OiLigJQiIH19PC9kZD4KICAgICAgICAgIDxkdCBjbGFzcz0iY29sLTUiPlNMQSBjdW1wbGlkbzwvZHQ+CiAgICAgICAgICA8ZGQgY2xhc3M9ImNvbC03Ij4KICAgICAgICAgICAgeyUgaWYgdGlja2V0LnNsYV9jdW1wbGlkbyAlfTxzcGFuIGNsYXNzPSJiYWRnZSB0ZXh0LWJnLXN1Y2Nlc3MiPlPDrTwvc3Bhbj57JSBlbHNlICV9PHNwYW4gY2xhc3M9ImJhZGdlIHRleHQtYmctc2Vjb25kYXJ5Ij5Obzwvc3Bhbj57JSBlbmRpZiAlfQogICAgICAgICAgPC9kZD4KICAgICAgICAgIDxkdCBjbGFzcz0iY29sLTUiPlJhesOzbiBjaWVycmU8L2R0PjxkZCBjbGFzcz0iY29sLTciPnt7IHRpY2tldC5yYXpvbl9jaWVycmV8ZGVmYXVsdDoi4oCUIiB9fTwvZGQ+CiAgICAgICAgPC9kbD4KICAgICAgPC9kaXY+CiAgICA8L2Rpdj4KICAgIHslIGlmIHRpY2tldC5zb2x1Y2lvbiAlfQogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20iPgogICAgICA8ZGl2IGNsYXNzPSJjYXJkLWhlYWRlciBiZy13aGl0ZSBmdy1zZW1pYm9sZCI+U29sdWNpw7NuPC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtYm9keSBzbWFsbCI+e3sgdGlja2V0LnNvbHVjaW9uIH19PC9kaXY+CiAgICA8L2Rpdj4KICAgIHslIGVuZGlmICV9CiAgPC9kaXY+CjwvZGl2Pgp7JSBlbmRibG9jayAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/wcgone/pgo/ticket_list.html
PATH_JSON="templates/wcgone/pgo/ticket_list.html"
FILENAME=ticket_list.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=80
SIZE_BYTES_UTF8=3015
CONTENT_SHA256=d6cedeb39c0bfba392a71cb4236fff73d9a4568379009ebfb777255636938b73
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

{% block title %}Tickets — PGO — WCG One{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-2">
  <div class="wcg-report-head">
    <h1 class="h4 fw-semibold mb-0">PGO — Tickets</h1>
    {% include "includes/module_mark.html" with module="pgo" %}
  </div>
  <div class="d-flex gap-1 flex-wrap">
    <a href="{% url 'wcgone_pgo:export_tickets' %}{% if export_query %}?{{ export_query }}{% endif %}" class="btn btn-sm btn-outline-primary">Exportar CSV</a>
    <a href="{% url 'wcgone_pgo:dashboard' %}" class="btn btn-sm btn-outline-secondary">Dashboard</a>
  </div>
</div>

<form method="get" class="row g-2 mb-3">
  <div class="col-md-3">
    <input type="text" name="estado" value="{{ request.GET.estado }}" class="form-control form-control-sm" placeholder="Estado">
  </div>
  <div class="col-md-2">
    <input type="text" name="periodo" value="{{ request.GET.periodo }}" class="form-control form-control-sm" placeholder="YYYY-MM">
  </div>
  <div class="col-md-2">
    <input type="text" name="prioridad" value="{{ request.GET.prioridad }}" class="form-control form-control-sm" placeholder="Prioridad">
  </div>
  <div class="col-md-2">
    <button type="submit" class="btn btn-primary btn-sm w-100">Filtrar</button>
  </div>
</form>

{% if not tickets and not request.GET %}
{% include "includes/empty_state.html" with title="Sin tickets" message="Cargue tickets desde Administración → Importación General." %}
{% endif %}

<div class="card border-0 shadow-sm">
  <div class="table-responsive">
    <table class="table table-hover table-wcg mb-0">
      <thead>
        <tr>
          <th>ID</th>
          <th>Título</th>
          <th>Estado</th>
          <th>Prioridad</th>
          <th>Sistema</th>
          <th>Período</th>
          <th>SLA</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {% for ticket in tickets %}
        <tr>
          <td>{{ ticket.ticket_externo_id|default:ticket.pk }}</td>
          <td>{{ ticket.titulo|truncatechars:60 }}</td>
          <td>{{ ticket.estado_normalizado|default:ticket.estado_raw|default:"—" }}</td>
          <td>{{ ticket.prioridad|default:"—" }}</td>
          <td>{{ ticket.sistema|default:"—" }}</td>
          <td>{{ ticket.anio_mes|default:"—" }}</td>
          <td>
            {% if ticket.sla_cumplido %}
            <span class="badge text-bg-success">Sí</span>
            {% else %}
            <span class="badge text-bg-secondary">No</span>
            {% endif %}
          </td>
          <td class="text-end">
            <a href="{% url 'wcgone_pgo:ticket_detail' ticket.pk %}" class="btn btn-sm btn-outline-primary">Ver</a>
          </td>
        </tr>
        {% empty %}
        <tr><td colspan="8" class="text-center text-muted py-4">
          No hay resultados con los filtros actuales.
        </td></tr>
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
00003|{% block title %}Tickets — PGO — WCG One{% endblock %}
00004|
00005|{% block content %}
00006|<div class="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-2">
00007|  <div class="wcg-report-head">
00008|    <h1 class="h4 fw-semibold mb-0">PGO — Tickets</h1>
00009|    {% include "includes/module_mark.html" with module="pgo" %}
00010|  </div>
00011|  <div class="d-flex gap-1 flex-wrap">
00012|    <a href="{% url 'wcgone_pgo:export_tickets' %}{% if export_query %}?{{ export_query }}{% endif %}" class="btn btn-sm btn-outline-primary">Exportar CSV</a>
00013|    <a href="{% url 'wcgone_pgo:dashboard' %}" class="btn btn-sm btn-outline-secondary">Dashboard</a>
00014|  </div>
00015|</div>
00016|
00017|<form method="get" class="row g-2 mb-3">
00018|  <div class="col-md-3">
00019|    <input type="text" name="estado" value="{{ request.GET.estado }}" class="form-control form-control-sm" placeholder="Estado">
00020|  </div>
00021|  <div class="col-md-2">
00022|    <input type="text" name="periodo" value="{{ request.GET.periodo }}" class="form-control form-control-sm" placeholder="YYYY-MM">
00023|  </div>
00024|  <div class="col-md-2">
00025|    <input type="text" name="prioridad" value="{{ request.GET.prioridad }}" class="form-control form-control-sm" placeholder="Prioridad">
00026|  </div>
00027|  <div class="col-md-2">
00028|    <button type="submit" class="btn btn-primary btn-sm w-100">Filtrar</button>
00029|  </div>
00030|</form>
00031|
00032|{% if not tickets and not request.GET %}
00033|{% include "includes/empty_state.html" with title="Sin tickets" message="Cargue tickets desde Administración → Importación General." %}
00034|{% endif %}
00035|
00036|<div class="card border-0 shadow-sm">
00037|  <div class="table-responsive">
00038|    <table class="table table-hover table-wcg mb-0">
00039|      <thead>
00040|        <tr>
00041|          <th>ID</th>
00042|          <th>Título</th>
00043|          <th>Estado</th>
00044|          <th>Prioridad</th>
00045|          <th>Sistema</th>
00046|          <th>Período</th>
00047|          <th>SLA</th>
00048|          <th></th>
00049|        </tr>
00050|      </thead>
00051|      <tbody>
00052|        {% for ticket in tickets %}
00053|        <tr>
00054|          <td>{{ ticket.ticket_externo_id|default:ticket.pk }}</td>
00055|          <td>{{ ticket.titulo|truncatechars:60 }}</td>
00056|          <td>{{ ticket.estado_normalizado|default:ticket.estado_raw|default:"—" }}</td>
00057|          <td>{{ ticket.prioridad|default:"—" }}</td>
00058|          <td>{{ ticket.sistema|default:"—" }}</td>
00059|          <td>{{ ticket.anio_mes|default:"—" }}</td>
00060|          <td>
00061|            {% if ticket.sla_cumplido %}
00062|            <span class="badge text-bg-success">Sí</span>
00063|            {% else %}
00064|            <span class="badge text-bg-secondary">No</span>
00065|            {% endif %}
00066|          </td>
00067|          <td class="text-end">
00068|            <a href="{% url 'wcgone_pgo:ticket_detail' ticket.pk %}" class="btn btn-sm btn-outline-primary">Ver</a>
00069|          </td>
00070|        </tr>
00071|        {% empty %}
00072|        <tr><td colspan="8" class="text-center text-muted py-4">
00073|          No hay resultados con los filtros actuales.
00074|        </td></tr>
00075|        {% endfor %}
00076|      </tbody>
00077|    </table>
00078|  </div>
00079|</div>
00080|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAid2Nnb25lX2Jhc2UuaHRtbCIgJX0KCnslIGJsb2NrIHRpdGxlICV9VGlja2V0cyDigJQgUEdPIOKAlCBXQ0cgT25leyUgZW5kYmxvY2sgJX0KCnslIGJsb2NrIGNvbnRlbnQgJX0KPGRpdiBjbGFzcz0iZC1mbGV4IGp1c3RpZnktY29udGVudC1iZXR3ZWVuIGFsaWduLWl0ZW1zLXN0YXJ0IG1iLTMgZmxleC13cmFwIGdhcC0yIj4KICA8ZGl2IGNsYXNzPSJ3Y2ctcmVwb3J0LWhlYWQiPgogICAgPGgxIGNsYXNzPSJoNCBmdy1zZW1pYm9sZCBtYi0wIj5QR08g4oCUIFRpY2tldHM8L2gxPgogICAgeyUgaW5jbHVkZSAiaW5jbHVkZXMvbW9kdWxlX21hcmsuaHRtbCIgd2l0aCBtb2R1bGU9InBnbyIgJX0KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJkLWZsZXggZ2FwLTEgZmxleC13cmFwIj4KICAgIDxhIGhyZWY9InslIHVybCAnd2Nnb25lX3BnbzpleHBvcnRfdGlja2V0cycgJX17JSBpZiBleHBvcnRfcXVlcnkgJX0/e3sgZXhwb3J0X3F1ZXJ5IH19eyUgZW5kaWYgJX0iIGNsYXNzPSJidG4gYnRuLXNtIGJ0bi1vdXRsaW5lLXByaW1hcnkiPkV4cG9ydGFyIENTVjwvYT4KICAgIDxhIGhyZWY9InslIHVybCAnd2Nnb25lX3BnbzpkYXNoYm9hcmQnICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1zZWNvbmRhcnkiPkRhc2hib2FyZDwvYT4KICA8L2Rpdj4KPC9kaXY+Cgo8Zm9ybSBtZXRob2Q9ImdldCIgY2xhc3M9InJvdyBnLTIgbWItMyI+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTMiPgogICAgPGlucHV0IHR5cGU9InRleHQiIG5hbWU9ImVzdGFkbyIgdmFsdWU9Int7IHJlcXVlc3QuR0VULmVzdGFkbyB9fSIgY2xhc3M9ImZvcm0tY29udHJvbCBmb3JtLWNvbnRyb2wtc20iIHBsYWNlaG9sZGVyPSJFc3RhZG8iPgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1tZC0yIj4KICAgIDxpbnB1dCB0eXBlPSJ0ZXh0IiBuYW1lPSJwZXJpb2RvIiB2YWx1ZT0ie3sgcmVxdWVzdC5HRVQucGVyaW9kbyB9fSIgY2xhc3M9ImZvcm0tY29udHJvbCBmb3JtLWNvbnRyb2wtc20iIHBsYWNlaG9sZGVyPSJZWVlZLU1NIj4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtMiI+CiAgICA8aW5wdXQgdHlwZT0idGV4dCIgbmFtZT0icHJpb3JpZGFkIiB2YWx1ZT0ie3sgcmVxdWVzdC5HRVQucHJpb3JpZGFkIH19IiBjbGFzcz0iZm9ybS1jb250cm9sIGZvcm0tY29udHJvbC1zbSIgcGxhY2Vob2xkZXI9IlByaW9yaWRhZCI+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTIiPgogICAgPGJ1dHRvbiB0eXBlPSJzdWJtaXQiIGNsYXNzPSJidG4gYnRuLXByaW1hcnkgYnRuLXNtIHctMTAwIj5GaWx0cmFyPC9idXR0b24+CiAgPC9kaXY+CjwvZm9ybT4KCnslIGlmIG5vdCB0aWNrZXRzIGFuZCBub3QgcmVxdWVzdC5HRVQgJX0KeyUgaW5jbHVkZSAiaW5jbHVkZXMvZW1wdHlfc3RhdGUuaHRtbCIgd2l0aCB0aXRsZT0iU2luIHRpY2tldHMiIG1lc3NhZ2U9IkNhcmd1ZSB0aWNrZXRzIGRlc2RlIEFkbWluaXN0cmFjacOzbiDihpIgSW1wb3J0YWNpw7NuIEdlbmVyYWwuIiAlfQp7JSBlbmRpZiAlfQoKPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20iPgogIDxkaXYgY2xhc3M9InRhYmxlLXJlc3BvbnNpdmUiPgogICAgPHRhYmxlIGNsYXNzPSJ0YWJsZSB0YWJsZS1ob3ZlciB0YWJsZS13Y2cgbWItMCI+CiAgICAgIDx0aGVhZD4KICAgICAgICA8dHI+CiAgICAgICAgICA8dGg+SUQ8L3RoPgogICAgICAgICAgPHRoPlTDrXR1bG88L3RoPgogICAgICAgICAgPHRoPkVzdGFkbzwvdGg+CiAgICAgICAgICA8dGg+UHJpb3JpZGFkPC90aD4KICAgICAgICAgIDx0aD5TaXN0ZW1hPC90aD4KICAgICAgICAgIDx0aD5QZXLDrW9kbzwvdGg+CiAgICAgICAgICA8dGg+U0xBPC90aD4KICAgICAgICAgIDx0aD48L3RoPgogICAgICAgIDwvdHI+CiAgICAgIDwvdGhlYWQ+CiAgICAgIDx0Ym9keT4KICAgICAgICB7JSBmb3IgdGlja2V0IGluIHRpY2tldHMgJX0KICAgICAgICA8dHI+CiAgICAgICAgICA8dGQ+e3sgdGlja2V0LnRpY2tldF9leHRlcm5vX2lkfGRlZmF1bHQ6dGlja2V0LnBrIH19PC90ZD4KICAgICAgICAgIDx0ZD57eyB0aWNrZXQudGl0dWxvfHRydW5jYXRlY2hhcnM6NjAgfX08L3RkPgogICAgICAgICAgPHRkPnt7IHRpY2tldC5lc3RhZG9fbm9ybWFsaXphZG98ZGVmYXVsdDp0aWNrZXQuZXN0YWRvX3Jhd3xkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgIDx0ZD57eyB0aWNrZXQucHJpb3JpZGFkfGRlZmF1bHQ6IuKAlCIgfX08L3RkPgogICAgICAgICAgPHRkPnt7IHRpY2tldC5zaXN0ZW1hfGRlZmF1bHQ6IuKAlCIgfX08L3RkPgogICAgICAgICAgPHRkPnt7IHRpY2tldC5hbmlvX21lc3xkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgIDx0ZD4KICAgICAgICAgICAgeyUgaWYgdGlja2V0LnNsYV9jdW1wbGlkbyAlfQogICAgICAgICAgICA8c3BhbiBjbGFzcz0iYmFkZ2UgdGV4dC1iZy1zdWNjZXNzIj5Tw608L3NwYW4+CiAgICAgICAgICAgIHslIGVsc2UgJX0KICAgICAgICAgICAgPHNwYW4gY2xhc3M9ImJhZGdlIHRleHQtYmctc2Vjb25kYXJ5Ij5Obzwvc3Bhbj4KICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgIDwvdGQ+CiAgICAgICAgICA8dGQgY2xhc3M9InRleHQtZW5kIj4KICAgICAgICAgICAgPGEgaHJlZj0ieyUgdXJsICd3Y2dvbmVfcGdvOnRpY2tldF9kZXRhaWwnIHRpY2tldC5wayAlfSIgY2xhc3M9ImJ0biBidG4tc20gYnRuLW91dGxpbmUtcHJpbWFyeSI+VmVyPC9hPgogICAgICAgICAgPC90ZD4KICAgICAgICA8L3RyPgogICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgPHRyPjx0ZCBjb2xzcGFuPSI4IiBjbGFzcz0idGV4dC1jZW50ZXIgdGV4dC1tdXRlZCBweS00Ij4KICAgICAgICAgIE5vIGhheSByZXN1bHRhZG9zIGNvbiBsb3MgZmlsdHJvcyBhY3R1YWxlcy4KICAgICAgICA8L3RkPjwvdHI+CiAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgIDwvdGJvZHk+CiAgICA8L3RhYmxlPgogIDwvZGl2Pgo8L2Rpdj4KeyUgZW5kYmxvY2sgJX0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/wcgone/risk/cliente_detail.html
PATH_JSON="templates/wcgone/risk/cliente_detail.html"
FILENAME=cliente_detail.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=66
SIZE_BYTES_UTF8=2625
CONTENT_SHA256=054ed126aa51d7f7ada7d1cbfef8afd59fa3a257e10493c69894a515689d5b94
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

{% block title %}{{ cliente.nombre }} — Balón de Riesgo — WCG One{% endblock %}

{% block content %}
<div class="mb-3">
  <h1 class="h4 fw-semibold mb-1">{{ cliente.nombre }}</h1>
  <p class="text-muted small mb-0">NIT {{ cliente.nit|default:"—" }} · {{ cliente.get_tipo_entidad_display }}</p>
</div>

<div class="row g-3">
  <div class="col-lg-7">
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white fw-semibold">Operaciones</div>
      <div class="table-responsive">
        <table class="table table-sm mb-0">
          <thead><tr><th>Código</th><th>Producto</th><th>Unidad</th><th>Estado</th><th></th></tr></thead>
          <tbody>
            {% for op in operaciones %}
            <tr>
              <td>{{ op.codigo_operacion }}</td>
              <td>{{ op.producto|default:"—" }}</td>
              <td>{{ op.unidad_negocio|default:"—" }}</td>
              <td>{{ op.estado|default:"—" }}</td>
              <td class="text-end">
                <a href="{% url 'wcgone_risk:operacion_detail' op.pk %}" class="btn btn-sm btn-outline-primary">Historial</a>
              </td>
            </tr>
            {% empty %}
            <tr><td colspan="5" class="text-muted text-center py-3">Sin operaciones.</td></tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>
  <div class="col-lg-5">
    <div class="card border-0 shadow-sm mb-3">
      <div class="card-header bg-white fw-semibold">Alertas activas</div>
      <ul class="list-group list-group-flush small">
        {% for alerta in alertas %}
        <li class="list-group-item">
          <span class="badge text-bg-{{ alerta.severidad|default:'secondary' }}">{{ alerta.tipo_alerta }}</span>
          {{ alerta.mensaje|truncatechars:80 }}
        </li>
        {% empty %}
        <li class="list-group-item text-muted">Sin alertas activas.</li>
        {% endfor %}
      </ul>
    </div>
    <div class="card border-0 shadow-sm">
      <div class="card-header bg-white fw-semibold">Snapshots recientes</div>
      <ul class="list-group list-group-flush small">
        {% for snap in snapshots_recientes %}
        <li class="list-group-item d-flex justify-content-between">
          <span>{{ snap.operacion.codigo_operacion }} · {{ snap.fecha_snapshot|date:"d/m/Y" }}</span>
          <span class="text-muted">{{ snap.due_days|default:0 }} días</span>
        </li>
        {% empty %}
        <li class="list-group-item text-muted">Sin snapshots.</li>
        {% endfor %}
      </ul>
    </div>
  </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "wcgone_base.html" %}
00002|
00003|{% block title %}{{ cliente.nombre }} — Balón de Riesgo — WCG One{% endblock %}
00004|
00005|{% block content %}
00006|<div class="mb-3">
00007|  <h1 class="h4 fw-semibold mb-1">{{ cliente.nombre }}</h1>
00008|  <p class="text-muted small mb-0">NIT {{ cliente.nit|default:"—" }} · {{ cliente.get_tipo_entidad_display }}</p>
00009|</div>
00010|
00011|<div class="row g-3">
00012|  <div class="col-lg-7">
00013|    <div class="card border-0 shadow-sm">
00014|      <div class="card-header bg-white fw-semibold">Operaciones</div>
00015|      <div class="table-responsive">
00016|        <table class="table table-sm mb-0">
00017|          <thead><tr><th>Código</th><th>Producto</th><th>Unidad</th><th>Estado</th><th></th></tr></thead>
00018|          <tbody>
00019|            {% for op in operaciones %}
00020|            <tr>
00021|              <td>{{ op.codigo_operacion }}</td>
00022|              <td>{{ op.producto|default:"—" }}</td>
00023|              <td>{{ op.unidad_negocio|default:"—" }}</td>
00024|              <td>{{ op.estado|default:"—" }}</td>
00025|              <td class="text-end">
00026|                <a href="{% url 'wcgone_risk:operacion_detail' op.pk %}" class="btn btn-sm btn-outline-primary">Historial</a>
00027|              </td>
00028|            </tr>
00029|            {% empty %}
00030|            <tr><td colspan="5" class="text-muted text-center py-3">Sin operaciones.</td></tr>
00031|            {% endfor %}
00032|          </tbody>
00033|        </table>
00034|      </div>
00035|    </div>
00036|  </div>
00037|  <div class="col-lg-5">
00038|    <div class="card border-0 shadow-sm mb-3">
00039|      <div class="card-header bg-white fw-semibold">Alertas activas</div>
00040|      <ul class="list-group list-group-flush small">
00041|        {% for alerta in alertas %}
00042|        <li class="list-group-item">
00043|          <span class="badge text-bg-{{ alerta.severidad|default:'secondary' }}">{{ alerta.tipo_alerta }}</span>
00044|          {{ alerta.mensaje|truncatechars:80 }}
00045|        </li>
00046|        {% empty %}
00047|        <li class="list-group-item text-muted">Sin alertas activas.</li>
00048|        {% endfor %}
00049|      </ul>
00050|    </div>
00051|    <div class="card border-0 shadow-sm">
00052|      <div class="card-header bg-white fw-semibold">Snapshots recientes</div>
00053|      <ul class="list-group list-group-flush small">
00054|        {% for snap in snapshots_recientes %}
00055|        <li class="list-group-item d-flex justify-content-between">
00056|          <span>{{ snap.operacion.codigo_operacion }} · {{ snap.fecha_snapshot|date:"d/m/Y" }}</span>
00057|          <span class="text-muted">{{ snap.due_days|default:0 }} días</span>
00058|        </li>
00059|        {% empty %}
00060|        <li class="list-group-item text-muted">Sin snapshots.</li>
00061|        {% endfor %}
00062|      </ul>
00063|    </div>
00064|  </div>
00065|</div>
00066|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAid2Nnb25lX2Jhc2UuaHRtbCIgJX0KCnslIGJsb2NrIHRpdGxlICV9e3sgY2xpZW50ZS5ub21icmUgfX0g4oCUIEJhbMOzbiBkZSBSaWVzZ28g4oCUIFdDRyBPbmV7JSBlbmRibG9jayAlfQoKeyUgYmxvY2sgY29udGVudCAlfQo8ZGl2IGNsYXNzPSJtYi0zIj4KICA8aDEgY2xhc3M9Img0IGZ3LXNlbWlib2xkIG1iLTEiPnt7IGNsaWVudGUubm9tYnJlIH19PC9oMT4KICA8cCBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCBtYi0wIj5OSVQge3sgY2xpZW50ZS5uaXR8ZGVmYXVsdDoi4oCUIiB9fSDCtyB7eyBjbGllbnRlLmdldF90aXBvX2VudGlkYWRfZGlzcGxheSB9fTwvcD4KPC9kaXY+Cgo8ZGl2IGNsYXNzPSJyb3cgZy0zIj4KICA8ZGl2IGNsYXNzPSJjb2wtbGctNyI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSI+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtaGVhZGVyIGJnLXdoaXRlIGZ3LXNlbWlib2xkIj5PcGVyYWNpb25lczwvZGl2PgogICAgICA8ZGl2IGNsYXNzPSJ0YWJsZS1yZXNwb25zaXZlIj4KICAgICAgICA8dGFibGUgY2xhc3M9InRhYmxlIHRhYmxlLXNtIG1iLTAiPgogICAgICAgICAgPHRoZWFkPjx0cj48dGg+Q8OzZGlnbzwvdGg+PHRoPlByb2R1Y3RvPC90aD48dGg+VW5pZGFkPC90aD48dGg+RXN0YWRvPC90aD48dGg+PC90aD48L3RyPjwvdGhlYWQ+CiAgICAgICAgICA8dGJvZHk+CiAgICAgICAgICAgIHslIGZvciBvcCBpbiBvcGVyYWNpb25lcyAlfQogICAgICAgICAgICA8dHI+CiAgICAgICAgICAgICAgPHRkPnt7IG9wLmNvZGlnb19vcGVyYWNpb24gfX08L3RkPgogICAgICAgICAgICAgIDx0ZD57eyBvcC5wcm9kdWN0b3xkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgICAgICA8dGQ+e3sgb3AudW5pZGFkX25lZ29jaW98ZGVmYXVsdDoi4oCUIiB9fTwvdGQ+CiAgICAgICAgICAgICAgPHRkPnt7IG9wLmVzdGFkb3xkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgICAgICA8dGQgY2xhc3M9InRleHQtZW5kIj4KICAgICAgICAgICAgICAgIDxhIGhyZWY9InslIHVybCAnd2Nnb25lX3Jpc2s6b3BlcmFjaW9uX2RldGFpbCcgb3AucGsgJX0iIGNsYXNzPSJidG4gYnRuLXNtIGJ0bi1vdXRsaW5lLXByaW1hcnkiPkhpc3RvcmlhbDwvYT4KICAgICAgICAgICAgICA8L3RkPgogICAgICAgICAgICA8L3RyPgogICAgICAgICAgICB7JSBlbXB0eSAlfQogICAgICAgICAgICA8dHI+PHRkIGNvbHNwYW49IjUiIGNsYXNzPSJ0ZXh0LW11dGVkIHRleHQtY2VudGVyIHB5LTMiPlNpbiBvcGVyYWNpb25lcy48L3RkPjwvdHI+CiAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgPC90Ym9keT4KICAgICAgICA8L3RhYmxlPgogICAgICA8L2Rpdj4KICAgIDwvZGl2PgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1sZy01Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIG1iLTMiPgogICAgICA8ZGl2IGNsYXNzPSJjYXJkLWhlYWRlciBiZy13aGl0ZSBmdy1zZW1pYm9sZCI+QWxlcnRhcyBhY3RpdmFzPC9kaXY+CiAgICAgIDx1bCBjbGFzcz0ibGlzdC1ncm91cCBsaXN0LWdyb3VwLWZsdXNoIHNtYWxsIj4KICAgICAgICB7JSBmb3IgYWxlcnRhIGluIGFsZXJ0YXMgJX0KICAgICAgICA8bGkgY2xhc3M9Imxpc3QtZ3JvdXAtaXRlbSI+CiAgICAgICAgICA8c3BhbiBjbGFzcz0iYmFkZ2UgdGV4dC1iZy17eyBhbGVydGEuc2V2ZXJpZGFkfGRlZmF1bHQ6J3NlY29uZGFyeScgfX0iPnt7IGFsZXJ0YS50aXBvX2FsZXJ0YSB9fTwvc3Bhbj4KICAgICAgICAgIHt7IGFsZXJ0YS5tZW5zYWplfHRydW5jYXRlY2hhcnM6ODAgfX0KICAgICAgICA8L2xpPgogICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgPGxpIGNsYXNzPSJsaXN0LWdyb3VwLWl0ZW0gdGV4dC1tdXRlZCI+U2luIGFsZXJ0YXMgYWN0aXZhcy48L2xpPgogICAgICAgIHslIGVuZGZvciAlfQogICAgICA8L3VsPgogICAgPC9kaXY+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSI+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtaGVhZGVyIGJnLXdoaXRlIGZ3LXNlbWlib2xkIj5TbmFwc2hvdHMgcmVjaWVudGVzPC9kaXY+CiAgICAgIDx1bCBjbGFzcz0ibGlzdC1ncm91cCBsaXN0LWdyb3VwLWZsdXNoIHNtYWxsIj4KICAgICAgICB7JSBmb3Igc25hcCBpbiBzbmFwc2hvdHNfcmVjaWVudGVzICV9CiAgICAgICAgPGxpIGNsYXNzPSJsaXN0LWdyb3VwLWl0ZW0gZC1mbGV4IGp1c3RpZnktY29udGVudC1iZXR3ZWVuIj4KICAgICAgICAgIDxzcGFuPnt7IHNuYXAub3BlcmFjaW9uLmNvZGlnb19vcGVyYWNpb24gfX0gwrcge3sgc25hcC5mZWNoYV9zbmFwc2hvdHxkYXRlOiJkL20vWSIgfX08L3NwYW4+CiAgICAgICAgICA8c3BhbiBjbGFzcz0idGV4dC1tdXRlZCI+e3sgc25hcC5kdWVfZGF5c3xkZWZhdWx0OjAgfX0gZMOtYXM8L3NwYW4+CiAgICAgICAgPC9saT4KICAgICAgICB7JSBlbXB0eSAlfQogICAgICAgIDxsaSBjbGFzcz0ibGlzdC1ncm91cC1pdGVtIHRleHQtbXV0ZWQiPlNpbiBzbmFwc2hvdHMuPC9saT4KICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgPC91bD4KICAgIDwvZGl2PgogIDwvZGl2Pgo8L2Rpdj4KeyUgZW5kYmxvY2sgJX0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/wcgone/risk/cliente_list.html
PATH_JSON="templates/wcgone/risk/cliente_list.html"
FILENAME=cliente_list.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=53
SIZE_BYTES_UTF8=1813
CONTENT_SHA256=ccaf1412ead5632285f35decd5e525d7d004ab986f512cd7237645062bcde754
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

{% block title %}Clientes — Balón de Riesgo — WCG One{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
  <div class="wcg-report-head">
    <h1 class="h4 fw-semibold mb-0">Clientes en riesgo</h1>
    {% include "includes/module_mark.html" with module="risk" %}
  </div>
  <a href="{% url 'wcgone_risk:comando_balon' %}" class="btn btn-sm btn-outline-secondary">Comando Balón</a>
</div>

<form method="get" class="mb-3">
  <div class="input-group input-group-sm" style="max-width: 320px;">
    <input type="search" name="q" value="{{ request.GET.q }}" class="form-control" placeholder="Buscar nombre o NIT">
    <button class="btn btn-primary" type="submit">Buscar</button>
  </div>
</form>

<div class="card border-0 shadow-sm">
  <div class="table-responsive">
    <table class="table table-hover table-wcg mb-0">
      <thead>
        <tr>
          <th>Cliente</th>
          <th>NIT</th>
          <th>Operaciones</th>
          <th>Último snapshot</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {% for cliente in clientes %}
        <tr>
          <td>{{ cliente.nombre }}</td>
          <td>{{ cliente.nit|default:"—" }}</td>
          <td>{{ cliente.num_operaciones }}</td>
          <td>{{ cliente.ultimo_snapshot|date:"d/m/Y"|default:"—" }}</td>
          <td class="text-end">
            <a href="{% url 'wcgone_risk:cliente_detail' cliente.pk %}" class="btn btn-sm btn-outline-primary">Ver</a>
          </td>
        </tr>
        {% empty %}
        <tr>
          <td colspan="5" class="text-center text-muted py-4">No hay clientes con operaciones de riesgo registradas.</td>
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
00003|{% block title %}Clientes — Balón de Riesgo — WCG One{% endblock %}
00004|
00005|{% block content %}
00006|<div class="d-flex justify-content-between align-items-center mb-3">
00007|  <div class="wcg-report-head">
00008|    <h1 class="h4 fw-semibold mb-0">Clientes en riesgo</h1>
00009|    {% include "includes/module_mark.html" with module="risk" %}
00010|  </div>
00011|  <a href="{% url 'wcgone_risk:comando_balon' %}" class="btn btn-sm btn-outline-secondary">Comando Balón</a>
00012|</div>
00013|
00014|<form method="get" class="mb-3">
00015|  <div class="input-group input-group-sm" style="max-width: 320px;">
00016|    <input type="search" name="q" value="{{ request.GET.q }}" class="form-control" placeholder="Buscar nombre o NIT">
00017|    <button class="btn btn-primary" type="submit">Buscar</button>
00018|  </div>
00019|</form>
00020|
00021|<div class="card border-0 shadow-sm">
00022|  <div class="table-responsive">
00023|    <table class="table table-hover table-wcg mb-0">
00024|      <thead>
00025|        <tr>
00026|          <th>Cliente</th>
00027|          <th>NIT</th>
00028|          <th>Operaciones</th>
00029|          <th>Último snapshot</th>
00030|          <th></th>
00031|        </tr>
00032|      </thead>
00033|      <tbody>
00034|        {% for cliente in clientes %}
00035|        <tr>
00036|          <td>{{ cliente.nombre }}</td>
00037|          <td>{{ cliente.nit|default:"—" }}</td>
00038|          <td>{{ cliente.num_operaciones }}</td>
00039|          <td>{{ cliente.ultimo_snapshot|date:"d/m/Y"|default:"—" }}</td>
00040|          <td class="text-end">
00041|            <a href="{% url 'wcgone_risk:cliente_detail' cliente.pk %}" class="btn btn-sm btn-outline-primary">Ver</a>
00042|          </td>
00043|        </tr>
00044|        {% empty %}
00045|        <tr>
00046|          <td colspan="5" class="text-center text-muted py-4">No hay clientes con operaciones de riesgo registradas.</td>
00047|        </tr>
00048|        {% endfor %}
00049|      </tbody>
00050|    </table>
00051|  </div>
00052|</div>
00053|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAid2Nnb25lX2Jhc2UuaHRtbCIgJX0KCnslIGJsb2NrIHRpdGxlICV9Q2xpZW50ZXMg4oCUIEJhbMOzbiBkZSBSaWVzZ28g4oCUIFdDRyBPbmV7JSBlbmRibG9jayAlfQoKeyUgYmxvY2sgY29udGVudCAlfQo8ZGl2IGNsYXNzPSJkLWZsZXgganVzdGlmeS1jb250ZW50LWJldHdlZW4gYWxpZ24taXRlbXMtY2VudGVyIG1iLTMiPgogIDxkaXYgY2xhc3M9IndjZy1yZXBvcnQtaGVhZCI+CiAgICA8aDEgY2xhc3M9Img0IGZ3LXNlbWlib2xkIG1iLTAiPkNsaWVudGVzIGVuIHJpZXNnbzwvaDE+CiAgICB7JSBpbmNsdWRlICJpbmNsdWRlcy9tb2R1bGVfbWFyay5odG1sIiB3aXRoIG1vZHVsZT0icmlzayIgJX0KICA8L2Rpdj4KICA8YSBocmVmPSJ7JSB1cmwgJ3djZ29uZV9yaXNrOmNvbWFuZG9fYmFsb24nICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1zZWNvbmRhcnkiPkNvbWFuZG8gQmFsw7NuPC9hPgo8L2Rpdj4KCjxmb3JtIG1ldGhvZD0iZ2V0IiBjbGFzcz0ibWItMyI+CiAgPGRpdiBjbGFzcz0iaW5wdXQtZ3JvdXAgaW5wdXQtZ3JvdXAtc20iIHN0eWxlPSJtYXgtd2lkdGg6IDMyMHB4OyI+CiAgICA8aW5wdXQgdHlwZT0ic2VhcmNoIiBuYW1lPSJxIiB2YWx1ZT0ie3sgcmVxdWVzdC5HRVQucSB9fSIgY2xhc3M9ImZvcm0tY29udHJvbCIgcGxhY2Vob2xkZXI9IkJ1c2NhciBub21icmUgbyBOSVQiPgogICAgPGJ1dHRvbiBjbGFzcz0iYnRuIGJ0bi1wcmltYXJ5IiB0eXBlPSJzdWJtaXQiPkJ1c2NhcjwvYnV0dG9uPgogIDwvZGl2Pgo8L2Zvcm0+Cgo8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSI+CiAgPGRpdiBjbGFzcz0idGFibGUtcmVzcG9uc2l2ZSI+CiAgICA8dGFibGUgY2xhc3M9InRhYmxlIHRhYmxlLWhvdmVyIHRhYmxlLXdjZyBtYi0wIj4KICAgICAgPHRoZWFkPgogICAgICAgIDx0cj4KICAgICAgICAgIDx0aD5DbGllbnRlPC90aD4KICAgICAgICAgIDx0aD5OSVQ8L3RoPgogICAgICAgICAgPHRoPk9wZXJhY2lvbmVzPC90aD4KICAgICAgICAgIDx0aD7Dmmx0aW1vIHNuYXBzaG90PC90aD4KICAgICAgICAgIDx0aD48L3RoPgogICAgICAgIDwvdHI+CiAgICAgIDwvdGhlYWQ+CiAgICAgIDx0Ym9keT4KICAgICAgICB7JSBmb3IgY2xpZW50ZSBpbiBjbGllbnRlcyAlfQogICAgICAgIDx0cj4KICAgICAgICAgIDx0ZD57eyBjbGllbnRlLm5vbWJyZSB9fTwvdGQ+CiAgICAgICAgICA8dGQ+e3sgY2xpZW50ZS5uaXR8ZGVmYXVsdDoi4oCUIiB9fTwvdGQ+CiAgICAgICAgICA8dGQ+e3sgY2xpZW50ZS5udW1fb3BlcmFjaW9uZXMgfX08L3RkPgogICAgICAgICAgPHRkPnt7IGNsaWVudGUudWx0aW1vX3NuYXBzaG90fGRhdGU6ImQvbS9ZInxkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgIDx0ZCBjbGFzcz0idGV4dC1lbmQiPgogICAgICAgICAgICA8YSBocmVmPSJ7JSB1cmwgJ3djZ29uZV9yaXNrOmNsaWVudGVfZGV0YWlsJyBjbGllbnRlLnBrICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1wcmltYXJ5Ij5WZXI8L2E+CiAgICAgICAgICA8L3RkPgogICAgICAgIDwvdHI+CiAgICAgICAgeyUgZW1wdHkgJX0KICAgICAgICA8dHI+CiAgICAgICAgICA8dGQgY29sc3Bhbj0iNSIgY2xhc3M9InRleHQtY2VudGVyIHRleHQtbXV0ZWQgcHktNCI+Tm8gaGF5IGNsaWVudGVzIGNvbiBvcGVyYWNpb25lcyBkZSByaWVzZ28gcmVnaXN0cmFkYXMuPC90ZD4KICAgICAgICA8L3RyPgogICAgICAgIHslIGVuZGZvciAlfQogICAgICA8L3Rib2R5PgogICAgPC90YWJsZT4KICA8L2Rpdj4KPC9kaXY+CnslIGVuZGJsb2NrICV9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/wcgone/risk/comando_balon.html
PATH_JSON="templates/wcgone/risk/comando_balon.html"
FILENAME=comando_balon.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=119
SIZE_BYTES_UTF8=4927
CONTENT_SHA256=7b19694013c132f527ff13c14b7192b325a7455247d6c765b7154e5e480291c0
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

{% block title %}Comando Balón — WCG One{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-2">
  <div class="wcg-report-head">
    <h1 class="h4 fw-semibold mb-0">Riesgo — Comando Balón</h1>
    {% include "includes/module_mark.html" with module="risk" %}
  </div>
  <div class="d-flex gap-1 flex-wrap">
    <a href="{% url 'wcgone_risk:export_comando_balon' %}{% if export_query %}?{{ export_query }}{% endif %}" class="btn btn-sm btn-outline-primary">Exportar CSV</a>
    <a href="{% url 'wcgone_risk:cliente_list' %}" class="btn btn-sm btn-outline-secondary">Clientes</a>
  </div>
</div>

<div class="row g-2 mb-3">
  <div class="col-md-3 col-6">
    <div class="card border-0 shadow-sm"><div class="card-body py-2 text-center">
      <div class="stat-value" style="font-size:1.35rem;">{{ summary.clientes }}</div>
      <div class="text-muted small">Clientes con snapshot</div>
    </div></div>
  </div>
  <div class="col-md-3 col-6">
    <div class="card border-0 shadow-sm"><div class="card-body py-2 text-center">
      <div class="stat-value" style="font-size:1.35rem;">{{ summary.operaciones }}</div>
      <div class="text-muted small">Operaciones</div>
    </div></div>
  </div>
  <div class="col-md-3 col-6">
    <div class="card border-0 shadow-sm"><div class="card-body py-2 text-center">
      <div class="stat-value text-warning" style="font-size:1.35rem;">{{ summary.con_mora }}</div>
      <div class="text-muted small">Snapshots con mora</div>
    </div></div>
  </div>
  <div class="col-md-3 col-6">
    <div class="card border-0 shadow-sm"><div class="card-body py-2 text-center">
      <div class="stat-value text-danger" style="font-size:1.35rem;">{{ summary.suma_vencido|default:"0" }}</div>
      <div class="text-muted small">Suma saldos vencidos</div>
    </div></div>
  </div>
</div>

<form method="get" class="row g-2 mb-3">
  <div class="col-md-4">
    <input type="search" name="cliente" value="{{ request.GET.cliente }}" class="form-control form-control-sm" placeholder="Filtrar por cliente">
  </div>
  <div class="col-md-3">
    <input type="text" name="estado" value="{{ request.GET.estado }}" class="form-control form-control-sm" placeholder="Estado operación">
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
    Mostrando hasta 100 registros{% if summary.total_snapshots > 100 %} de {{ summary.total_snapshots }} filtrados{% endif %}.
  </div>
  <div class="table-responsive">
    <table class="table table-hover table-wcg mb-0 align-middle small">
      <thead>
        <tr>
          <th>Fecha</th>
          <th>Cliente</th>
          <th>Operación</th>
          <th>Producto</th>
          <th>Estado</th>
          <th class="text-end">Saldo capital</th>
          <th class="text-end">Vencido</th>
          <th class="text-center">Días atraso</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {% for snap in snapshots %}
        <tr>
          <td>{{ snap.fecha_snapshot|date:"d/m/Y" }}</td>
          <td>
            <a href="{% url 'wcgone_risk:cliente_detail' snap.entidad_id %}">{{ snap.entidad.nombre }}</a>
          </td>
          <td>{{ snap.operacion.codigo_operacion }}</td>
          <td>{{ snap.producto_nombre_raw|default:snap.operacion.producto|default:"—" }}</td>
          <td>{{ snap.estado_operacion|default:"—" }}</td>
          <td class="text-end">{{ snap.capital_balance|default:"—" }}</td>
          <td class="text-end">
            {% if snap.past_due_balance and snap.past_due_balance > 0 %}
            <span class="text-danger fw-semibold">{{ snap.past_due_balance }}</span>
            {% else %}
            {{ snap.past_due_balance|default:"—" }}
            {% endif %}
          </td>
          <td class="text-center">
            {% if snap.due_days and snap.due_days > 0 %}
            <span class="badge text-bg-warning">{{ snap.due_days }}</span>
            {% else %}
            {{ snap.due_days|default:"0" }}
            {% endif %}
          </td>
          <td class="text-end">
            <a href="{% url 'wcgone_risk:operacion_detail' snap.operacion_id %}" class="btn btn-sm btn-outline-primary">Detalle</a>
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
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "wcgone_base.html" %}
00002|
00003|{% block title %}Comando Balón — WCG One{% endblock %}
00004|
00005|{% block content %}
00006|<div class="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-2">
00007|  <div class="wcg-report-head">
00008|    <h1 class="h4 fw-semibold mb-0">Riesgo — Comando Balón</h1>
00009|    {% include "includes/module_mark.html" with module="risk" %}
00010|  </div>
00011|  <div class="d-flex gap-1 flex-wrap">
00012|    <a href="{% url 'wcgone_risk:export_comando_balon' %}{% if export_query %}?{{ export_query }}{% endif %}" class="btn btn-sm btn-outline-primary">Exportar CSV</a>
00013|    <a href="{% url 'wcgone_risk:cliente_list' %}" class="btn btn-sm btn-outline-secondary">Clientes</a>
00014|  </div>
00015|</div>
00016|
00017|<div class="row g-2 mb-3">
00018|  <div class="col-md-3 col-6">
00019|    <div class="card border-0 shadow-sm"><div class="card-body py-2 text-center">
00020|      <div class="stat-value" style="font-size:1.35rem;">{{ summary.clientes }}</div>
00021|      <div class="text-muted small">Clientes con snapshot</div>
00022|    </div></div>
00023|  </div>
00024|  <div class="col-md-3 col-6">
00025|    <div class="card border-0 shadow-sm"><div class="card-body py-2 text-center">
00026|      <div class="stat-value" style="font-size:1.35rem;">{{ summary.operaciones }}</div>
00027|      <div class="text-muted small">Operaciones</div>
00028|    </div></div>
00029|  </div>
00030|  <div class="col-md-3 col-6">
00031|    <div class="card border-0 shadow-sm"><div class="card-body py-2 text-center">
00032|      <div class="stat-value text-warning" style="font-size:1.35rem;">{{ summary.con_mora }}</div>
00033|      <div class="text-muted small">Snapshots con mora</div>
00034|    </div></div>
00035|  </div>
00036|  <div class="col-md-3 col-6">
00037|    <div class="card border-0 shadow-sm"><div class="card-body py-2 text-center">
00038|      <div class="stat-value text-danger" style="font-size:1.35rem;">{{ summary.suma_vencido|default:"0" }}</div>
00039|      <div class="text-muted small">Suma saldos vencidos</div>
00040|    </div></div>
00041|  </div>
00042|</div>
00043|
00044|<form method="get" class="row g-2 mb-3">
00045|  <div class="col-md-4">
00046|    <input type="search" name="cliente" value="{{ request.GET.cliente }}" class="form-control form-control-sm" placeholder="Filtrar por cliente">
00047|  </div>
00048|  <div class="col-md-3">
00049|    <input type="text" name="estado" value="{{ request.GET.estado }}" class="form-control form-control-sm" placeholder="Estado operación">
00050|  </div>
00051|  <div class="col-md-2">
00052|    <button type="submit" class="btn btn-primary btn-sm w-100">Filtrar</button>
00053|  </div>
00054|</form>
00055|
00056|{% if not snapshots and not request.GET %}
00057|{% include "includes/empty_state.html" with title="Sin snapshots operativos" message="Cargue BaseLeasing desde Administración → Importación General." %}
00058|{% endif %}
00059|
00060|<div class="card border-0 shadow-sm">
00061|  <div class="card-header bg-white small text-muted">
00062|    Mostrando hasta 100 registros{% if summary.total_snapshots > 100 %} de {{ summary.total_snapshots }} filtrados{% endif %}.
00063|  </div>
00064|  <div class="table-responsive">
00065|    <table class="table table-hover table-wcg mb-0 align-middle small">
00066|      <thead>
00067|        <tr>
00068|          <th>Fecha</th>
00069|          <th>Cliente</th>
00070|          <th>Operación</th>
00071|          <th>Producto</th>
00072|          <th>Estado</th>
00073|          <th class="text-end">Saldo capital</th>
00074|          <th class="text-end">Vencido</th>
00075|          <th class="text-center">Días atraso</th>
00076|          <th></th>
00077|        </tr>
00078|      </thead>
00079|      <tbody>
00080|        {% for snap in snapshots %}
00081|        <tr>
00082|          <td>{{ snap.fecha_snapshot|date:"d/m/Y" }}</td>
00083|          <td>
00084|            <a href="{% url 'wcgone_risk:cliente_detail' snap.entidad_id %}">{{ snap.entidad.nombre }}</a>
00085|          </td>
00086|          <td>{{ snap.operacion.codigo_operacion }}</td>
00087|          <td>{{ snap.producto_nombre_raw|default:snap.operacion.producto|default:"—" }}</td>
00088|          <td>{{ snap.estado_operacion|default:"—" }}</td>
00089|          <td class="text-end">{{ snap.capital_balance|default:"—" }}</td>
00090|          <td class="text-end">
00091|            {% if snap.past_due_balance and snap.past_due_balance > 0 %}
00092|            <span class="text-danger fw-semibold">{{ snap.past_due_balance }}</span>
00093|            {% else %}
00094|            {{ snap.past_due_balance|default:"—" }}
00095|            {% endif %}
00096|          </td>
00097|          <td class="text-center">
00098|            {% if snap.due_days and snap.due_days > 0 %}
00099|            <span class="badge text-bg-warning">{{ snap.due_days }}</span>
00100|            {% else %}
00101|            {{ snap.due_days|default:"0" }}
00102|            {% endif %}
00103|          </td>
00104|          <td class="text-end">
00105|            <a href="{% url 'wcgone_risk:operacion_detail' snap.operacion_id %}" class="btn btn-sm btn-outline-primary">Detalle</a>
00106|          </td>
00107|        </tr>
00108|        {% empty %}
00109|        <tr>
00110|          <td colspan="9" class="text-center text-muted py-4">
00111|            No hay resultados con los filtros actuales.
00112|          </td>
00113|        </tr>
00114|        {% endfor %}
00115|      </tbody>
00116|    </table>
00117|  </div>
00118|</div>
00119|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAid2Nnb25lX2Jhc2UuaHRtbCIgJX0KCnslIGJsb2NrIHRpdGxlICV9Q29tYW5kbyBCYWzDs24g4oCUIFdDRyBPbmV7JSBlbmRibG9jayAlfQoKeyUgYmxvY2sgY29udGVudCAlfQo8ZGl2IGNsYXNzPSJkLWZsZXgganVzdGlmeS1jb250ZW50LWJldHdlZW4gYWxpZ24taXRlbXMtc3RhcnQgbWItMyBmbGV4LXdyYXAgZ2FwLTIiPgogIDxkaXYgY2xhc3M9IndjZy1yZXBvcnQtaGVhZCI+CiAgICA8aDEgY2xhc3M9Img0IGZ3LXNlbWlib2xkIG1iLTAiPlJpZXNnbyDigJQgQ29tYW5kbyBCYWzDs248L2gxPgogICAgeyUgaW5jbHVkZSAiaW5jbHVkZXMvbW9kdWxlX21hcmsuaHRtbCIgd2l0aCBtb2R1bGU9InJpc2siICV9CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iZC1mbGV4IGdhcC0xIGZsZXgtd3JhcCI+CiAgICA8YSBocmVmPSJ7JSB1cmwgJ3djZ29uZV9yaXNrOmV4cG9ydF9jb21hbmRvX2JhbG9uJyAlfXslIGlmIGV4cG9ydF9xdWVyeSAlfT97eyBleHBvcnRfcXVlcnkgfX17JSBlbmRpZiAlfSIgY2xhc3M9ImJ0biBidG4tc20gYnRuLW91dGxpbmUtcHJpbWFyeSI+RXhwb3J0YXIgQ1NWPC9hPgogICAgPGEgaHJlZj0ieyUgdXJsICd3Y2dvbmVfcmlzazpjbGllbnRlX2xpc3QnICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1zZWNvbmRhcnkiPkNsaWVudGVzPC9hPgogIDwvZGl2Pgo8L2Rpdj4KCjxkaXYgY2xhc3M9InJvdyBnLTIgbWItMyI+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTMgY29sLTYiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20iPjxkaXYgY2xhc3M9ImNhcmQtYm9keSBweS0yIHRleHQtY2VudGVyIj4KICAgICAgPGRpdiBjbGFzcz0ic3RhdC12YWx1ZSIgc3R5bGU9ImZvbnQtc2l6ZToxLjM1cmVtOyI+e3sgc3VtbWFyeS5jbGllbnRlcyB9fTwvZGl2PgogICAgICA8ZGl2IGNsYXNzPSJ0ZXh0LW11dGVkIHNtYWxsIj5DbGllbnRlcyBjb24gc25hcHNob3Q8L2Rpdj4KICAgIDwvZGl2PjwvZGl2PgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1tZC0zIGNvbC02Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIj48ZGl2IGNsYXNzPSJjYXJkLWJvZHkgcHktMiB0ZXh0LWNlbnRlciI+CiAgICAgIDxkaXYgY2xhc3M9InN0YXQtdmFsdWUiIHN0eWxlPSJmb250LXNpemU6MS4zNXJlbTsiPnt7IHN1bW1hcnkub3BlcmFjaW9uZXMgfX08L2Rpdj4KICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+T3BlcmFjaW9uZXM8L2Rpdj4KICAgIDwvZGl2PjwvZGl2PgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1tZC0zIGNvbC02Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIj48ZGl2IGNsYXNzPSJjYXJkLWJvZHkgcHktMiB0ZXh0LWNlbnRlciI+CiAgICAgIDxkaXYgY2xhc3M9InN0YXQtdmFsdWUgdGV4dC13YXJuaW5nIiBzdHlsZT0iZm9udC1zaXplOjEuMzVyZW07Ij57eyBzdW1tYXJ5LmNvbl9tb3JhIH19PC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9InRleHQtbXV0ZWQgc21hbGwiPlNuYXBzaG90cyBjb24gbW9yYTwvZGl2PgogICAgPC9kaXY+PC9kaXY+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTMgY29sLTYiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20iPjxkaXYgY2xhc3M9ImNhcmQtYm9keSBweS0yIHRleHQtY2VudGVyIj4KICAgICAgPGRpdiBjbGFzcz0ic3RhdC12YWx1ZSB0ZXh0LWRhbmdlciIgc3R5bGU9ImZvbnQtc2l6ZToxLjM1cmVtOyI+e3sgc3VtbWFyeS5zdW1hX3ZlbmNpZG98ZGVmYXVsdDoiMCIgfX08L2Rpdj4KICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+U3VtYSBzYWxkb3MgdmVuY2lkb3M8L2Rpdj4KICAgIDwvZGl2PjwvZGl2PgogIDwvZGl2Pgo8L2Rpdj4KCjxmb3JtIG1ldGhvZD0iZ2V0IiBjbGFzcz0icm93IGctMiBtYi0zIj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtNCI+CiAgICA8aW5wdXQgdHlwZT0ic2VhcmNoIiBuYW1lPSJjbGllbnRlIiB2YWx1ZT0ie3sgcmVxdWVzdC5HRVQuY2xpZW50ZSB9fSIgY2xhc3M9ImZvcm0tY29udHJvbCBmb3JtLWNvbnRyb2wtc20iIHBsYWNlaG9sZGVyPSJGaWx0cmFyIHBvciBjbGllbnRlIj4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtMyI+CiAgICA8aW5wdXQgdHlwZT0idGV4dCIgbmFtZT0iZXN0YWRvIiB2YWx1ZT0ie3sgcmVxdWVzdC5HRVQuZXN0YWRvIH19IiBjbGFzcz0iZm9ybS1jb250cm9sIGZvcm0tY29udHJvbC1zbSIgcGxhY2Vob2xkZXI9IkVzdGFkbyBvcGVyYWNpw7NuIj4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtMiI+CiAgICA8YnV0dG9uIHR5cGU9InN1Ym1pdCIgY2xhc3M9ImJ0biBidG4tcHJpbWFyeSBidG4tc20gdy0xMDAiPkZpbHRyYXI8L2J1dHRvbj4KICA8L2Rpdj4KPC9mb3JtPgoKeyUgaWYgbm90IHNuYXBzaG90cyBhbmQgbm90IHJlcXVlc3QuR0VUICV9CnslIGluY2x1ZGUgImluY2x1ZGVzL2VtcHR5X3N0YXRlLmh0bWwiIHdpdGggdGl0bGU9IlNpbiBzbmFwc2hvdHMgb3BlcmF0aXZvcyIgbWVzc2FnZT0iQ2FyZ3VlIEJhc2VMZWFzaW5nIGRlc2RlIEFkbWluaXN0cmFjacOzbiDihpIgSW1wb3J0YWNpw7NuIEdlbmVyYWwuIiAlfQp7JSBlbmRpZiAlfQoKPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20iPgogIDxkaXYgY2xhc3M9ImNhcmQtaGVhZGVyIGJnLXdoaXRlIHNtYWxsIHRleHQtbXV0ZWQiPgogICAgTW9zdHJhbmRvIGhhc3RhIDEwMCByZWdpc3Ryb3N7JSBpZiBzdW1tYXJ5LnRvdGFsX3NuYXBzaG90cyA+IDEwMCAlfSBkZSB7eyBzdW1tYXJ5LnRvdGFsX3NuYXBzaG90cyB9fSBmaWx0cmFkb3N7JSBlbmRpZiAlfS4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJ0YWJsZS1yZXNwb25zaXZlIj4KICAgIDx0YWJsZSBjbGFzcz0idGFibGUgdGFibGUtaG92ZXIgdGFibGUtd2NnIG1iLTAgYWxpZ24tbWlkZGxlIHNtYWxsIj4KICAgICAgPHRoZWFkPgogICAgICAgIDx0cj4KICAgICAgICAgIDx0aD5GZWNoYTwvdGg+CiAgICAgICAgICA8dGg+Q2xpZW50ZTwvdGg+CiAgICAgICAgICA8dGg+T3BlcmFjacOzbjwvdGg+CiAgICAgICAgICA8dGg+UHJvZHVjdG88L3RoPgogICAgICAgICAgPHRoPkVzdGFkbzwvdGg+CiAgICAgICAgICA8dGggY2xhc3M9InRleHQtZW5kIj5TYWxkbyBjYXBpdGFsPC90aD4KICAgICAgICAgIDx0aCBjbGFzcz0idGV4dC1lbmQiPlZlbmNpZG88L3RoPgogICAgICAgICAgPHRoIGNsYXNzPSJ0ZXh0LWNlbnRlciI+RMOtYXMgYXRyYXNvPC90aD4KICAgICAgICAgIDx0aD48L3RoPgogICAgICAgIDwvdHI+CiAgICAgIDwvdGhlYWQ+CiAgICAgIDx0Ym9keT4KICAgICAgICB7JSBmb3Igc25hcCBpbiBzbmFwc2hvdHMgJX0KICAgICAgICA8dHI+CiAgICAgICAgICA8dGQ+e3sgc25hcC5mZWNoYV9zbmFwc2hvdHxkYXRlOiJkL20vWSIgfX08L3RkPgogICAgICAgICAgPHRkPgogICAgICAgICAgICA8YSBocmVmPSJ7JSB1cmwgJ3djZ29uZV9yaXNrOmNsaWVudGVfZGV0YWlsJyBzbmFwLmVudGlkYWRfaWQgJX0iPnt7IHNuYXAuZW50aWRhZC5ub21icmUgfX08L2E+CiAgICAgICAgICA8L3RkPgogICAgICAgICAgPHRkPnt7IHNuYXAub3BlcmFjaW9uLmNvZGlnb19vcGVyYWNpb24gfX08L3RkPgogICAgICAgICAgPHRkPnt7IHNuYXAucHJvZHVjdG9fbm9tYnJlX3Jhd3xkZWZhdWx0OnNuYXAub3BlcmFjaW9uLnByb2R1Y3RvfGRlZmF1bHQ6IuKAlCIgfX08L3RkPgogICAgICAgICAgPHRkPnt7IHNuYXAuZXN0YWRvX29wZXJhY2lvbnxkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgIDx0ZCBjbGFzcz0idGV4dC1lbmQiPnt7IHNuYXAuY2FwaXRhbF9iYWxhbmNlfGRlZmF1bHQ6IuKAlCIgfX08L3RkPgogICAgICAgICAgPHRkIGNsYXNzPSJ0ZXh0LWVuZCI+CiAgICAgICAgICAgIHslIGlmIHNuYXAucGFzdF9kdWVfYmFsYW5jZSBhbmQgc25hcC5wYXN0X2R1ZV9iYWxhbmNlID4gMCAlfQogICAgICAgICAgICA8c3BhbiBjbGFzcz0idGV4dC1kYW5nZXIgZnctc2VtaWJvbGQiPnt7IHNuYXAucGFzdF9kdWVfYmFsYW5jZSB9fTwvc3Bhbj4KICAgICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgICB7eyBzbmFwLnBhc3RfZHVlX2JhbGFuY2V8ZGVmYXVsdDoi4oCUIiB9fQogICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgPC90ZD4KICAgICAgICAgIDx0ZCBjbGFzcz0idGV4dC1jZW50ZXIiPgogICAgICAgICAgICB7JSBpZiBzbmFwLmR1ZV9kYXlzIGFuZCBzbmFwLmR1ZV9kYXlzID4gMCAlfQogICAgICAgICAgICA8c3BhbiBjbGFzcz0iYmFkZ2UgdGV4dC1iZy13YXJuaW5nIj57eyBzbmFwLmR1ZV9kYXlzIH19PC9zcGFuPgogICAgICAgICAgICB7JSBlbHNlICV9CiAgICAgICAgICAgIHt7IHNuYXAuZHVlX2RheXN8ZGVmYXVsdDoiMCIgfX0KICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgIDwvdGQ+CiAgICAgICAgICA8dGQgY2xhc3M9InRleHQtZW5kIj4KICAgICAgICAgICAgPGEgaHJlZj0ieyUgdXJsICd3Y2dvbmVfcmlzazpvcGVyYWNpb25fZGV0YWlsJyBzbmFwLm9wZXJhY2lvbl9pZCAlfSIgY2xhc3M9ImJ0biBidG4tc20gYnRuLW91dGxpbmUtcHJpbWFyeSI+RGV0YWxsZTwvYT4KICAgICAgICAgIDwvdGQ+CiAgICAgICAgPC90cj4KICAgICAgICB7JSBlbXB0eSAlfQogICAgICAgIDx0cj4KICAgICAgICAgIDx0ZCBjb2xzcGFuPSI5IiBjbGFzcz0idGV4dC1jZW50ZXIgdGV4dC1tdXRlZCBweS00Ij4KICAgICAgICAgICAgTm8gaGF5IHJlc3VsdGFkb3MgY29uIGxvcyBmaWx0cm9zIGFjdHVhbGVzLgogICAgICAgICAgPC90ZD4KICAgICAgICA8L3RyPgogICAgICAgIHslIGVuZGZvciAlfQogICAgICA8L3Rib2R5PgogICAgPC90YWJsZT4KICA8L2Rpdj4KPC9kaXY+CnslIGVuZGJsb2NrICV9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/wcgone/risk/operacion_detail.html
PATH_JSON="templates/wcgone/risk/operacion_detail.html"
FILENAME=operacion_detail.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=87
SIZE_BYTES_UTF8=3864
CONTENT_SHA256=ab26828236f63ddbdc70eb7b2f60cd1f1b88f04891a5224377df261d61a7c6f0
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

{% block title %}{{ operacion.codigo_operacion }} — Balón de Riesgo — WCG One{% endblock %}

{% block content %}
<div class="mb-3">
  <h1 class="h4 fw-semibold mb-1">Operación {{ operacion.codigo_operacion }}</h1>
  <p class="text-muted small mb-0">
    Cliente: <a href="{% url 'wcgone_risk:cliente_detail' operacion.entidad_id %}">{{ operacion.entidad.nombre }}</a>
    {% if operacion.contrato_numero %} · Contrato {{ operacion.contrato_numero }}{% endif %}
  </p>
</div>

<div class="row g-3 mb-3">
  <div class="col-md-3"><div class="card border-0 shadow-sm"><div class="card-body small"><div class="text-muted">Producto</div><div class="fw-semibold">{{ operacion.producto|default:"—" }}</div></div></div></div>
  <div class="col-md-3"><div class="card border-0 shadow-sm"><div class="card-body small"><div class="text-muted">Unidad</div><div class="fw-semibold">{{ operacion.unidad_negocio|default:"—" }}</div></div></div></div>
  <div class="col-md-3"><div class="card border-0 shadow-sm"><div class="card-body small"><div class="text-muted">Monto original</div><div class="fw-semibold">{{ operacion.monto_original|default:"—" }}</div></div></div></div>
  <div class="col-md-3"><div class="card border-0 shadow-sm"><div class="card-body small"><div class="text-muted">Estado</div><div class="fw-semibold">{{ operacion.estado|default:"—" }}</div></div></div></div>
</div>

<div class="card border-0 shadow-sm mb-3">
  <div class="card-header bg-white fw-semibold">Historial de snapshots</div>
  <div class="table-responsive">
    <table class="table table-sm table-hover mb-0">
      <thead>
        <tr>
          <th>Fecha</th>
          <th>Estado</th>
          <th class="text-end">Capital</th>
          <th class="text-end">Vencido</th>
          <th class="text-center">Días</th>
          <th class="text-end">Renta</th>
        </tr>
      </thead>
      <tbody>
        {% for snap in snapshots %}
        <tr>
          <td>{{ snap.fecha_snapshot|date:"d/m/Y" }}</td>
          <td>{{ snap.estado_operacion|default:"—" }}</td>
          <td class="text-end">{{ snap.capital_balance|default:"—" }}</td>
          <td class="text-end">{{ snap.past_due_balance|default:"—" }}</td>
          <td class="text-center">{{ snap.due_days|default:"0" }}</td>
          <td class="text-end">{{ snap.monthly_rent|default:"—" }}</td>
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
          <tbody>
            {% for p in pagos_programados %}
            <tr><td>{{ p.fecha_programada|date:"d/m/Y" }}</td><td class="text-end">{{ p.monto_capital|default:"—" }}</td></tr>
            {% empty %}
            <tr><td class="text-muted py-3">Sin pagos programados.</td></tr>
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
          <tbody>
            {% for p in pagos_realizados %}
            <tr><td>{{ p.fecha_pago|date:"d/m/Y" }}</td><td class="text-end">{{ p.monto_capital|default:"—" }}</td></tr>
            {% empty %}
            <tr><td class="text-muted py-3">Sin pagos realizados.</td></tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "wcgone_base.html" %}
00002|
00003|{% block title %}{{ operacion.codigo_operacion }} — Balón de Riesgo — WCG One{% endblock %}
00004|
00005|{% block content %}
00006|<div class="mb-3">
00007|  <h1 class="h4 fw-semibold mb-1">Operación {{ operacion.codigo_operacion }}</h1>
00008|  <p class="text-muted small mb-0">
00009|    Cliente: <a href="{% url 'wcgone_risk:cliente_detail' operacion.entidad_id %}">{{ operacion.entidad.nombre }}</a>
00010|    {% if operacion.contrato_numero %} · Contrato {{ operacion.contrato_numero }}{% endif %}
00011|  </p>
00012|</div>
00013|
00014|<div class="row g-3 mb-3">
00015|  <div class="col-md-3"><div class="card border-0 shadow-sm"><div class="card-body small"><div class="text-muted">Producto</div><div class="fw-semibold">{{ operacion.producto|default:"—" }}</div></div></div></div>
00016|  <div class="col-md-3"><div class="card border-0 shadow-sm"><div class="card-body small"><div class="text-muted">Unidad</div><div class="fw-semibold">{{ operacion.unidad_negocio|default:"—" }}</div></div></div></div>
00017|  <div class="col-md-3"><div class="card border-0 shadow-sm"><div class="card-body small"><div class="text-muted">Monto original</div><div class="fw-semibold">{{ operacion.monto_original|default:"—" }}</div></div></div></div>
00018|  <div class="col-md-3"><div class="card border-0 shadow-sm"><div class="card-body small"><div class="text-muted">Estado</div><div class="fw-semibold">{{ operacion.estado|default:"—" }}</div></div></div></div>
00019|</div>
00020|
00021|<div class="card border-0 shadow-sm mb-3">
00022|  <div class="card-header bg-white fw-semibold">Historial de snapshots</div>
00023|  <div class="table-responsive">
00024|    <table class="table table-sm table-hover mb-0">
00025|      <thead>
00026|        <tr>
00027|          <th>Fecha</th>
00028|          <th>Estado</th>
00029|          <th class="text-end">Capital</th>
00030|          <th class="text-end">Vencido</th>
00031|          <th class="text-center">Días</th>
00032|          <th class="text-end">Renta</th>
00033|        </tr>
00034|      </thead>
00035|      <tbody>
00036|        {% for snap in snapshots %}
00037|        <tr>
00038|          <td>{{ snap.fecha_snapshot|date:"d/m/Y" }}</td>
00039|          <td>{{ snap.estado_operacion|default:"—" }}</td>
00040|          <td class="text-end">{{ snap.capital_balance|default:"—" }}</td>
00041|          <td class="text-end">{{ snap.past_due_balance|default:"—" }}</td>
00042|          <td class="text-center">{{ snap.due_days|default:"0" }}</td>
00043|          <td class="text-end">{{ snap.monthly_rent|default:"—" }}</td>
00044|        </tr>
00045|        {% empty %}
00046|        <tr><td colspan="6" class="text-muted text-center py-3">Sin snapshots para esta operación.</td></tr>
00047|        {% endfor %}
00048|      </tbody>
00049|    </table>
00050|  </div>
00051|</div>
00052|
00053|<div class="row g-3">
00054|  <div class="col-md-6">
00055|    <div class="card border-0 shadow-sm">
00056|      <div class="card-header bg-white fw-semibold">Pagos programados</div>
00057|      <div class="table-responsive">
00058|        <table class="table table-sm mb-0">
00059|          <tbody>
00060|            {% for p in pagos_programados %}
00061|            <tr><td>{{ p.fecha_programada|date:"d/m/Y" }}</td><td class="text-end">{{ p.monto_capital|default:"—" }}</td></tr>
00062|            {% empty %}
00063|            <tr><td class="text-muted py-3">Sin pagos programados.</td></tr>
00064|            {% endfor %}
00065|          </tbody>
00066|        </table>
00067|      </div>
00068|    </div>
00069|  </div>
00070|  <div class="col-md-6">
00071|    <div class="card border-0 shadow-sm">
00072|      <div class="card-header bg-white fw-semibold">Pagos realizados</div>
00073|      <div class="table-responsive">
00074|        <table class="table table-sm mb-0">
00075|          <tbody>
00076|            {% for p in pagos_realizados %}
00077|            <tr><td>{{ p.fecha_pago|date:"d/m/Y" }}</td><td class="text-end">{{ p.monto_capital|default:"—" }}</td></tr>
00078|            {% empty %}
00079|            <tr><td class="text-muted py-3">Sin pagos realizados.</td></tr>
00080|            {% endfor %}
00081|          </tbody>
00082|        </table>
00083|      </div>
00084|    </div>
00085|  </div>
00086|</div>
00087|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAid2Nnb25lX2Jhc2UuaHRtbCIgJX0KCnslIGJsb2NrIHRpdGxlICV9e3sgb3BlcmFjaW9uLmNvZGlnb19vcGVyYWNpb24gfX0g4oCUIEJhbMOzbiBkZSBSaWVzZ28g4oCUIFdDRyBPbmV7JSBlbmRibG9jayAlfQoKeyUgYmxvY2sgY29udGVudCAlfQo8ZGl2IGNsYXNzPSJtYi0zIj4KICA8aDEgY2xhc3M9Img0IGZ3LXNlbWlib2xkIG1iLTEiPk9wZXJhY2nDs24ge3sgb3BlcmFjaW9uLmNvZGlnb19vcGVyYWNpb24gfX08L2gxPgogIDxwIGNsYXNzPSJ0ZXh0LW11dGVkIHNtYWxsIG1iLTAiPgogICAgQ2xpZW50ZTogPGEgaHJlZj0ieyUgdXJsICd3Y2dvbmVfcmlzazpjbGllbnRlX2RldGFpbCcgb3BlcmFjaW9uLmVudGlkYWRfaWQgJX0iPnt7IG9wZXJhY2lvbi5lbnRpZGFkLm5vbWJyZSB9fTwvYT4KICAgIHslIGlmIG9wZXJhY2lvbi5jb250cmF0b19udW1lcm8gJX0gwrcgQ29udHJhdG8ge3sgb3BlcmFjaW9uLmNvbnRyYXRvX251bWVybyB9fXslIGVuZGlmICV9CiAgPC9wPgo8L2Rpdj4KCjxkaXYgY2xhc3M9InJvdyBnLTMgbWItMyI+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTMiPjxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIj48ZGl2IGNsYXNzPSJjYXJkLWJvZHkgc21hbGwiPjxkaXYgY2xhc3M9InRleHQtbXV0ZWQiPlByb2R1Y3RvPC9kaXY+PGRpdiBjbGFzcz0iZnctc2VtaWJvbGQiPnt7IG9wZXJhY2lvbi5wcm9kdWN0b3xkZWZhdWx0OiLigJQiIH19PC9kaXY+PC9kaXY+PC9kaXY+PC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTMiPjxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIj48ZGl2IGNsYXNzPSJjYXJkLWJvZHkgc21hbGwiPjxkaXYgY2xhc3M9InRleHQtbXV0ZWQiPlVuaWRhZDwvZGl2PjxkaXYgY2xhc3M9ImZ3LXNlbWlib2xkIj57eyBvcGVyYWNpb24udW5pZGFkX25lZ29jaW98ZGVmYXVsdDoi4oCUIiB9fTwvZGl2PjwvZGl2PjwvZGl2PjwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1tZC0zIj48ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSI+PGRpdiBjbGFzcz0iY2FyZC1ib2R5IHNtYWxsIj48ZGl2IGNsYXNzPSJ0ZXh0LW11dGVkIj5Nb250byBvcmlnaW5hbDwvZGl2PjxkaXYgY2xhc3M9ImZ3LXNlbWlib2xkIj57eyBvcGVyYWNpb24ubW9udG9fb3JpZ2luYWx8ZGVmYXVsdDoi4oCUIiB9fTwvZGl2PjwvZGl2PjwvZGl2PjwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1tZC0zIj48ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSI+PGRpdiBjbGFzcz0iY2FyZC1ib2R5IHNtYWxsIj48ZGl2IGNsYXNzPSJ0ZXh0LW11dGVkIj5Fc3RhZG88L2Rpdj48ZGl2IGNsYXNzPSJmdy1zZW1pYm9sZCI+e3sgb3BlcmFjaW9uLmVzdGFkb3xkZWZhdWx0OiLigJQiIH19PC9kaXY+PC9kaXY+PC9kaXY+PC9kaXY+CjwvZGl2PgoKPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20gbWItMyI+CiAgPGRpdiBjbGFzcz0iY2FyZC1oZWFkZXIgYmctd2hpdGUgZnctc2VtaWJvbGQiPkhpc3RvcmlhbCBkZSBzbmFwc2hvdHM8L2Rpdj4KICA8ZGl2IGNsYXNzPSJ0YWJsZS1yZXNwb25zaXZlIj4KICAgIDx0YWJsZSBjbGFzcz0idGFibGUgdGFibGUtc20gdGFibGUtaG92ZXIgbWItMCI+CiAgICAgIDx0aGVhZD4KICAgICAgICA8dHI+CiAgICAgICAgICA8dGg+RmVjaGE8L3RoPgogICAgICAgICAgPHRoPkVzdGFkbzwvdGg+CiAgICAgICAgICA8dGggY2xhc3M9InRleHQtZW5kIj5DYXBpdGFsPC90aD4KICAgICAgICAgIDx0aCBjbGFzcz0idGV4dC1lbmQiPlZlbmNpZG88L3RoPgogICAgICAgICAgPHRoIGNsYXNzPSJ0ZXh0LWNlbnRlciI+RMOtYXM8L3RoPgogICAgICAgICAgPHRoIGNsYXNzPSJ0ZXh0LWVuZCI+UmVudGE8L3RoPgogICAgICAgIDwvdHI+CiAgICAgIDwvdGhlYWQ+CiAgICAgIDx0Ym9keT4KICAgICAgICB7JSBmb3Igc25hcCBpbiBzbmFwc2hvdHMgJX0KICAgICAgICA8dHI+CiAgICAgICAgICA8dGQ+e3sgc25hcC5mZWNoYV9zbmFwc2hvdHxkYXRlOiJkL20vWSIgfX08L3RkPgogICAgICAgICAgPHRkPnt7IHNuYXAuZXN0YWRvX29wZXJhY2lvbnxkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgIDx0ZCBjbGFzcz0idGV4dC1lbmQiPnt7IHNuYXAuY2FwaXRhbF9iYWxhbmNlfGRlZmF1bHQ6IuKAlCIgfX08L3RkPgogICAgICAgICAgPHRkIGNsYXNzPSJ0ZXh0LWVuZCI+e3sgc25hcC5wYXN0X2R1ZV9iYWxhbmNlfGRlZmF1bHQ6IuKAlCIgfX08L3RkPgogICAgICAgICAgPHRkIGNsYXNzPSJ0ZXh0LWNlbnRlciI+e3sgc25hcC5kdWVfZGF5c3xkZWZhdWx0OiIwIiB9fTwvdGQ+CiAgICAgICAgICA8dGQgY2xhc3M9InRleHQtZW5kIj57eyBzbmFwLm1vbnRobHlfcmVudHxkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICA8L3RyPgogICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgPHRyPjx0ZCBjb2xzcGFuPSI2IiBjbGFzcz0idGV4dC1tdXRlZCB0ZXh0LWNlbnRlciBweS0zIj5TaW4gc25hcHNob3RzIHBhcmEgZXN0YSBvcGVyYWNpw7NuLjwvdGQ+PC90cj4KICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgPC90Ym9keT4KICAgIDwvdGFibGU+CiAgPC9kaXY+CjwvZGl2PgoKPGRpdiBjbGFzcz0icm93IGctMyI+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTYiPgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20iPgogICAgICA8ZGl2IGNsYXNzPSJjYXJkLWhlYWRlciBiZy13aGl0ZSBmdy1zZW1pYm9sZCI+UGFnb3MgcHJvZ3JhbWFkb3M8L2Rpdj4KICAgICAgPGRpdiBjbGFzcz0idGFibGUtcmVzcG9uc2l2ZSI+CiAgICAgICAgPHRhYmxlIGNsYXNzPSJ0YWJsZSB0YWJsZS1zbSBtYi0wIj4KICAgICAgICAgIDx0Ym9keT4KICAgICAgICAgICAgeyUgZm9yIHAgaW4gcGFnb3NfcHJvZ3JhbWFkb3MgJX0KICAgICAgICAgICAgPHRyPjx0ZD57eyBwLmZlY2hhX3Byb2dyYW1hZGF8ZGF0ZToiZC9tL1kiIH19PC90ZD48dGQgY2xhc3M9InRleHQtZW5kIj57eyBwLm1vbnRvX2NhcGl0YWx8ZGVmYXVsdDoi4oCUIiB9fTwvdGQ+PC90cj4KICAgICAgICAgICAgeyUgZW1wdHkgJX0KICAgICAgICAgICAgPHRyPjx0ZCBjbGFzcz0idGV4dC1tdXRlZCBweS0zIj5TaW4gcGFnb3MgcHJvZ3JhbWFkb3MuPC90ZD48L3RyPgogICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgIDwvdGJvZHk+CiAgICAgICAgPC90YWJsZT4KICAgICAgPC9kaXY+CiAgICA8L2Rpdj4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtNiI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSI+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtaGVhZGVyIGJnLXdoaXRlIGZ3LXNlbWlib2xkIj5QYWdvcyByZWFsaXphZG9zPC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9InRhYmxlLXJlc3BvbnNpdmUiPgogICAgICAgIDx0YWJsZSBjbGFzcz0idGFibGUgdGFibGUtc20gbWItMCI+CiAgICAgICAgICA8dGJvZHk+CiAgICAgICAgICAgIHslIGZvciBwIGluIHBhZ29zX3JlYWxpemFkb3MgJX0KICAgICAgICAgICAgPHRyPjx0ZD57eyBwLmZlY2hhX3BhZ298ZGF0ZToiZC9tL1kiIH19PC90ZD48dGQgY2xhc3M9InRleHQtZW5kIj57eyBwLm1vbnRvX2NhcGl0YWx8ZGVmYXVsdDoi4oCUIiB9fTwvdGQ+PC90cj4KICAgICAgICAgICAgeyUgZW1wdHkgJX0KICAgICAgICAgICAgPHRyPjx0ZCBjbGFzcz0idGV4dC1tdXRlZCBweS0zIj5TaW4gcGFnb3MgcmVhbGl6YWRvcy48L3RkPjwvdHI+CiAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgPC90Ym9keT4KICAgICAgICA8L3RhYmxlPgogICAgICA8L2Rpdj4KICAgIDwvZGl2PgogIDwvZGl2Pgo8L2Rpdj4KeyUgZW5kYmxvY2sgJX0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/wcgone_base.html
PATH_JSON="templates/wcgone_base.html"
FILENAME=wcgone_base.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=192
SIZE_BYTES_UTF8=6473
CONTENT_SHA256=40901eb8f85adb85a279c705bb279f21e6a32a8da322a1da5f644f86b098863d
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
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}WCG One{% endblock %}</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap" rel="stylesheet">
  <style>
    :root {
      --wcg-bg: #f3f6f9;
      --wcg-surface: #ffffff;
      --wcg-ink: #2a3441;
      --wcg-muted: #6b7a8d;
      --wcg-line: #e2e8f0;
      --wcg-accent: #7a9bb8;
      --wcg-accent-soft: #e8f0f6;
      --wcg-accent-ink: #3d5a73;
      --wcg-nav-bg: #eef3f7;
      --wcg-nav-ink: #3a4a5c;
      --wcg-radius: 10px;
      --wcg-shadow: 0 1px 2px rgba(42, 52, 65, 0.04), 0 4px 12px rgba(42, 52, 65, 0.04);
    }
    body {
      font-family: "DM Sans", system-ui, sans-serif;
      background:
        radial-gradient(1200px 500px at 10% -10%, #e8f1f7 0%, transparent 55%),
        radial-gradient(900px 400px at 100% 0%, #edf2f6 0%, transparent 50%),
        var(--wcg-bg);
      color: var(--wcg-ink);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    .wcg-topbar {
      background: var(--wcg-nav-bg);
      border-bottom: 1px solid var(--wcg-line);
    }
    .wcg-brand {
      font-weight: 700;
      letter-spacing: -0.02em;
      color: var(--wcg-accent-ink) !important;
      font-size: 1.05rem;
      margin-right: 1.25rem;
    }
    .wcg-home-link {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      padding: 0.4rem 0.85rem;
      border-radius: var(--wcg-radius);
      background: var(--wcg-surface);
      border: 1px solid var(--wcg-line);
      color: var(--wcg-accent-ink) !important;
      font-weight: 600;
      font-size: 0.82rem;
      text-decoration: none;
      margin-right: 1rem;
      white-space: nowrap;
    }
    .wcg-home-link:hover {
      background: var(--wcg-accent-soft);
      color: var(--wcg-ink) !important;
    }
    .wcg-nav-primary { gap: 0.35rem; }
    .wcg-nav-primary .nav-link {
      color: var(--wcg-nav-ink) !important;
      font-weight: 500;
      font-size: 0.9rem;
      padding: 0.45rem 0.9rem !important;
      border-radius: var(--wcg-radius);
      border: 1px solid transparent;
    }
    .wcg-nav-primary .nav-link:hover { background: rgba(255,255,255,0.7); }
    .wcg-nav-primary .nav-link.active {
      background: var(--wcg-surface);
      border-color: var(--wcg-line);
      color: var(--wcg-accent-ink) !important;
      box-shadow: var(--wcg-shadow);
    }
    .wcg-mod-ico {
      font-size: 1.05em;
      margin-right: 0.15rem;
      line-height: 1;
    }
    .wcg-nav-secondary .nav-link,
    .wcg-nav-secondary .btn-link {
      color: var(--wcg-muted) !important;
      font-size: 0.85rem;
      font-weight: 500;
      text-decoration: none;
    }
    .wcg-nav-secondary .dropdown-menu {
      border: 1px solid var(--wcg-line);
      border-radius: var(--wcg-radius);
      box-shadow: var(--wcg-shadow);
      padding: 0.35rem;
    }
    .wcg-nav-secondary .dropdown-item {
      border-radius: 4px;
      font-size: 0.88rem;
      padding: 0.45rem 0.75rem;
    }
    .wcg-nav-secondary .dropdown-item:hover { background: var(--wcg-accent-soft); }
    .card-module { transition: box-shadow .15s ease; border: 1px solid var(--wcg-line) !important; border-radius: var(--wcg-radius) !important; box-shadow: var(--wcg-shadow); }
    .card-module .card-header {
      background: var(--wcg-accent-soft);
      color: var(--wcg-accent-ink);
      font-weight: 600;
      border-bottom: 1px solid var(--wcg-line);
    }
    .table-wcg thead { background: #f0f4f8; color: var(--wcg-accent-ink); }
    .table-wcg thead th { font-weight: 600; font-size: .78rem; border: none; text-transform: uppercase; letter-spacing: 0.03em; }
    .stat-value { font-size: 1.65rem; font-weight: 700; color: var(--wcg-accent-ink); }
    .breadcrumb { background: transparent; padding-left: 0; margin-bottom: 1rem; }
    main { padding-bottom: 3rem; flex: 1; }
    .btn { border-radius: var(--wcg-radius); font-weight: 500; }
    .btn-primary { background: var(--wcg-accent-ink); border-color: var(--wcg-accent-ink); }
    .btn-outline-primary { color: var(--wcg-accent-ink); border-color: #b7c9d8; }
    .wcg-title-ico {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      flex: 0 0 auto;
      font-size: 1.9em;
      line-height: 1;
      margin: 0;
      padding: 0.05rem 0.1rem;
      opacity: 0.92;
      filter: saturate(1.12);
      user-select: none;
      pointer-events: none;
    }
    .wcg-report-head {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 0.75rem;
      flex: 1 1 auto;
      min-width: 0;
      margin: 0;
    }
    .wcg-report-head > h1,
    .wcg-report-head > h2,
    .wcg-report-head > .h4 {
      margin: 0;
      flex: 1 1 auto;
      min-width: 0;
      line-height: 1.25;
    }
    .btn { border-radius: 10px; font-weight: 500; }
    .btn-primary { background: #5a7a94; border-color: #5a7a94; color: #fff; }
    .btn-outline-primary { color: #3d5a73; background: #e4eef6; border-color: #c5d4e2; }
    .btn-outline-secondary { color: #4a5562; background: #e8edf2; border-color: #d0d8e0; }
    .wcg-home-link {
      background: #ffffff !important;
      border-color: #b7c9d8 !important;
    }
    footer.wcg-footer {
      border-top: 1px solid var(--wcg-line);
      background: rgba(255,255,255,0.65);
      padding: 0.85rem 0;
      color: var(--wcg-muted);
      font-size: 0.8rem;
    }
  </style>
  {% block extra_css %}{% endblock %}
</head>
<body>
  <header class="wcg-topbar sticky-top">
    {% include "includes/navbar.html" %}
  </header>

  <main class="container py-4">
    {% include "includes/messages.html" %}
    {% include "includes/breadcrumbs.html" %}

    {% block content %}{% endblock %}
  </main>

  <footer class="wcg-footer mt-auto">
    <div class="container">
      WCG One — Working Capital Group
    </div>
  </footer>

  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  {% block extra_js %}{% endblock %}
</body>
</html>

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|<!DOCTYPE html>
00002|<html lang="es">
00003|<head>
00004|  <meta charset="utf-8">
00005|  <meta name="viewport" content="width=device-width, initial-scale=1">
00006|  <title>{% block title %}WCG One{% endblock %}</title>
00007|  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
00008|  <link rel="preconnect" href="https://fonts.googleapis.com">
00009|  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
00010|  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap" rel="stylesheet">
00011|  <style>
00012|    :root {
00013|      --wcg-bg: #f3f6f9;
00014|      --wcg-surface: #ffffff;
00015|      --wcg-ink: #2a3441;
00016|      --wcg-muted: #6b7a8d;
00017|      --wcg-line: #e2e8f0;
00018|      --wcg-accent: #7a9bb8;
00019|      --wcg-accent-soft: #e8f0f6;
00020|      --wcg-accent-ink: #3d5a73;
00021|      --wcg-nav-bg: #eef3f7;
00022|      --wcg-nav-ink: #3a4a5c;
00023|      --wcg-radius: 10px;
00024|      --wcg-shadow: 0 1px 2px rgba(42, 52, 65, 0.04), 0 4px 12px rgba(42, 52, 65, 0.04);
00025|    }
00026|    body {
00027|      font-family: "DM Sans", system-ui, sans-serif;
00028|      background:
00029|        radial-gradient(1200px 500px at 10% -10%, #e8f1f7 0%, transparent 55%),
00030|        radial-gradient(900px 400px at 100% 0%, #edf2f6 0%, transparent 50%),
00031|        var(--wcg-bg);
00032|      color: var(--wcg-ink);
00033|      min-height: 100vh;
00034|      display: flex;
00035|      flex-direction: column;
00036|    }
00037|    .wcg-topbar {
00038|      background: var(--wcg-nav-bg);
00039|      border-bottom: 1px solid var(--wcg-line);
00040|    }
00041|    .wcg-brand {
00042|      font-weight: 700;
00043|      letter-spacing: -0.02em;
00044|      color: var(--wcg-accent-ink) !important;
00045|      font-size: 1.05rem;
00046|      margin-right: 1.25rem;
00047|    }
00048|    .wcg-home-link {
00049|      display: inline-flex;
00050|      align-items: center;
00051|      gap: 0.35rem;
00052|      padding: 0.4rem 0.85rem;
00053|      border-radius: var(--wcg-radius);
00054|      background: var(--wcg-surface);
00055|      border: 1px solid var(--wcg-line);
00056|      color: var(--wcg-accent-ink) !important;
00057|      font-weight: 600;
00058|      font-size: 0.82rem;
00059|      text-decoration: none;
00060|      margin-right: 1rem;
00061|      white-space: nowrap;
00062|    }
00063|    .wcg-home-link:hover {
00064|      background: var(--wcg-accent-soft);
00065|      color: var(--wcg-ink) !important;
00066|    }
00067|    .wcg-nav-primary { gap: 0.35rem; }
00068|    .wcg-nav-primary .nav-link {
00069|      color: var(--wcg-nav-ink) !important;
00070|      font-weight: 500;
00071|      font-size: 0.9rem;
00072|      padding: 0.45rem 0.9rem !important;
00073|      border-radius: var(--wcg-radius);
00074|      border: 1px solid transparent;
00075|    }
00076|    .wcg-nav-primary .nav-link:hover { background: rgba(255,255,255,0.7); }
00077|    .wcg-nav-primary .nav-link.active {
00078|      background: var(--wcg-surface);
00079|      border-color: var(--wcg-line);
00080|      color: var(--wcg-accent-ink) !important;
00081|      box-shadow: var(--wcg-shadow);
00082|    }
00083|    .wcg-mod-ico {
00084|      font-size: 1.05em;
00085|      margin-right: 0.15rem;
00086|      line-height: 1;
00087|    }
00088|    .wcg-nav-secondary .nav-link,
00089|    .wcg-nav-secondary .btn-link {
00090|      color: var(--wcg-muted) !important;
00091|      font-size: 0.85rem;
00092|      font-weight: 500;
00093|      text-decoration: none;
00094|    }
00095|    .wcg-nav-secondary .dropdown-menu {
00096|      border: 1px solid var(--wcg-line);
00097|      border-radius: var(--wcg-radius);
00098|      box-shadow: var(--wcg-shadow);
00099|      padding: 0.35rem;
00100|    }
00101|    .wcg-nav-secondary .dropdown-item {
00102|      border-radius: 4px;
00103|      font-size: 0.88rem;
00104|      padding: 0.45rem 0.75rem;
00105|    }
00106|    .wcg-nav-secondary .dropdown-item:hover { background: var(--wcg-accent-soft); }
00107|    .card-module { transition: box-shadow .15s ease; border: 1px solid var(--wcg-line) !important; border-radius: var(--wcg-radius) !important; box-shadow: var(--wcg-shadow); }
00108|    .card-module .card-header {
00109|      background: var(--wcg-accent-soft);
00110|      color: var(--wcg-accent-ink);
00111|      font-weight: 600;
00112|      border-bottom: 1px solid var(--wcg-line);
00113|    }
00114|    .table-wcg thead { background: #f0f4f8; color: var(--wcg-accent-ink); }
00115|    .table-wcg thead th { font-weight: 600; font-size: .78rem; border: none; text-transform: uppercase; letter-spacing: 0.03em; }
00116|    .stat-value { font-size: 1.65rem; font-weight: 700; color: var(--wcg-accent-ink); }
00117|    .breadcrumb { background: transparent; padding-left: 0; margin-bottom: 1rem; }
00118|    main { padding-bottom: 3rem; flex: 1; }
00119|    .btn { border-radius: var(--wcg-radius); font-weight: 500; }
00120|    .btn-primary { background: var(--wcg-accent-ink); border-color: var(--wcg-accent-ink); }
00121|    .btn-outline-primary { color: var(--wcg-accent-ink); border-color: #b7c9d8; }
00122|    .wcg-title-ico {
00123|      display: inline-flex;
00124|      align-items: center;
00125|      justify-content: center;
00126|      flex: 0 0 auto;
00127|      font-size: 1.9em;
00128|      line-height: 1;
00129|      margin: 0;
00130|      padding: 0.05rem 0.1rem;
00131|      opacity: 0.92;
00132|      filter: saturate(1.12);
00133|      user-select: none;
00134|      pointer-events: none;
00135|    }
00136|    .wcg-report-head {
00137|      display: flex;
00138|      align-items: flex-start;
00139|      justify-content: space-between;
00140|      gap: 0.75rem;
00141|      flex: 1 1 auto;
00142|      min-width: 0;
00143|      margin: 0;
00144|    }
00145|    .wcg-report-head > h1,
00146|    .wcg-report-head > h2,
00147|    .wcg-report-head > .h4 {
00148|      margin: 0;
00149|      flex: 1 1 auto;
00150|      min-width: 0;
00151|      line-height: 1.25;
00152|    }
00153|    .btn { border-radius: 10px; font-weight: 500; }
00154|    .btn-primary { background: #5a7a94; border-color: #5a7a94; color: #fff; }
00155|    .btn-outline-primary { color: #3d5a73; background: #e4eef6; border-color: #c5d4e2; }
00156|    .btn-outline-secondary { color: #4a5562; background: #e8edf2; border-color: #d0d8e0; }
00157|    .wcg-home-link {
00158|      background: #ffffff !important;
00159|      border-color: #b7c9d8 !important;
00160|    }
00161|    footer.wcg-footer {
00162|      border-top: 1px solid var(--wcg-line);
00163|      background: rgba(255,255,255,0.65);
00164|      padding: 0.85rem 0;
00165|      color: var(--wcg-muted);
00166|      font-size: 0.8rem;
00167|    }
00168|  </style>
00169|  {% block extra_css %}{% endblock %}
00170|</head>
00171|<body>
00172|  <header class="wcg-topbar sticky-top">
00173|    {% include "includes/navbar.html" %}
00174|  </header>
00175|
00176|  <main class="container py-4">
00177|    {% include "includes/messages.html" %}
00178|    {% include "includes/breadcrumbs.html" %}
00179|
00180|    {% block content %}{% endblock %}
00181|  </main>
00182|
00183|  <footer class="wcg-footer mt-auto">
00184|    <div class="container">
00185|      WCG One — Working Capital Group
00186|    </div>
00187|  </footer>
00188|
00189|  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
00190|  {% block extra_js %}{% endblock %}
00191|</body>
00192|</html>

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
PCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVzIj4KPGhlYWQ+CiAgPG1ldGEgY2hhcnNldD0idXRmLTgiPgogIDxtZXRhIG5hbWU9InZpZXdwb3J0IiBjb250ZW50PSJ3aWR0aD1kZXZpY2Utd2lkdGgsIGluaXRpYWwtc2NhbGU9MSI+CiAgPHRpdGxlPnslIGJsb2NrIHRpdGxlICV9V0NHIE9uZXslIGVuZGJsb2NrICV9PC90aXRsZT4KICA8bGluayBocmVmPSJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvbnBtL2Jvb3RzdHJhcEA1LjMuMy9kaXN0L2Nzcy9ib290c3RyYXAubWluLmNzcyIgcmVsPSJzdHlsZXNoZWV0Ij4KICA8bGluayByZWw9InByZWNvbm5lY3QiIGhyZWY9Imh0dHBzOi8vZm9udHMuZ29vZ2xlYXBpcy5jb20iPgogIDxsaW5rIHJlbD0icHJlY29ubmVjdCIgaHJlZj0iaHR0cHM6Ly9mb250cy5nc3RhdGljLmNvbSIgY3Jvc3NvcmlnaW4+CiAgPGxpbmsgaHJlZj0iaHR0cHM6Ly9mb250cy5nb29nbGVhcGlzLmNvbS9jc3MyP2ZhbWlseT1ETStTYW5zOml0YWwsb3Bzeix3Z2h0QDAsOS4uNDAsNDAwOzAsOS4uNDAsNTAwOzAsOS4uNDAsNjAwOzAsOS4uNDAsNzAwOzEsOS4uNDAsNDAwJmRpc3BsYXk9c3dhcCIgcmVsPSJzdHlsZXNoZWV0Ij4KICA8c3R5bGU+CiAgICA6cm9vdCB7CiAgICAgIC0td2NnLWJnOiAjZjNmNmY5OwogICAgICAtLXdjZy1zdXJmYWNlOiAjZmZmZmZmOwogICAgICAtLXdjZy1pbms6ICMyYTM0NDE7CiAgICAgIC0td2NnLW11dGVkOiAjNmI3YThkOwogICAgICAtLXdjZy1saW5lOiAjZTJlOGYwOwogICAgICAtLXdjZy1hY2NlbnQ6ICM3YTliYjg7CiAgICAgIC0td2NnLWFjY2VudC1zb2Z0OiAjZThmMGY2OwogICAgICAtLXdjZy1hY2NlbnQtaW5rOiAjM2Q1YTczOwogICAgICAtLXdjZy1uYXYtYmc6ICNlZWYzZjc7CiAgICAgIC0td2NnLW5hdi1pbms6ICMzYTRhNWM7CiAgICAgIC0td2NnLXJhZGl1czogMTBweDsKICAgICAgLS13Y2ctc2hhZG93OiAwIDFweCAycHggcmdiYSg0MiwgNTIsIDY1LCAwLjA0KSwgMCA0cHggMTJweCByZ2JhKDQyLCA1MiwgNjUsIDAuMDQpOwogICAgfQogICAgYm9keSB7CiAgICAgIGZvbnQtZmFtaWx5OiAiRE0gU2FucyIsIHN5c3RlbS11aSwgc2Fucy1zZXJpZjsKICAgICAgYmFja2dyb3VuZDoKICAgICAgICByYWRpYWwtZ3JhZGllbnQoMTIwMHB4IDUwMHB4IGF0IDEwJSAtMTAlLCAjZThmMWY3IDAlLCB0cmFuc3BhcmVudCA1NSUpLAogICAgICAgIHJhZGlhbC1ncmFkaWVudCg5MDBweCA0MDBweCBhdCAxMDAlIDAlLCAjZWRmMmY2IDAlLCB0cmFuc3BhcmVudCA1MCUpLAogICAgICAgIHZhcigtLXdjZy1iZyk7CiAgICAgIGNvbG9yOiB2YXIoLS13Y2ctaW5rKTsKICAgICAgbWluLWhlaWdodDogMTAwdmg7CiAgICAgIGRpc3BsYXk6IGZsZXg7CiAgICAgIGZsZXgtZGlyZWN0aW9uOiBjb2x1bW47CiAgICB9CiAgICAud2NnLXRvcGJhciB7CiAgICAgIGJhY2tncm91bmQ6IHZhcigtLXdjZy1uYXYtYmcpOwogICAgICBib3JkZXItYm90dG9tOiAxcHggc29saWQgdmFyKC0td2NnLWxpbmUpOwogICAgfQogICAgLndjZy1icmFuZCB7CiAgICAgIGZvbnQtd2VpZ2h0OiA3MDA7CiAgICAgIGxldHRlci1zcGFjaW5nOiAtMC4wMmVtOwogICAgICBjb2xvcjogdmFyKC0td2NnLWFjY2VudC1pbmspICFpbXBvcnRhbnQ7CiAgICAgIGZvbnQtc2l6ZTogMS4wNXJlbTsKICAgICAgbWFyZ2luLXJpZ2h0OiAxLjI1cmVtOwogICAgfQogICAgLndjZy1ob21lLWxpbmsgewogICAgICBkaXNwbGF5OiBpbmxpbmUtZmxleDsKICAgICAgYWxpZ24taXRlbXM6IGNlbnRlcjsKICAgICAgZ2FwOiAwLjM1cmVtOwogICAgICBwYWRkaW5nOiAwLjRyZW0gMC44NXJlbTsKICAgICAgYm9yZGVyLXJhZGl1czogdmFyKC0td2NnLXJhZGl1cyk7CiAgICAgIGJhY2tncm91bmQ6IHZhcigtLXdjZy1zdXJmYWNlKTsKICAgICAgYm9yZGVyOiAxcHggc29saWQgdmFyKC0td2NnLWxpbmUpOwogICAgICBjb2xvcjogdmFyKC0td2NnLWFjY2VudC1pbmspICFpbXBvcnRhbnQ7CiAgICAgIGZvbnQtd2VpZ2h0OiA2MDA7CiAgICAgIGZvbnQtc2l6ZTogMC44MnJlbTsKICAgICAgdGV4dC1kZWNvcmF0aW9uOiBub25lOwogICAgICBtYXJnaW4tcmlnaHQ6IDFyZW07CiAgICAgIHdoaXRlLXNwYWNlOiBub3dyYXA7CiAgICB9CiAgICAud2NnLWhvbWUtbGluazpob3ZlciB7CiAgICAgIGJhY2tncm91bmQ6IHZhcigtLXdjZy1hY2NlbnQtc29mdCk7CiAgICAgIGNvbG9yOiB2YXIoLS13Y2ctaW5rKSAhaW1wb3J0YW50OwogICAgfQogICAgLndjZy1uYXYtcHJpbWFyeSB7IGdhcDogMC4zNXJlbTsgfQogICAgLndjZy1uYXYtcHJpbWFyeSAubmF2LWxpbmsgewogICAgICBjb2xvcjogdmFyKC0td2NnLW5hdi1pbmspICFpbXBvcnRhbnQ7CiAgICAgIGZvbnQtd2VpZ2h0OiA1MDA7CiAgICAgIGZvbnQtc2l6ZTogMC45cmVtOwogICAgICBwYWRkaW5nOiAwLjQ1cmVtIDAuOXJlbSAhaW1wb3J0YW50OwogICAgICBib3JkZXItcmFkaXVzOiB2YXIoLS13Y2ctcmFkaXVzKTsKICAgICAgYm9yZGVyOiAxcHggc29saWQgdHJhbnNwYXJlbnQ7CiAgICB9CiAgICAud2NnLW5hdi1wcmltYXJ5IC5uYXYtbGluazpob3ZlciB7IGJhY2tncm91bmQ6IHJnYmEoMjU1LDI1NSwyNTUsMC43KTsgfQogICAgLndjZy1uYXYtcHJpbWFyeSAubmF2LWxpbmsuYWN0aXZlIHsKICAgICAgYmFja2dyb3VuZDogdmFyKC0td2NnLXN1cmZhY2UpOwogICAgICBib3JkZXItY29sb3I6IHZhcigtLXdjZy1saW5lKTsKICAgICAgY29sb3I6IHZhcigtLXdjZy1hY2NlbnQtaW5rKSAhaW1wb3J0YW50OwogICAgICBib3gtc2hhZG93OiB2YXIoLS13Y2ctc2hhZG93KTsKICAgIH0KICAgIC53Y2ctbW9kLWljbyB7CiAgICAgIGZvbnQtc2l6ZTogMS4wNWVtOwogICAgICBtYXJnaW4tcmlnaHQ6IDAuMTVyZW07CiAgICAgIGxpbmUtaGVpZ2h0OiAxOwogICAgfQogICAgLndjZy1uYXYtc2Vjb25kYXJ5IC5uYXYtbGluaywKICAgIC53Y2ctbmF2LXNlY29uZGFyeSAuYnRuLWxpbmsgewogICAgICBjb2xvcjogdmFyKC0td2NnLW11dGVkKSAhaW1wb3J0YW50OwogICAgICBmb250LXNpemU6IDAuODVyZW07CiAgICAgIGZvbnQtd2VpZ2h0OiA1MDA7CiAgICAgIHRleHQtZGVjb3JhdGlvbjogbm9uZTsKICAgIH0KICAgIC53Y2ctbmF2LXNlY29uZGFyeSAuZHJvcGRvd24tbWVudSB7CiAgICAgIGJvcmRlcjogMXB4IHNvbGlkIHZhcigtLXdjZy1saW5lKTsKICAgICAgYm9yZGVyLXJhZGl1czogdmFyKC0td2NnLXJhZGl1cyk7CiAgICAgIGJveC1zaGFkb3c6IHZhcigtLXdjZy1zaGFkb3cpOwogICAgICBwYWRkaW5nOiAwLjM1cmVtOwogICAgfQogICAgLndjZy1uYXYtc2Vjb25kYXJ5IC5kcm9wZG93bi1pdGVtIHsKICAgICAgYm9yZGVyLXJhZGl1czogNHB4OwogICAgICBmb250LXNpemU6IDAuODhyZW07CiAgICAgIHBhZGRpbmc6IDAuNDVyZW0gMC43NXJlbTsKICAgIH0KICAgIC53Y2ctbmF2LXNlY29uZGFyeSAuZHJvcGRvd24taXRlbTpob3ZlciB7IGJhY2tncm91bmQ6IHZhcigtLXdjZy1hY2NlbnQtc29mdCk7IH0KICAgIC5jYXJkLW1vZHVsZSB7IHRyYW5zaXRpb246IGJveC1zaGFkb3cgLjE1cyBlYXNlOyBib3JkZXI6IDFweCBzb2xpZCB2YXIoLS13Y2ctbGluZSkgIWltcG9ydGFudDsgYm9yZGVyLXJhZGl1czogdmFyKC0td2NnLXJhZGl1cykgIWltcG9ydGFudDsgYm94LXNoYWRvdzogdmFyKC0td2NnLXNoYWRvdyk7IH0KICAgIC5jYXJkLW1vZHVsZSAuY2FyZC1oZWFkZXIgewogICAgICBiYWNrZ3JvdW5kOiB2YXIoLS13Y2ctYWNjZW50LXNvZnQpOwogICAgICBjb2xvcjogdmFyKC0td2NnLWFjY2VudC1pbmspOwogICAgICBmb250LXdlaWdodDogNjAwOwogICAgICBib3JkZXItYm90dG9tOiAxcHggc29saWQgdmFyKC0td2NnLWxpbmUpOwogICAgfQogICAgLnRhYmxlLXdjZyB0aGVhZCB7IGJhY2tncm91bmQ6ICNmMGY0Zjg7IGNvbG9yOiB2YXIoLS13Y2ctYWNjZW50LWluayk7IH0KICAgIC50YWJsZS13Y2cgdGhlYWQgdGggeyBmb250LXdlaWdodDogNjAwOyBmb250LXNpemU6IC43OHJlbTsgYm9yZGVyOiBub25lOyB0ZXh0LXRyYW5zZm9ybTogdXBwZXJjYXNlOyBsZXR0ZXItc3BhY2luZzogMC4wM2VtOyB9CiAgICAuc3RhdC12YWx1ZSB7IGZvbnQtc2l6ZTogMS42NXJlbTsgZm9udC13ZWlnaHQ6IDcwMDsgY29sb3I6IHZhcigtLXdjZy1hY2NlbnQtaW5rKTsgfQogICAgLmJyZWFkY3J1bWIgeyBiYWNrZ3JvdW5kOiB0cmFuc3BhcmVudDsgcGFkZGluZy1sZWZ0OiAwOyBtYXJnaW4tYm90dG9tOiAxcmVtOyB9CiAgICBtYWluIHsgcGFkZGluZy1ib3R0b206IDNyZW07IGZsZXg6IDE7IH0KICAgIC5idG4geyBib3JkZXItcmFkaXVzOiB2YXIoLS13Y2ctcmFkaXVzKTsgZm9udC13ZWlnaHQ6IDUwMDsgfQogICAgLmJ0bi1wcmltYXJ5IHsgYmFja2dyb3VuZDogdmFyKC0td2NnLWFjY2VudC1pbmspOyBib3JkZXItY29sb3I6IHZhcigtLXdjZy1hY2NlbnQtaW5rKTsgfQogICAgLmJ0bi1vdXRsaW5lLXByaW1hcnkgeyBjb2xvcjogdmFyKC0td2NnLWFjY2VudC1pbmspOyBib3JkZXItY29sb3I6ICNiN2M5ZDg7IH0KICAgIC53Y2ctdGl0bGUtaWNvIHsKICAgICAgZGlzcGxheTogaW5saW5lLWZsZXg7CiAgICAgIGFsaWduLWl0ZW1zOiBjZW50ZXI7CiAgICAgIGp1c3RpZnktY29udGVudDogY2VudGVyOwogICAgICBmbGV4OiAwIDAgYXV0bzsKICAgICAgZm9udC1zaXplOiAxLjllbTsKICAgICAgbGluZS1oZWlnaHQ6IDE7CiAgICAgIG1hcmdpbjogMDsKICAgICAgcGFkZGluZzogMC4wNXJlbSAwLjFyZW07CiAgICAgIG9wYWNpdHk6IDAuOTI7CiAgICAgIGZpbHRlcjogc2F0dXJhdGUoMS4xMik7CiAgICAgIHVzZXItc2VsZWN0OiBub25lOwogICAgICBwb2ludGVyLWV2ZW50czogbm9uZTsKICAgIH0KICAgIC53Y2ctcmVwb3J0LWhlYWQgewogICAgICBkaXNwbGF5OiBmbGV4OwogICAgICBhbGlnbi1pdGVtczogZmxleC1zdGFydDsKICAgICAganVzdGlmeS1jb250ZW50OiBzcGFjZS1iZXR3ZWVuOwogICAgICBnYXA6IDAuNzVyZW07CiAgICAgIGZsZXg6IDEgMSBhdXRvOwogICAgICBtaW4td2lkdGg6IDA7CiAgICAgIG1hcmdpbjogMDsKICAgIH0KICAgIC53Y2ctcmVwb3J0LWhlYWQgPiBoMSwKICAgIC53Y2ctcmVwb3J0LWhlYWQgPiBoMiwKICAgIC53Y2ctcmVwb3J0LWhlYWQgPiAuaDQgewogICAgICBtYXJnaW46IDA7CiAgICAgIGZsZXg6IDEgMSBhdXRvOwogICAgICBtaW4td2lkdGg6IDA7CiAgICAgIGxpbmUtaGVpZ2h0OiAxLjI1OwogICAgfQogICAgLmJ0biB7IGJvcmRlci1yYWRpdXM6IDEwcHg7IGZvbnQtd2VpZ2h0OiA1MDA7IH0KICAgIC5idG4tcHJpbWFyeSB7IGJhY2tncm91bmQ6ICM1YTdhOTQ7IGJvcmRlci1jb2xvcjogIzVhN2E5NDsgY29sb3I6ICNmZmY7IH0KICAgIC5idG4tb3V0bGluZS1wcmltYXJ5IHsgY29sb3I6ICMzZDVhNzM7IGJhY2tncm91bmQ6ICNlNGVlZjY7IGJvcmRlci1jb2xvcjogI2M1ZDRlMjsgfQogICAgLmJ0bi1vdXRsaW5lLXNlY29uZGFyeSB7IGNvbG9yOiAjNGE1NTYyOyBiYWNrZ3JvdW5kOiAjZThlZGYyOyBib3JkZXItY29sb3I6ICNkMGQ4ZTA7IH0KICAgIC53Y2ctaG9tZS1saW5rIHsKICAgICAgYmFja2dyb3VuZDogI2ZmZmZmZiAhaW1wb3J0YW50OwogICAgICBib3JkZXItY29sb3I6ICNiN2M5ZDggIWltcG9ydGFudDsKICAgIH0KICAgIGZvb3Rlci53Y2ctZm9vdGVyIHsKICAgICAgYm9yZGVyLXRvcDogMXB4IHNvbGlkIHZhcigtLXdjZy1saW5lKTsKICAgICAgYmFja2dyb3VuZDogcmdiYSgyNTUsMjU1LDI1NSwwLjY1KTsKICAgICAgcGFkZGluZzogMC44NXJlbSAwOwogICAgICBjb2xvcjogdmFyKC0td2NnLW11dGVkKTsKICAgICAgZm9udC1zaXplOiAwLjhyZW07CiAgICB9CiAgPC9zdHlsZT4KICB7JSBibG9jayBleHRyYV9jc3MgJX17JSBlbmRibG9jayAlfQo8L2hlYWQ+Cjxib2R5PgogIDxoZWFkZXIgY2xhc3M9IndjZy10b3BiYXIgc3RpY2t5LXRvcCI+CiAgICB7JSBpbmNsdWRlICJpbmNsdWRlcy9uYXZiYXIuaHRtbCIgJX0KICA8L2hlYWRlcj4KCiAgPG1haW4gY2xhc3M9ImNvbnRhaW5lciBweS00Ij4KICAgIHslIGluY2x1ZGUgImluY2x1ZGVzL21lc3NhZ2VzLmh0bWwiICV9CiAgICB7JSBpbmNsdWRlICJpbmNsdWRlcy9icmVhZGNydW1icy5odG1sIiAlfQoKICAgIHslIGJsb2NrIGNvbnRlbnQgJX17JSBlbmRibG9jayAlfQogIDwvbWFpbj4KCiAgPGZvb3RlciBjbGFzcz0id2NnLWZvb3RlciBtdC1hdXRvIj4KICAgIDxkaXYgY2xhc3M9ImNvbnRhaW5lciI+CiAgICAgIFdDRyBPbmUg4oCUIFdvcmtpbmcgQ2FwaXRhbCBHcm91cAogICAgPC9kaXY+CiAgPC9mb290ZXI+CgogIDxzY3JpcHQgc3JjPSJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvbnBtL2Jvb3RzdHJhcEA1LjMuMy9kaXN0L2pzL2Jvb3RzdHJhcC5idW5kbGUubWluLmpzIj48L3NjcmlwdD4KICB7JSBibG9jayBleHRyYV9qcyAlfXslIGVuZGJsb2NrICV9CjwvYm9keT4KPC9odG1sPgo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
