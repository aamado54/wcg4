# CONCATENATED .HTML FILES

PART_NUMBER=1
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
PATH_LITERAL=templates/admin/base_site.html
PATH_JSON="templates/admin/base_site.html"
FILENAME=base_site.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=21
SIZE_BYTES_UTF8=551
CONTENT_SHA256=37da4e537c3b998d70a2f5d1b745094b310a81c3a368bdbe444c3cc2a5ba548f
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
{% extends "admin/base_site.html" %}

{% block nav-global %}
  {{ block.super }}
  {% if user.is_authenticated and user.is_superuser %}
    <div style="margin: 10px 0 0 0;">
      <a href="{% url 'pgc:admin_monthly' %}"
         style="
           display: inline-block;
           padding: 8px 12px;
           background: #0f766e;
           color: white;
           text-decoration: none;
           border-radius: 6px;
           font-weight: 600;
         ">
        ← Volver a la aplicación
      </a>
    </div>
  {% endif %}
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "admin/base_site.html" %}
00002|
00003|{% block nav-global %}
00004|  {{ block.super }}
00005|  {% if user.is_authenticated and user.is_superuser %}
00006|    <div style="margin: 10px 0 0 0;">
00007|      <a href="{% url 'pgc:admin_monthly' %}"
00008|         style="
00009|           display: inline-block;
00010|           padding: 8px 12px;
00011|           background: #0f766e;
00012|           color: white;
00013|           text-decoration: none;
00014|           border-radius: 6px;
00015|           font-weight: 600;
00016|         ">
00017|        ← Volver a la aplicación
00018|      </a>
00019|    </div>
00020|  {% endif %}
00021|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYWRtaW4vYmFzZV9zaXRlLmh0bWwiICV9Cgp7JSBibG9jayBuYXYtZ2xvYmFsICV9CiAge3sgYmxvY2suc3VwZXIgfX0KICB7JSBpZiB1c2VyLmlzX2F1dGhlbnRpY2F0ZWQgYW5kIHVzZXIuaXNfc3VwZXJ1c2VyICV9CiAgICA8ZGl2IHN0eWxlPSJtYXJnaW46IDEwcHggMCAwIDA7Ij4KICAgICAgPGEgaHJlZj0ieyUgdXJsICdwZ2M6YWRtaW5fbW9udGhseScgJX0iCiAgICAgICAgIHN0eWxlPSIKICAgICAgICAgICBkaXNwbGF5OiBpbmxpbmUtYmxvY2s7CiAgICAgICAgICAgcGFkZGluZzogOHB4IDEycHg7CiAgICAgICAgICAgYmFja2dyb3VuZDogIzBmNzY2ZTsKICAgICAgICAgICBjb2xvcjogd2hpdGU7CiAgICAgICAgICAgdGV4dC1kZWNvcmF0aW9uOiBub25lOwogICAgICAgICAgIGJvcmRlci1yYWRpdXM6IDZweDsKICAgICAgICAgICBmb250LXdlaWdodDogNjAwOwogICAgICAgICAiPgogICAgICAgIOKGkCBWb2x2ZXIgYSBsYSBhcGxpY2FjacOzbgogICAgICA8L2E+CiAgICA8L2Rpdj4KICB7JSBlbmRpZiAlfQp7JSBlbmRibG9jayAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/admin/change_list.html.html
PATH_JSON="templates/admin/change_list.html.html"
FILENAME=change_list.html.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=11
SIZE_BYTES_UTF8=228
CONTENT_SHA256=0a5f7d62ab68dd6d1b45a64938d703ac5c53892dc7fb0741875f0a11a8343d52
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
{% extends "admin/change_list.html" %}

{% block object-tools-items %}
  <li>
    <a href="{% url 'admin:core_systemsetting_run_recalc_ops' %}">
      Operaciones de recálculo
    </a>
  </li>
  {{ block.super }}
{% endblock %}
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "admin/change_list.html" %}
00002|
00003|{% block object-tools-items %}
00004|  <li>
00005|    <a href="{% url 'admin:core_systemsetting_run_recalc_ops' %}">
00006|      Operaciones de recálculo
00007|    </a>
00008|  </li>
00009|  {{ block.super }}
00010|{% endblock %}
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYWRtaW4vY2hhbmdlX2xpc3QuaHRtbCIgJX0KCnslIGJsb2NrIG9iamVjdC10b29scy1pdGVtcyAlfQogIDxsaT4KICAgIDxhIGhyZWY9InslIHVybCAnYWRtaW46Y29yZV9zeXN0ZW1zZXR0aW5nX3J1bl9yZWNhbGNfb3BzJyAlfSI+CiAgICAgIE9wZXJhY2lvbmVzIGRlIHJlY8OhbGN1bG8KICAgIDwvYT4KICA8L2xpPgogIHt7IGJsb2NrLnN1cGVyIH19CnslIGVuZGJsb2NrICV9
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/admin/run_recalc_ops.html
PATH_JSON="templates/admin/run_recalc_ops.html"
FILENAME=run_recalc_ops.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=20
SIZE_BYTES_UTF8=481
CONTENT_SHA256=a0866fe35292386f5b0f6698dab96fb3c30bf8fb06c3d2621d628c4ca0d6b5fa
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
{% extends "admin/base_site.html" %}

{% block content %}
  <div id="content-main">
    <form method="post">
      {% csrf_token %}

      <fieldset class="module aligned">
        <h2>Parámetros</h2>
        {{ form.as_p }}
      </fieldset>

      <div class="submit-row">
        <input type="submit" value="Ejecutar" class="default">
        <a href="{% url 'admin:core_systemsetting_changelist' %}" class="button">Cancelar</a>
      </div>
    </form>
  </div>
{% endblock %}
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "admin/base_site.html" %}
00002|
00003|{% block content %}
00004|  <div id="content-main">
00005|    <form method="post">
00006|      {% csrf_token %}
00007|
00008|      <fieldset class="module aligned">
00009|        <h2>Parámetros</h2>
00010|        {{ form.as_p }}
00011|      </fieldset>
00012|
00013|      <div class="submit-row">
00014|        <input type="submit" value="Ejecutar" class="default">
00015|        <a href="{% url 'admin:core_systemsetting_changelist' %}" class="button">Cancelar</a>
00016|      </div>
00017|    </form>
00018|  </div>
00019|{% endblock %}
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYWRtaW4vYmFzZV9zaXRlLmh0bWwiICV9Cgp7JSBibG9jayBjb250ZW50ICV9CiAgPGRpdiBpZD0iY29udGVudC1tYWluIj4KICAgIDxmb3JtIG1ldGhvZD0icG9zdCI+CiAgICAgIHslIGNzcmZfdG9rZW4gJX0KCiAgICAgIDxmaWVsZHNldCBjbGFzcz0ibW9kdWxlIGFsaWduZWQiPgogICAgICAgIDxoMj5QYXLDoW1ldHJvczwvaDI+CiAgICAgICAge3sgZm9ybS5hc19wIH19CiAgICAgIDwvZmllbGRzZXQ+CgogICAgICA8ZGl2IGNsYXNzPSJzdWJtaXQtcm93Ij4KICAgICAgICA8aW5wdXQgdHlwZT0ic3VibWl0IiB2YWx1ZT0iRWplY3V0YXIiIGNsYXNzPSJkZWZhdWx0Ij4KICAgICAgICA8YSBocmVmPSJ7JSB1cmwgJ2FkbWluOmNvcmVfc3lzdGVtc2V0dGluZ19jaGFuZ2VsaXN0JyAlfSIgY2xhc3M9ImJ1dHRvbiI+Q2FuY2VsYXI8L2E+CiAgICAgIDwvZGl2PgogICAgPC9mb3JtPgogIDwvZGl2Pgp7JSBlbmRibG9jayAlfQ==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/base.html
PATH_JSON="templates/base.html"
FILENAME=base.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=391
SIZE_BYTES_UTF8=10959
CONTENT_SHA256=5cdeddb4376d4b6cf0a557ac7718af92f179756152aafbceea542e3d68815662
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
{% load static %}
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}PGC - WCG{% endblock %}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: "DM Sans", Arial, sans-serif;
            margin: 0;
            background: #f3f6f9;
            color: #2a3441;
        }

        header {
            background: #eef3f7;
            color: #3d5a73;
            padding: 16px 24px;
            border-bottom: 1px solid #e2e8f0;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
        }

        .header-left {
            display: flex;
            align-items: center;
            gap: 18px;
            flex-wrap: wrap;
        }

        .brand-title {
            margin: 0;
            font-size: 1.35rem;
        }

        .top-nav {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .top-nav a {
            color: #3a4a5c;
            text-decoration: none;
            padding: 8px 12px;
            border-radius: 10px;
            background: #dce8f2;
            border: 1px solid #c5d4e2;
            font-weight: 500;
        }

        .top-nav a:hover {
            background: #cfdce8;
            border-color: #b7c9d8;
        }

        /* Destacado: volver al menú principal WCG (siempre claro) */
        .top-nav a.nav-menu-principal {
            background: #ffffff;
            color: #3d5a73;
            font-weight: 700;
            border: 1px solid #b7c9d8;
            box-shadow: 0 1px 2px rgba(42, 52, 65, 0.04);
        }

        .top-nav a.nav-menu-principal:hover {
            background: #ffffff;
            color: #2a3441;
        }

        .header-right {
            display: flex;
            align-items: center;
            gap: 12px;
            position: relative;
        }

        .user-badge {
            font-size: 0.92rem;
            color: #6b7a8d;
            white-space: nowrap;
        }

        .gear-wrap {
            position: relative;
        }

        .gear-btn {
            width: 42px;
            height: 42px;
            border-radius: 10px;
            border: 1px solid #c5d4e2;
            background: #dce8f2;
            color: #3d5a73;
            cursor: pointer;
            font-size: 1.2rem;
            line-height: 1;
        }

        .gear-btn:hover {
            background: #cfdce8;
        }

        .gear-menu {
            position: absolute;
            right: 0;
            top: calc(100% + 8px);
            min-width: 240px;
            background: white;
            color: #1f2937;
            border: 1px solid #d1d5db;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.14);
            display: none;
            z-index: 1000;
            overflow: hidden;
        }

        .gear-menu.open {
            display: block;
        }

        .gear-menu a,
        .gear-menu button {
            display: block;
            width: 100%;
            text-align: left;
            padding: 12px 14px;
            background: white;
            color: #1f2937;
            border: none;
            border-bottom: 1px solid #eef2f7;
            text-decoration: none;
            font-size: 0.95rem;
            cursor: pointer;
        }

        .gear-menu a:hover,
        .gear-menu button:hover {
            background: #f8fafc;
        }

        .gear-menu .menu-label {
            padding: 10px 14px;
            font-size: 0.82rem;
            font-weight: 700;
            color: #64748b;
            background: #f8fafc;
            border-bottom: 1px solid #e5e7eb;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }

        main {
            padding: 24px;
        }

        .card {
            background: white;
            border: 1px solid #d9e2ec;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        .filters {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 18px;
        }

        label {
            font-size: 0.9rem;
            font-weight: 600;
        }

        select, button {
            padding: 8px 12px;
            border: 1px solid #c5d4e2;
            border-radius: 10px;
            font-size: 0.95rem;
        }

        button {
            background: #d7e4ef;
            color: #2a3441;
            border: 1px solid #c5d4e2;
            cursor: pointer;
            border-radius: 10px;
        }

        button:hover {
            background: #c9dae8;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 8px;
        }

        th, td {
            padding: 10px 12px;
            border-bottom: 1px solid #e5e7eb;
            text-align: center;
            font-size: 0.95rem;
            vertical-align: middle;
        }

        th {
            background: #f8fafc;
            text-align: center;
        }

        th:first-child, td:first-child {
            text-align: left;
        }

        .ok {
            color: #166534;
            font-weight: 700;
        }

        .bad {
            color: #b91c1c;
            font-weight: 700;
        }

        .muted {
            color: #64748b;
        }

        /* Cabecera de reporte: título izquierda, emoji derecha (sin empujar abajo) */
        .wcg-report-head {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 0.75rem;
            margin: 0 0 0.35rem;
        }
        .wcg-report-head > h1,
        .wcg-report-head > h2,
        .wcg-report-head > .h4 {
            margin: 0;
            flex: 1 1 auto;
            min-width: 0;
            line-height: 1.25;
        }
        .wcg-title-ico {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            flex: 0 0 auto;
            font-size: 1.85em;
            line-height: 1;
            margin: 0;
            padding: 0.1rem 0.15rem;
            opacity: 0.92;
            filter: saturate(1.12);
            user-select: none;
            pointer-events: none;
        }

        tbody tr:hover {
            background: #f8fafc;
        }

        @media (max-width: 900px) {
            .header-row {
                flex-direction: column;
                align-items: stretch;
            }

            .header-left,
            .header-right {
                justify-content: space-between;
            }

            .top-nav {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="container header-row">
            <div class="header-left">
                <h1 class="brand-title">PGC - Working Capital Group</h1>

                {% if user.is_authenticated %}
                <nav class="top-nav">
                    <a href="{% url 'portal:home' %}" class="nav-menu-principal">Menú principal</a>
                    <a href="{% url 'pgc:dashboard' %}">Tablero</a>
                    <a href="{% url 'pgc:ingresos' %}">Ingresos vs meta</a>
                    <a href="{% url 'pgc:clientes_nuevos' %}">Clientes</a>
                    <a href="{% url 'pgc:venta_cruzada' %}">Venta cruzada</a>
                    <a href="{% url 'pgc:respuesta_reqs' %}">Respuesta reqs</a>
                  <a href="{% static 'docs/WCG-PGC.pdf' %}" target="_blank" rel="noopener noreferrer">Ayuda</a>
                </nav>
                {% endif %}
            </div>

            {% if user.is_authenticated %}
            <div class="header-right">
                <div class="user-badge">
                    {{ user.username }}
                </div>

                <div class="gear-wrap">
                    <button type="button" class="gear-btn" id="gear-btn" aria-label="Abrir opciones">⚙</button>

                    <div class="gear-menu" id="gear-menu">
                        <div class="menu-label">Sesión</div>
                        <form method="post" action="{% url 'logout' %}">
                            {% csrf_token %}
                            <button type="submit">Cambiar de usuario</button>
                        </form>

                        {% if user.is_superuser %}
                            <div class="menu-label">Administración</div>
                            <a href="{% url 'imports:import_hub' %}">Importación General</a>
                            <a href="{% url 'pgc:admin_monthly' %}">Admin PGC (período)</a>
                        {% endif %}
                    </div>
                </div>
            </div>
            {% endif %}
        </div>
    </header>

    <main>

        {% if messages %}
          <div style="margin:16px 0;">
            {% for message in messages %}
              <div style="padding:12px 14px; border-radius:8px; margin-bottom:10px;{% if message.tags == 'error' %} background:#fef2f2; border:1px solid #fecaca; color:#991b1b;{% elif message.tags == 'warning' %} background:#fffbeb; border:1px solid #fde68a; color:#92400e;{% elif message.tags == 'info' %} background:#eff6ff; border:1px solid #bfdbfe; color:#1e40af;{% else %} background:#ecfdf5; border:1px solid #a7f3d0; color:#065f46;{% endif %}">
                {{ message }}
              </div>
            {% endfor %}
          </div>
        {% endif %}
      
        <div class="container">
            {% block content %}{% endblock %}
        </div>
    </main>

    {% if user.is_authenticated %}
    <script>
        (function () {
            const btn = document.getElementById("gear-btn");
            const menu = document.getElementById("gear-menu");
            if (!btn || !menu) return;

            btn.addEventListener("click", function (e) {
                e.stopPropagation();
                menu.classList.toggle("open");
            });

            document.addEventListener("click", function (e) {
                if (!menu.contains(e.target) && !btn.contains(e.target)) {
                    menu.classList.remove("open");
                }
            });

            document.addEventListener("keydown", function (e) {
                if (e.key === "Escape") {
                    menu.classList.remove("open");
                }
            });
        })();
    </script>
    {% endif %}
</body>
</html>
~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% load static %}
00002|<!DOCTYPE html>
00003|<html lang="es">
00004|<head>
00005|    <meta charset="UTF-8">
00006|    <title>{% block title %}PGC - WCG{% endblock %}</title>
00007|    <link rel="preconnect" href="https://fonts.googleapis.com">
00008|    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
00009|    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap" rel="stylesheet">
00010|    <style>
00011|        body {
00012|            font-family: "DM Sans", Arial, sans-serif;
00013|            margin: 0;
00014|            background: #f3f6f9;
00015|            color: #2a3441;
00016|        }
00017|
00018|        header {
00019|            background: #eef3f7;
00020|            color: #3d5a73;
00021|            padding: 16px 24px;
00022|            border-bottom: 1px solid #e2e8f0;
00023|        }
00024|
00025|        .container {
00026|            max-width: 1200px;
00027|            margin: 0 auto;
00028|        }
00029|
00030|        .header-row {
00031|            display: flex;
00032|            align-items: center;
00033|            justify-content: space-between;
00034|            gap: 16px;
00035|        }
00036|
00037|        .header-left {
00038|            display: flex;
00039|            align-items: center;
00040|            gap: 18px;
00041|            flex-wrap: wrap;
00042|        }
00043|
00044|        .brand-title {
00045|            margin: 0;
00046|            font-size: 1.35rem;
00047|        }
00048|
00049|        .top-nav {
00050|            display: flex;
00051|            flex-wrap: wrap;
00052|            gap: 10px;
00053|        }
00054|
00055|        .top-nav a {
00056|            color: #3a4a5c;
00057|            text-decoration: none;
00058|            padding: 8px 12px;
00059|            border-radius: 10px;
00060|            background: #dce8f2;
00061|            border: 1px solid #c5d4e2;
00062|            font-weight: 500;
00063|        }
00064|
00065|        .top-nav a:hover {
00066|            background: #cfdce8;
00067|            border-color: #b7c9d8;
00068|        }
00069|
00070|        /* Destacado: volver al menú principal WCG (siempre claro) */
00071|        .top-nav a.nav-menu-principal {
00072|            background: #ffffff;
00073|            color: #3d5a73;
00074|            font-weight: 700;
00075|            border: 1px solid #b7c9d8;
00076|            box-shadow: 0 1px 2px rgba(42, 52, 65, 0.04);
00077|        }
00078|
00079|        .top-nav a.nav-menu-principal:hover {
00080|            background: #ffffff;
00081|            color: #2a3441;
00082|        }
00083|
00084|        .header-right {
00085|            display: flex;
00086|            align-items: center;
00087|            gap: 12px;
00088|            position: relative;
00089|        }
00090|
00091|        .user-badge {
00092|            font-size: 0.92rem;
00093|            color: #6b7a8d;
00094|            white-space: nowrap;
00095|        }
00096|
00097|        .gear-wrap {
00098|            position: relative;
00099|        }
00100|
00101|        .gear-btn {
00102|            width: 42px;
00103|            height: 42px;
00104|            border-radius: 10px;
00105|            border: 1px solid #c5d4e2;
00106|            background: #dce8f2;
00107|            color: #3d5a73;
00108|            cursor: pointer;
00109|            font-size: 1.2rem;
00110|            line-height: 1;
00111|        }
00112|
00113|        .gear-btn:hover {
00114|            background: #cfdce8;
00115|        }
00116|
00117|        .gear-menu {
00118|            position: absolute;
00119|            right: 0;
00120|            top: calc(100% + 8px);
00121|            min-width: 240px;
00122|            background: white;
00123|            color: #1f2937;
00124|            border: 1px solid #d1d5db;
00125|            border-radius: 10px;
00126|            box-shadow: 0 10px 30px rgba(0,0,0,0.14);
00127|            display: none;
00128|            z-index: 1000;
00129|            overflow: hidden;
00130|        }
00131|
00132|        .gear-menu.open {
00133|            display: block;
00134|        }
00135|
00136|        .gear-menu a,
00137|        .gear-menu button {
00138|            display: block;
00139|            width: 100%;
00140|            text-align: left;
00141|            padding: 12px 14px;
00142|            background: white;
00143|            color: #1f2937;
00144|            border: none;
00145|            border-bottom: 1px solid #eef2f7;
00146|            text-decoration: none;
00147|            font-size: 0.95rem;
00148|            cursor: pointer;
00149|        }
00150|
00151|        .gear-menu a:hover,
00152|        .gear-menu button:hover {
00153|            background: #f8fafc;
00154|        }
00155|
00156|        .gear-menu .menu-label {
00157|            padding: 10px 14px;
00158|            font-size: 0.82rem;
00159|            font-weight: 700;
00160|            color: #64748b;
00161|            background: #f8fafc;
00162|            border-bottom: 1px solid #e5e7eb;
00163|            text-transform: uppercase;
00164|            letter-spacing: 0.03em;
00165|        }
00166|
00167|        main {
00168|            padding: 24px;
00169|        }
00170|
00171|        .card {
00172|            background: white;
00173|            border: 1px solid #d9e2ec;
00174|            border-radius: 8px;
00175|            padding: 20px;
00176|            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
00177|        }
00178|
00179|        .filters {
00180|            display: flex;
00181|            gap: 12px;
00182|            flex-wrap: wrap;
00183|            margin-bottom: 18px;
00184|        }
00185|
00186|        label {
00187|            font-size: 0.9rem;
00188|            font-weight: 600;
00189|        }
00190|
00191|        select, button {
00192|            padding: 8px 12px;
00193|            border: 1px solid #c5d4e2;
00194|            border-radius: 10px;
00195|            font-size: 0.95rem;
00196|        }
00197|
00198|        button {
00199|            background: #d7e4ef;
00200|            color: #2a3441;
00201|            border: 1px solid #c5d4e2;
00202|            cursor: pointer;
00203|            border-radius: 10px;
00204|        }
00205|
00206|        button:hover {
00207|            background: #c9dae8;
00208|        }
00209|
00210|        table {
00211|            width: 100%;
00212|            border-collapse: collapse;
00213|            margin-top: 8px;
00214|        }
00215|
00216|        th, td {
00217|            padding: 10px 12px;
00218|            border-bottom: 1px solid #e5e7eb;
00219|            text-align: center;
00220|            font-size: 0.95rem;
00221|            vertical-align: middle;
00222|        }
00223|
00224|        th {
00225|            background: #f8fafc;
00226|            text-align: center;
00227|        }
00228|
00229|        th:first-child, td:first-child {
00230|            text-align: left;
00231|        }
00232|
00233|        .ok {
00234|            color: #166534;
00235|            font-weight: 700;
00236|        }
00237|
00238|        .bad {
00239|            color: #b91c1c;
00240|            font-weight: 700;
00241|        }
00242|
00243|        .muted {
00244|            color: #64748b;
00245|        }
00246|
00247|        /* Cabecera de reporte: título izquierda, emoji derecha (sin empujar abajo) */
00248|        .wcg-report-head {
00249|            display: flex;
00250|            align-items: flex-start;
00251|            justify-content: space-between;
00252|            gap: 0.75rem;
00253|            margin: 0 0 0.35rem;
00254|        }
00255|        .wcg-report-head > h1,
00256|        .wcg-report-head > h2,
00257|        .wcg-report-head > .h4 {
00258|            margin: 0;
00259|            flex: 1 1 auto;
00260|            min-width: 0;
00261|            line-height: 1.25;
00262|        }
00263|        .wcg-title-ico {
00264|            display: inline-flex;
00265|            align-items: center;
00266|            justify-content: center;
00267|            flex: 0 0 auto;
00268|            font-size: 1.85em;
00269|            line-height: 1;
00270|            margin: 0;
00271|            padding: 0.1rem 0.15rem;
00272|            opacity: 0.92;
00273|            filter: saturate(1.12);
00274|            user-select: none;
00275|            pointer-events: none;
00276|        }
00277|
00278|        tbody tr:hover {
00279|            background: #f8fafc;
00280|        }
00281|
00282|        @media (max-width: 900px) {
00283|            .header-row {
00284|                flex-direction: column;
00285|                align-items: stretch;
00286|            }
00287|
00288|            .header-left,
00289|            .header-right {
00290|                justify-content: space-between;
00291|            }
00292|
00293|            .top-nav {
00294|                width: 100%;
00295|            }
00296|        }
00297|    </style>
00298|</head>
00299|<body>
00300|    <header>
00301|        <div class="container header-row">
00302|            <div class="header-left">
00303|                <h1 class="brand-title">PGC - Working Capital Group</h1>
00304|
00305|                {% if user.is_authenticated %}
00306|                <nav class="top-nav">
00307|                    <a href="{% url 'portal:home' %}" class="nav-menu-principal">Menú principal</a>
00308|                    <a href="{% url 'pgc:dashboard' %}">Tablero</a>
00309|                    <a href="{% url 'pgc:ingresos' %}">Ingresos vs meta</a>
00310|                    <a href="{% url 'pgc:clientes_nuevos' %}">Clientes</a>
00311|                    <a href="{% url 'pgc:venta_cruzada' %}">Venta cruzada</a>
00312|                    <a href="{% url 'pgc:respuesta_reqs' %}">Respuesta reqs</a>
00313|                  <a href="{% static 'docs/WCG-PGC.pdf' %}" target="_blank" rel="noopener noreferrer">Ayuda</a>
00314|                </nav>
00315|                {% endif %}
00316|            </div>
00317|
00318|            {% if user.is_authenticated %}
00319|            <div class="header-right">
00320|                <div class="user-badge">
00321|                    {{ user.username }}
00322|                </div>
00323|
00324|                <div class="gear-wrap">
00325|                    <button type="button" class="gear-btn" id="gear-btn" aria-label="Abrir opciones">⚙</button>
00326|
00327|                    <div class="gear-menu" id="gear-menu">
00328|                        <div class="menu-label">Sesión</div>
00329|                        <form method="post" action="{% url 'logout' %}">
00330|                            {% csrf_token %}
00331|                            <button type="submit">Cambiar de usuario</button>
00332|                        </form>
00333|
00334|                        {% if user.is_superuser %}
00335|                            <div class="menu-label">Administración</div>
00336|                            <a href="{% url 'imports:import_hub' %}">Importación General</a>
00337|                            <a href="{% url 'pgc:admin_monthly' %}">Admin PGC (período)</a>
00338|                        {% endif %}
00339|                    </div>
00340|                </div>
00341|            </div>
00342|            {% endif %}
00343|        </div>
00344|    </header>
00345|
00346|    <main>
00347|
00348|        {% if messages %}
00349|          <div style="margin:16px 0;">
00350|            {% for message in messages %}
00351|              <div style="padding:12px 14px; border-radius:8px; margin-bottom:10px;{% if message.tags == 'error' %} background:#fef2f2; border:1px solid #fecaca; color:#991b1b;{% elif message.tags == 'warning' %} background:#fffbeb; border:1px solid #fde68a; color:#92400e;{% elif message.tags == 'info' %} background:#eff6ff; border:1px solid #bfdbfe; color:#1e40af;{% else %} background:#ecfdf5; border:1px solid #a7f3d0; color:#065f46;{% endif %}">
00352|                {{ message }}
00353|              </div>
00354|            {% endfor %}
00355|          </div>
00356|        {% endif %}
00357|      
00358|        <div class="container">
00359|            {% block content %}{% endblock %}
00360|        </div>
00361|    </main>
00362|
00363|    {% if user.is_authenticated %}
00364|    <script>
00365|        (function () {
00366|            const btn = document.getElementById("gear-btn");
00367|            const menu = document.getElementById("gear-menu");
00368|            if (!btn || !menu) return;
00369|
00370|            btn.addEventListener("click", function (e) {
00371|                e.stopPropagation();
00372|                menu.classList.toggle("open");
00373|            });
00374|
00375|            document.addEventListener("click", function (e) {
00376|                if (!menu.contains(e.target) && !btn.contains(e.target)) {
00377|                    menu.classList.remove("open");
00378|                }
00379|            });
00380|
00381|            document.addEventListener("keydown", function (e) {
00382|                if (e.key === "Escape") {
00383|                    menu.classList.remove("open");
00384|                }
00385|            });
00386|        })();
00387|    </script>
00388|    {% endif %}
00389|</body>
00390|</html>
CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgbG9hZCBzdGF0aWMgJX0KPCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVzIj4KPGhlYWQ+CiAgICA8bWV0YSBjaGFyc2V0PSJVVEYtOCI+CiAgICA8dGl0bGU+eyUgYmxvY2sgdGl0bGUgJX1QR0MgLSBXQ0d7JSBlbmRibG9jayAlfTwvdGl0bGU+CiAgICA8bGluayByZWw9InByZWNvbm5lY3QiIGhyZWY9Imh0dHBzOi8vZm9udHMuZ29vZ2xlYXBpcy5jb20iPgogICAgPGxpbmsgcmVsPSJwcmVjb25uZWN0IiBocmVmPSJodHRwczovL2ZvbnRzLmdzdGF0aWMuY29tIiBjcm9zc29yaWdpbj4KICAgIDxsaW5rIGhyZWY9Imh0dHBzOi8vZm9udHMuZ29vZ2xlYXBpcy5jb20vY3NzMj9mYW1pbHk9RE0rU2FuczppdGFsLG9wc3osd2dodEAwLDkuLjQwLDQwMDswLDkuLjQwLDUwMDswLDkuLjQwLDYwMDswLDkuLjQwLDcwMDsxLDkuLjQwLDQwMCZkaXNwbGF5PXN3YXAiIHJlbD0ic3R5bGVzaGVldCI+CiAgICA8c3R5bGU+CiAgICAgICAgYm9keSB7CiAgICAgICAgICAgIGZvbnQtZmFtaWx5OiAiRE0gU2FucyIsIEFyaWFsLCBzYW5zLXNlcmlmOwogICAgICAgICAgICBtYXJnaW46IDA7CiAgICAgICAgICAgIGJhY2tncm91bmQ6ICNmM2Y2Zjk7CiAgICAgICAgICAgIGNvbG9yOiAjMmEzNDQxOwogICAgICAgIH0KCiAgICAgICAgaGVhZGVyIHsKICAgICAgICAgICAgYmFja2dyb3VuZDogI2VlZjNmNzsKICAgICAgICAgICAgY29sb3I6ICMzZDVhNzM7CiAgICAgICAgICAgIHBhZGRpbmc6IDE2cHggMjRweDsKICAgICAgICAgICAgYm9yZGVyLWJvdHRvbTogMXB4IHNvbGlkICNlMmU4ZjA7CiAgICAgICAgfQoKICAgICAgICAuY29udGFpbmVyIHsKICAgICAgICAgICAgbWF4LXdpZHRoOiAxMjAwcHg7CiAgICAgICAgICAgIG1hcmdpbjogMCBhdXRvOwogICAgICAgIH0KCiAgICAgICAgLmhlYWRlci1yb3cgewogICAgICAgICAgICBkaXNwbGF5OiBmbGV4OwogICAgICAgICAgICBhbGlnbi1pdGVtczogY2VudGVyOwogICAgICAgICAgICBqdXN0aWZ5LWNvbnRlbnQ6IHNwYWNlLWJldHdlZW47CiAgICAgICAgICAgIGdhcDogMTZweDsKICAgICAgICB9CgogICAgICAgIC5oZWFkZXItbGVmdCB7CiAgICAgICAgICAgIGRpc3BsYXk6IGZsZXg7CiAgICAgICAgICAgIGFsaWduLWl0ZW1zOiBjZW50ZXI7CiAgICAgICAgICAgIGdhcDogMThweDsKICAgICAgICAgICAgZmxleC13cmFwOiB3cmFwOwogICAgICAgIH0KCiAgICAgICAgLmJyYW5kLXRpdGxlIHsKICAgICAgICAgICAgbWFyZ2luOiAwOwogICAgICAgICAgICBmb250LXNpemU6IDEuMzVyZW07CiAgICAgICAgfQoKICAgICAgICAudG9wLW5hdiB7CiAgICAgICAgICAgIGRpc3BsYXk6IGZsZXg7CiAgICAgICAgICAgIGZsZXgtd3JhcDogd3JhcDsKICAgICAgICAgICAgZ2FwOiAxMHB4OwogICAgICAgIH0KCiAgICAgICAgLnRvcC1uYXYgYSB7CiAgICAgICAgICAgIGNvbG9yOiAjM2E0YTVjOwogICAgICAgICAgICB0ZXh0LWRlY29yYXRpb246IG5vbmU7CiAgICAgICAgICAgIHBhZGRpbmc6IDhweCAxMnB4OwogICAgICAgICAgICBib3JkZXItcmFkaXVzOiAxMHB4OwogICAgICAgICAgICBiYWNrZ3JvdW5kOiAjZGNlOGYyOwogICAgICAgICAgICBib3JkZXI6IDFweCBzb2xpZCAjYzVkNGUyOwogICAgICAgICAgICBmb250LXdlaWdodDogNTAwOwogICAgICAgIH0KCiAgICAgICAgLnRvcC1uYXYgYTpob3ZlciB7CiAgICAgICAgICAgIGJhY2tncm91bmQ6ICNjZmRjZTg7CiAgICAgICAgICAgIGJvcmRlci1jb2xvcjogI2I3YzlkODsKICAgICAgICB9CgogICAgICAgIC8qIERlc3RhY2Fkbzogdm9sdmVyIGFsIG1lbsO6IHByaW5jaXBhbCBXQ0cgKHNpZW1wcmUgY2xhcm8pICovCiAgICAgICAgLnRvcC1uYXYgYS5uYXYtbWVudS1wcmluY2lwYWwgewogICAgICAgICAgICBiYWNrZ3JvdW5kOiAjZmZmZmZmOwogICAgICAgICAgICBjb2xvcjogIzNkNWE3MzsKICAgICAgICAgICAgZm9udC13ZWlnaHQ6IDcwMDsKICAgICAgICAgICAgYm9yZGVyOiAxcHggc29saWQgI2I3YzlkODsKICAgICAgICAgICAgYm94LXNoYWRvdzogMCAxcHggMnB4IHJnYmEoNDIsIDUyLCA2NSwgMC4wNCk7CiAgICAgICAgfQoKICAgICAgICAudG9wLW5hdiBhLm5hdi1tZW51LXByaW5jaXBhbDpob3ZlciB7CiAgICAgICAgICAgIGJhY2tncm91bmQ6ICNmZmZmZmY7CiAgICAgICAgICAgIGNvbG9yOiAjMmEzNDQxOwogICAgICAgIH0KCiAgICAgICAgLmhlYWRlci1yaWdodCB7CiAgICAgICAgICAgIGRpc3BsYXk6IGZsZXg7CiAgICAgICAgICAgIGFsaWduLWl0ZW1zOiBjZW50ZXI7CiAgICAgICAgICAgIGdhcDogMTJweDsKICAgICAgICAgICAgcG9zaXRpb246IHJlbGF0aXZlOwogICAgICAgIH0KCiAgICAgICAgLnVzZXItYmFkZ2UgewogICAgICAgICAgICBmb250LXNpemU6IDAuOTJyZW07CiAgICAgICAgICAgIGNvbG9yOiAjNmI3YThkOwogICAgICAgICAgICB3aGl0ZS1zcGFjZTogbm93cmFwOwogICAgICAgIH0KCiAgICAgICAgLmdlYXItd3JhcCB7CiAgICAgICAgICAgIHBvc2l0aW9uOiByZWxhdGl2ZTsKICAgICAgICB9CgogICAgICAgIC5nZWFyLWJ0biB7CiAgICAgICAgICAgIHdpZHRoOiA0MnB4OwogICAgICAgICAgICBoZWlnaHQ6IDQycHg7CiAgICAgICAgICAgIGJvcmRlci1yYWRpdXM6IDEwcHg7CiAgICAgICAgICAgIGJvcmRlcjogMXB4IHNvbGlkICNjNWQ0ZTI7CiAgICAgICAgICAgIGJhY2tncm91bmQ6ICNkY2U4ZjI7CiAgICAgICAgICAgIGNvbG9yOiAjM2Q1YTczOwogICAgICAgICAgICBjdXJzb3I6IHBvaW50ZXI7CiAgICAgICAgICAgIGZvbnQtc2l6ZTogMS4ycmVtOwogICAgICAgICAgICBsaW5lLWhlaWdodDogMTsKICAgICAgICB9CgogICAgICAgIC5nZWFyLWJ0bjpob3ZlciB7CiAgICAgICAgICAgIGJhY2tncm91bmQ6ICNjZmRjZTg7CiAgICAgICAgfQoKICAgICAgICAuZ2Vhci1tZW51IHsKICAgICAgICAgICAgcG9zaXRpb246IGFic29sdXRlOwogICAgICAgICAgICByaWdodDogMDsKICAgICAgICAgICAgdG9wOiBjYWxjKDEwMCUgKyA4cHgpOwogICAgICAgICAgICBtaW4td2lkdGg6IDI0MHB4OwogICAgICAgICAgICBiYWNrZ3JvdW5kOiB3aGl0ZTsKICAgICAgICAgICAgY29sb3I6ICMxZjI5Mzc7CiAgICAgICAgICAgIGJvcmRlcjogMXB4IHNvbGlkICNkMWQ1ZGI7CiAgICAgICAgICAgIGJvcmRlci1yYWRpdXM6IDEwcHg7CiAgICAgICAgICAgIGJveC1zaGFkb3c6IDAgMTBweCAzMHB4IHJnYmEoMCwwLDAsMC4xNCk7CiAgICAgICAgICAgIGRpc3BsYXk6IG5vbmU7CiAgICAgICAgICAgIHotaW5kZXg6IDEwMDA7CiAgICAgICAgICAgIG92ZXJmbG93OiBoaWRkZW47CiAgICAgICAgfQoKICAgICAgICAuZ2Vhci1tZW51Lm9wZW4gewogICAgICAgICAgICBkaXNwbGF5OiBibG9jazsKICAgICAgICB9CgogICAgICAgIC5nZWFyLW1lbnUgYSwKICAgICAgICAuZ2Vhci1tZW51IGJ1dHRvbiB7CiAgICAgICAgICAgIGRpc3BsYXk6IGJsb2NrOwogICAgICAgICAgICB3aWR0aDogMTAwJTsKICAgICAgICAgICAgdGV4dC1hbGlnbjogbGVmdDsKICAgICAgICAgICAgcGFkZGluZzogMTJweCAxNHB4OwogICAgICAgICAgICBiYWNrZ3JvdW5kOiB3aGl0ZTsKICAgICAgICAgICAgY29sb3I6ICMxZjI5Mzc7CiAgICAgICAgICAgIGJvcmRlcjogbm9uZTsKICAgICAgICAgICAgYm9yZGVyLWJvdHRvbTogMXB4IHNvbGlkICNlZWYyZjc7CiAgICAgICAgICAgIHRleHQtZGVjb3JhdGlvbjogbm9uZTsKICAgICAgICAgICAgZm9udC1zaXplOiAwLjk1cmVtOwogICAgICAgICAgICBjdXJzb3I6IHBvaW50ZXI7CiAgICAgICAgfQoKICAgICAgICAuZ2Vhci1tZW51IGE6aG92ZXIsCiAgICAgICAgLmdlYXItbWVudSBidXR0b246aG92ZXIgewogICAgICAgICAgICBiYWNrZ3JvdW5kOiAjZjhmYWZjOwogICAgICAgIH0KCiAgICAgICAgLmdlYXItbWVudSAubWVudS1sYWJlbCB7CiAgICAgICAgICAgIHBhZGRpbmc6IDEwcHggMTRweDsKICAgICAgICAgICAgZm9udC1zaXplOiAwLjgycmVtOwogICAgICAgICAgICBmb250LXdlaWdodDogNzAwOwogICAgICAgICAgICBjb2xvcjogIzY0NzQ4YjsKICAgICAgICAgICAgYmFja2dyb3VuZDogI2Y4ZmFmYzsKICAgICAgICAgICAgYm9yZGVyLWJvdHRvbTogMXB4IHNvbGlkICNlNWU3ZWI7CiAgICAgICAgICAgIHRleHQtdHJhbnNmb3JtOiB1cHBlcmNhc2U7CiAgICAgICAgICAgIGxldHRlci1zcGFjaW5nOiAwLjAzZW07CiAgICAgICAgfQoKICAgICAgICBtYWluIHsKICAgICAgICAgICAgcGFkZGluZzogMjRweDsKICAgICAgICB9CgogICAgICAgIC5jYXJkIHsKICAgICAgICAgICAgYmFja2dyb3VuZDogd2hpdGU7CiAgICAgICAgICAgIGJvcmRlcjogMXB4IHNvbGlkICNkOWUyZWM7CiAgICAgICAgICAgIGJvcmRlci1yYWRpdXM6IDhweDsKICAgICAgICAgICAgcGFkZGluZzogMjBweDsKICAgICAgICAgICAgYm94LXNoYWRvdzogMCAycHggOHB4IHJnYmEoMCwwLDAsMC4wNSk7CiAgICAgICAgfQoKICAgICAgICAuZmlsdGVycyB7CiAgICAgICAgICAgIGRpc3BsYXk6IGZsZXg7CiAgICAgICAgICAgIGdhcDogMTJweDsKICAgICAgICAgICAgZmxleC13cmFwOiB3cmFwOwogICAgICAgICAgICBtYXJnaW4tYm90dG9tOiAxOHB4OwogICAgICAgIH0KCiAgICAgICAgbGFiZWwgewogICAgICAgICAgICBmb250LXNpemU6IDAuOXJlbTsKICAgICAgICAgICAgZm9udC13ZWlnaHQ6IDYwMDsKICAgICAgICB9CgogICAgICAgIHNlbGVjdCwgYnV0dG9uIHsKICAgICAgICAgICAgcGFkZGluZzogOHB4IDEycHg7CiAgICAgICAgICAgIGJvcmRlcjogMXB4IHNvbGlkICNjNWQ0ZTI7CiAgICAgICAgICAgIGJvcmRlci1yYWRpdXM6IDEwcHg7CiAgICAgICAgICAgIGZvbnQtc2l6ZTogMC45NXJlbTsKICAgICAgICB9CgogICAgICAgIGJ1dHRvbiB7CiAgICAgICAgICAgIGJhY2tncm91bmQ6ICNkN2U0ZWY7CiAgICAgICAgICAgIGNvbG9yOiAjMmEzNDQxOwogICAgICAgICAgICBib3JkZXI6IDFweCBzb2xpZCAjYzVkNGUyOwogICAgICAgICAgICBjdXJzb3I6IHBvaW50ZXI7CiAgICAgICAgICAgIGJvcmRlci1yYWRpdXM6IDEwcHg7CiAgICAgICAgfQoKICAgICAgICBidXR0b246aG92ZXIgewogICAgICAgICAgICBiYWNrZ3JvdW5kOiAjYzlkYWU4OwogICAgICAgIH0KCiAgICAgICAgdGFibGUgewogICAgICAgICAgICB3aWR0aDogMTAwJTsKICAgICAgICAgICAgYm9yZGVyLWNvbGxhcHNlOiBjb2xsYXBzZTsKICAgICAgICAgICAgbWFyZ2luLXRvcDogOHB4OwogICAgICAgIH0KCiAgICAgICAgdGgsIHRkIHsKICAgICAgICAgICAgcGFkZGluZzogMTBweCAxMnB4OwogICAgICAgICAgICBib3JkZXItYm90dG9tOiAxcHggc29saWQgI2U1ZTdlYjsKICAgICAgICAgICAgdGV4dC1hbGlnbjogY2VudGVyOwogICAgICAgICAgICBmb250LXNpemU6IDAuOTVyZW07CiAgICAgICAgICAgIHZlcnRpY2FsLWFsaWduOiBtaWRkbGU7CiAgICAgICAgfQoKICAgICAgICB0aCB7CiAgICAgICAgICAgIGJhY2tncm91bmQ6ICNmOGZhZmM7CiAgICAgICAgICAgIHRleHQtYWxpZ246IGNlbnRlcjsKICAgICAgICB9CgogICAgICAgIHRoOmZpcnN0LWNoaWxkLCB0ZDpmaXJzdC1jaGlsZCB7CiAgICAgICAgICAgIHRleHQtYWxpZ246IGxlZnQ7CiAgICAgICAgfQoKICAgICAgICAub2sgewogICAgICAgICAgICBjb2xvcjogIzE2NjUzNDsKICAgICAgICAgICAgZm9udC13ZWlnaHQ6IDcwMDsKICAgICAgICB9CgogICAgICAgIC5iYWQgewogICAgICAgICAgICBjb2xvcjogI2I5MWMxYzsKICAgICAgICAgICAgZm9udC13ZWlnaHQ6IDcwMDsKICAgICAgICB9CgogICAgICAgIC5tdXRlZCB7CiAgICAgICAgICAgIGNvbG9yOiAjNjQ3NDhiOwogICAgICAgIH0KCiAgICAgICAgLyogQ2FiZWNlcmEgZGUgcmVwb3J0ZTogdMOtdHVsbyBpenF1aWVyZGEsIGVtb2ppIGRlcmVjaGEgKHNpbiBlbXB1amFyIGFiYWpvKSAqLwogICAgICAgIC53Y2ctcmVwb3J0LWhlYWQgewogICAgICAgICAgICBkaXNwbGF5OiBmbGV4OwogICAgICAgICAgICBhbGlnbi1pdGVtczogZmxleC1zdGFydDsKICAgICAgICAgICAganVzdGlmeS1jb250ZW50OiBzcGFjZS1iZXR3ZWVuOwogICAgICAgICAgICBnYXA6IDAuNzVyZW07CiAgICAgICAgICAgIG1hcmdpbjogMCAwIDAuMzVyZW07CiAgICAgICAgfQogICAgICAgIC53Y2ctcmVwb3J0LWhlYWQgPiBoMSwKICAgICAgICAud2NnLXJlcG9ydC1oZWFkID4gaDIsCiAgICAgICAgLndjZy1yZXBvcnQtaGVhZCA+IC5oNCB7CiAgICAgICAgICAgIG1hcmdpbjogMDsKICAgICAgICAgICAgZmxleDogMSAxIGF1dG87CiAgICAgICAgICAgIG1pbi13aWR0aDogMDsKICAgICAgICAgICAgbGluZS1oZWlnaHQ6IDEuMjU7CiAgICAgICAgfQogICAgICAgIC53Y2ctdGl0bGUtaWNvIHsKICAgICAgICAgICAgZGlzcGxheTogaW5saW5lLWZsZXg7CiAgICAgICAgICAgIGFsaWduLWl0ZW1zOiBjZW50ZXI7CiAgICAgICAgICAgIGp1c3RpZnktY29udGVudDogY2VudGVyOwogICAgICAgICAgICBmbGV4OiAwIDAgYXV0bzsKICAgICAgICAgICAgZm9udC1zaXplOiAxLjg1ZW07CiAgICAgICAgICAgIGxpbmUtaGVpZ2h0OiAxOwogICAgICAgICAgICBtYXJnaW46IDA7CiAgICAgICAgICAgIHBhZGRpbmc6IDAuMXJlbSAwLjE1cmVtOwogICAgICAgICAgICBvcGFjaXR5OiAwLjkyOwogICAgICAgICAgICBmaWx0ZXI6IHNhdHVyYXRlKDEuMTIpOwogICAgICAgICAgICB1c2VyLXNlbGVjdDogbm9uZTsKICAgICAgICAgICAgcG9pbnRlci1ldmVudHM6IG5vbmU7CiAgICAgICAgfQoKICAgICAgICB0Ym9keSB0cjpob3ZlciB7CiAgICAgICAgICAgIGJhY2tncm91bmQ6ICNmOGZhZmM7CiAgICAgICAgfQoKICAgICAgICBAbWVkaWEgKG1heC13aWR0aDogOTAwcHgpIHsKICAgICAgICAgICAgLmhlYWRlci1yb3cgewogICAgICAgICAgICAgICAgZmxleC1kaXJlY3Rpb246IGNvbHVtbjsKICAgICAgICAgICAgICAgIGFsaWduLWl0ZW1zOiBzdHJldGNoOwogICAgICAgICAgICB9CgogICAgICAgICAgICAuaGVhZGVyLWxlZnQsCiAgICAgICAgICAgIC5oZWFkZXItcmlnaHQgewogICAgICAgICAgICAgICAganVzdGlmeS1jb250ZW50OiBzcGFjZS1iZXR3ZWVuOwogICAgICAgICAgICB9CgogICAgICAgICAgICAudG9wLW5hdiB7CiAgICAgICAgICAgICAgICB3aWR0aDogMTAwJTsKICAgICAgICAgICAgfQogICAgICAgIH0KICAgIDwvc3R5bGU+CjwvaGVhZD4KPGJvZHk+CiAgICA8aGVhZGVyPgogICAgICAgIDxkaXYgY2xhc3M9ImNvbnRhaW5lciBoZWFkZXItcm93Ij4KICAgICAgICAgICAgPGRpdiBjbGFzcz0iaGVhZGVyLWxlZnQiPgogICAgICAgICAgICAgICAgPGgxIGNsYXNzPSJicmFuZC10aXRsZSI+UEdDIC0gV29ya2luZyBDYXBpdGFsIEdyb3VwPC9oMT4KCiAgICAgICAgICAgICAgICB7JSBpZiB1c2VyLmlzX2F1dGhlbnRpY2F0ZWQgJX0KICAgICAgICAgICAgICAgIDxuYXYgY2xhc3M9InRvcC1uYXYiPgogICAgICAgICAgICAgICAgICAgIDxhIGhyZWY9InslIHVybCAncG9ydGFsOmhvbWUnICV9IiBjbGFzcz0ibmF2LW1lbnUtcHJpbmNpcGFsIj5NZW7DuiBwcmluY2lwYWw8L2E+CiAgICAgICAgICAgICAgICAgICAgPGEgaHJlZj0ieyUgdXJsICdwZ2M6ZGFzaGJvYXJkJyAlfSI+VGFibGVybzwvYT4KICAgICAgICAgICAgICAgICAgICA8YSBocmVmPSJ7JSB1cmwgJ3BnYzppbmdyZXNvcycgJX0iPkluZ3Jlc29zIHZzIG1ldGE8L2E+CiAgICAgICAgICAgICAgICAgICAgPGEgaHJlZj0ieyUgdXJsICdwZ2M6Y2xpZW50ZXNfbnVldm9zJyAlfSI+Q2xpZW50ZXM8L2E+CiAgICAgICAgICAgICAgICAgICAgPGEgaHJlZj0ieyUgdXJsICdwZ2M6dmVudGFfY3J1emFkYScgJX0iPlZlbnRhIGNydXphZGE8L2E+CiAgICAgICAgICAgICAgICAgICAgPGEgaHJlZj0ieyUgdXJsICdwZ2M6cmVzcHVlc3RhX3JlcXMnICV9Ij5SZXNwdWVzdGEgcmVxczwvYT4KICAgICAgICAgICAgICAgICAgPGEgaHJlZj0ieyUgc3RhdGljICdkb2NzL1dDRy1QR0MucGRmJyAlfSIgdGFyZ2V0PSJfYmxhbmsiIHJlbD0ibm9vcGVuZXIgbm9yZWZlcnJlciI+QXl1ZGE8L2E+CiAgICAgICAgICAgICAgICA8L25hdj4KICAgICAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgIDwvZGl2PgoKICAgICAgICAgICAgeyUgaWYgdXNlci5pc19hdXRoZW50aWNhdGVkICV9CiAgICAgICAgICAgIDxkaXYgY2xhc3M9ImhlYWRlci1yaWdodCI+CiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJ1c2VyLWJhZGdlIj4KICAgICAgICAgICAgICAgICAgICB7eyB1c2VyLnVzZXJuYW1lIH19CiAgICAgICAgICAgICAgICA8L2Rpdj4KCiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJnZWFyLXdyYXAiPgogICAgICAgICAgICAgICAgICAgIDxidXR0b24gdHlwZT0iYnV0dG9uIiBjbGFzcz0iZ2Vhci1idG4iIGlkPSJnZWFyLWJ0biIgYXJpYS1sYWJlbD0iQWJyaXIgb3BjaW9uZXMiPuKamTwvYnV0dG9uPgoKICAgICAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJnZWFyLW1lbnUiIGlkPSJnZWFyLW1lbnUiPgogICAgICAgICAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzPSJtZW51LWxhYmVsIj5TZXNpw7NuPC9kaXY+CiAgICAgICAgICAgICAgICAgICAgICAgIDxmb3JtIG1ldGhvZD0icG9zdCIgYWN0aW9uPSJ7JSB1cmwgJ2xvZ291dCcgJX0iPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgeyUgY3NyZl90b2tlbiAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgPGJ1dHRvbiB0eXBlPSJzdWJtaXQiPkNhbWJpYXIgZGUgdXN1YXJpbzwvYnV0dG9uPgogICAgICAgICAgICAgICAgICAgICAgICA8L2Zvcm0+CgogICAgICAgICAgICAgICAgICAgICAgICB7JSBpZiB1c2VyLmlzX3N1cGVydXNlciAlfQogICAgICAgICAgICAgICAgICAgICAgICAgICAgPGRpdiBjbGFzcz0ibWVudS1sYWJlbCI+QWRtaW5pc3RyYWNpw7NuPC9kaXY+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICA8YSBocmVmPSJ7JSB1cmwgJ2ltcG9ydHM6aW1wb3J0X2h1YicgJX0iPkltcG9ydGFjacOzbiBHZW5lcmFsPC9hPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgPGEgaHJlZj0ieyUgdXJsICdwZ2M6YWRtaW5fbW9udGhseScgJX0iPkFkbWluIFBHQyAocGVyw61vZG8pPC9hPgogICAgICAgICAgICAgICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgICAgICAgICAgIDwvZGl2PgogICAgICAgICAgICAgICAgPC9kaXY+CiAgICAgICAgICAgIDwvZGl2PgogICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgIDwvZGl2PgogICAgPC9oZWFkZXI+CgogICAgPG1haW4+CgogICAgICAgIHslIGlmIG1lc3NhZ2VzICV9CiAgICAgICAgICA8ZGl2IHN0eWxlPSJtYXJnaW46MTZweCAwOyI+CiAgICAgICAgICAgIHslIGZvciBtZXNzYWdlIGluIG1lc3NhZ2VzICV9CiAgICAgICAgICAgICAgPGRpdiBzdHlsZT0icGFkZGluZzoxMnB4IDE0cHg7IGJvcmRlci1yYWRpdXM6OHB4OyBtYXJnaW4tYm90dG9tOjEwcHg7eyUgaWYgbWVzc2FnZS50YWdzID09ICdlcnJvcicgJX0gYmFja2dyb3VuZDojZmVmMmYyOyBib3JkZXI6MXB4IHNvbGlkICNmZWNhY2E7IGNvbG9yOiM5OTFiMWI7eyUgZWxpZiBtZXNzYWdlLnRhZ3MgPT0gJ3dhcm5pbmcnICV9IGJhY2tncm91bmQ6I2ZmZmJlYjsgYm9yZGVyOjFweCBzb2xpZCAjZmRlNjhhOyBjb2xvcjojOTI0MDBlO3slIGVsaWYgbWVzc2FnZS50YWdzID09ICdpbmZvJyAlfSBiYWNrZ3JvdW5kOiNlZmY2ZmY7IGJvcmRlcjoxcHggc29saWQgI2JmZGJmZTsgY29sb3I6IzFlNDBhZjt7JSBlbHNlICV9IGJhY2tncm91bmQ6I2VjZmRmNTsgYm9yZGVyOjFweCBzb2xpZCAjYTdmM2QwOyBjb2xvcjojMDY1ZjQ2O3slIGVuZGlmICV9Ij4KICAgICAgICAgICAgICAgIHt7IG1lc3NhZ2UgfX0KICAgICAgICAgICAgICA8L2Rpdj4KICAgICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgICA8L2Rpdj4KICAgICAgICB7JSBlbmRpZiAlfQogICAgICAKICAgICAgICA8ZGl2IGNsYXNzPSJjb250YWluZXIiPgogICAgICAgICAgICB7JSBibG9jayBjb250ZW50ICV9eyUgZW5kYmxvY2sgJX0KICAgICAgICA8L2Rpdj4KICAgIDwvbWFpbj4KCiAgICB7JSBpZiB1c2VyLmlzX2F1dGhlbnRpY2F0ZWQgJX0KICAgIDxzY3JpcHQ+CiAgICAgICAgKGZ1bmN0aW9uICgpIHsKICAgICAgICAgICAgY29uc3QgYnRuID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoImdlYXItYnRuIik7CiAgICAgICAgICAgIGNvbnN0IG1lbnUgPSBkb2N1bWVudC5nZXRFbGVtZW50QnlJZCgiZ2Vhci1tZW51Iik7CiAgICAgICAgICAgIGlmICghYnRuIHx8ICFtZW51KSByZXR1cm47CgogICAgICAgICAgICBidG4uYWRkRXZlbnRMaXN0ZW5lcigiY2xpY2siLCBmdW5jdGlvbiAoZSkgewogICAgICAgICAgICAgICAgZS5zdG9wUHJvcGFnYXRpb24oKTsKICAgICAgICAgICAgICAgIG1lbnUuY2xhc3NMaXN0LnRvZ2dsZSgib3BlbiIpOwogICAgICAgICAgICB9KTsKCiAgICAgICAgICAgIGRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoImNsaWNrIiwgZnVuY3Rpb24gKGUpIHsKICAgICAgICAgICAgICAgIGlmICghbWVudS5jb250YWlucyhlLnRhcmdldCkgJiYgIWJ0bi5jb250YWlucyhlLnRhcmdldCkpIHsKICAgICAgICAgICAgICAgICAgICBtZW51LmNsYXNzTGlzdC5yZW1vdmUoIm9wZW4iKTsKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgfSk7CgogICAgICAgICAgICBkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCJrZXlkb3duIiwgZnVuY3Rpb24gKGUpIHsKICAgICAgICAgICAgICAgIGlmIChlLmtleSA9PT0gIkVzY2FwZSIpIHsKICAgICAgICAgICAgICAgICAgICBtZW51LmNsYXNzTGlzdC5yZW1vdmUoIm9wZW4iKTsKICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgfSk7CiAgICAgICAgfSkoKTsKICAgIDwvc2NyaXB0PgogICAgeyUgZW5kaWYgJX0KPC9ib2R5Pgo8L2h0bWw+
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/base_wcg.html
PATH_JSON="templates/base_wcg.html"
FILENAME=base_wcg.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=382
SIZE_BYTES_UTF8=14724
CONTENT_SHA256=0469718d142e8c25ede06280287b171cda0e9fd86da73c7eb0a98fa75f3dad3e
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
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}WCG One{% endblock %}</title>
    {% block extra_head %}{% endblock %}
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
        * { box-sizing: border-box; }
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
          font-size: 0.95rem;
        }
        .wcg-topbar {
          background: var(--wcg-nav-bg);
          border-bottom: 1px solid var(--wcg-line);
          backdrop-filter: blur(8px);
        }
        .wcg-topbar .navbar { padding-top: 0.65rem; padding-bottom: 0.65rem; }
        .wcg-brand {
          font-weight: 700;
          letter-spacing: -0.02em;
          color: var(--wcg-accent-ink) !important;
          font-size: 1.05rem;
          margin-right: 1.25rem;
        }
        .wcg-brand:hover { color: var(--wcg-ink) !important; }
        .wcg-home-link {
          display: inline-flex;
          align-items: center;
          gap: 0.35rem;
          padding: 0.4rem 0.85rem;
          border-radius: var(--wcg-radius);
          background: #ffffff;
          border: 1px solid #b7c9d8;
          color: var(--wcg-accent-ink) !important;
          font-weight: 600;
          font-size: 0.82rem;
          text-decoration: none;
          margin-right: 1rem;
          white-space: nowrap;
        }
        .wcg-home-link:hover {
          background: #ffffff;
          border-color: #b7c9d8;
          color: var(--wcg-ink) !important;
        }
        .wcg-nav-primary {
          display: flex;
          align-items: center;
          gap: 0.35rem;
          list-style: none;
          margin: 0;
          padding: 0;
        }
        .wcg-nav-primary .nav-link {
          color: var(--wcg-nav-ink) !important;
          font-weight: 500;
          font-size: 0.9rem;
          padding: 0.45rem 0.9rem !important;
          border-radius: var(--wcg-radius);
          border: 1px solid transparent;
        }
        .wcg-nav-primary .nav-link:hover {
          background: rgba(255,255,255,0.7);
          color: var(--wcg-ink) !important;
        }
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
          padding: 0.4rem 0.65rem !important;
        }
        .wcg-nav-secondary .nav-link:hover,
        .wcg-nav-secondary .btn-link:hover {
          color: var(--wcg-accent-ink) !important;
        }
        .wcg-nav-secondary .dropdown-menu {
          border: 1px solid var(--wcg-line);
          border-radius: var(--wcg-radius);
          box-shadow: var(--wcg-shadow);
          padding: 0.35rem;
          min-width: 14rem;
        }
        .wcg-nav-secondary .dropdown-item {
          border-radius: 4px;
          font-size: 0.88rem;
          padding: 0.45rem 0.75rem;
          color: var(--wcg-ink);
        }
        .wcg-nav-secondary .dropdown-item:hover {
          background: var(--wcg-accent-soft);
        }
        .wcg-nav-secondary .dropdown-header {
          font-size: 0.72rem;
          text-transform: uppercase;
          letter-spacing: 0.04em;
          color: var(--wcg-muted);
          font-weight: 600;
        }
        main { flex: 1; padding: 1.75rem 0 3rem; }
        .card, .card-module {
          background: var(--wcg-surface);
          border: 1px solid var(--wcg-line) !important;
          border-radius: var(--wcg-radius) !important;
          box-shadow: var(--wcg-shadow);
        }
        .card-module { transition: box-shadow .15s ease, border-color .15s ease; }
        .card-module:hover {
          box-shadow: 0 2px 8px rgba(42, 52, 65, 0.08);
          border-color: #d0dbe6 !important;
        }
        .card-module .card-header {
          background: var(--wcg-accent-soft);
          color: var(--wcg-accent-ink);
          font-weight: 600;
          border-bottom: 1px solid var(--wcg-line);
          font-size: 0.92rem;
          padding: 0.75rem 1rem;
        }
        .card-header.bg-white {
          background: #fafbfc !important;
          border-bottom: 1px solid var(--wcg-line);
          color: var(--wcg-ink);
        }
        .table-wcg thead {
          background: #f0f4f8;
          color: var(--wcg-accent-ink);
        }
        .table-wcg thead th {
          font-weight: 600;
          font-size: 0.78rem;
          text-transform: uppercase;
          letter-spacing: 0.03em;
          border: none;
          padding-top: 0.7rem;
          padding-bottom: 0.7rem;
        }
        .table { --bs-table-hover-bg: #f7fafc; }
        .stat-value {
          font-size: 1.65rem;
          font-weight: 700;
          color: var(--wcg-accent-ink);
          letter-spacing: -0.02em;
        }
        .btn {
          border-radius: 10px;
          font-weight: 500;
        }
        .btn-primary {
          background: #5a7a94;
          border-color: #5a7a94;
          color: #fff;
        }
        .btn-primary:hover {
          background: #4d6b84;
          border-color: #4d6b84;
        }
        .btn-outline-primary {
          color: #3d5a73;
          background: #e4eef6;
          border-color: #c5d4e2;
        }
        .btn-outline-primary:hover {
          background: #d5e4f0;
          color: #2a3441;
          border-color: #b7c9d8;
        }
        .btn-outline-secondary {
          color: #4a5562;
          background: #e8edf2;
          border-color: #d0d8e0;
        }
        .btn-outline-secondary:hover {
          background: #dde4eb;
          color: #2a3441;
          border-color: #c5d0dc;
        }
        .form-control, .form-select {
          border-radius: 10px;
          border-color: var(--wcg-line);
        }
        .form-control:focus, .form-select:focus {
          border-color: #a8c0d4;
          box-shadow: 0 0 0 0.2rem rgba(122, 155, 184, 0.2);
        }
        .badge.text-bg-secondary { background: #d5dee8 !important; color: var(--wcg-accent-ink) !important; }
        .badge.text-bg-success { background: #d8ebe3 !important; color: #2f5e4e !important; }
        .badge.text-bg-warning { background: #f3ead6 !important; color: #6e5a2e !important; }
        .alert {
          border-radius: var(--wcg-radius);
          border: 1px solid var(--wcg-line);
        }
        .breadcrumb { background: transparent; padding-left: 0; margin-bottom: 1rem; }
        .page-toolbar {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          flex-wrap: wrap;
          gap: 0.75rem;
          margin-bottom: 1.25rem;
        }
        .page-toolbar h1 { margin: 0; }
        /* Cabecera de reporte: título izq, emoji der */
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
        /* Menú principal: siempre claro */
        .wcg-home-link {
          background: #ffffff !important;
          border-color: #b7c9d8 !important;
          color: var(--wcg-accent-ink) !important;
        }
        .wcg-home-link:hover {
          background: #ffffff !important;
          color: var(--wcg-ink) !important;
        }
        footer.wcg-footer {
          border-top: 1px solid var(--wcg-line);
          background: rgba(255,255,255,0.65);
          padding: 0.85rem 0;
          color: var(--wcg-muted);
          font-size: 0.8rem;
        }
        {% block extra_css %}{% endblock %}
    </style>
</head>
<body>
    <header class="wcg-topbar sticky-top">
      <nav class="navbar navbar-expand-lg">
        <div class="container">
          <a class="navbar-brand wcg-brand mb-0" href="{% url 'portal:home' %}">WCG One</a>
          <a class="wcg-home-link d-none d-md-inline-flex" href="{% url 'portal:home' %}" title="Volver al menú principal">
            ← Menú principal
          </a>
          <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#wcgNav" aria-controls="wcgNav" aria-expanded="false" aria-label="Menú">
            <span class="navbar-toggler-icon" style="filter: invert(0.45);"></span>
          </button>
          <div class="collapse navbar-collapse" id="wcgNav">
            {% if user.is_authenticated %}
            <ul class="navbar-nav wcg-nav-primary me-auto mb-2 mb-lg-0 mt-2 mt-lg-0">
              <li class="nav-item d-md-none">
                <a class="nav-link fw-semibold" href="{% url 'portal:home' %}">← Menú principal</a>
              </li>
              <li class="nav-item">
                <a class="nav-link{% if '/pgc/' in request.path or '/tablero/' in request.path %} active{% endif %}" href="{% url 'pgc:dashboard' %}"><span class="wcg-mod-ico" aria-hidden="true">📊</span> PGC</a>
              </li>
              <li class="nav-item">
                <a class="nav-link{% if '/pgo/' in request.path %} active{% endif %}" href="{% url 'pgo:dashboard' %}"><span class="wcg-mod-ico" aria-hidden="true">⚙️</span> PGO</a>
              </li>
              <li class="nav-item">
                <a class="nav-link{% if '/crm/' in request.path %} active{% endif %}" href="{% url 'crm:entidad_list' %}"><span class="wcg-mod-ico" aria-hidden="true">👥</span> CRM</a>
              </li>
              <li class="nav-item">
                <a class="nav-link{% if '/risk/' in request.path %} active{% endif %}" href="{% url 'risk:comando_balon' %}"><span class="wcg-mod-ico" aria-hidden="true">⚽</span> Balón de Riesgo</a>
              </li>
            </ul>
            <ul class="navbar-nav wcg-nav-secondary align-items-lg-center gap-lg-1">
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle{% if '/importaciones/' in request.path or '/panel/estado' in request.path %} active{% endif %}" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Administración
                </a>
                <ul class="dropdown-menu dropdown-menu-end">
                  <li><h6 class="dropdown-header">Configuración del sistema</h6></li>
                  <li>
                    <a class="dropdown-item{% if '/importaciones/' in request.path %} active{% endif %}" href="{% url 'imports:import_hub' %}">
                      Importación General
                    </a>
                  </li>
                  <li><a class="dropdown-item" href="{% url 'portal:estado' %}">Estado del sistema</a></li>
                  <li><a class="dropdown-item" href="{% url 'portal:ayuda' %}">Guía de uso</a></li>
                  {% if user.is_superuser %}
                  <li><hr class="dropdown-divider"></li>
                  <li><a class="dropdown-item" href="/admin/" target="_blank" rel="noopener">Admin Django</a></li>
                  <li><a class="dropdown-item" href="{% url 'pgc:admin_monthly' %}">Admin PGC (período)</a></li>
                  {% endif %}
                </ul>
              </li>
              <li class="nav-item">
                <span class="nav-link disabled" style="opacity:0.7;">{{ user.get_username }}</span>
              </li>
              <li class="nav-item">
                <form method="post" action="{% url 'logout' %}" class="d-inline">
                  {% csrf_token %}
                  <button type="submit" class="btn btn-link nav-link">Salir</button>
                </form>
              </li>
            </ul>
            {% endif %}
          </div>
        </div>
      </nav>
    </header>

    <main>
        <div class="container">
            {% if messages %}
            {% for message in messages %}
            <div class="alert alert-{% if message.tags == 'error' %}danger{% elif message.tags == 'warning' %}warning{% elif message.tags == 'success' %}success{% else %}info{% endif %} mt-2">{{ message }}</div>
            {% endfor %}
            {% endif %}
            {% if breadcrumbs %}
            {% include "includes/breadcrumbs.html" %}
            {% endif %}
            {% block content %}{% endblock %}
        </div>
    </main>
    <footer class="wcg-footer mt-auto">
      <div class="container">WCG One — Working Capital Group</div>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% load static %}
00002|<!DOCTYPE html>
00003|<html lang="es">
00004|<head>
00005|    <meta charset="UTF-8">
00006|    <meta name="viewport" content="width=device-width, initial-scale=1">
00007|    <title>{% block title %}WCG One{% endblock %}</title>
00008|    {% block extra_head %}{% endblock %}
00009|    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
00010|    <link rel="preconnect" href="https://fonts.googleapis.com">
00011|    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
00012|    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap" rel="stylesheet">
00013|    <style>
00014|        :root {
00015|          --wcg-bg: #f3f6f9;
00016|          --wcg-surface: #ffffff;
00017|          --wcg-ink: #2a3441;
00018|          --wcg-muted: #6b7a8d;
00019|          --wcg-line: #e2e8f0;
00020|          --wcg-accent: #7a9bb8;
00021|          --wcg-accent-soft: #e8f0f6;
00022|          --wcg-accent-ink: #3d5a73;
00023|          --wcg-nav-bg: #eef3f7;
00024|          --wcg-nav-ink: #3a4a5c;
00025|          --wcg-radius: 10px;
00026|          --wcg-shadow: 0 1px 2px rgba(42, 52, 65, 0.04), 0 4px 12px rgba(42, 52, 65, 0.04);
00027|        }
00028|        * { box-sizing: border-box; }
00029|        body {
00030|          font-family: "DM Sans", system-ui, sans-serif;
00031|          background:
00032|            radial-gradient(1200px 500px at 10% -10%, #e8f1f7 0%, transparent 55%),
00033|            radial-gradient(900px 400px at 100% 0%, #edf2f6 0%, transparent 50%),
00034|            var(--wcg-bg);
00035|          color: var(--wcg-ink);
00036|          min-height: 100vh;
00037|          display: flex;
00038|          flex-direction: column;
00039|          font-size: 0.95rem;
00040|        }
00041|        .wcg-topbar {
00042|          background: var(--wcg-nav-bg);
00043|          border-bottom: 1px solid var(--wcg-line);
00044|          backdrop-filter: blur(8px);
00045|        }
00046|        .wcg-topbar .navbar { padding-top: 0.65rem; padding-bottom: 0.65rem; }
00047|        .wcg-brand {
00048|          font-weight: 700;
00049|          letter-spacing: -0.02em;
00050|          color: var(--wcg-accent-ink) !important;
00051|          font-size: 1.05rem;
00052|          margin-right: 1.25rem;
00053|        }
00054|        .wcg-brand:hover { color: var(--wcg-ink) !important; }
00055|        .wcg-home-link {
00056|          display: inline-flex;
00057|          align-items: center;
00058|          gap: 0.35rem;
00059|          padding: 0.4rem 0.85rem;
00060|          border-radius: var(--wcg-radius);
00061|          background: #ffffff;
00062|          border: 1px solid #b7c9d8;
00063|          color: var(--wcg-accent-ink) !important;
00064|          font-weight: 600;
00065|          font-size: 0.82rem;
00066|          text-decoration: none;
00067|          margin-right: 1rem;
00068|          white-space: nowrap;
00069|        }
00070|        .wcg-home-link:hover {
00071|          background: #ffffff;
00072|          border-color: #b7c9d8;
00073|          color: var(--wcg-ink) !important;
00074|        }
00075|        .wcg-nav-primary {
00076|          display: flex;
00077|          align-items: center;
00078|          gap: 0.35rem;
00079|          list-style: none;
00080|          margin: 0;
00081|          padding: 0;
00082|        }
00083|        .wcg-nav-primary .nav-link {
00084|          color: var(--wcg-nav-ink) !important;
00085|          font-weight: 500;
00086|          font-size: 0.9rem;
00087|          padding: 0.45rem 0.9rem !important;
00088|          border-radius: var(--wcg-radius);
00089|          border: 1px solid transparent;
00090|        }
00091|        .wcg-nav-primary .nav-link:hover {
00092|          background: rgba(255,255,255,0.7);
00093|          color: var(--wcg-ink) !important;
00094|        }
00095|        .wcg-nav-primary .nav-link.active {
00096|          background: var(--wcg-surface);
00097|          border-color: var(--wcg-line);
00098|          color: var(--wcg-accent-ink) !important;
00099|          box-shadow: var(--wcg-shadow);
00100|        }
00101|        .wcg-mod-ico {
00102|          font-size: 1.05em;
00103|          margin-right: 0.15rem;
00104|          line-height: 1;
00105|        }
00106|        .wcg-nav-secondary .nav-link,
00107|        .wcg-nav-secondary .btn-link {
00108|          color: var(--wcg-muted) !important;
00109|          font-size: 0.85rem;
00110|          font-weight: 500;
00111|          text-decoration: none;
00112|          padding: 0.4rem 0.65rem !important;
00113|        }
00114|        .wcg-nav-secondary .nav-link:hover,
00115|        .wcg-nav-secondary .btn-link:hover {
00116|          color: var(--wcg-accent-ink) !important;
00117|        }
00118|        .wcg-nav-secondary .dropdown-menu {
00119|          border: 1px solid var(--wcg-line);
00120|          border-radius: var(--wcg-radius);
00121|          box-shadow: var(--wcg-shadow);
00122|          padding: 0.35rem;
00123|          min-width: 14rem;
00124|        }
00125|        .wcg-nav-secondary .dropdown-item {
00126|          border-radius: 4px;
00127|          font-size: 0.88rem;
00128|          padding: 0.45rem 0.75rem;
00129|          color: var(--wcg-ink);
00130|        }
00131|        .wcg-nav-secondary .dropdown-item:hover {
00132|          background: var(--wcg-accent-soft);
00133|        }
00134|        .wcg-nav-secondary .dropdown-header {
00135|          font-size: 0.72rem;
00136|          text-transform: uppercase;
00137|          letter-spacing: 0.04em;
00138|          color: var(--wcg-muted);
00139|          font-weight: 600;
00140|        }
00141|        main { flex: 1; padding: 1.75rem 0 3rem; }
00142|        .card, .card-module {
00143|          background: var(--wcg-surface);
00144|          border: 1px solid var(--wcg-line) !important;
00145|          border-radius: var(--wcg-radius) !important;
00146|          box-shadow: var(--wcg-shadow);
00147|        }
00148|        .card-module { transition: box-shadow .15s ease, border-color .15s ease; }
00149|        .card-module:hover {
00150|          box-shadow: 0 2px 8px rgba(42, 52, 65, 0.08);
00151|          border-color: #d0dbe6 !important;
00152|        }
00153|        .card-module .card-header {
00154|          background: var(--wcg-accent-soft);
00155|          color: var(--wcg-accent-ink);
00156|          font-weight: 600;
00157|          border-bottom: 1px solid var(--wcg-line);
00158|          font-size: 0.92rem;
00159|          padding: 0.75rem 1rem;
00160|        }
00161|        .card-header.bg-white {
00162|          background: #fafbfc !important;
00163|          border-bottom: 1px solid var(--wcg-line);
00164|          color: var(--wcg-ink);
00165|        }
00166|        .table-wcg thead {
00167|          background: #f0f4f8;
00168|          color: var(--wcg-accent-ink);
00169|        }
00170|        .table-wcg thead th {
00171|          font-weight: 600;
00172|          font-size: 0.78rem;
00173|          text-transform: uppercase;
00174|          letter-spacing: 0.03em;
00175|          border: none;
00176|          padding-top: 0.7rem;
00177|          padding-bottom: 0.7rem;
00178|        }
00179|        .table { --bs-table-hover-bg: #f7fafc; }
00180|        .stat-value {
00181|          font-size: 1.65rem;
00182|          font-weight: 700;
00183|          color: var(--wcg-accent-ink);
00184|          letter-spacing: -0.02em;
00185|        }
00186|        .btn {
00187|          border-radius: 10px;
00188|          font-weight: 500;
00189|        }
00190|        .btn-primary {
00191|          background: #5a7a94;
00192|          border-color: #5a7a94;
00193|          color: #fff;
00194|        }
00195|        .btn-primary:hover {
00196|          background: #4d6b84;
00197|          border-color: #4d6b84;
00198|        }
00199|        .btn-outline-primary {
00200|          color: #3d5a73;
00201|          background: #e4eef6;
00202|          border-color: #c5d4e2;
00203|        }
00204|        .btn-outline-primary:hover {
00205|          background: #d5e4f0;
00206|          color: #2a3441;
00207|          border-color: #b7c9d8;
00208|        }
00209|        .btn-outline-secondary {
00210|          color: #4a5562;
00211|          background: #e8edf2;
00212|          border-color: #d0d8e0;
00213|        }
00214|        .btn-outline-secondary:hover {
00215|          background: #dde4eb;
00216|          color: #2a3441;
00217|          border-color: #c5d0dc;
00218|        }
00219|        .form-control, .form-select {
00220|          border-radius: 10px;
00221|          border-color: var(--wcg-line);
00222|        }
00223|        .form-control:focus, .form-select:focus {
00224|          border-color: #a8c0d4;
00225|          box-shadow: 0 0 0 0.2rem rgba(122, 155, 184, 0.2);
00226|        }
00227|        .badge.text-bg-secondary { background: #d5dee8 !important; color: var(--wcg-accent-ink) !important; }
00228|        .badge.text-bg-success { background: #d8ebe3 !important; color: #2f5e4e !important; }
00229|        .badge.text-bg-warning { background: #f3ead6 !important; color: #6e5a2e !important; }
00230|        .alert {
00231|          border-radius: var(--wcg-radius);
00232|          border: 1px solid var(--wcg-line);
00233|        }
00234|        .breadcrumb { background: transparent; padding-left: 0; margin-bottom: 1rem; }
00235|        .page-toolbar {
00236|          display: flex;
00237|          justify-content: space-between;
00238|          align-items: flex-start;
00239|          flex-wrap: wrap;
00240|          gap: 0.75rem;
00241|          margin-bottom: 1.25rem;
00242|        }
00243|        .page-toolbar h1 { margin: 0; }
00244|        /* Cabecera de reporte: título izq, emoji der */
00245|        .wcg-report-head {
00246|          display: flex;
00247|          align-items: flex-start;
00248|          justify-content: space-between;
00249|          gap: 0.75rem;
00250|          flex: 1 1 auto;
00251|          min-width: 0;
00252|          margin: 0;
00253|        }
00254|        .wcg-report-head > h1,
00255|        .wcg-report-head > h2,
00256|        .wcg-report-head > .h4 {
00257|          margin: 0;
00258|          flex: 1 1 auto;
00259|          min-width: 0;
00260|          line-height: 1.25;
00261|        }
00262|        .wcg-title-ico {
00263|          display: inline-flex;
00264|          align-items: center;
00265|          justify-content: center;
00266|          flex: 0 0 auto;
00267|          font-size: 1.9em;
00268|          line-height: 1;
00269|          margin: 0;
00270|          padding: 0.05rem 0.1rem;
00271|          opacity: 0.92;
00272|          filter: saturate(1.12);
00273|          user-select: none;
00274|          pointer-events: none;
00275|        }
00276|        /* Menú principal: siempre claro */
00277|        .wcg-home-link {
00278|          background: #ffffff !important;
00279|          border-color: #b7c9d8 !important;
00280|          color: var(--wcg-accent-ink) !important;
00281|        }
00282|        .wcg-home-link:hover {
00283|          background: #ffffff !important;
00284|          color: var(--wcg-ink) !important;
00285|        }
00286|        footer.wcg-footer {
00287|          border-top: 1px solid var(--wcg-line);
00288|          background: rgba(255,255,255,0.65);
00289|          padding: 0.85rem 0;
00290|          color: var(--wcg-muted);
00291|          font-size: 0.8rem;
00292|        }
00293|        {% block extra_css %}{% endblock %}
00294|    </style>
00295|</head>
00296|<body>
00297|    <header class="wcg-topbar sticky-top">
00298|      <nav class="navbar navbar-expand-lg">
00299|        <div class="container">
00300|          <a class="navbar-brand wcg-brand mb-0" href="{% url 'portal:home' %}">WCG One</a>
00301|          <a class="wcg-home-link d-none d-md-inline-flex" href="{% url 'portal:home' %}" title="Volver al menú principal">
00302|            ← Menú principal
00303|          </a>
00304|          <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#wcgNav" aria-controls="wcgNav" aria-expanded="false" aria-label="Menú">
00305|            <span class="navbar-toggler-icon" style="filter: invert(0.45);"></span>
00306|          </button>
00307|          <div class="collapse navbar-collapse" id="wcgNav">
00308|            {% if user.is_authenticated %}
00309|            <ul class="navbar-nav wcg-nav-primary me-auto mb-2 mb-lg-0 mt-2 mt-lg-0">
00310|              <li class="nav-item d-md-none">
00311|                <a class="nav-link fw-semibold" href="{% url 'portal:home' %}">← Menú principal</a>
00312|              </li>
00313|              <li class="nav-item">
00314|                <a class="nav-link{% if '/pgc/' in request.path or '/tablero/' in request.path %} active{% endif %}" href="{% url 'pgc:dashboard' %}"><span class="wcg-mod-ico" aria-hidden="true">📊</span> PGC</a>
00315|              </li>
00316|              <li class="nav-item">
00317|                <a class="nav-link{% if '/pgo/' in request.path %} active{% endif %}" href="{% url 'pgo:dashboard' %}"><span class="wcg-mod-ico" aria-hidden="true">⚙️</span> PGO</a>
00318|              </li>
00319|              <li class="nav-item">
00320|                <a class="nav-link{% if '/crm/' in request.path %} active{% endif %}" href="{% url 'crm:entidad_list' %}"><span class="wcg-mod-ico" aria-hidden="true">👥</span> CRM</a>
00321|              </li>
00322|              <li class="nav-item">
00323|                <a class="nav-link{% if '/risk/' in request.path %} active{% endif %}" href="{% url 'risk:comando_balon' %}"><span class="wcg-mod-ico" aria-hidden="true">⚽</span> Balón de Riesgo</a>
00324|              </li>
00325|            </ul>
00326|            <ul class="navbar-nav wcg-nav-secondary align-items-lg-center gap-lg-1">
00327|              <li class="nav-item dropdown">
00328|                <a class="nav-link dropdown-toggle{% if '/importaciones/' in request.path or '/panel/estado' in request.path %} active{% endif %}" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
00329|                  Administración
00330|                </a>
00331|                <ul class="dropdown-menu dropdown-menu-end">
00332|                  <li><h6 class="dropdown-header">Configuración del sistema</h6></li>
00333|                  <li>
00334|                    <a class="dropdown-item{% if '/importaciones/' in request.path %} active{% endif %}" href="{% url 'imports:import_hub' %}">
00335|                      Importación General
00336|                    </a>
00337|                  </li>
00338|                  <li><a class="dropdown-item" href="{% url 'portal:estado' %}">Estado del sistema</a></li>
00339|                  <li><a class="dropdown-item" href="{% url 'portal:ayuda' %}">Guía de uso</a></li>
00340|                  {% if user.is_superuser %}
00341|                  <li><hr class="dropdown-divider"></li>
00342|                  <li><a class="dropdown-item" href="/admin/" target="_blank" rel="noopener">Admin Django</a></li>
00343|                  <li><a class="dropdown-item" href="{% url 'pgc:admin_monthly' %}">Admin PGC (período)</a></li>
00344|                  {% endif %}
00345|                </ul>
00346|              </li>
00347|              <li class="nav-item">
00348|                <span class="nav-link disabled" style="opacity:0.7;">{{ user.get_username }}</span>
00349|              </li>
00350|              <li class="nav-item">
00351|                <form method="post" action="{% url 'logout' %}" class="d-inline">
00352|                  {% csrf_token %}
00353|                  <button type="submit" class="btn btn-link nav-link">Salir</button>
00354|                </form>
00355|              </li>
00356|            </ul>
00357|            {% endif %}
00358|          </div>
00359|        </div>
00360|      </nav>
00361|    </header>
00362|
00363|    <main>
00364|        <div class="container">
00365|            {% if messages %}
00366|            {% for message in messages %}
00367|            <div class="alert alert-{% if message.tags == 'error' %}danger{% elif message.tags == 'warning' %}warning{% elif message.tags == 'success' %}success{% else %}info{% endif %} mt-2">{{ message }}</div>
00368|            {% endfor %}
00369|            {% endif %}
00370|            {% if breadcrumbs %}
00371|            {% include "includes/breadcrumbs.html" %}
00372|            {% endif %}
00373|            {% block content %}{% endblock %}
00374|        </div>
00375|    </main>
00376|    <footer class="wcg-footer mt-auto">
00377|      <div class="container">WCG One — Working Capital Group</div>
00378|    </footer>
00379|    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
00380|    {% block extra_js %}{% endblock %}
00381|</body>
00382|</html>

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgbG9hZCBzdGF0aWMgJX0KPCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVzIj4KPGhlYWQ+CiAgICA8bWV0YSBjaGFyc2V0PSJVVEYtOCI+CiAgICA8bWV0YSBuYW1lPSJ2aWV3cG9ydCIgY29udGVudD0id2lkdGg9ZGV2aWNlLXdpZHRoLCBpbml0aWFsLXNjYWxlPTEiPgogICAgPHRpdGxlPnslIGJsb2NrIHRpdGxlICV9V0NHIE9uZXslIGVuZGJsb2NrICV9PC90aXRsZT4KICAgIHslIGJsb2NrIGV4dHJhX2hlYWQgJX17JSBlbmRibG9jayAlfQogICAgPGxpbmsgaHJlZj0iaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L25wbS9ib290c3RyYXBANS4zLjMvZGlzdC9jc3MvYm9vdHN0cmFwLm1pbi5jc3MiIHJlbD0ic3R5bGVzaGVldCI+CiAgICA8bGluayByZWw9InByZWNvbm5lY3QiIGhyZWY9Imh0dHBzOi8vZm9udHMuZ29vZ2xlYXBpcy5jb20iPgogICAgPGxpbmsgcmVsPSJwcmVjb25uZWN0IiBocmVmPSJodHRwczovL2ZvbnRzLmdzdGF0aWMuY29tIiBjcm9zc29yaWdpbj4KICAgIDxsaW5rIGhyZWY9Imh0dHBzOi8vZm9udHMuZ29vZ2xlYXBpcy5jb20vY3NzMj9mYW1pbHk9RE0rU2FuczppdGFsLG9wc3osd2dodEAwLDkuLjQwLDQwMDswLDkuLjQwLDUwMDswLDkuLjQwLDYwMDswLDkuLjQwLDcwMDsxLDkuLjQwLDQwMCZkaXNwbGF5PXN3YXAiIHJlbD0ic3R5bGVzaGVldCI+CiAgICA8c3R5bGU+CiAgICAgICAgOnJvb3QgewogICAgICAgICAgLS13Y2ctYmc6ICNmM2Y2Zjk7CiAgICAgICAgICAtLXdjZy1zdXJmYWNlOiAjZmZmZmZmOwogICAgICAgICAgLS13Y2ctaW5rOiAjMmEzNDQxOwogICAgICAgICAgLS13Y2ctbXV0ZWQ6ICM2YjdhOGQ7CiAgICAgICAgICAtLXdjZy1saW5lOiAjZTJlOGYwOwogICAgICAgICAgLS13Y2ctYWNjZW50OiAjN2E5YmI4OwogICAgICAgICAgLS13Y2ctYWNjZW50LXNvZnQ6ICNlOGYwZjY7CiAgICAgICAgICAtLXdjZy1hY2NlbnQtaW5rOiAjM2Q1YTczOwogICAgICAgICAgLS13Y2ctbmF2LWJnOiAjZWVmM2Y3OwogICAgICAgICAgLS13Y2ctbmF2LWluazogIzNhNGE1YzsKICAgICAgICAgIC0td2NnLXJhZGl1czogMTBweDsKICAgICAgICAgIC0td2NnLXNoYWRvdzogMCAxcHggMnB4IHJnYmEoNDIsIDUyLCA2NSwgMC4wNCksIDAgNHB4IDEycHggcmdiYSg0MiwgNTIsIDY1LCAwLjA0KTsKICAgICAgICB9CiAgICAgICAgKiB7IGJveC1zaXppbmc6IGJvcmRlci1ib3g7IH0KICAgICAgICBib2R5IHsKICAgICAgICAgIGZvbnQtZmFtaWx5OiAiRE0gU2FucyIsIHN5c3RlbS11aSwgc2Fucy1zZXJpZjsKICAgICAgICAgIGJhY2tncm91bmQ6CiAgICAgICAgICAgIHJhZGlhbC1ncmFkaWVudCgxMjAwcHggNTAwcHggYXQgMTAlIC0xMCUsICNlOGYxZjcgMCUsIHRyYW5zcGFyZW50IDU1JSksCiAgICAgICAgICAgIHJhZGlhbC1ncmFkaWVudCg5MDBweCA0MDBweCBhdCAxMDAlIDAlLCAjZWRmMmY2IDAlLCB0cmFuc3BhcmVudCA1MCUpLAogICAgICAgICAgICB2YXIoLS13Y2ctYmcpOwogICAgICAgICAgY29sb3I6IHZhcigtLXdjZy1pbmspOwogICAgICAgICAgbWluLWhlaWdodDogMTAwdmg7CiAgICAgICAgICBkaXNwbGF5OiBmbGV4OwogICAgICAgICAgZmxleC1kaXJlY3Rpb246IGNvbHVtbjsKICAgICAgICAgIGZvbnQtc2l6ZTogMC45NXJlbTsKICAgICAgICB9CiAgICAgICAgLndjZy10b3BiYXIgewogICAgICAgICAgYmFja2dyb3VuZDogdmFyKC0td2NnLW5hdi1iZyk7CiAgICAgICAgICBib3JkZXItYm90dG9tOiAxcHggc29saWQgdmFyKC0td2NnLWxpbmUpOwogICAgICAgICAgYmFja2Ryb3AtZmlsdGVyOiBibHVyKDhweCk7CiAgICAgICAgfQogICAgICAgIC53Y2ctdG9wYmFyIC5uYXZiYXIgeyBwYWRkaW5nLXRvcDogMC42NXJlbTsgcGFkZGluZy1ib3R0b206IDAuNjVyZW07IH0KICAgICAgICAud2NnLWJyYW5kIHsKICAgICAgICAgIGZvbnQtd2VpZ2h0OiA3MDA7CiAgICAgICAgICBsZXR0ZXItc3BhY2luZzogLTAuMDJlbTsKICAgICAgICAgIGNvbG9yOiB2YXIoLS13Y2ctYWNjZW50LWluaykgIWltcG9ydGFudDsKICAgICAgICAgIGZvbnQtc2l6ZTogMS4wNXJlbTsKICAgICAgICAgIG1hcmdpbi1yaWdodDogMS4yNXJlbTsKICAgICAgICB9CiAgICAgICAgLndjZy1icmFuZDpob3ZlciB7IGNvbG9yOiB2YXIoLS13Y2ctaW5rKSAhaW1wb3J0YW50OyB9CiAgICAgICAgLndjZy1ob21lLWxpbmsgewogICAgICAgICAgZGlzcGxheTogaW5saW5lLWZsZXg7CiAgICAgICAgICBhbGlnbi1pdGVtczogY2VudGVyOwogICAgICAgICAgZ2FwOiAwLjM1cmVtOwogICAgICAgICAgcGFkZGluZzogMC40cmVtIDAuODVyZW07CiAgICAgICAgICBib3JkZXItcmFkaXVzOiB2YXIoLS13Y2ctcmFkaXVzKTsKICAgICAgICAgIGJhY2tncm91bmQ6ICNmZmZmZmY7CiAgICAgICAgICBib3JkZXI6IDFweCBzb2xpZCAjYjdjOWQ4OwogICAgICAgICAgY29sb3I6IHZhcigtLXdjZy1hY2NlbnQtaW5rKSAhaW1wb3J0YW50OwogICAgICAgICAgZm9udC13ZWlnaHQ6IDYwMDsKICAgICAgICAgIGZvbnQtc2l6ZTogMC44MnJlbTsKICAgICAgICAgIHRleHQtZGVjb3JhdGlvbjogbm9uZTsKICAgICAgICAgIG1hcmdpbi1yaWdodDogMXJlbTsKICAgICAgICAgIHdoaXRlLXNwYWNlOiBub3dyYXA7CiAgICAgICAgfQogICAgICAgIC53Y2ctaG9tZS1saW5rOmhvdmVyIHsKICAgICAgICAgIGJhY2tncm91bmQ6ICNmZmZmZmY7CiAgICAgICAgICBib3JkZXItY29sb3I6ICNiN2M5ZDg7CiAgICAgICAgICBjb2xvcjogdmFyKC0td2NnLWluaykgIWltcG9ydGFudDsKICAgICAgICB9CiAgICAgICAgLndjZy1uYXYtcHJpbWFyeSB7CiAgICAgICAgICBkaXNwbGF5OiBmbGV4OwogICAgICAgICAgYWxpZ24taXRlbXM6IGNlbnRlcjsKICAgICAgICAgIGdhcDogMC4zNXJlbTsKICAgICAgICAgIGxpc3Qtc3R5bGU6IG5vbmU7CiAgICAgICAgICBtYXJnaW46IDA7CiAgICAgICAgICBwYWRkaW5nOiAwOwogICAgICAgIH0KICAgICAgICAud2NnLW5hdi1wcmltYXJ5IC5uYXYtbGluayB7CiAgICAgICAgICBjb2xvcjogdmFyKC0td2NnLW5hdi1pbmspICFpbXBvcnRhbnQ7CiAgICAgICAgICBmb250LXdlaWdodDogNTAwOwogICAgICAgICAgZm9udC1zaXplOiAwLjlyZW07CiAgICAgICAgICBwYWRkaW5nOiAwLjQ1cmVtIDAuOXJlbSAhaW1wb3J0YW50OwogICAgICAgICAgYm9yZGVyLXJhZGl1czogdmFyKC0td2NnLXJhZGl1cyk7CiAgICAgICAgICBib3JkZXI6IDFweCBzb2xpZCB0cmFuc3BhcmVudDsKICAgICAgICB9CiAgICAgICAgLndjZy1uYXYtcHJpbWFyeSAubmF2LWxpbms6aG92ZXIgewogICAgICAgICAgYmFja2dyb3VuZDogcmdiYSgyNTUsMjU1LDI1NSwwLjcpOwogICAgICAgICAgY29sb3I6IHZhcigtLXdjZy1pbmspICFpbXBvcnRhbnQ7CiAgICAgICAgfQogICAgICAgIC53Y2ctbmF2LXByaW1hcnkgLm5hdi1saW5rLmFjdGl2ZSB7CiAgICAgICAgICBiYWNrZ3JvdW5kOiB2YXIoLS13Y2ctc3VyZmFjZSk7CiAgICAgICAgICBib3JkZXItY29sb3I6IHZhcigtLXdjZy1saW5lKTsKICAgICAgICAgIGNvbG9yOiB2YXIoLS13Y2ctYWNjZW50LWluaykgIWltcG9ydGFudDsKICAgICAgICAgIGJveC1zaGFkb3c6IHZhcigtLXdjZy1zaGFkb3cpOwogICAgICAgIH0KICAgICAgICAud2NnLW1vZC1pY28gewogICAgICAgICAgZm9udC1zaXplOiAxLjA1ZW07CiAgICAgICAgICBtYXJnaW4tcmlnaHQ6IDAuMTVyZW07CiAgICAgICAgICBsaW5lLWhlaWdodDogMTsKICAgICAgICB9CiAgICAgICAgLndjZy1uYXYtc2Vjb25kYXJ5IC5uYXYtbGluaywKICAgICAgICAud2NnLW5hdi1zZWNvbmRhcnkgLmJ0bi1saW5rIHsKICAgICAgICAgIGNvbG9yOiB2YXIoLS13Y2ctbXV0ZWQpICFpbXBvcnRhbnQ7CiAgICAgICAgICBmb250LXNpemU6IDAuODVyZW07CiAgICAgICAgICBmb250LXdlaWdodDogNTAwOwogICAgICAgICAgdGV4dC1kZWNvcmF0aW9uOiBub25lOwogICAgICAgICAgcGFkZGluZzogMC40cmVtIDAuNjVyZW0gIWltcG9ydGFudDsKICAgICAgICB9CiAgICAgICAgLndjZy1uYXYtc2Vjb25kYXJ5IC5uYXYtbGluazpob3ZlciwKICAgICAgICAud2NnLW5hdi1zZWNvbmRhcnkgLmJ0bi1saW5rOmhvdmVyIHsKICAgICAgICAgIGNvbG9yOiB2YXIoLS13Y2ctYWNjZW50LWluaykgIWltcG9ydGFudDsKICAgICAgICB9CiAgICAgICAgLndjZy1uYXYtc2Vjb25kYXJ5IC5kcm9wZG93bi1tZW51IHsKICAgICAgICAgIGJvcmRlcjogMXB4IHNvbGlkIHZhcigtLXdjZy1saW5lKTsKICAgICAgICAgIGJvcmRlci1yYWRpdXM6IHZhcigtLXdjZy1yYWRpdXMpOwogICAgICAgICAgYm94LXNoYWRvdzogdmFyKC0td2NnLXNoYWRvdyk7CiAgICAgICAgICBwYWRkaW5nOiAwLjM1cmVtOwogICAgICAgICAgbWluLXdpZHRoOiAxNHJlbTsKICAgICAgICB9CiAgICAgICAgLndjZy1uYXYtc2Vjb25kYXJ5IC5kcm9wZG93bi1pdGVtIHsKICAgICAgICAgIGJvcmRlci1yYWRpdXM6IDRweDsKICAgICAgICAgIGZvbnQtc2l6ZTogMC44OHJlbTsKICAgICAgICAgIHBhZGRpbmc6IDAuNDVyZW0gMC43NXJlbTsKICAgICAgICAgIGNvbG9yOiB2YXIoLS13Y2ctaW5rKTsKICAgICAgICB9CiAgICAgICAgLndjZy1uYXYtc2Vjb25kYXJ5IC5kcm9wZG93bi1pdGVtOmhvdmVyIHsKICAgICAgICAgIGJhY2tncm91bmQ6IHZhcigtLXdjZy1hY2NlbnQtc29mdCk7CiAgICAgICAgfQogICAgICAgIC53Y2ctbmF2LXNlY29uZGFyeSAuZHJvcGRvd24taGVhZGVyIHsKICAgICAgICAgIGZvbnQtc2l6ZTogMC43MnJlbTsKICAgICAgICAgIHRleHQtdHJhbnNmb3JtOiB1cHBlcmNhc2U7CiAgICAgICAgICBsZXR0ZXItc3BhY2luZzogMC4wNGVtOwogICAgICAgICAgY29sb3I6IHZhcigtLXdjZy1tdXRlZCk7CiAgICAgICAgICBmb250LXdlaWdodDogNjAwOwogICAgICAgIH0KICAgICAgICBtYWluIHsgZmxleDogMTsgcGFkZGluZzogMS43NXJlbSAwIDNyZW07IH0KICAgICAgICAuY2FyZCwgLmNhcmQtbW9kdWxlIHsKICAgICAgICAgIGJhY2tncm91bmQ6IHZhcigtLXdjZy1zdXJmYWNlKTsKICAgICAgICAgIGJvcmRlcjogMXB4IHNvbGlkIHZhcigtLXdjZy1saW5lKSAhaW1wb3J0YW50OwogICAgICAgICAgYm9yZGVyLXJhZGl1czogdmFyKC0td2NnLXJhZGl1cykgIWltcG9ydGFudDsKICAgICAgICAgIGJveC1zaGFkb3c6IHZhcigtLXdjZy1zaGFkb3cpOwogICAgICAgIH0KICAgICAgICAuY2FyZC1tb2R1bGUgeyB0cmFuc2l0aW9uOiBib3gtc2hhZG93IC4xNXMgZWFzZSwgYm9yZGVyLWNvbG9yIC4xNXMgZWFzZTsgfQogICAgICAgIC5jYXJkLW1vZHVsZTpob3ZlciB7CiAgICAgICAgICBib3gtc2hhZG93OiAwIDJweCA4cHggcmdiYSg0MiwgNTIsIDY1LCAwLjA4KTsKICAgICAgICAgIGJvcmRlci1jb2xvcjogI2QwZGJlNiAhaW1wb3J0YW50OwogICAgICAgIH0KICAgICAgICAuY2FyZC1tb2R1bGUgLmNhcmQtaGVhZGVyIHsKICAgICAgICAgIGJhY2tncm91bmQ6IHZhcigtLXdjZy1hY2NlbnQtc29mdCk7CiAgICAgICAgICBjb2xvcjogdmFyKC0td2NnLWFjY2VudC1pbmspOwogICAgICAgICAgZm9udC13ZWlnaHQ6IDYwMDsKICAgICAgICAgIGJvcmRlci1ib3R0b206IDFweCBzb2xpZCB2YXIoLS13Y2ctbGluZSk7CiAgICAgICAgICBmb250LXNpemU6IDAuOTJyZW07CiAgICAgICAgICBwYWRkaW5nOiAwLjc1cmVtIDFyZW07CiAgICAgICAgfQogICAgICAgIC5jYXJkLWhlYWRlci5iZy13aGl0ZSB7CiAgICAgICAgICBiYWNrZ3JvdW5kOiAjZmFmYmZjICFpbXBvcnRhbnQ7CiAgICAgICAgICBib3JkZXItYm90dG9tOiAxcHggc29saWQgdmFyKC0td2NnLWxpbmUpOwogICAgICAgICAgY29sb3I6IHZhcigtLXdjZy1pbmspOwogICAgICAgIH0KICAgICAgICAudGFibGUtd2NnIHRoZWFkIHsKICAgICAgICAgIGJhY2tncm91bmQ6ICNmMGY0Zjg7CiAgICAgICAgICBjb2xvcjogdmFyKC0td2NnLWFjY2VudC1pbmspOwogICAgICAgIH0KICAgICAgICAudGFibGUtd2NnIHRoZWFkIHRoIHsKICAgICAgICAgIGZvbnQtd2VpZ2h0OiA2MDA7CiAgICAgICAgICBmb250LXNpemU6IDAuNzhyZW07CiAgICAgICAgICB0ZXh0LXRyYW5zZm9ybTogdXBwZXJjYXNlOwogICAgICAgICAgbGV0dGVyLXNwYWNpbmc6IDAuMDNlbTsKICAgICAgICAgIGJvcmRlcjogbm9uZTsKICAgICAgICAgIHBhZGRpbmctdG9wOiAwLjdyZW07CiAgICAgICAgICBwYWRkaW5nLWJvdHRvbTogMC43cmVtOwogICAgICAgIH0KICAgICAgICAudGFibGUgeyAtLWJzLXRhYmxlLWhvdmVyLWJnOiAjZjdmYWZjOyB9CiAgICAgICAgLnN0YXQtdmFsdWUgewogICAgICAgICAgZm9udC1zaXplOiAxLjY1cmVtOwogICAgICAgICAgZm9udC13ZWlnaHQ6IDcwMDsKICAgICAgICAgIGNvbG9yOiB2YXIoLS13Y2ctYWNjZW50LWluayk7CiAgICAgICAgICBsZXR0ZXItc3BhY2luZzogLTAuMDJlbTsKICAgICAgICB9CiAgICAgICAgLmJ0biB7CiAgICAgICAgICBib3JkZXItcmFkaXVzOiAxMHB4OwogICAgICAgICAgZm9udC13ZWlnaHQ6IDUwMDsKICAgICAgICB9CiAgICAgICAgLmJ0bi1wcmltYXJ5IHsKICAgICAgICAgIGJhY2tncm91bmQ6ICM1YTdhOTQ7CiAgICAgICAgICBib3JkZXItY29sb3I6ICM1YTdhOTQ7CiAgICAgICAgICBjb2xvcjogI2ZmZjsKICAgICAgICB9CiAgICAgICAgLmJ0bi1wcmltYXJ5OmhvdmVyIHsKICAgICAgICAgIGJhY2tncm91bmQ6ICM0ZDZiODQ7CiAgICAgICAgICBib3JkZXItY29sb3I6ICM0ZDZiODQ7CiAgICAgICAgfQogICAgICAgIC5idG4tb3V0bGluZS1wcmltYXJ5IHsKICAgICAgICAgIGNvbG9yOiAjM2Q1YTczOwogICAgICAgICAgYmFja2dyb3VuZDogI2U0ZWVmNjsKICAgICAgICAgIGJvcmRlci1jb2xvcjogI2M1ZDRlMjsKICAgICAgICB9CiAgICAgICAgLmJ0bi1vdXRsaW5lLXByaW1hcnk6aG92ZXIgewogICAgICAgICAgYmFja2dyb3VuZDogI2Q1ZTRmMDsKICAgICAgICAgIGNvbG9yOiAjMmEzNDQxOwogICAgICAgICAgYm9yZGVyLWNvbG9yOiAjYjdjOWQ4OwogICAgICAgIH0KICAgICAgICAuYnRuLW91dGxpbmUtc2Vjb25kYXJ5IHsKICAgICAgICAgIGNvbG9yOiAjNGE1NTYyOwogICAgICAgICAgYmFja2dyb3VuZDogI2U4ZWRmMjsKICAgICAgICAgIGJvcmRlci1jb2xvcjogI2QwZDhlMDsKICAgICAgICB9CiAgICAgICAgLmJ0bi1vdXRsaW5lLXNlY29uZGFyeTpob3ZlciB7CiAgICAgICAgICBiYWNrZ3JvdW5kOiAjZGRlNGViOwogICAgICAgICAgY29sb3I6ICMyYTM0NDE7CiAgICAgICAgICBib3JkZXItY29sb3I6ICNjNWQwZGM7CiAgICAgICAgfQogICAgICAgIC5mb3JtLWNvbnRyb2wsIC5mb3JtLXNlbGVjdCB7CiAgICAgICAgICBib3JkZXItcmFkaXVzOiAxMHB4OwogICAgICAgICAgYm9yZGVyLWNvbG9yOiB2YXIoLS13Y2ctbGluZSk7CiAgICAgICAgfQogICAgICAgIC5mb3JtLWNvbnRyb2w6Zm9jdXMsIC5mb3JtLXNlbGVjdDpmb2N1cyB7CiAgICAgICAgICBib3JkZXItY29sb3I6ICNhOGMwZDQ7CiAgICAgICAgICBib3gtc2hhZG93OiAwIDAgMCAwLjJyZW0gcmdiYSgxMjIsIDE1NSwgMTg0LCAwLjIpOwogICAgICAgIH0KICAgICAgICAuYmFkZ2UudGV4dC1iZy1zZWNvbmRhcnkgeyBiYWNrZ3JvdW5kOiAjZDVkZWU4ICFpbXBvcnRhbnQ7IGNvbG9yOiB2YXIoLS13Y2ctYWNjZW50LWluaykgIWltcG9ydGFudDsgfQogICAgICAgIC5iYWRnZS50ZXh0LWJnLXN1Y2Nlc3MgeyBiYWNrZ3JvdW5kOiAjZDhlYmUzICFpbXBvcnRhbnQ7IGNvbG9yOiAjMmY1ZTRlICFpbXBvcnRhbnQ7IH0KICAgICAgICAuYmFkZ2UudGV4dC1iZy13YXJuaW5nIHsgYmFja2dyb3VuZDogI2YzZWFkNiAhaW1wb3J0YW50OyBjb2xvcjogIzZlNWEyZSAhaW1wb3J0YW50OyB9CiAgICAgICAgLmFsZXJ0IHsKICAgICAgICAgIGJvcmRlci1yYWRpdXM6IHZhcigtLXdjZy1yYWRpdXMpOwogICAgICAgICAgYm9yZGVyOiAxcHggc29saWQgdmFyKC0td2NnLWxpbmUpOwogICAgICAgIH0KICAgICAgICAuYnJlYWRjcnVtYiB7IGJhY2tncm91bmQ6IHRyYW5zcGFyZW50OyBwYWRkaW5nLWxlZnQ6IDA7IG1hcmdpbi1ib3R0b206IDFyZW07IH0KICAgICAgICAucGFnZS10b29sYmFyIHsKICAgICAgICAgIGRpc3BsYXk6IGZsZXg7CiAgICAgICAgICBqdXN0aWZ5LWNvbnRlbnQ6IHNwYWNlLWJldHdlZW47CiAgICAgICAgICBhbGlnbi1pdGVtczogZmxleC1zdGFydDsKICAgICAgICAgIGZsZXgtd3JhcDogd3JhcDsKICAgICAgICAgIGdhcDogMC43NXJlbTsKICAgICAgICAgIG1hcmdpbi1ib3R0b206IDEuMjVyZW07CiAgICAgICAgfQogICAgICAgIC5wYWdlLXRvb2xiYXIgaDEgeyBtYXJnaW46IDA7IH0KICAgICAgICAvKiBDYWJlY2VyYSBkZSByZXBvcnRlOiB0w610dWxvIGl6cSwgZW1vamkgZGVyICovCiAgICAgICAgLndjZy1yZXBvcnQtaGVhZCB7CiAgICAgICAgICBkaXNwbGF5OiBmbGV4OwogICAgICAgICAgYWxpZ24taXRlbXM6IGZsZXgtc3RhcnQ7CiAgICAgICAgICBqdXN0aWZ5LWNvbnRlbnQ6IHNwYWNlLWJldHdlZW47CiAgICAgICAgICBnYXA6IDAuNzVyZW07CiAgICAgICAgICBmbGV4OiAxIDEgYXV0bzsKICAgICAgICAgIG1pbi13aWR0aDogMDsKICAgICAgICAgIG1hcmdpbjogMDsKICAgICAgICB9CiAgICAgICAgLndjZy1yZXBvcnQtaGVhZCA+IGgxLAogICAgICAgIC53Y2ctcmVwb3J0LWhlYWQgPiBoMiwKICAgICAgICAud2NnLXJlcG9ydC1oZWFkID4gLmg0IHsKICAgICAgICAgIG1hcmdpbjogMDsKICAgICAgICAgIGZsZXg6IDEgMSBhdXRvOwogICAgICAgICAgbWluLXdpZHRoOiAwOwogICAgICAgICAgbGluZS1oZWlnaHQ6IDEuMjU7CiAgICAgICAgfQogICAgICAgIC53Y2ctdGl0bGUtaWNvIHsKICAgICAgICAgIGRpc3BsYXk6IGlubGluZS1mbGV4OwogICAgICAgICAgYWxpZ24taXRlbXM6IGNlbnRlcjsKICAgICAgICAgIGp1c3RpZnktY29udGVudDogY2VudGVyOwogICAgICAgICAgZmxleDogMCAwIGF1dG87CiAgICAgICAgICBmb250LXNpemU6IDEuOWVtOwogICAgICAgICAgbGluZS1oZWlnaHQ6IDE7CiAgICAgICAgICBtYXJnaW46IDA7CiAgICAgICAgICBwYWRkaW5nOiAwLjA1cmVtIDAuMXJlbTsKICAgICAgICAgIG9wYWNpdHk6IDAuOTI7CiAgICAgICAgICBmaWx0ZXI6IHNhdHVyYXRlKDEuMTIpOwogICAgICAgICAgdXNlci1zZWxlY3Q6IG5vbmU7CiAgICAgICAgICBwb2ludGVyLWV2ZW50czogbm9uZTsKICAgICAgICB9CiAgICAgICAgLyogTWVuw7ogcHJpbmNpcGFsOiBzaWVtcHJlIGNsYXJvICovCiAgICAgICAgLndjZy1ob21lLWxpbmsgewogICAgICAgICAgYmFja2dyb3VuZDogI2ZmZmZmZiAhaW1wb3J0YW50OwogICAgICAgICAgYm9yZGVyLWNvbG9yOiAjYjdjOWQ4ICFpbXBvcnRhbnQ7CiAgICAgICAgICBjb2xvcjogdmFyKC0td2NnLWFjY2VudC1pbmspICFpbXBvcnRhbnQ7CiAgICAgICAgfQogICAgICAgIC53Y2ctaG9tZS1saW5rOmhvdmVyIHsKICAgICAgICAgIGJhY2tncm91bmQ6ICNmZmZmZmYgIWltcG9ydGFudDsKICAgICAgICAgIGNvbG9yOiB2YXIoLS13Y2ctaW5rKSAhaW1wb3J0YW50OwogICAgICAgIH0KICAgICAgICBmb290ZXIud2NnLWZvb3RlciB7CiAgICAgICAgICBib3JkZXItdG9wOiAxcHggc29saWQgdmFyKC0td2NnLWxpbmUpOwogICAgICAgICAgYmFja2dyb3VuZDogcmdiYSgyNTUsMjU1LDI1NSwwLjY1KTsKICAgICAgICAgIHBhZGRpbmc6IDAuODVyZW0gMDsKICAgICAgICAgIGNvbG9yOiB2YXIoLS13Y2ctbXV0ZWQpOwogICAgICAgICAgZm9udC1zaXplOiAwLjhyZW07CiAgICAgICAgfQogICAgICAgIHslIGJsb2NrIGV4dHJhX2NzcyAlfXslIGVuZGJsb2NrICV9CiAgICA8L3N0eWxlPgo8L2hlYWQ+Cjxib2R5PgogICAgPGhlYWRlciBjbGFzcz0id2NnLXRvcGJhciBzdGlja3ktdG9wIj4KICAgICAgPG5hdiBjbGFzcz0ibmF2YmFyIG5hdmJhci1leHBhbmQtbGciPgogICAgICAgIDxkaXYgY2xhc3M9ImNvbnRhaW5lciI+CiAgICAgICAgICA8YSBjbGFzcz0ibmF2YmFyLWJyYW5kIHdjZy1icmFuZCBtYi0wIiBocmVmPSJ7JSB1cmwgJ3BvcnRhbDpob21lJyAlfSI+V0NHIE9uZTwvYT4KICAgICAgICAgIDxhIGNsYXNzPSJ3Y2ctaG9tZS1saW5rIGQtbm9uZSBkLW1kLWlubGluZS1mbGV4IiBocmVmPSJ7JSB1cmwgJ3BvcnRhbDpob21lJyAlfSIgdGl0bGU9IlZvbHZlciBhbCBtZW7DuiBwcmluY2lwYWwiPgogICAgICAgICAgICDihpAgTWVuw7ogcHJpbmNpcGFsCiAgICAgICAgICA8L2E+CiAgICAgICAgICA8YnV0dG9uIGNsYXNzPSJuYXZiYXItdG9nZ2xlciBib3JkZXItMCIgdHlwZT0iYnV0dG9uIiBkYXRhLWJzLXRvZ2dsZT0iY29sbGFwc2UiIGRhdGEtYnMtdGFyZ2V0PSIjd2NnTmF2IiBhcmlhLWNvbnRyb2xzPSJ3Y2dOYXYiIGFyaWEtZXhwYW5kZWQ9ImZhbHNlIiBhcmlhLWxhYmVsPSJNZW7DuiI+CiAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJuYXZiYXItdG9nZ2xlci1pY29uIiBzdHlsZT0iZmlsdGVyOiBpbnZlcnQoMC40NSk7Ij48L3NwYW4+CiAgICAgICAgICA8L2J1dHRvbj4KICAgICAgICAgIDxkaXYgY2xhc3M9ImNvbGxhcHNlIG5hdmJhci1jb2xsYXBzZSIgaWQ9IndjZ05hdiI+CiAgICAgICAgICAgIHslIGlmIHVzZXIuaXNfYXV0aGVudGljYXRlZCAlfQogICAgICAgICAgICA8dWwgY2xhc3M9Im5hdmJhci1uYXYgd2NnLW5hdi1wcmltYXJ5IG1lLWF1dG8gbWItMiBtYi1sZy0wIG10LTIgbXQtbGctMCI+CiAgICAgICAgICAgICAgPGxpIGNsYXNzPSJuYXYtaXRlbSBkLW1kLW5vbmUiPgogICAgICAgICAgICAgICAgPGEgY2xhc3M9Im5hdi1saW5rIGZ3LXNlbWlib2xkIiBocmVmPSJ7JSB1cmwgJ3BvcnRhbDpob21lJyAlfSI+4oaQIE1lbsO6IHByaW5jaXBhbDwvYT4KICAgICAgICAgICAgICA8L2xpPgogICAgICAgICAgICAgIDxsaSBjbGFzcz0ibmF2LWl0ZW0iPgogICAgICAgICAgICAgICAgPGEgY2xhc3M9Im5hdi1saW5reyUgaWYgJy9wZ2MvJyBpbiByZXF1ZXN0LnBhdGggb3IgJy90YWJsZXJvLycgaW4gcmVxdWVzdC5wYXRoICV9IGFjdGl2ZXslIGVuZGlmICV9IiBocmVmPSJ7JSB1cmwgJ3BnYzpkYXNoYm9hcmQnICV9Ij48c3BhbiBjbGFzcz0id2NnLW1vZC1pY28iIGFyaWEtaGlkZGVuPSJ0cnVlIj7wn5OKPC9zcGFuPiBQR0M8L2E+CiAgICAgICAgICAgICAgPC9saT4KICAgICAgICAgICAgICA8bGkgY2xhc3M9Im5hdi1pdGVtIj4KICAgICAgICAgICAgICAgIDxhIGNsYXNzPSJuYXYtbGlua3slIGlmICcvcGdvLycgaW4gcmVxdWVzdC5wYXRoICV9IGFjdGl2ZXslIGVuZGlmICV9IiBocmVmPSJ7JSB1cmwgJ3BnbzpkYXNoYm9hcmQnICV9Ij48c3BhbiBjbGFzcz0id2NnLW1vZC1pY28iIGFyaWEtaGlkZGVuPSJ0cnVlIj7impnvuI88L3NwYW4+IFBHTzwvYT4KICAgICAgICAgICAgICA8L2xpPgogICAgICAgICAgICAgIDxsaSBjbGFzcz0ibmF2LWl0ZW0iPgogICAgICAgICAgICAgICAgPGEgY2xhc3M9Im5hdi1saW5reyUgaWYgJy9jcm0vJyBpbiByZXF1ZXN0LnBhdGggJX0gYWN0aXZleyUgZW5kaWYgJX0iIGhyZWY9InslIHVybCAnY3JtOmVudGlkYWRfbGlzdCcgJX0iPjxzcGFuIGNsYXNzPSJ3Y2ctbW9kLWljbyIgYXJpYS1oaWRkZW49InRydWUiPvCfkaU8L3NwYW4+IENSTTwvYT4KICAgICAgICAgICAgICA8L2xpPgogICAgICAgICAgICAgIDxsaSBjbGFzcz0ibmF2LWl0ZW0iPgogICAgICAgICAgICAgICAgPGEgY2xhc3M9Im5hdi1saW5reyUgaWYgJy9yaXNrLycgaW4gcmVxdWVzdC5wYXRoICV9IGFjdGl2ZXslIGVuZGlmICV9IiBocmVmPSJ7JSB1cmwgJ3Jpc2s6Y29tYW5kb19iYWxvbicgJX0iPjxzcGFuIGNsYXNzPSJ3Y2ctbW9kLWljbyIgYXJpYS1oaWRkZW49InRydWUiPuKavTwvc3Bhbj4gQmFsw7NuIGRlIFJpZXNnbzwvYT4KICAgICAgICAgICAgICA8L2xpPgogICAgICAgICAgICA8L3VsPgogICAgICAgICAgICA8dWwgY2xhc3M9Im5hdmJhci1uYXYgd2NnLW5hdi1zZWNvbmRhcnkgYWxpZ24taXRlbXMtbGctY2VudGVyIGdhcC1sZy0xIj4KICAgICAgICAgICAgICA8bGkgY2xhc3M9Im5hdi1pdGVtIGRyb3Bkb3duIj4KICAgICAgICAgICAgICAgIDxhIGNsYXNzPSJuYXYtbGluayBkcm9wZG93bi10b2dnbGV7JSBpZiAnL2ltcG9ydGFjaW9uZXMvJyBpbiByZXF1ZXN0LnBhdGggb3IgJy9wYW5lbC9lc3RhZG8nIGluIHJlcXVlc3QucGF0aCAlfSBhY3RpdmV7JSBlbmRpZiAlfSIgaHJlZj0iIyIgcm9sZT0iYnV0dG9uIiBkYXRhLWJzLXRvZ2dsZT0iZHJvcGRvd24iIGFyaWEtZXhwYW5kZWQ9ImZhbHNlIj4KICAgICAgICAgICAgICAgICAgQWRtaW5pc3RyYWNpw7NuCiAgICAgICAgICAgICAgICA8L2E+CiAgICAgICAgICAgICAgICA8dWwgY2xhc3M9ImRyb3Bkb3duLW1lbnUgZHJvcGRvd24tbWVudS1lbmQiPgogICAgICAgICAgICAgICAgICA8bGk+PGg2IGNsYXNzPSJkcm9wZG93bi1oZWFkZXIiPkNvbmZpZ3VyYWNpw7NuIGRlbCBzaXN0ZW1hPC9oNj48L2xpPgogICAgICAgICAgICAgICAgICA8bGk+CiAgICAgICAgICAgICAgICAgICAgPGEgY2xhc3M9ImRyb3Bkb3duLWl0ZW17JSBpZiAnL2ltcG9ydGFjaW9uZXMvJyBpbiByZXF1ZXN0LnBhdGggJX0gYWN0aXZleyUgZW5kaWYgJX0iIGhyZWY9InslIHVybCAnaW1wb3J0czppbXBvcnRfaHViJyAlfSI+CiAgICAgICAgICAgICAgICAgICAgICBJbXBvcnRhY2nDs24gR2VuZXJhbAogICAgICAgICAgICAgICAgICAgIDwvYT4KICAgICAgICAgICAgICAgICAgPC9saT4KICAgICAgICAgICAgICAgICAgPGxpPjxhIGNsYXNzPSJkcm9wZG93bi1pdGVtIiBocmVmPSJ7JSB1cmwgJ3BvcnRhbDplc3RhZG8nICV9Ij5Fc3RhZG8gZGVsIHNpc3RlbWE8L2E+PC9saT4KICAgICAgICAgICAgICAgICAgPGxpPjxhIGNsYXNzPSJkcm9wZG93bi1pdGVtIiBocmVmPSJ7JSB1cmwgJ3BvcnRhbDpheXVkYScgJX0iPkd1w61hIGRlIHVzbzwvYT48L2xpPgogICAgICAgICAgICAgICAgICB7JSBpZiB1c2VyLmlzX3N1cGVydXNlciAlfQogICAgICAgICAgICAgICAgICA8bGk+PGhyIGNsYXNzPSJkcm9wZG93bi1kaXZpZGVyIj48L2xpPgogICAgICAgICAgICAgICAgICA8bGk+PGEgY2xhc3M9ImRyb3Bkb3duLWl0ZW0iIGhyZWY9Ii9hZG1pbi8iIHRhcmdldD0iX2JsYW5rIiByZWw9Im5vb3BlbmVyIj5BZG1pbiBEamFuZ288L2E+PC9saT4KICAgICAgICAgICAgICAgICAgPGxpPjxhIGNsYXNzPSJkcm9wZG93bi1pdGVtIiBocmVmPSJ7JSB1cmwgJ3BnYzphZG1pbl9tb250aGx5JyAlfSI+QWRtaW4gUEdDIChwZXLDrW9kbyk8L2E+PC9saT4KICAgICAgICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgICAgICAgIDwvdWw+CiAgICAgICAgICAgICAgPC9saT4KICAgICAgICAgICAgICA8bGkgY2xhc3M9Im5hdi1pdGVtIj4KICAgICAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJuYXYtbGluayBkaXNhYmxlZCIgc3R5bGU9Im9wYWNpdHk6MC43OyI+e3sgdXNlci5nZXRfdXNlcm5hbWUgfX08L3NwYW4+CiAgICAgICAgICAgICAgPC9saT4KICAgICAgICAgICAgICA8bGkgY2xhc3M9Im5hdi1pdGVtIj4KICAgICAgICAgICAgICAgIDxmb3JtIG1ldGhvZD0icG9zdCIgYWN0aW9uPSJ7JSB1cmwgJ2xvZ291dCcgJX0iIGNsYXNzPSJkLWlubGluZSI+CiAgICAgICAgICAgICAgICAgIHslIGNzcmZfdG9rZW4gJX0KICAgICAgICAgICAgICAgICAgPGJ1dHRvbiB0eXBlPSJzdWJtaXQiIGNsYXNzPSJidG4gYnRuLWxpbmsgbmF2LWxpbmsiPlNhbGlyPC9idXR0b24+CiAgICAgICAgICAgICAgICA8L2Zvcm0+CiAgICAgICAgICAgICAgPC9saT4KICAgICAgICAgICAgPC91bD4KICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgIDwvZGl2PgogICAgICAgIDwvZGl2PgogICAgICA8L25hdj4KICAgIDwvaGVhZGVyPgoKICAgIDxtYWluPgogICAgICAgIDxkaXYgY2xhc3M9ImNvbnRhaW5lciI+CiAgICAgICAgICAgIHslIGlmIG1lc3NhZ2VzICV9CiAgICAgICAgICAgIHslIGZvciBtZXNzYWdlIGluIG1lc3NhZ2VzICV9CiAgICAgICAgICAgIDxkaXYgY2xhc3M9ImFsZXJ0IGFsZXJ0LXslIGlmIG1lc3NhZ2UudGFncyA9PSAnZXJyb3InICV9ZGFuZ2VyeyUgZWxpZiBtZXNzYWdlLnRhZ3MgPT0gJ3dhcm5pbmcnICV9d2FybmluZ3slIGVsaWYgbWVzc2FnZS50YWdzID09ICdzdWNjZXNzJyAlfXN1Y2Nlc3N7JSBlbHNlICV9aW5mb3slIGVuZGlmICV9IG10LTIiPnt7IG1lc3NhZ2UgfX08L2Rpdj4KICAgICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgIHslIGlmIGJyZWFkY3J1bWJzICV9CiAgICAgICAgICAgIHslIGluY2x1ZGUgImluY2x1ZGVzL2JyZWFkY3J1bWJzLmh0bWwiICV9CiAgICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICAgIHslIGJsb2NrIGNvbnRlbnQgJX17JSBlbmRibG9jayAlfQogICAgICAgIDwvZGl2PgogICAgPC9tYWluPgogICAgPGZvb3RlciBjbGFzcz0id2NnLWZvb3RlciBtdC1hdXRvIj4KICAgICAgPGRpdiBjbGFzcz0iY29udGFpbmVyIj5XQ0cgT25lIOKAlCBXb3JraW5nIENhcGl0YWwgR3JvdXA8L2Rpdj4KICAgIDwvZm9vdGVyPgogICAgPHNjcmlwdCBzcmM9Imh0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9ucG0vYm9vdHN0cmFwQDUuMy4zL2Rpc3QvanMvYm9vdHN0cmFwLmJ1bmRsZS5taW4uanMiPjwvc2NyaXB0PgogICAgeyUgYmxvY2sgZXh0cmFfanMgJX17JSBlbmRibG9jayAlfQo8L2JvZHk+CjwvaHRtbD4K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/crm/crmcontactolist.html
PATH_JSON="templates/crm/crmcontactolist.html"
FILENAME=crmcontactolist.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=34
SIZE_BYTES_UTF8=1514
CONTENT_SHA256=6a32bef418fd9b3069a1c9296321a8bba21e27c645fb322a19507d13b5a3251f
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
{% block title %}Contactos — CRM{% endblock %}
{% block content %}
<div class="d-flex justify-content-between mb-3 mt-2">
  <div class="wcg-report-head">
    <h1 class="h4 fw-semibold mb-0">CRM — Contactos</h1>
    {% include "includes/module_mark.html" with module="crm" %}
  </div>
  <a href="{% url 'crm:entidad_list' %}" class="btn btn-sm btn-outline-secondary">← Entidades</a>
</div>
<form method="get" class="mb-3">
  <input type="search" name="q" value="{{ request.GET.q }}" class="form-control form-control-sm" placeholder="Buscar contacto, email o cliente" style="max-width:360px">
</form>
<div class="card border-0 shadow-sm">
  <div class="table-responsive">
    <table class="table table-hover table-wcg mb-0 small">
      <thead><tr><th>Contacto</th><th>Email</th><th>Teléfono</th><th>Entidad</th><th></th></tr></thead>
      <tbody>
        {% for c in contactos %}
        <tr>
          <td>{{ c.nombre }}{% if c.es_principal %} <span class="badge text-bg-info">Principal</span>{% endif %}</td>
          <td>{{ c.email|default:"—" }}</td>
          <td>{{ c.telefono|default:"—" }}</td>
          <td>{{ c.entidad.nombre }}</td>
          <td><a href="{% url 'crm:entidad_detail' c.entidad.codigo %}" class="btn btn-sm btn-outline-primary">Ver</a></td>
        </tr>
        {% empty %}
        <tr><td colspan="5" class="text-muted text-center py-4">Sin contactos.</td></tr>
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
00002|{% block title %}Contactos — CRM{% endblock %}
00003|{% block content %}
00004|<div class="d-flex justify-content-between mb-3 mt-2">
00005|  <div class="wcg-report-head">
00006|    <h1 class="h4 fw-semibold mb-0">CRM — Contactos</h1>
00007|    {% include "includes/module_mark.html" with module="crm" %}
00008|  </div>
00009|  <a href="{% url 'crm:entidad_list' %}" class="btn btn-sm btn-outline-secondary">← Entidades</a>
00010|</div>
00011|<form method="get" class="mb-3">
00012|  <input type="search" name="q" value="{{ request.GET.q }}" class="form-control form-control-sm" placeholder="Buscar contacto, email o cliente" style="max-width:360px">
00013|</form>
00014|<div class="card border-0 shadow-sm">
00015|  <div class="table-responsive">
00016|    <table class="table table-hover table-wcg mb-0 small">
00017|      <thead><tr><th>Contacto</th><th>Email</th><th>Teléfono</th><th>Entidad</th><th></th></tr></thead>
00018|      <tbody>
00019|        {% for c in contactos %}
00020|        <tr>
00021|          <td>{{ c.nombre }}{% if c.es_principal %} <span class="badge text-bg-info">Principal</span>{% endif %}</td>
00022|          <td>{{ c.email|default:"—" }}</td>
00023|          <td>{{ c.telefono|default:"—" }}</td>
00024|          <td>{{ c.entidad.nombre }}</td>
00025|          <td><a href="{% url 'crm:entidad_detail' c.entidad.codigo %}" class="btn btn-sm btn-outline-primary">Ver</a></td>
00026|        </tr>
00027|        {% empty %}
00028|        <tr><td colspan="5" class="text-muted text-center py-4">Sin contactos.</td></tr>
00029|        {% endfor %}
00030|      </tbody>
00031|    </table>
00032|  </div>
00033|</div>
00034|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1Db250YWN0b3Mg4oCUIENSTXslIGVuZGJsb2NrICV9CnslIGJsb2NrIGNvbnRlbnQgJX0KPGRpdiBjbGFzcz0iZC1mbGV4IGp1c3RpZnktY29udGVudC1iZXR3ZWVuIG1iLTMgbXQtMiI+CiAgPGRpdiBjbGFzcz0id2NnLXJlcG9ydC1oZWFkIj4KICAgIDxoMSBjbGFzcz0iaDQgZnctc2VtaWJvbGQgbWItMCI+Q1JNIOKAlCBDb250YWN0b3M8L2gxPgogICAgeyUgaW5jbHVkZSAiaW5jbHVkZXMvbW9kdWxlX21hcmsuaHRtbCIgd2l0aCBtb2R1bGU9ImNybSIgJX0KICA8L2Rpdj4KICA8YSBocmVmPSJ7JSB1cmwgJ2NybTplbnRpZGFkX2xpc3QnICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1zZWNvbmRhcnkiPuKGkCBFbnRpZGFkZXM8L2E+CjwvZGl2Pgo8Zm9ybSBtZXRob2Q9ImdldCIgY2xhc3M9Im1iLTMiPgogIDxpbnB1dCB0eXBlPSJzZWFyY2giIG5hbWU9InEiIHZhbHVlPSJ7eyByZXF1ZXN0LkdFVC5xIH19IiBjbGFzcz0iZm9ybS1jb250cm9sIGZvcm0tY29udHJvbC1zbSIgcGxhY2Vob2xkZXI9IkJ1c2NhciBjb250YWN0bywgZW1haWwgbyBjbGllbnRlIiBzdHlsZT0ibWF4LXdpZHRoOjM2MHB4Ij4KPC9mb3JtPgo8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSI+CiAgPGRpdiBjbGFzcz0idGFibGUtcmVzcG9uc2l2ZSI+CiAgICA8dGFibGUgY2xhc3M9InRhYmxlIHRhYmxlLWhvdmVyIHRhYmxlLXdjZyBtYi0wIHNtYWxsIj4KICAgICAgPHRoZWFkPjx0cj48dGg+Q29udGFjdG88L3RoPjx0aD5FbWFpbDwvdGg+PHRoPlRlbMOpZm9ubzwvdGg+PHRoPkVudGlkYWQ8L3RoPjx0aD48L3RoPjwvdHI+PC90aGVhZD4KICAgICAgPHRib2R5PgogICAgICAgIHslIGZvciBjIGluIGNvbnRhY3RvcyAlfQogICAgICAgIDx0cj4KICAgICAgICAgIDx0ZD57eyBjLm5vbWJyZSB9fXslIGlmIGMuZXNfcHJpbmNpcGFsICV9IDxzcGFuIGNsYXNzPSJiYWRnZSB0ZXh0LWJnLWluZm8iPlByaW5jaXBhbDwvc3Bhbj57JSBlbmRpZiAlfTwvdGQ+CiAgICAgICAgICA8dGQ+e3sgYy5lbWFpbHxkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgIDx0ZD57eyBjLnRlbGVmb25vfGRlZmF1bHQ6IuKAlCIgfX08L3RkPgogICAgICAgICAgPHRkPnt7IGMuZW50aWRhZC5ub21icmUgfX08L3RkPgogICAgICAgICAgPHRkPjxhIGhyZWY9InslIHVybCAnY3JtOmVudGlkYWRfZGV0YWlsJyBjLmVudGlkYWQuY29kaWdvICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1wcmltYXJ5Ij5WZXI8L2E+PC90ZD4KICAgICAgICA8L3RyPgogICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgPHRyPjx0ZCBjb2xzcGFuPSI1IiBjbGFzcz0idGV4dC1tdXRlZCB0ZXh0LWNlbnRlciBweS00Ij5TaW4gY29udGFjdG9zLjwvdGQ+PC90cj4KICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgPC90Ym9keT4KICAgIDwvdGFibGU+CiAgPC9kaXY+CjwvZGl2Pgp7JSBlbmRibG9jayAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/crm/crmentitydetail.html
PATH_JSON="templates/crm/crmentitydetail.html"
FILENAME=crmentitydetail.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=124
SIZE_BYTES_UTF8=5224
CONTENT_SHA256=69db5d33d0777c8516ac8025b19d00489ac1846a1e5388276ba191d2c5e6dc81
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
{% block title %}{{ entidad.nombre }} — CRM — WCG One{% endblock %}
{% block content %}
<div class="mb-2 mt-1">
  <a href="{% url 'crm:entidad_list' %}" class="btn btn-sm btn-outline-secondary">← Volver a clientes</a>
</div>
<div class="d-flex justify-content-between align-items-start mb-3">
  <div>
    <h1 class="h4 fw-semibold mb-1">{{ entidad.nombre }}</h1>
    <p class="text-muted small mb-0">
      {{ entidad.get_tipo_display }}
      {% if entidad.nit %} · NIT {{ entidad.nit }}{% endif %}
      {% if entidad.unidad_negocio %} · {{ entidad.unidad_negocio.nombre }}{% endif %}
    </p>
  </div>
  {% if entidad.activa %}
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
          <dt class="col-5">Código</dt><dd class="col-7">{{ entidad.codigo }}</dd>
          <dt class="col-5">Unidad</dt><dd class="col-7">{{ entidad.unidad_negocio.nombre|default:"—" }}</dd>
          <dt class="col-5">Email</dt><dd class="col-7">{{ contacto_principal.email|default:"—" }}</dd>
          <dt class="col-5">Teléfono</dt><dd class="col-7">{{ contacto_principal.telefono|default:"—" }}</dd>
          <dt class="col-5">Productos</dt><dd class="col-7">{{ productos|length }}</dd>
        </dl>
        {% if entidad.notas %}
        <hr>
        <p class="mb-0 text-muted">{{ entidad.notas }}</p>
        {% endif %}
        <div class="mt-3 d-flex flex-wrap gap-1">
          <a class="btn btn-sm btn-primary" href="{% url 'crm:nueva_interaccion' entidad.codigo %}">Nueva interacción</a>
          <a class="btn btn-sm btn-outline-primary" href="{% url 'crm:nueva_tarea' entidad.codigo %}">Nueva tarea</a>
          <a class="btn btn-sm btn-outline-secondary" href="{% url 'risk:cliente_detail' entidad.codigo %}">Ver en Riesgo</a>
        </div>
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
            <tr>
              <td>{{ c.nombre }}{% if c.es_principal %} <span class="badge text-bg-info">Principal</span>{% endif %}</td>
              <td>{{ c.cargo|default:"—" }}</td>
              <td>{{ c.email|default:"—" }}</td>
              <td>{{ c.telefono|default:"—" }}</td>
            </tr>
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
            {% for rel in productos %}
            <tr>
              <td>{{ rel.producto.nombre }}</td>
              <td>{{ rel.producto.unidad_negocio.nombre|default:"—" }}</td>
              <td>{{ rel.get_estado_display }}</td>
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
              <strong>{{ i.fecha|date:"d/m/Y" }}</strong> — {{ i.get_tipo_display }}: {{ i.asunto }}
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
              {{ t.titulo|truncatechars:60 }}
              {% if t.fecha_vencimiento %}<span class="text-muted">· {{ t.fecha_vencimiento|date:"d/m/Y" }}</span>{% endif %}
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
00001|{% extends "base_wcg.html" %}
00002|{% block title %}{{ entidad.nombre }} — CRM — WCG One{% endblock %}
00003|{% block content %}
00004|<div class="mb-2 mt-1">
00005|  <a href="{% url 'crm:entidad_list' %}" class="btn btn-sm btn-outline-secondary">← Volver a clientes</a>
00006|</div>
00007|<div class="d-flex justify-content-between align-items-start mb-3">
00008|  <div>
00009|    <h1 class="h4 fw-semibold mb-1">{{ entidad.nombre }}</h1>
00010|    <p class="text-muted small mb-0">
00011|      {{ entidad.get_tipo_display }}
00012|      {% if entidad.nit %} · NIT {{ entidad.nit }}{% endif %}
00013|      {% if entidad.unidad_negocio %} · {{ entidad.unidad_negocio.nombre }}{% endif %}
00014|    </p>
00015|  </div>
00016|  {% if entidad.activa %}
00017|  <span class="badge text-bg-success">Activo</span>
00018|  {% else %}
00019|  <span class="badge text-bg-secondary">Inactivo</span>
00020|  {% endif %}
00021|</div>
00022|
00023|<div class="row g-3">
00024|  <div class="col-lg-4">
00025|    <div class="card border-0 shadow-sm h-100">
00026|      <div class="card-header bg-white fw-semibold">Datos generales</div>
00027|      <div class="card-body small">
00028|        <dl class="row mb-0">
00029|          <dt class="col-5">Código</dt><dd class="col-7">{{ entidad.codigo }}</dd>
00030|          <dt class="col-5">Unidad</dt><dd class="col-7">{{ entidad.unidad_negocio.nombre|default:"—" }}</dd>
00031|          <dt class="col-5">Email</dt><dd class="col-7">{{ contacto_principal.email|default:"—" }}</dd>
00032|          <dt class="col-5">Teléfono</dt><dd class="col-7">{{ contacto_principal.telefono|default:"—" }}</dd>
00033|          <dt class="col-5">Productos</dt><dd class="col-7">{{ productos|length }}</dd>
00034|        </dl>
00035|        {% if entidad.notas %}
00036|        <hr>
00037|        <p class="mb-0 text-muted">{{ entidad.notas }}</p>
00038|        {% endif %}
00039|        <div class="mt-3 d-flex flex-wrap gap-1">
00040|          <a class="btn btn-sm btn-primary" href="{% url 'crm:nueva_interaccion' entidad.codigo %}">Nueva interacción</a>
00041|          <a class="btn btn-sm btn-outline-primary" href="{% url 'crm:nueva_tarea' entidad.codigo %}">Nueva tarea</a>
00042|          <a class="btn btn-sm btn-outline-secondary" href="{% url 'risk:cliente_detail' entidad.codigo %}">Ver en Riesgo</a>
00043|        </div>
00044|      </div>
00045|    </div>
00046|  </div>
00047|
00048|  <div class="col-lg-8">
00049|    <div class="card border-0 shadow-sm mb-3">
00050|      <div class="card-header bg-white fw-semibold">Contactos</div>
00051|      <div class="table-responsive">
00052|        <table class="table table-sm mb-0">
00053|          <thead><tr><th>Nombre</th><th>Cargo</th><th>Email</th><th>Teléfono</th></tr></thead>
00054|          <tbody>
00055|            {% for c in contactos %}
00056|            <tr>
00057|              <td>{{ c.nombre }}{% if c.es_principal %} <span class="badge text-bg-info">Principal</span>{% endif %}</td>
00058|              <td>{{ c.cargo|default:"—" }}</td>
00059|              <td>{{ c.email|default:"—" }}</td>
00060|              <td>{{ c.telefono|default:"—" }}</td>
00061|            </tr>
00062|            {% empty %}
00063|            <tr><td colspan="4" class="text-muted text-center py-3">Sin contactos.</td></tr>
00064|            {% endfor %}
00065|          </tbody>
00066|        </table>
00067|      </div>
00068|    </div>
00069|
00070|    <div class="card border-0 shadow-sm mb-3">
00071|      <div class="card-header bg-white fw-semibold">Productos relacionados</div>
00072|      <div class="table-responsive">
00073|        <table class="table table-sm mb-0">
00074|          <thead><tr><th>Producto</th><th>Unidad</th><th>Estado</th><th>Inicio</th></tr></thead>
00075|          <tbody>
00076|            {% for rel in productos %}
00077|            <tr>
00078|              <td>{{ rel.producto.nombre }}</td>
00079|              <td>{{ rel.producto.unidad_negocio.nombre|default:"—" }}</td>
00080|              <td>{{ rel.get_estado_display }}</td>
00081|              <td>{{ rel.fecha_inicio|date:"d/m/Y"|default:"—" }}</td>
00082|            </tr>
00083|            {% empty %}
00084|            <tr><td colspan="4" class="text-muted text-center py-3">Sin productos relacionados.</td></tr>
00085|            {% endfor %}
00086|          </tbody>
00087|        </table>
00088|      </div>
00089|    </div>
00090|
00091|    <div class="row g-3">
00092|      <div class="col-md-6">
00093|        <div class="card border-0 shadow-sm h-100">
00094|          <div class="card-header bg-white fw-semibold">Interacciones recientes</div>
00095|          <ul class="list-group list-group-flush small">
00096|            {% for i in interacciones %}
00097|            <li class="list-group-item">
00098|              <strong>{{ i.fecha|date:"d/m/Y" }}</strong> — {{ i.get_tipo_display }}: {{ i.asunto }}
00099|            </li>
00100|            {% empty %}
00101|            <li class="list-group-item text-muted">Sin interacciones.</li>
00102|            {% endfor %}
00103|          </ul>
00104|        </div>
00105|      </div>
00106|      <div class="col-md-6">
00107|        <div class="card border-0 shadow-sm h-100">
00108|          <div class="card-header bg-white fw-semibold">Tareas abiertas</div>
00109|          <ul class="list-group list-group-flush small">
00110|            {% for t in tareas %}
00111|            <li class="list-group-item">
00112|              {{ t.titulo|truncatechars:60 }}
00113|              {% if t.fecha_vencimiento %}<span class="text-muted">· {{ t.fecha_vencimiento|date:"d/m/Y" }}</span>{% endif %}
00114|            </li>
00115|            {% empty %}
00116|            <li class="list-group-item text-muted">Sin tareas pendientes.</li>
00117|            {% endfor %}
00118|          </ul>
00119|        </div>
00120|      </div>
00121|    </div>
00122|  </div>
00123|</div>
00124|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX17eyBlbnRpZGFkLm5vbWJyZSB9fSDigJQgQ1JNIOKAlCBXQ0cgT25leyUgZW5kYmxvY2sgJX0KeyUgYmxvY2sgY29udGVudCAlfQo8ZGl2IGNsYXNzPSJtYi0yIG10LTEiPgogIDxhIGhyZWY9InslIHVybCAnY3JtOmVudGlkYWRfbGlzdCcgJX0iIGNsYXNzPSJidG4gYnRuLXNtIGJ0bi1vdXRsaW5lLXNlY29uZGFyeSI+4oaQIFZvbHZlciBhIGNsaWVudGVzPC9hPgo8L2Rpdj4KPGRpdiBjbGFzcz0iZC1mbGV4IGp1c3RpZnktY29udGVudC1iZXR3ZWVuIGFsaWduLWl0ZW1zLXN0YXJ0IG1iLTMiPgogIDxkaXY+CiAgICA8aDEgY2xhc3M9Img0IGZ3LXNlbWlib2xkIG1iLTEiPnt7IGVudGlkYWQubm9tYnJlIH19PC9oMT4KICAgIDxwIGNsYXNzPSJ0ZXh0LW11dGVkIHNtYWxsIG1iLTAiPgogICAgICB7eyBlbnRpZGFkLmdldF90aXBvX2Rpc3BsYXkgfX0KICAgICAgeyUgaWYgZW50aWRhZC5uaXQgJX0gwrcgTklUIHt7IGVudGlkYWQubml0IH19eyUgZW5kaWYgJX0KICAgICAgeyUgaWYgZW50aWRhZC51bmlkYWRfbmVnb2NpbyAlfSDCtyB7eyBlbnRpZGFkLnVuaWRhZF9uZWdvY2lvLm5vbWJyZSB9fXslIGVuZGlmICV9CiAgICA8L3A+CiAgPC9kaXY+CiAgeyUgaWYgZW50aWRhZC5hY3RpdmEgJX0KICA8c3BhbiBjbGFzcz0iYmFkZ2UgdGV4dC1iZy1zdWNjZXNzIj5BY3Rpdm88L3NwYW4+CiAgeyUgZWxzZSAlfQogIDxzcGFuIGNsYXNzPSJiYWRnZSB0ZXh0LWJnLXNlY29uZGFyeSI+SW5hY3Rpdm88L3NwYW4+CiAgeyUgZW5kaWYgJX0KPC9kaXY+Cgo8ZGl2IGNsYXNzPSJyb3cgZy0zIj4KICA8ZGl2IGNsYXNzPSJjb2wtbGctNCI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSBoLTEwMCI+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtaGVhZGVyIGJnLXdoaXRlIGZ3LXNlbWlib2xkIj5EYXRvcyBnZW5lcmFsZXM8L2Rpdj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1ib2R5IHNtYWxsIj4KICAgICAgICA8ZGwgY2xhc3M9InJvdyBtYi0wIj4KICAgICAgICAgIDxkdCBjbGFzcz0iY29sLTUiPkPDs2RpZ288L2R0PjxkZCBjbGFzcz0iY29sLTciPnt7IGVudGlkYWQuY29kaWdvIH19PC9kZD4KICAgICAgICAgIDxkdCBjbGFzcz0iY29sLTUiPlVuaWRhZDwvZHQ+PGRkIGNsYXNzPSJjb2wtNyI+e3sgZW50aWRhZC51bmlkYWRfbmVnb2Npby5ub21icmV8ZGVmYXVsdDoi4oCUIiB9fTwvZGQ+CiAgICAgICAgICA8ZHQgY2xhc3M9ImNvbC01Ij5FbWFpbDwvZHQ+PGRkIGNsYXNzPSJjb2wtNyI+e3sgY29udGFjdG9fcHJpbmNpcGFsLmVtYWlsfGRlZmF1bHQ6IuKAlCIgfX08L2RkPgogICAgICAgICAgPGR0IGNsYXNzPSJjb2wtNSI+VGVsw6lmb25vPC9kdD48ZGQgY2xhc3M9ImNvbC03Ij57eyBjb250YWN0b19wcmluY2lwYWwudGVsZWZvbm98ZGVmYXVsdDoi4oCUIiB9fTwvZGQ+CiAgICAgICAgICA8ZHQgY2xhc3M9ImNvbC01Ij5Qcm9kdWN0b3M8L2R0PjxkZCBjbGFzcz0iY29sLTciPnt7IHByb2R1Y3Rvc3xsZW5ndGggfX08L2RkPgogICAgICAgIDwvZGw+CiAgICAgICAgeyUgaWYgZW50aWRhZC5ub3RhcyAlfQogICAgICAgIDxocj4KICAgICAgICA8cCBjbGFzcz0ibWItMCB0ZXh0LW11dGVkIj57eyBlbnRpZGFkLm5vdGFzIH19PC9wPgogICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgPGRpdiBjbGFzcz0ibXQtMyBkLWZsZXggZmxleC13cmFwIGdhcC0xIj4KICAgICAgICAgIDxhIGNsYXNzPSJidG4gYnRuLXNtIGJ0bi1wcmltYXJ5IiBocmVmPSJ7JSB1cmwgJ2NybTpudWV2YV9pbnRlcmFjY2lvbicgZW50aWRhZC5jb2RpZ28gJX0iPk51ZXZhIGludGVyYWNjacOzbjwvYT4KICAgICAgICAgIDxhIGNsYXNzPSJidG4gYnRuLXNtIGJ0bi1vdXRsaW5lLXByaW1hcnkiIGhyZWY9InslIHVybCAnY3JtOm51ZXZhX3RhcmVhJyBlbnRpZGFkLmNvZGlnbyAlfSI+TnVldmEgdGFyZWE8L2E+CiAgICAgICAgICA8YSBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1zZWNvbmRhcnkiIGhyZWY9InslIHVybCAncmlzazpjbGllbnRlX2RldGFpbCcgZW50aWRhZC5jb2RpZ28gJX0iPlZlciBlbiBSaWVzZ288L2E+CiAgICAgICAgPC9kaXY+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CiAgPC9kaXY+CgogIDxkaXYgY2xhc3M9ImNvbC1sZy04Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIG1iLTMiPgogICAgICA8ZGl2IGNsYXNzPSJjYXJkLWhlYWRlciBiZy13aGl0ZSBmdy1zZW1pYm9sZCI+Q29udGFjdG9zPC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9InRhYmxlLXJlc3BvbnNpdmUiPgogICAgICAgIDx0YWJsZSBjbGFzcz0idGFibGUgdGFibGUtc20gbWItMCI+CiAgICAgICAgICA8dGhlYWQ+PHRyPjx0aD5Ob21icmU8L3RoPjx0aD5DYXJnbzwvdGg+PHRoPkVtYWlsPC90aD48dGg+VGVsw6lmb25vPC90aD48L3RyPjwvdGhlYWQ+CiAgICAgICAgICA8dGJvZHk+CiAgICAgICAgICAgIHslIGZvciBjIGluIGNvbnRhY3RvcyAlfQogICAgICAgICAgICA8dHI+CiAgICAgICAgICAgICAgPHRkPnt7IGMubm9tYnJlIH19eyUgaWYgYy5lc19wcmluY2lwYWwgJX0gPHNwYW4gY2xhc3M9ImJhZGdlIHRleHQtYmctaW5mbyI+UHJpbmNpcGFsPC9zcGFuPnslIGVuZGlmICV9PC90ZD4KICAgICAgICAgICAgICA8dGQ+e3sgYy5jYXJnb3xkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgICAgICA8dGQ+e3sgYy5lbWFpbHxkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgICAgICA8dGQ+e3sgYy50ZWxlZm9ub3xkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICAgICAgPC90cj4KICAgICAgICAgICAgeyUgZW1wdHkgJX0KICAgICAgICAgICAgPHRyPjx0ZCBjb2xzcGFuPSI0IiBjbGFzcz0idGV4dC1tdXRlZCB0ZXh0LWNlbnRlciBweS0zIj5TaW4gY29udGFjdG9zLjwvdGQ+PC90cj4KICAgICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgICA8L3Rib2R5PgogICAgICAgIDwvdGFibGU+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CgogICAgPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20gbWItMyI+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtaGVhZGVyIGJnLXdoaXRlIGZ3LXNlbWlib2xkIj5Qcm9kdWN0b3MgcmVsYWNpb25hZG9zPC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9InRhYmxlLXJlc3BvbnNpdmUiPgogICAgICAgIDx0YWJsZSBjbGFzcz0idGFibGUgdGFibGUtc20gbWItMCI+CiAgICAgICAgICA8dGhlYWQ+PHRyPjx0aD5Qcm9kdWN0bzwvdGg+PHRoPlVuaWRhZDwvdGg+PHRoPkVzdGFkbzwvdGg+PHRoPkluaWNpbzwvdGg+PC90cj48L3RoZWFkPgogICAgICAgICAgPHRib2R5PgogICAgICAgICAgICB7JSBmb3IgcmVsIGluIHByb2R1Y3RvcyAlfQogICAgICAgICAgICA8dHI+CiAgICAgICAgICAgICAgPHRkPnt7IHJlbC5wcm9kdWN0by5ub21icmUgfX08L3RkPgogICAgICAgICAgICAgIDx0ZD57eyByZWwucHJvZHVjdG8udW5pZGFkX25lZ29jaW8ubm9tYnJlfGRlZmF1bHQ6IuKAlCIgfX08L3RkPgogICAgICAgICAgICAgIDx0ZD57eyByZWwuZ2V0X2VzdGFkb19kaXNwbGF5IH19PC90ZD4KICAgICAgICAgICAgICA8dGQ+e3sgcmVsLmZlY2hhX2luaWNpb3xkYXRlOiJkL20vWSJ8ZGVmYXVsdDoi4oCUIiB9fTwvdGQ+CiAgICAgICAgICAgIDwvdHI+CiAgICAgICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgICAgIDx0cj48dGQgY29sc3Bhbj0iNCIgY2xhc3M9InRleHQtbXV0ZWQgdGV4dC1jZW50ZXIgcHktMyI+U2luIHByb2R1Y3RvcyByZWxhY2lvbmFkb3MuPC90ZD48L3RyPgogICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICAgIDwvdGJvZHk+CiAgICAgICAgPC90YWJsZT4KICAgICAgPC9kaXY+CiAgICA8L2Rpdj4KCiAgICA8ZGl2IGNsYXNzPSJyb3cgZy0zIj4KICAgICAgPGRpdiBjbGFzcz0iY29sLW1kLTYiPgogICAgICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAgc2hhZG93LXNtIGgtMTAwIj4KICAgICAgICAgIDxkaXYgY2xhc3M9ImNhcmQtaGVhZGVyIGJnLXdoaXRlIGZ3LXNlbWlib2xkIj5JbnRlcmFjY2lvbmVzIHJlY2llbnRlczwvZGl2PgogICAgICAgICAgPHVsIGNsYXNzPSJsaXN0LWdyb3VwIGxpc3QtZ3JvdXAtZmx1c2ggc21hbGwiPgogICAgICAgICAgICB7JSBmb3IgaSBpbiBpbnRlcmFjY2lvbmVzICV9CiAgICAgICAgICAgIDxsaSBjbGFzcz0ibGlzdC1ncm91cC1pdGVtIj4KICAgICAgICAgICAgICA8c3Ryb25nPnt7IGkuZmVjaGF8ZGF0ZToiZC9tL1kiIH19PC9zdHJvbmc+IOKAlCB7eyBpLmdldF90aXBvX2Rpc3BsYXkgfX06IHt7IGkuYXN1bnRvIH19CiAgICAgICAgICAgIDwvbGk+CiAgICAgICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgICAgIDxsaSBjbGFzcz0ibGlzdC1ncm91cC1pdGVtIHRleHQtbXV0ZWQiPlNpbiBpbnRlcmFjY2lvbmVzLjwvbGk+CiAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgPC91bD4KICAgICAgICA8L2Rpdj4KICAgICAgPC9kaXY+CiAgICAgIDxkaXYgY2xhc3M9ImNvbC1tZC02Ij4KICAgICAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSBoLTEwMCI+CiAgICAgICAgICA8ZGl2IGNsYXNzPSJjYXJkLWhlYWRlciBiZy13aGl0ZSBmdy1zZW1pYm9sZCI+VGFyZWFzIGFiaWVydGFzPC9kaXY+CiAgICAgICAgICA8dWwgY2xhc3M9Imxpc3QtZ3JvdXAgbGlzdC1ncm91cC1mbHVzaCBzbWFsbCI+CiAgICAgICAgICAgIHslIGZvciB0IGluIHRhcmVhcyAlfQogICAgICAgICAgICA8bGkgY2xhc3M9Imxpc3QtZ3JvdXAtaXRlbSI+CiAgICAgICAgICAgICAge3sgdC50aXR1bG98dHJ1bmNhdGVjaGFyczo2MCB9fQogICAgICAgICAgICAgIHslIGlmIHQuZmVjaGFfdmVuY2ltaWVudG8gJX08c3BhbiBjbGFzcz0idGV4dC1tdXRlZCI+wrcge3sgdC5mZWNoYV92ZW5jaW1pZW50b3xkYXRlOiJkL20vWSIgfX08L3NwYW4+eyUgZW5kaWYgJX0KICAgICAgICAgICAgPC9saT4KICAgICAgICAgICAgeyUgZW1wdHkgJX0KICAgICAgICAgICAgPGxpIGNsYXNzPSJsaXN0LWdyb3VwLWl0ZW0gdGV4dC1tdXRlZCI+U2luIHRhcmVhcyBwZW5kaWVudGVzLjwvbGk+CiAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgPC91bD4KICAgICAgICA8L2Rpdj4KICAgICAgPC9kaXY+CiAgICA8L2Rpdj4KICA8L2Rpdj4KPC9kaXY+CnslIGVuZGJsb2NrICV9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/crm/crmentitylist.html
PATH_JSON="templates/crm/crmentitylist.html"
FILENAME=crmentitylist.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=126
SIZE_BYTES_UTF8=5358
CONTENT_SHA256=18fee5edc39508eb8cfb096ec816e226a6d8a9f6e8c16a3fe02e3d4efce4f54e
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
{% block title %}Clientes — CRM — WCG{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-2 mt-2">
  <div class="wcg-report-head">
    <h1 class="h4 fw-semibold mb-0">CRM — Clientes y entidades</h1>
    {% include "includes/module_mark.html" with module="crm" %}
  </div>
  <div class="d-flex gap-1 flex-wrap">
    <a href="{% url 'crm:export_entidades' %}?q={{ request.GET.q }}&tipo={{ request.GET.tipo }}&activo={{ request.GET.activo }}" class="btn btn-sm btn-outline-primary">Exportar CSV</a>
    <a href="{% url 'crm:contacto_list' %}" class="btn btn-sm btn-outline-secondary">Contactos</a>
    <a href="{% url 'crm:tarea_list' %}" class="btn btn-sm btn-outline-secondary">Tareas</a>
  </div>
</div>

<div class="card border-0 shadow-sm mb-3">
  <div class="card-body py-2 px-3 small">
    <div class="row g-2">
      <div class="col-md-3"><strong>Total:</strong> {{ summary.total }}</div>
      <div class="col-md-3"><strong>Activas:</strong> {{ summary.activas }}</div>
      <div class="col-md-3"><strong>Inactivas:</strong> {{ summary.inactivas }}</div>
      <div class="col-md-3">
        <strong>Top UNEs:</strong>
        {% for item in summary.por_unidad %}{{ item.unidad_negocio__nombre }} ({{ item.total }}){% if not forloop.last %}, {% endif %}{% empty %}—{% endfor %}
      </div>
    </div>
  </div>
</div>

<form method="get" class="row g-2 mb-3">
  <div class="col-md-3">
    <input type="search" name="q" value="{{ request.GET.q }}" class="form-control form-control-sm" placeholder="Buscar nombre, código o NIT">
  </div>
  <div class="col-md-2">
    <select name="tipo" class="form-select form-select-sm">
      <option value="">Todos los tipos</option>
      {% for value, label in tipos %}
      <option value="{{ value }}"{% if request.GET.tipo == value %} selected{% endif %}>{{ label }}</option>
      {% endfor %}
    </select>
  </div>
  <div class="col-md-2">
    <select name="unidad" class="form-select form-select-sm">
      <option value="">Todas las unidades</option>
      {% for u in unidades %}
      <option value="{{ u.id }}"{% if request.GET.unidad == u.id|stringformat:"s" %} selected{% endif %}>{{ u.nombre }}</option>
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
{% include "includes/empty_state.html" with title="Sin clientes registrados" message="Cargue InfoClientes desde Administración → Importación General." %}
{% endif %}

<div class="card border-0 shadow-sm">
  <div class="table-responsive">
    <table class="table table-hover table-wcg mb-0 align-middle">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Código / NIT</th>
          <th>Tipo</th>
          <th>Unidad</th>
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
          <td class="small">{{ entidad.codigo }}{% if entidad.nit %}<br><span class="text-muted">{{ entidad.nit }}</span>{% endif %}</td>
          <td>{{ entidad.get_tipo_display }}</td>
          <td>{{ entidad.unidad_negocio.nombre|default:"—" }}</td>
          <td>{{ entidad.num_contactos }}</td>
          <td>{{ entidad.num_productos }}</td>
          <td>
            {% if entidad.activa %}
            <span class="badge text-bg-success">Activo</span>
            {% else %}
            <span class="badge text-bg-secondary">Inactivo</span>
            {% endif %}
          </td>
          <td class="text-end">
            <a href="{% url 'crm:entidad_detail' entidad.codigo %}" class="btn btn-sm btn-outline-primary">Ver</a>
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
    <li class="page-item"><a class="page-link" href="?page={{ page_obj.previous_page_number }}&q={{ request.GET.q }}&tipo={{ request.GET.tipo }}&activo={{ request.GET.activo }}&unidad={{ request.GET.unidad }}">Anterior</a></li>
    {% endif %}
    <li class="page-item disabled"><span class="page-link">Pág. {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}</span></li>
    {% if page_obj.has_next %}
    <li class="page-item"><a class="page-link" href="?page={{ page_obj.next_page_number }}&q={{ request.GET.q }}&tipo={{ request.GET.tipo }}&activo={{ request.GET.activo }}&unidad={{ request.GET.unidad }}">Siguiente</a></li>
    {% endif %}
  </ul>
</nav>
{% endif %}
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}Clientes — CRM — WCG{% endblock %}
00003|{% block content %}
00004|<div class="d-flex justify-content-between align-items-start mb-3 flex-wrap gap-2 mt-2">
00005|  <div class="wcg-report-head">
00006|    <h1 class="h4 fw-semibold mb-0">CRM — Clientes y entidades</h1>
00007|    {% include "includes/module_mark.html" with module="crm" %}
00008|  </div>
00009|  <div class="d-flex gap-1 flex-wrap">
00010|    <a href="{% url 'crm:export_entidades' %}?q={{ request.GET.q }}&tipo={{ request.GET.tipo }}&activo={{ request.GET.activo }}" class="btn btn-sm btn-outline-primary">Exportar CSV</a>
00011|    <a href="{% url 'crm:contacto_list' %}" class="btn btn-sm btn-outline-secondary">Contactos</a>
00012|    <a href="{% url 'crm:tarea_list' %}" class="btn btn-sm btn-outline-secondary">Tareas</a>
00013|  </div>
00014|</div>
00015|
00016|<div class="card border-0 shadow-sm mb-3">
00017|  <div class="card-body py-2 px-3 small">
00018|    <div class="row g-2">
00019|      <div class="col-md-3"><strong>Total:</strong> {{ summary.total }}</div>
00020|      <div class="col-md-3"><strong>Activas:</strong> {{ summary.activas }}</div>
00021|      <div class="col-md-3"><strong>Inactivas:</strong> {{ summary.inactivas }}</div>
00022|      <div class="col-md-3">
00023|        <strong>Top UNEs:</strong>
00024|        {% for item in summary.por_unidad %}{{ item.unidad_negocio__nombre }} ({{ item.total }}){% if not forloop.last %}, {% endif %}{% empty %}—{% endfor %}
00025|      </div>
00026|    </div>
00027|  </div>
00028|</div>
00029|
00030|<form method="get" class="row g-2 mb-3">
00031|  <div class="col-md-3">
00032|    <input type="search" name="q" value="{{ request.GET.q }}" class="form-control form-control-sm" placeholder="Buscar nombre, código o NIT">
00033|  </div>
00034|  <div class="col-md-2">
00035|    <select name="tipo" class="form-select form-select-sm">
00036|      <option value="">Todos los tipos</option>
00037|      {% for value, label in tipos %}
00038|      <option value="{{ value }}"{% if request.GET.tipo == value %} selected{% endif %}>{{ label }}</option>
00039|      {% endfor %}
00040|    </select>
00041|  </div>
00042|  <div class="col-md-2">
00043|    <select name="unidad" class="form-select form-select-sm">
00044|      <option value="">Todas las unidades</option>
00045|      {% for u in unidades %}
00046|      <option value="{{ u.id }}"{% if request.GET.unidad == u.id|stringformat:"s" %} selected{% endif %}>{{ u.nombre }}</option>
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
00063|{% include "includes/empty_state.html" with title="Sin clientes registrados" message="Cargue InfoClientes desde Administración → Importación General." %}
00064|{% endif %}
00065|
00066|<div class="card border-0 shadow-sm">
00067|  <div class="table-responsive">
00068|    <table class="table table-hover table-wcg mb-0 align-middle">
00069|      <thead>
00070|        <tr>
00071|          <th>Nombre</th>
00072|          <th>Código / NIT</th>
00073|          <th>Tipo</th>
00074|          <th>Unidad</th>
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
00085|          <td class="small">{{ entidad.codigo }}{% if entidad.nit %}<br><span class="text-muted">{{ entidad.nit }}</span>{% endif %}</td>
00086|          <td>{{ entidad.get_tipo_display }}</td>
00087|          <td>{{ entidad.unidad_negocio.nombre|default:"—" }}</td>
00088|          <td>{{ entidad.num_contactos }}</td>
00089|          <td>{{ entidad.num_productos }}</td>
00090|          <td>
00091|            {% if entidad.activa %}
00092|            <span class="badge text-bg-success">Activo</span>
00093|            {% else %}
00094|            <span class="badge text-bg-secondary">Inactivo</span>
00095|            {% endif %}
00096|          </td>
00097|          <td class="text-end">
00098|            <a href="{% url 'crm:entidad_detail' entidad.codigo %}" class="btn btn-sm btn-outline-primary">Ver</a>
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
00117|    <li class="page-item"><a class="page-link" href="?page={{ page_obj.previous_page_number }}&q={{ request.GET.q }}&tipo={{ request.GET.tipo }}&activo={{ request.GET.activo }}&unidad={{ request.GET.unidad }}">Anterior</a></li>
00118|    {% endif %}
00119|    <li class="page-item disabled"><span class="page-link">Pág. {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}</span></li>
00120|    {% if page_obj.has_next %}
00121|    <li class="page-item"><a class="page-link" href="?page={{ page_obj.next_page_number }}&q={{ request.GET.q }}&tipo={{ request.GET.tipo }}&activo={{ request.GET.activo }}&unidad={{ request.GET.unidad }}">Siguiente</a></li>
00122|    {% endif %}
00123|  </ul>
00124|</nav>
00125|{% endif %}
00126|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1DbGllbnRlcyDigJQgQ1JNIOKAlCBXQ0d7JSBlbmRibG9jayAlfQp7JSBibG9jayBjb250ZW50ICV9CjxkaXYgY2xhc3M9ImQtZmxleCBqdXN0aWZ5LWNvbnRlbnQtYmV0d2VlbiBhbGlnbi1pdGVtcy1zdGFydCBtYi0zIGZsZXgtd3JhcCBnYXAtMiBtdC0yIj4KICA8ZGl2IGNsYXNzPSJ3Y2ctcmVwb3J0LWhlYWQiPgogICAgPGgxIGNsYXNzPSJoNCBmdy1zZW1pYm9sZCBtYi0wIj5DUk0g4oCUIENsaWVudGVzIHkgZW50aWRhZGVzPC9oMT4KICAgIHslIGluY2x1ZGUgImluY2x1ZGVzL21vZHVsZV9tYXJrLmh0bWwiIHdpdGggbW9kdWxlPSJjcm0iICV9CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iZC1mbGV4IGdhcC0xIGZsZXgtd3JhcCI+CiAgICA8YSBocmVmPSJ7JSB1cmwgJ2NybTpleHBvcnRfZW50aWRhZGVzJyAlfT9xPXt7IHJlcXVlc3QuR0VULnEgfX0mdGlwbz17eyByZXF1ZXN0LkdFVC50aXBvIH19JmFjdGl2bz17eyByZXF1ZXN0LkdFVC5hY3Rpdm8gfX0iIGNsYXNzPSJidG4gYnRuLXNtIGJ0bi1vdXRsaW5lLXByaW1hcnkiPkV4cG9ydGFyIENTVjwvYT4KICAgIDxhIGhyZWY9InslIHVybCAnY3JtOmNvbnRhY3RvX2xpc3QnICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1zZWNvbmRhcnkiPkNvbnRhY3RvczwvYT4KICAgIDxhIGhyZWY9InslIHVybCAnY3JtOnRhcmVhX2xpc3QnICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1zZWNvbmRhcnkiPlRhcmVhczwvYT4KICA8L2Rpdj4KPC9kaXY+Cgo8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSBtYi0zIj4KICA8ZGl2IGNsYXNzPSJjYXJkLWJvZHkgcHktMiBweC0zIHNtYWxsIj4KICAgIDxkaXYgY2xhc3M9InJvdyBnLTIiPgogICAgICA8ZGl2IGNsYXNzPSJjb2wtbWQtMyI+PHN0cm9uZz5Ub3RhbDo8L3N0cm9uZz4ge3sgc3VtbWFyeS50b3RhbCB9fTwvZGl2PgogICAgICA8ZGl2IGNsYXNzPSJjb2wtbWQtMyI+PHN0cm9uZz5BY3RpdmFzOjwvc3Ryb25nPiB7eyBzdW1tYXJ5LmFjdGl2YXMgfX08L2Rpdj4KICAgICAgPGRpdiBjbGFzcz0iY29sLW1kLTMiPjxzdHJvbmc+SW5hY3RpdmFzOjwvc3Ryb25nPiB7eyBzdW1tYXJ5LmluYWN0aXZhcyB9fTwvZGl2PgogICAgICA8ZGl2IGNsYXNzPSJjb2wtbWQtMyI+CiAgICAgICAgPHN0cm9uZz5Ub3AgVU5Fczo8L3N0cm9uZz4KICAgICAgICB7JSBmb3IgaXRlbSBpbiBzdW1tYXJ5LnBvcl91bmlkYWQgJX17eyBpdGVtLnVuaWRhZF9uZWdvY2lvX19ub21icmUgfX0gKHt7IGl0ZW0udG90YWwgfX0peyUgaWYgbm90IGZvcmxvb3AubGFzdCAlfSwgeyUgZW5kaWYgJX17JSBlbXB0eSAlfeKAlHslIGVuZGZvciAlfQogICAgICA8L2Rpdj4KICAgIDwvZGl2PgogIDwvZGl2Pgo8L2Rpdj4KCjxmb3JtIG1ldGhvZD0iZ2V0IiBjbGFzcz0icm93IGctMiBtYi0zIj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtMyI+CiAgICA8aW5wdXQgdHlwZT0ic2VhcmNoIiBuYW1lPSJxIiB2YWx1ZT0ie3sgcmVxdWVzdC5HRVQucSB9fSIgY2xhc3M9ImZvcm0tY29udHJvbCBmb3JtLWNvbnRyb2wtc20iIHBsYWNlaG9sZGVyPSJCdXNjYXIgbm9tYnJlLCBjw7NkaWdvIG8gTklUIj4KICA8L2Rpdj4KICA8ZGl2IGNsYXNzPSJjb2wtbWQtMiI+CiAgICA8c2VsZWN0IG5hbWU9InRpcG8iIGNsYXNzPSJmb3JtLXNlbGVjdCBmb3JtLXNlbGVjdC1zbSI+CiAgICAgIDxvcHRpb24gdmFsdWU9IiI+VG9kb3MgbG9zIHRpcG9zPC9vcHRpb24+CiAgICAgIHslIGZvciB2YWx1ZSwgbGFiZWwgaW4gdGlwb3MgJX0KICAgICAgPG9wdGlvbiB2YWx1ZT0ie3sgdmFsdWUgfX0ieyUgaWYgcmVxdWVzdC5HRVQudGlwbyA9PSB2YWx1ZSAlfSBzZWxlY3RlZHslIGVuZGlmICV9Pnt7IGxhYmVsIH19PC9vcHRpb24+CiAgICAgIHslIGVuZGZvciAlfQogICAgPC9zZWxlY3Q+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTIiPgogICAgPHNlbGVjdCBuYW1lPSJ1bmlkYWQiIGNsYXNzPSJmb3JtLXNlbGVjdCBmb3JtLXNlbGVjdC1zbSI+CiAgICAgIDxvcHRpb24gdmFsdWU9IiI+VG9kYXMgbGFzIHVuaWRhZGVzPC9vcHRpb24+CiAgICAgIHslIGZvciB1IGluIHVuaWRhZGVzICV9CiAgICAgIDxvcHRpb24gdmFsdWU9Int7IHUuaWQgfX0ieyUgaWYgcmVxdWVzdC5HRVQudW5pZGFkID09IHUuaWR8c3RyaW5nZm9ybWF0OiJzIiAlfSBzZWxlY3RlZHslIGVuZGlmICV9Pnt7IHUubm9tYnJlIH19PC9vcHRpb24+CiAgICAgIHslIGVuZGZvciAlfQogICAgPC9zZWxlY3Q+CiAgPC9kaXY+CiAgPGRpdiBjbGFzcz0iY29sLW1kLTIiPgogICAgPHNlbGVjdCBuYW1lPSJhY3Rpdm8iIGNsYXNzPSJmb3JtLXNlbGVjdCBmb3JtLXNlbGVjdC1zbSI+CiAgICAgIDxvcHRpb24gdmFsdWU9IiI+QWN0aXZvIC8gSW5hY3Rpdm88L29wdGlvbj4KICAgICAgPG9wdGlvbiB2YWx1ZT0iMSJ7JSBpZiByZXF1ZXN0LkdFVC5hY3Rpdm8gPT0gJzEnICV9IHNlbGVjdGVkeyUgZW5kaWYgJX0+QWN0aXZvczwvb3B0aW9uPgogICAgICA8b3B0aW9uIHZhbHVlPSIwInslIGlmIHJlcXVlc3QuR0VULmFjdGl2byA9PSAnMCcgJX0gc2VsZWN0ZWR7JSBlbmRpZiAlfT5JbmFjdGl2b3M8L29wdGlvbj4KICAgIDwvc2VsZWN0PgogIDwvZGl2PgogIDxkaXYgY2xhc3M9ImNvbC1tZC0yIj4KICAgIDxidXR0b24gdHlwZT0ic3VibWl0IiBjbGFzcz0iYnRuIGJ0bi1wcmltYXJ5IGJ0bi1zbSB3LTEwMCI+RmlsdHJhcjwvYnV0dG9uPgogIDwvZGl2Pgo8L2Zvcm0+Cgp7JSBpZiBub3QgZW50aWRhZGVzIGFuZCBub3QgcmVxdWVzdC5HRVQgJX0KeyUgaW5jbHVkZSAiaW5jbHVkZXMvZW1wdHlfc3RhdGUuaHRtbCIgd2l0aCB0aXRsZT0iU2luIGNsaWVudGVzIHJlZ2lzdHJhZG9zIiBtZXNzYWdlPSJDYXJndWUgSW5mb0NsaWVudGVzIGRlc2RlIEFkbWluaXN0cmFjacOzbiDihpIgSW1wb3J0YWNpw7NuIEdlbmVyYWwuIiAlfQp7JSBlbmRpZiAlfQoKPGRpdiBjbGFzcz0iY2FyZCBib3JkZXItMCBzaGFkb3ctc20iPgogIDxkaXYgY2xhc3M9InRhYmxlLXJlc3BvbnNpdmUiPgogICAgPHRhYmxlIGNsYXNzPSJ0YWJsZSB0YWJsZS1ob3ZlciB0YWJsZS13Y2cgbWItMCBhbGlnbi1taWRkbGUiPgogICAgICA8dGhlYWQ+CiAgICAgICAgPHRyPgogICAgICAgICAgPHRoPk5vbWJyZTwvdGg+CiAgICAgICAgICA8dGg+Q8OzZGlnbyAvIE5JVDwvdGg+CiAgICAgICAgICA8dGg+VGlwbzwvdGg+CiAgICAgICAgICA8dGg+VW5pZGFkPC90aD4KICAgICAgICAgIDx0aD5Db250YWN0b3M8L3RoPgogICAgICAgICAgPHRoPlByb2R1Y3RvczwvdGg+CiAgICAgICAgICA8dGg+RXN0YWRvPC90aD4KICAgICAgICAgIDx0aD48L3RoPgogICAgICAgIDwvdHI+CiAgICAgIDwvdGhlYWQ+CiAgICAgIDx0Ym9keT4KICAgICAgICB7JSBmb3IgZW50aWRhZCBpbiBlbnRpZGFkZXMgJX0KICAgICAgICA8dHI+CiAgICAgICAgICA8dGQ+e3sgZW50aWRhZC5ub21icmUgfX08L3RkPgogICAgICAgICAgPHRkIGNsYXNzPSJzbWFsbCI+e3sgZW50aWRhZC5jb2RpZ28gfX17JSBpZiBlbnRpZGFkLm5pdCAlfTxicj48c3BhbiBjbGFzcz0idGV4dC1tdXRlZCI+e3sgZW50aWRhZC5uaXQgfX08L3NwYW4+eyUgZW5kaWYgJX08L3RkPgogICAgICAgICAgPHRkPnt7IGVudGlkYWQuZ2V0X3RpcG9fZGlzcGxheSB9fTwvdGQ+CiAgICAgICAgICA8dGQ+e3sgZW50aWRhZC51bmlkYWRfbmVnb2Npby5ub21icmV8ZGVmYXVsdDoi4oCUIiB9fTwvdGQ+CiAgICAgICAgICA8dGQ+e3sgZW50aWRhZC5udW1fY29udGFjdG9zIH19PC90ZD4KICAgICAgICAgIDx0ZD57eyBlbnRpZGFkLm51bV9wcm9kdWN0b3MgfX08L3RkPgogICAgICAgICAgPHRkPgogICAgICAgICAgICB7JSBpZiBlbnRpZGFkLmFjdGl2YSAlfQogICAgICAgICAgICA8c3BhbiBjbGFzcz0iYmFkZ2UgdGV4dC1iZy1zdWNjZXNzIj5BY3Rpdm88L3NwYW4+CiAgICAgICAgICAgIHslIGVsc2UgJX0KICAgICAgICAgICAgPHNwYW4gY2xhc3M9ImJhZGdlIHRleHQtYmctc2Vjb25kYXJ5Ij5JbmFjdGl2bzwvc3Bhbj4KICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICAgIDwvdGQ+CiAgICAgICAgICA8dGQgY2xhc3M9InRleHQtZW5kIj4KICAgICAgICAgICAgPGEgaHJlZj0ieyUgdXJsICdjcm06ZW50aWRhZF9kZXRhaWwnIGVudGlkYWQuY29kaWdvICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1wcmltYXJ5Ij5WZXI8L2E+CiAgICAgICAgICA8L3RkPgogICAgICAgIDwvdHI+CiAgICAgICAgeyUgZW1wdHkgJX0KICAgICAgICA8dHI+CiAgICAgICAgICA8dGQgY29sc3Bhbj0iOCIgY2xhc3M9InRleHQtY2VudGVyIHRleHQtbXV0ZWQgcHktNCI+CiAgICAgICAgICAgIE5vIGhheSByZXN1bHRhZG9zIGNvbiBsb3MgZmlsdHJvcyBhY3R1YWxlcy4KICAgICAgICAgIDwvdGQ+CiAgICAgICAgPC90cj4KICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgPC90Ym9keT4KICAgIDwvdGFibGU+CiAgPC9kaXY+CjwvZGl2PgoKeyUgaWYgaXNfcGFnaW5hdGVkICV9CjxuYXYgY2xhc3M9Im10LTMiPgogIDx1bCBjbGFzcz0icGFnaW5hdGlvbiBwYWdpbmF0aW9uLXNtIGp1c3RpZnktY29udGVudC1jZW50ZXIiPgogICAgeyUgaWYgcGFnZV9vYmouaGFzX3ByZXZpb3VzICV9CiAgICA8bGkgY2xhc3M9InBhZ2UtaXRlbSI+PGEgY2xhc3M9InBhZ2UtbGluayIgaHJlZj0iP3BhZ2U9e3sgcGFnZV9vYmoucHJldmlvdXNfcGFnZV9udW1iZXIgfX0mcT17eyByZXF1ZXN0LkdFVC5xIH19JnRpcG89e3sgcmVxdWVzdC5HRVQudGlwbyB9fSZhY3Rpdm89e3sgcmVxdWVzdC5HRVQuYWN0aXZvIH19JnVuaWRhZD17eyByZXF1ZXN0LkdFVC51bmlkYWQgfX0iPkFudGVyaW9yPC9hPjwvbGk+CiAgICB7JSBlbmRpZiAlfQogICAgPGxpIGNsYXNzPSJwYWdlLWl0ZW0gZGlzYWJsZWQiPjxzcGFuIGNsYXNzPSJwYWdlLWxpbmsiPlDDoWcuIHt7IHBhZ2Vfb2JqLm51bWJlciB9fSBkZSB7eyBwYWdlX29iai5wYWdpbmF0b3IubnVtX3BhZ2VzIH19PC9zcGFuPjwvbGk+CiAgICB7JSBpZiBwYWdlX29iai5oYXNfbmV4dCAlfQogICAgPGxpIGNsYXNzPSJwYWdlLWl0ZW0iPjxhIGNsYXNzPSJwYWdlLWxpbmsiIGhyZWY9Ij9wYWdlPXt7IHBhZ2Vfb2JqLm5leHRfcGFnZV9udW1iZXIgfX0mcT17eyByZXF1ZXN0LkdFVC5xIH19JnRpcG89e3sgcmVxdWVzdC5HRVQudGlwbyB9fSZhY3Rpdm89e3sgcmVxdWVzdC5HRVQuYWN0aXZvIH19JnVuaWRhZD17eyByZXF1ZXN0LkdFVC51bmlkYWQgfX0iPlNpZ3VpZW50ZTwvYT48L2xpPgogICAgeyUgZW5kaWYgJX0KICA8L3VsPgo8L25hdj4KeyUgZW5kaWYgJX0KeyUgZW5kYmxvY2sgJX0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/crm/crmimportform.html
PATH_JSON="templates/crm/crmimportform.html"
FILENAME=crmimportform.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=19
SIZE_BYTES_UTF8=832
CONTENT_SHA256=73b5e5e182bf14c568a008c53ecb02a6806143a923559e222c68c76bcc00fbd2
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
{% block title %}{{ titulo }} — CRM{% endblock %}
{% block content %}
<h1>{{ titulo }}</h1>
<form method="post" enctype="multipart/form-data" class="card p-3">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary mt-2">Importar</button>
    <a href="{% url 'crm:entidad_list' %}" class="btn btn-link">Volver</a>
</form>
{% if batch %}
<div class="card mt-3 p-3">
    <h6>Resultado</h6>
    <p class="mb-1">Estado: <strong>{{ batch.get_status_display }}</strong></p>
    <p class="mb-1">Leídas: {{ batch.filas_leidas }} · Creados: {{ batch.creados }} · Actualizados: {{ batch.actualizados }} · Errores: {{ batch.errores }}</p>
    {% if batch.log_texto %}<pre class="small bg-light p-2">{{ batch.log_texto }}</pre>{% endif %}
</div>
{% endif %}
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}{{ titulo }} — CRM{% endblock %}
00003|{% block content %}
00004|<h1>{{ titulo }}</h1>
00005|<form method="post" enctype="multipart/form-data" class="card p-3">
00006|    {% csrf_token %}
00007|    {{ form.as_p }}
00008|    <button type="submit" class="btn btn-primary mt-2">Importar</button>
00009|    <a href="{% url 'crm:entidad_list' %}" class="btn btn-link">Volver</a>
00010|</form>
00011|{% if batch %}
00012|<div class="card mt-3 p-3">
00013|    <h6>Resultado</h6>
00014|    <p class="mb-1">Estado: <strong>{{ batch.get_status_display }}</strong></p>
00015|    <p class="mb-1">Leídas: {{ batch.filas_leidas }} · Creados: {{ batch.creados }} · Actualizados: {{ batch.actualizados }} · Errores: {{ batch.errores }}</p>
00016|    {% if batch.log_texto %}<pre class="small bg-light p-2">{{ batch.log_texto }}</pre>{% endif %}
00017|</div>
00018|{% endif %}
00019|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX17eyB0aXR1bG8gfX0g4oCUIENSTXslIGVuZGJsb2NrICV9CnslIGJsb2NrIGNvbnRlbnQgJX0KPGgxPnt7IHRpdHVsbyB9fTwvaDE+Cjxmb3JtIG1ldGhvZD0icG9zdCIgZW5jdHlwZT0ibXVsdGlwYXJ0L2Zvcm0tZGF0YSIgY2xhc3M9ImNhcmQgcC0zIj4KICAgIHslIGNzcmZfdG9rZW4gJX0KICAgIHt7IGZvcm0uYXNfcCB9fQogICAgPGJ1dHRvbiB0eXBlPSJzdWJtaXQiIGNsYXNzPSJidG4gYnRuLXByaW1hcnkgbXQtMiI+SW1wb3J0YXI8L2J1dHRvbj4KICAgIDxhIGhyZWY9InslIHVybCAnY3JtOmVudGlkYWRfbGlzdCcgJX0iIGNsYXNzPSJidG4gYnRuLWxpbmsiPlZvbHZlcjwvYT4KPC9mb3JtPgp7JSBpZiBiYXRjaCAlfQo8ZGl2IGNsYXNzPSJjYXJkIG10LTMgcC0zIj4KICAgIDxoNj5SZXN1bHRhZG88L2g2PgogICAgPHAgY2xhc3M9Im1iLTEiPkVzdGFkbzogPHN0cm9uZz57eyBiYXRjaC5nZXRfc3RhdHVzX2Rpc3BsYXkgfX08L3N0cm9uZz48L3A+CiAgICA8cCBjbGFzcz0ibWItMSI+TGXDrWRhczoge3sgYmF0Y2guZmlsYXNfbGVpZGFzIH19IMK3IENyZWFkb3M6IHt7IGJhdGNoLmNyZWFkb3MgfX0gwrcgQWN0dWFsaXphZG9zOiB7eyBiYXRjaC5hY3R1YWxpemFkb3MgfX0gwrcgRXJyb3Jlczoge3sgYmF0Y2guZXJyb3JlcyB9fTwvcD4KICAgIHslIGlmIGJhdGNoLmxvZ190ZXh0byAlfTxwcmUgY2xhc3M9InNtYWxsIGJnLWxpZ2h0IHAtMiI+e3sgYmF0Y2gubG9nX3RleHRvIH19PC9wcmU+eyUgZW5kaWYgJX0KPC9kaXY+CnslIGVuZGlmICV9CnslIGVuZGJsb2NrICV9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/crm/crminteractionform.html
PATH_JSON="templates/crm/crminteractionform.html"
FILENAME=crminteractionform.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=12
SIZE_BYTES_UTF8=468
CONTENT_SHA256=d45df3316c422f3839f41234647f42c7dcd6bd55f4522292721c5dbf9f71b6f5
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
{% block title %}Nueva interacción — {{ entidad.codigo }}{% endblock %}
{% block content %}
<h1>Nueva interacción</h1>
<p class="text-muted">{{ entidad.nombre }}</p>
<form method="post" class="card p-3">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary mt-2">Guardar</button>
    <a href="{% url 'crm:entidad_detail' entidad.codigo %}" class="btn btn-link">Cancelar</a>
</form>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}Nueva interacción — {{ entidad.codigo }}{% endblock %}
00003|{% block content %}
00004|<h1>Nueva interacción</h1>
00005|<p class="text-muted">{{ entidad.nombre }}</p>
00006|<form method="post" class="card p-3">
00007|    {% csrf_token %}
00008|    {{ form.as_p }}
00009|    <button type="submit" class="btn btn-primary mt-2">Guardar</button>
00010|    <a href="{% url 'crm:entidad_detail' entidad.codigo %}" class="btn btn-link">Cancelar</a>
00011|</form>
00012|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1OdWV2YSBpbnRlcmFjY2nDs24g4oCUIHt7IGVudGlkYWQuY29kaWdvIH19eyUgZW5kYmxvY2sgJX0KeyUgYmxvY2sgY29udGVudCAlfQo8aDE+TnVldmEgaW50ZXJhY2Npw7NuPC9oMT4KPHAgY2xhc3M9InRleHQtbXV0ZWQiPnt7IGVudGlkYWQubm9tYnJlIH19PC9wPgo8Zm9ybSBtZXRob2Q9InBvc3QiIGNsYXNzPSJjYXJkIHAtMyI+CiAgICB7JSBjc3JmX3Rva2VuICV9CiAgICB7eyBmb3JtLmFzX3AgfX0KICAgIDxidXR0b24gdHlwZT0ic3VibWl0IiBjbGFzcz0iYnRuIGJ0bi1wcmltYXJ5IG10LTIiPkd1YXJkYXI8L2J1dHRvbj4KICAgIDxhIGhyZWY9InslIHVybCAnY3JtOmVudGlkYWRfZGV0YWlsJyBlbnRpZGFkLmNvZGlnbyAlfSIgY2xhc3M9ImJ0biBidG4tbGluayI+Q2FuY2VsYXI8L2E+CjwvZm9ybT4KeyUgZW5kYmxvY2sgJX0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/crm/crmtarealist.html
PATH_JSON="templates/crm/crmtarealist.html"
FILENAME=crmtarealist.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=31
SIZE_BYTES_UTF8=1223
CONTENT_SHA256=78bc6ef0e88ad6f4b548d24d1699afeb71dfd7322adee5d4cd3f15fbbb976ae3
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
{% block title %}Tareas — CRM{% endblock %}
{% block content %}
<div class="d-flex justify-content-between mb-3 mt-2">
  <div class="wcg-report-head">
    <h1 class="h4 fw-semibold mb-0">CRM — Tareas</h1>
    {% include "includes/module_mark.html" with module="crm" %}
  </div>
  <a href="{% url 'crm:entidad_list' %}" class="btn btn-sm btn-outline-secondary">← Entidades</a>
</div>
<div class="card border-0 shadow-sm">
  <div class="table-responsive">
    <table class="table table-hover table-wcg mb-0 small">
      <thead><tr><th>Título</th><th>Entidad</th><th>Estado</th><th>Vence</th><th>Asignado</th></tr></thead>
      <tbody>
        {% for t in tareas %}
        <tr>
          <td><a href="{% url 'crm:entidad_detail' t.entidad.codigo %}">{{ t.titulo }}</a></td>
          <td>{{ t.entidad.nombre }}</td>
          <td>{{ t.get_estado_display }}</td>
          <td>{{ t.fecha_vencimiento|date:"d/m/Y"|default:"—" }}</td>
          <td>{{ t.asignado_a|default:"—" }}</td>
        </tr>
        {% empty %}
        <tr><td colspan="5" class="text-muted text-center py-4">Sin tareas.</td></tr>
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
00002|{% block title %}Tareas — CRM{% endblock %}
00003|{% block content %}
00004|<div class="d-flex justify-content-between mb-3 mt-2">
00005|  <div class="wcg-report-head">
00006|    <h1 class="h4 fw-semibold mb-0">CRM — Tareas</h1>
00007|    {% include "includes/module_mark.html" with module="crm" %}
00008|  </div>
00009|  <a href="{% url 'crm:entidad_list' %}" class="btn btn-sm btn-outline-secondary">← Entidades</a>
00010|</div>
00011|<div class="card border-0 shadow-sm">
00012|  <div class="table-responsive">
00013|    <table class="table table-hover table-wcg mb-0 small">
00014|      <thead><tr><th>Título</th><th>Entidad</th><th>Estado</th><th>Vence</th><th>Asignado</th></tr></thead>
00015|      <tbody>
00016|        {% for t in tareas %}
00017|        <tr>
00018|          <td><a href="{% url 'crm:entidad_detail' t.entidad.codigo %}">{{ t.titulo }}</a></td>
00019|          <td>{{ t.entidad.nombre }}</td>
00020|          <td>{{ t.get_estado_display }}</td>
00021|          <td>{{ t.fecha_vencimiento|date:"d/m/Y"|default:"—" }}</td>
00022|          <td>{{ t.asignado_a|default:"—" }}</td>
00023|        </tr>
00024|        {% empty %}
00025|        <tr><td colspan="5" class="text-muted text-center py-4">Sin tareas.</td></tr>
00026|        {% endfor %}
00027|      </tbody>
00028|    </table>
00029|  </div>
00030|</div>
00031|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1UYXJlYXMg4oCUIENSTXslIGVuZGJsb2NrICV9CnslIGJsb2NrIGNvbnRlbnQgJX0KPGRpdiBjbGFzcz0iZC1mbGV4IGp1c3RpZnktY29udGVudC1iZXR3ZWVuIG1iLTMgbXQtMiI+CiAgPGRpdiBjbGFzcz0id2NnLXJlcG9ydC1oZWFkIj4KICAgIDxoMSBjbGFzcz0iaDQgZnctc2VtaWJvbGQgbWItMCI+Q1JNIOKAlCBUYXJlYXM8L2gxPgogICAgeyUgaW5jbHVkZSAiaW5jbHVkZXMvbW9kdWxlX21hcmsuaHRtbCIgd2l0aCBtb2R1bGU9ImNybSIgJX0KICA8L2Rpdj4KICA8YSBocmVmPSJ7JSB1cmwgJ2NybTplbnRpZGFkX2xpc3QnICV9IiBjbGFzcz0iYnRuIGJ0bi1zbSBidG4tb3V0bGluZS1zZWNvbmRhcnkiPuKGkCBFbnRpZGFkZXM8L2E+CjwvZGl2Pgo8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSI+CiAgPGRpdiBjbGFzcz0idGFibGUtcmVzcG9uc2l2ZSI+CiAgICA8dGFibGUgY2xhc3M9InRhYmxlIHRhYmxlLWhvdmVyIHRhYmxlLXdjZyBtYi0wIHNtYWxsIj4KICAgICAgPHRoZWFkPjx0cj48dGg+VMOtdHVsbzwvdGg+PHRoPkVudGlkYWQ8L3RoPjx0aD5Fc3RhZG88L3RoPjx0aD5WZW5jZTwvdGg+PHRoPkFzaWduYWRvPC90aD48L3RyPjwvdGhlYWQ+CiAgICAgIDx0Ym9keT4KICAgICAgICB7JSBmb3IgdCBpbiB0YXJlYXMgJX0KICAgICAgICA8dHI+CiAgICAgICAgICA8dGQ+PGEgaHJlZj0ieyUgdXJsICdjcm06ZW50aWRhZF9kZXRhaWwnIHQuZW50aWRhZC5jb2RpZ28gJX0iPnt7IHQudGl0dWxvIH19PC9hPjwvdGQ+CiAgICAgICAgICA8dGQ+e3sgdC5lbnRpZGFkLm5vbWJyZSB9fTwvdGQ+CiAgICAgICAgICA8dGQ+e3sgdC5nZXRfZXN0YWRvX2Rpc3BsYXkgfX08L3RkPgogICAgICAgICAgPHRkPnt7IHQuZmVjaGFfdmVuY2ltaWVudG98ZGF0ZToiZC9tL1kifGRlZmF1bHQ6IuKAlCIgfX08L3RkPgogICAgICAgICAgPHRkPnt7IHQuYXNpZ25hZG9fYXxkZWZhdWx0OiLigJQiIH19PC90ZD4KICAgICAgICA8L3RyPgogICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgPHRyPjx0ZCBjb2xzcGFuPSI1IiBjbGFzcz0idGV4dC1tdXRlZCB0ZXh0LWNlbnRlciBweS00Ij5TaW4gdGFyZWFzLjwvdGQ+PC90cj4KICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgPC90Ym9keT4KICAgIDwvdGFibGU+CiAgPC9kaXY+CjwvZGl2Pgp7JSBlbmRibG9jayAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/crm/crmtaskform.html
PATH_JSON="templates/crm/crmtaskform.html"
FILENAME=crmtaskform.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=12
SIZE_BYTES_UTF8=454
CONTENT_SHA256=cfacd0c1871ff4f21a796ed86bb4094d20244806fd6c5e9221eee1167183ddfc
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
{% block title %}Nueva tarea — {{ entidad.codigo }}{% endblock %}
{% block content %}
<h1>Nueva tarea</h1>
<p class="text-muted">{{ entidad.nombre }}</p>
<form method="post" class="card p-3">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary mt-2">Guardar</button>
    <a href="{% url 'crm:entidad_detail' entidad.codigo %}" class="btn btn-link">Cancelar</a>
</form>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}Nueva tarea — {{ entidad.codigo }}{% endblock %}
00003|{% block content %}
00004|<h1>Nueva tarea</h1>
00005|<p class="text-muted">{{ entidad.nombre }}</p>
00006|<form method="post" class="card p-3">
00007|    {% csrf_token %}
00008|    {{ form.as_p }}
00009|    <button type="submit" class="btn btn-primary mt-2">Guardar</button>
00010|    <a href="{% url 'crm:entidad_detail' entidad.codigo %}" class="btn btn-link">Cancelar</a>
00011|</form>
00012|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1OdWV2YSB0YXJlYSDigJQge3sgZW50aWRhZC5jb2RpZ28gfX17JSBlbmRibG9jayAlfQp7JSBibG9jayBjb250ZW50ICV9CjxoMT5OdWV2YSB0YXJlYTwvaDE+CjxwIGNsYXNzPSJ0ZXh0LW11dGVkIj57eyBlbnRpZGFkLm5vbWJyZSB9fTwvcD4KPGZvcm0gbWV0aG9kPSJwb3N0IiBjbGFzcz0iY2FyZCBwLTMiPgogICAgeyUgY3NyZl90b2tlbiAlfQogICAge3sgZm9ybS5hc19wIH19CiAgICA8YnV0dG9uIHR5cGU9InN1Ym1pdCIgY2xhc3M9ImJ0biBidG4tcHJpbWFyeSBtdC0yIj5HdWFyZGFyPC9idXR0b24+CiAgICA8YSBocmVmPSJ7JSB1cmwgJ2NybTplbnRpZGFkX2RldGFpbCcgZW50aWRhZC5jb2RpZ28gJX0iIGNsYXNzPSJidG4gYnRuLWxpbmsiPkNhbmNlbGFyPC9hPgo8L2Zvcm0+CnslIGVuZGJsb2NrICV9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/dashboard/dashboardhome.html
PATH_JSON="templates/dashboard/dashboardhome.html"
FILENAME=dashboardhome.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=241
SIZE_BYTES_UTF8=5779
CONTENT_SHA256=b3962c886e49d7111d99dbf110458757461f81a0f428e733df08460d5ec00918
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
{% load static %}
{% block title %}Menú principal — WCG{% endblock %}
{% block extra_css %}
.menu-page {
  --ink: #2a3441;
  --muted: #6b7a8d;
  --accent: #3d5a73;
  --soft: #e8f0f6;
  --panel: #ffffff;
  --shadow: #c5d0dc;
  font-family: "DM Sans", system-ui, sans-serif;
  color: var(--ink);
  position: relative;
  min-height: calc(100vh - 140px);
  margin: -8px -12px 0;
  padding: 28px 20px 40px;
  overflow: hidden;
}

.menu-bg { display: none; }

.menu-shell {
  position: relative;
  z-index: 1;
  max-width: 640px;
  margin: 0 auto;
}

.menu-brand {
  font-size: clamp(1.75rem, 3vw, 2.35rem);
  font-weight: 700;
  margin: 0 0 6px;
  color: var(--accent);
  letter-spacing: -0.03em;
}

.menu-lead {
  color: var(--muted);
  margin: 0 0 28px;
  font-size: 1.02rem;
  max-width: 28rem;
  line-height: 1.45;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.menu-card {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-decoration: none;
  color: inherit;
  background: var(--panel);
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 22px 20px 18px;
  box-shadow:
    0 1px 0 rgba(255,255,255,0.9) inset,
    0 6px 0 var(--shadow),
    0 12px 28px rgba(42, 52, 65, 0.08);
  transform: translateY(0);
  transition:
    transform 0.12s ease,
    box-shadow 0.12s ease,
    border-color 0.12s ease,
    background 0.12s ease;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
}

.menu-card:hover {
  transform: translateY(-3px);
  border-color: #b7c9d8;
  background: #fafcfd;
  box-shadow:
    0 1px 0 rgba(255,255,255,0.95) inset,
    0 8px 0 var(--shadow),
    0 18px 36px rgba(42, 52, 65, 0.1);
  color: inherit;
}

.menu-card:active {
  transform: translateY(5px);
  box-shadow:
    0 1px 0 rgba(255,255,255,0.6) inset,
    0 1px 0 #a8b8c8,
    0 4px 12px rgba(42, 52, 65, 0.08);
}

.menu-emoji {
  font-size: 2.75rem;
  line-height: 1;
  margin-bottom: 12px;
  filter: drop-shadow(0 2px 0 rgba(42, 52, 65, 0.06));
}

.menu-card h2 {
  margin: 0 0 6px;
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: -0.02em;
}

.menu-card p {
  margin: 0;
  color: var(--muted);
  font-size: 0.9rem;
  line-height: 1.4;
  flex-grow: 1;
}

.menu-card .go {
  display: inline-block;
  margin-top: 14px;
  font-weight: 600;
  color: var(--accent);
  font-size: 0.88rem;
  opacity: 0.85;
}

.menu-foot {
  margin-top: 32px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}

.menu-status-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.45rem 0.9rem;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  background: rgba(255,255,255,0.7);
  color: var(--muted);
  font-size: 0.82rem;
  font-weight: 500;
  text-decoration: none;
  transition: background 0.12s ease, color 0.12s ease, border-color 0.12s ease;
}

.menu-status-btn:hover {
  background: var(--soft);
  color: var(--accent);
  border-color: #c9d9e6;
}

/* Desktop: imagen vertical a la izquierda, crop leve + esquinas redondeadas */
@media (min-width: 900px) {
  .menu-page {
    display: grid;
    grid-template-columns: minmax(240px, 34%) 1fr;
    gap: 36px;
    align-items: center;
    padding: 36px 32px 56px;
    margin: -8px -16px 0;
  }
  .menu-bg {
    display: block;
    position: relative;
    border-radius: 18px;
    overflow: hidden;
    min-height: 560px;
    max-height: calc(100vh - 160px);
    aspect-ratio: 3 / 5;
    box-shadow: 0 14px 36px rgba(42, 52, 65, 0.1);
    background: var(--soft);
  }
  .menu-bg img {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center center;
    /* Crop leve en ambas dimensiones (≈ splash vertical + milímetros) */
    transform: scale(1.06);
    transform-origin: center center;
    display: block;
  }
  .menu-shell { padding-top: 8px; max-width: none; }
}

@media (max-width: 899px) {
  .menu-grid { grid-template-columns: 1fr; max-width: 420px; }
  .menu-card { border-radius: 12px; }
  .menu-emoji { font-size: 2.4rem; }
}
{% endblock %}

{% block content %}
<div class="menu-page">
  <aside class="menu-bg" aria-hidden="true">
    <img src="{% static 'img/splashv.jpg' %}" alt="">
  </aside>

  <div class="menu-shell">
    <h1 class="menu-brand">Working Capital Group</h1>
    <p class="menu-lead">Elija un módulo para continuar.</p>

    <div class="menu-grid">
      <a class="menu-card" href="{% url 'pgc:dashboard' %}">
        <span class="menu-emoji" aria-hidden="true">📊</span>
        <h2>PGC</h2>
        <p>Planeación comercial, metas, clientes nuevos y venta cruzada.</p>
        <span class="go">Entrar →</span>
      </a>
      <a class="menu-card" href="{% url 'pgo:dashboard' %}">
        <span class="menu-emoji" aria-hidden="true">⚙️</span>
        <h2>PGO</h2>
        <p>Tickets helpdesk, tiempos de atención y cumplimiento de SLA.</p>
        <span class="go">Entrar →</span>
      </a>
      <a class="menu-card" href="{% url 'crm:entidad_list' %}">
        <span class="menu-emoji" aria-hidden="true">👥</span>
        <h2>CRM</h2>
        <p>Clientes, contactos, productos y seguimiento comercial.</p>
        <span class="go">Entrar →</span>
      </a>
      <a class="menu-card" href="{% url 'risk:comando_balon' %}">
        <span class="menu-emoji" aria-hidden="true">⚽</span>
        <h2>Balón de Riesgo</h2>
        <p>Mora, saldos vencidos y alertas por operación leasing.</p>
        <span class="go">Entrar →</span>
      </a>
    </div>

    <div class="menu-foot">
      <a class="menu-status-btn" href="{% url 'portal:estado' %}">📋 Estado del sistema</a>
    </div>
  </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% load static %}
00003|{% block title %}Menú principal — WCG{% endblock %}
00004|{% block extra_css %}
00005|.menu-page {
00006|  --ink: #2a3441;
00007|  --muted: #6b7a8d;
00008|  --accent: #3d5a73;
00009|  --soft: #e8f0f6;
00010|  --panel: #ffffff;
00011|  --shadow: #c5d0dc;
00012|  font-family: "DM Sans", system-ui, sans-serif;
00013|  color: var(--ink);
00014|  position: relative;
00015|  min-height: calc(100vh - 140px);
00016|  margin: -8px -12px 0;
00017|  padding: 28px 20px 40px;
00018|  overflow: hidden;
00019|}
00020|
00021|.menu-bg { display: none; }
00022|
00023|.menu-shell {
00024|  position: relative;
00025|  z-index: 1;
00026|  max-width: 640px;
00027|  margin: 0 auto;
00028|}
00029|
00030|.menu-brand {
00031|  font-size: clamp(1.75rem, 3vw, 2.35rem);
00032|  font-weight: 700;
00033|  margin: 0 0 6px;
00034|  color: var(--accent);
00035|  letter-spacing: -0.03em;
00036|}
00037|
00038|.menu-lead {
00039|  color: var(--muted);
00040|  margin: 0 0 28px;
00041|  font-size: 1.02rem;
00042|  max-width: 28rem;
00043|  line-height: 1.45;
00044|}
00045|
00046|.menu-grid {
00047|  display: grid;
00048|  grid-template-columns: repeat(2, minmax(0, 1fr));
00049|  gap: 18px;
00050|}
00051|
00052|.menu-card {
00053|  display: flex;
00054|  flex-direction: column;
00055|  align-items: flex-start;
00056|  text-decoration: none;
00057|  color: inherit;
00058|  background: var(--panel);
00059|  border: 1px solid #e2e8f0;
00060|  border-radius: 14px;
00061|  padding: 22px 20px 18px;
00062|  box-shadow:
00063|    0 1px 0 rgba(255,255,255,0.9) inset,
00064|    0 6px 0 var(--shadow),
00065|    0 12px 28px rgba(42, 52, 65, 0.08);
00066|  transform: translateY(0);
00067|  transition:
00068|    transform 0.12s ease,
00069|    box-shadow 0.12s ease,
00070|    border-color 0.12s ease,
00071|    background 0.12s ease;
00072|  -webkit-tap-highlight-color: transparent;
00073|  user-select: none;
00074|}
00075|
00076|.menu-card:hover {
00077|  transform: translateY(-3px);
00078|  border-color: #b7c9d8;
00079|  background: #fafcfd;
00080|  box-shadow:
00081|    0 1px 0 rgba(255,255,255,0.95) inset,
00082|    0 8px 0 var(--shadow),
00083|    0 18px 36px rgba(42, 52, 65, 0.1);
00084|  color: inherit;
00085|}
00086|
00087|.menu-card:active {
00088|  transform: translateY(5px);
00089|  box-shadow:
00090|    0 1px 0 rgba(255,255,255,0.6) inset,
00091|    0 1px 0 #a8b8c8,
00092|    0 4px 12px rgba(42, 52, 65, 0.08);
00093|}
00094|
00095|.menu-emoji {
00096|  font-size: 2.75rem;
00097|  line-height: 1;
00098|  margin-bottom: 12px;
00099|  filter: drop-shadow(0 2px 0 rgba(42, 52, 65, 0.06));
00100|}
00101|
00102|.menu-card h2 {
00103|  margin: 0 0 6px;
00104|  font-size: 1.35rem;
00105|  font-weight: 700;
00106|  color: var(--accent);
00107|  letter-spacing: -0.02em;
00108|}
00109|
00110|.menu-card p {
00111|  margin: 0;
00112|  color: var(--muted);
00113|  font-size: 0.9rem;
00114|  line-height: 1.4;
00115|  flex-grow: 1;
00116|}
00117|
00118|.menu-card .go {
00119|  display: inline-block;
00120|  margin-top: 14px;
00121|  font-weight: 600;
00122|  color: var(--accent);
00123|  font-size: 0.88rem;
00124|  opacity: 0.85;
00125|}
00126|
00127|.menu-foot {
00128|  margin-top: 32px;
00129|  display: flex;
00130|  flex-wrap: wrap;
00131|  gap: 10px;
00132|  align-items: center;
00133|}
00134|
00135|.menu-status-btn {
00136|  display: inline-flex;
00137|  align-items: center;
00138|  gap: 0.4rem;
00139|  padding: 0.45rem 0.9rem;
00140|  border-radius: 6px;
00141|  border: 1px solid #e2e8f0;
00142|  background: rgba(255,255,255,0.7);
00143|  color: var(--muted);
00144|  font-size: 0.82rem;
00145|  font-weight: 500;
00146|  text-decoration: none;
00147|  transition: background 0.12s ease, color 0.12s ease, border-color 0.12s ease;
00148|}
00149|
00150|.menu-status-btn:hover {
00151|  background: var(--soft);
00152|  color: var(--accent);
00153|  border-color: #c9d9e6;
00154|}
00155|
00156|/* Desktop: imagen vertical a la izquierda, crop leve + esquinas redondeadas */
00157|@media (min-width: 900px) {
00158|  .menu-page {
00159|    display: grid;
00160|    grid-template-columns: minmax(240px, 34%) 1fr;
00161|    gap: 36px;
00162|    align-items: center;
00163|    padding: 36px 32px 56px;
00164|    margin: -8px -16px 0;
00165|  }
00166|  .menu-bg {
00167|    display: block;
00168|    position: relative;
00169|    border-radius: 18px;
00170|    overflow: hidden;
00171|    min-height: 560px;
00172|    max-height: calc(100vh - 160px);
00173|    aspect-ratio: 3 / 5;
00174|    box-shadow: 0 14px 36px rgba(42, 52, 65, 0.1);
00175|    background: var(--soft);
00176|  }
00177|  .menu-bg img {
00178|    position: absolute;
00179|    inset: 0;
00180|    width: 100%;
00181|    height: 100%;
00182|    object-fit: cover;
00183|    object-position: center center;
00184|    /* Crop leve en ambas dimensiones (≈ splash vertical + milímetros) */
00185|    transform: scale(1.06);
00186|    transform-origin: center center;
00187|    display: block;
00188|  }
00189|  .menu-shell { padding-top: 8px; max-width: none; }
00190|}
00191|
00192|@media (max-width: 899px) {
00193|  .menu-grid { grid-template-columns: 1fr; max-width: 420px; }
00194|  .menu-card { border-radius: 12px; }
00195|  .menu-emoji { font-size: 2.4rem; }
00196|}
00197|{% endblock %}
00198|
00199|{% block content %}
00200|<div class="menu-page">
00201|  <aside class="menu-bg" aria-hidden="true">
00202|    <img src="{% static 'img/splashv.jpg' %}" alt="">
00203|  </aside>
00204|
00205|  <div class="menu-shell">
00206|    <h1 class="menu-brand">Working Capital Group</h1>
00207|    <p class="menu-lead">Elija un módulo para continuar.</p>
00208|
00209|    <div class="menu-grid">
00210|      <a class="menu-card" href="{% url 'pgc:dashboard' %}">
00211|        <span class="menu-emoji" aria-hidden="true">📊</span>
00212|        <h2>PGC</h2>
00213|        <p>Planeación comercial, metas, clientes nuevos y venta cruzada.</p>
00214|        <span class="go">Entrar →</span>
00215|      </a>
00216|      <a class="menu-card" href="{% url 'pgo:dashboard' %}">
00217|        <span class="menu-emoji" aria-hidden="true">⚙️</span>
00218|        <h2>PGO</h2>
00219|        <p>Tickets helpdesk, tiempos de atención y cumplimiento de SLA.</p>
00220|        <span class="go">Entrar →</span>
00221|      </a>
00222|      <a class="menu-card" href="{% url 'crm:entidad_list' %}">
00223|        <span class="menu-emoji" aria-hidden="true">👥</span>
00224|        <h2>CRM</h2>
00225|        <p>Clientes, contactos, productos y seguimiento comercial.</p>
00226|        <span class="go">Entrar →</span>
00227|      </a>
00228|      <a class="menu-card" href="{% url 'risk:comando_balon' %}">
00229|        <span class="menu-emoji" aria-hidden="true">⚽</span>
00230|        <h2>Balón de Riesgo</h2>
00231|        <p>Mora, saldos vencidos y alertas por operación leasing.</p>
00232|        <span class="go">Entrar →</span>
00233|      </a>
00234|    </div>
00235|
00236|    <div class="menu-foot">
00237|      <a class="menu-status-btn" href="{% url 'portal:estado' %}">📋 Estado del sistema</a>
00238|    </div>
00239|  </div>
00240|</div>
00241|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgbG9hZCBzdGF0aWMgJX0KeyUgYmxvY2sgdGl0bGUgJX1NZW7DuiBwcmluY2lwYWwg4oCUIFdDR3slIGVuZGJsb2NrICV9CnslIGJsb2NrIGV4dHJhX2NzcyAlfQoubWVudS1wYWdlIHsKICAtLWluazogIzJhMzQ0MTsKICAtLW11dGVkOiAjNmI3YThkOwogIC0tYWNjZW50OiAjM2Q1YTczOwogIC0tc29mdDogI2U4ZjBmNjsKICAtLXBhbmVsOiAjZmZmZmZmOwogIC0tc2hhZG93OiAjYzVkMGRjOwogIGZvbnQtZmFtaWx5OiAiRE0gU2FucyIsIHN5c3RlbS11aSwgc2Fucy1zZXJpZjsKICBjb2xvcjogdmFyKC0taW5rKTsKICBwb3NpdGlvbjogcmVsYXRpdmU7CiAgbWluLWhlaWdodDogY2FsYygxMDB2aCAtIDE0MHB4KTsKICBtYXJnaW46IC04cHggLTEycHggMDsKICBwYWRkaW5nOiAyOHB4IDIwcHggNDBweDsKICBvdmVyZmxvdzogaGlkZGVuOwp9CgoubWVudS1iZyB7IGRpc3BsYXk6IG5vbmU7IH0KCi5tZW51LXNoZWxsIHsKICBwb3NpdGlvbjogcmVsYXRpdmU7CiAgei1pbmRleDogMTsKICBtYXgtd2lkdGg6IDY0MHB4OwogIG1hcmdpbjogMCBhdXRvOwp9CgoubWVudS1icmFuZCB7CiAgZm9udC1zaXplOiBjbGFtcCgxLjc1cmVtLCAzdncsIDIuMzVyZW0pOwogIGZvbnQtd2VpZ2h0OiA3MDA7CiAgbWFyZ2luOiAwIDAgNnB4OwogIGNvbG9yOiB2YXIoLS1hY2NlbnQpOwogIGxldHRlci1zcGFjaW5nOiAtMC4wM2VtOwp9CgoubWVudS1sZWFkIHsKICBjb2xvcjogdmFyKC0tbXV0ZWQpOwogIG1hcmdpbjogMCAwIDI4cHg7CiAgZm9udC1zaXplOiAxLjAycmVtOwogIG1heC13aWR0aDogMjhyZW07CiAgbGluZS1oZWlnaHQ6IDEuNDU7Cn0KCi5tZW51LWdyaWQgewogIGRpc3BsYXk6IGdyaWQ7CiAgZ3JpZC10ZW1wbGF0ZS1jb2x1bW5zOiByZXBlYXQoMiwgbWlubWF4KDAsIDFmcikpOwogIGdhcDogMThweDsKfQoKLm1lbnUtY2FyZCB7CiAgZGlzcGxheTogZmxleDsKICBmbGV4LWRpcmVjdGlvbjogY29sdW1uOwogIGFsaWduLWl0ZW1zOiBmbGV4LXN0YXJ0OwogIHRleHQtZGVjb3JhdGlvbjogbm9uZTsKICBjb2xvcjogaW5oZXJpdDsKICBiYWNrZ3JvdW5kOiB2YXIoLS1wYW5lbCk7CiAgYm9yZGVyOiAxcHggc29saWQgI2UyZThmMDsKICBib3JkZXItcmFkaXVzOiAxNHB4OwogIHBhZGRpbmc6IDIycHggMjBweCAxOHB4OwogIGJveC1zaGFkb3c6CiAgICAwIDFweCAwIHJnYmEoMjU1LDI1NSwyNTUsMC45KSBpbnNldCwKICAgIDAgNnB4IDAgdmFyKC0tc2hhZG93KSwKICAgIDAgMTJweCAyOHB4IHJnYmEoNDIsIDUyLCA2NSwgMC4wOCk7CiAgdHJhbnNmb3JtOiB0cmFuc2xhdGVZKDApOwogIHRyYW5zaXRpb246CiAgICB0cmFuc2Zvcm0gMC4xMnMgZWFzZSwKICAgIGJveC1zaGFkb3cgMC4xMnMgZWFzZSwKICAgIGJvcmRlci1jb2xvciAwLjEycyBlYXNlLAogICAgYmFja2dyb3VuZCAwLjEycyBlYXNlOwogIC13ZWJraXQtdGFwLWhpZ2hsaWdodC1jb2xvcjogdHJhbnNwYXJlbnQ7CiAgdXNlci1zZWxlY3Q6IG5vbmU7Cn0KCi5tZW51LWNhcmQ6aG92ZXIgewogIHRyYW5zZm9ybTogdHJhbnNsYXRlWSgtM3B4KTsKICBib3JkZXItY29sb3I6ICNiN2M5ZDg7CiAgYmFja2dyb3VuZDogI2ZhZmNmZDsKICBib3gtc2hhZG93OgogICAgMCAxcHggMCByZ2JhKDI1NSwyNTUsMjU1LDAuOTUpIGluc2V0LAogICAgMCA4cHggMCB2YXIoLS1zaGFkb3cpLAogICAgMCAxOHB4IDM2cHggcmdiYSg0MiwgNTIsIDY1LCAwLjEpOwogIGNvbG9yOiBpbmhlcml0Owp9CgoubWVudS1jYXJkOmFjdGl2ZSB7CiAgdHJhbnNmb3JtOiB0cmFuc2xhdGVZKDVweCk7CiAgYm94LXNoYWRvdzoKICAgIDAgMXB4IDAgcmdiYSgyNTUsMjU1LDI1NSwwLjYpIGluc2V0LAogICAgMCAxcHggMCAjYThiOGM4LAogICAgMCA0cHggMTJweCByZ2JhKDQyLCA1MiwgNjUsIDAuMDgpOwp9CgoubWVudS1lbW9qaSB7CiAgZm9udC1zaXplOiAyLjc1cmVtOwogIGxpbmUtaGVpZ2h0OiAxOwogIG1hcmdpbi1ib3R0b206IDEycHg7CiAgZmlsdGVyOiBkcm9wLXNoYWRvdygwIDJweCAwIHJnYmEoNDIsIDUyLCA2NSwgMC4wNikpOwp9CgoubWVudS1jYXJkIGgyIHsKICBtYXJnaW46IDAgMCA2cHg7CiAgZm9udC1zaXplOiAxLjM1cmVtOwogIGZvbnQtd2VpZ2h0OiA3MDA7CiAgY29sb3I6IHZhcigtLWFjY2VudCk7CiAgbGV0dGVyLXNwYWNpbmc6IC0wLjAyZW07Cn0KCi5tZW51LWNhcmQgcCB7CiAgbWFyZ2luOiAwOwogIGNvbG9yOiB2YXIoLS1tdXRlZCk7CiAgZm9udC1zaXplOiAwLjlyZW07CiAgbGluZS1oZWlnaHQ6IDEuNDsKICBmbGV4LWdyb3c6IDE7Cn0KCi5tZW51LWNhcmQgLmdvIHsKICBkaXNwbGF5OiBpbmxpbmUtYmxvY2s7CiAgbWFyZ2luLXRvcDogMTRweDsKICBmb250LXdlaWdodDogNjAwOwogIGNvbG9yOiB2YXIoLS1hY2NlbnQpOwogIGZvbnQtc2l6ZTogMC44OHJlbTsKICBvcGFjaXR5OiAwLjg1Owp9CgoubWVudS1mb290IHsKICBtYXJnaW4tdG9wOiAzMnB4OwogIGRpc3BsYXk6IGZsZXg7CiAgZmxleC13cmFwOiB3cmFwOwogIGdhcDogMTBweDsKICBhbGlnbi1pdGVtczogY2VudGVyOwp9CgoubWVudS1zdGF0dXMtYnRuIHsKICBkaXNwbGF5OiBpbmxpbmUtZmxleDsKICBhbGlnbi1pdGVtczogY2VudGVyOwogIGdhcDogMC40cmVtOwogIHBhZGRpbmc6IDAuNDVyZW0gMC45cmVtOwogIGJvcmRlci1yYWRpdXM6IDZweDsKICBib3JkZXI6IDFweCBzb2xpZCAjZTJlOGYwOwogIGJhY2tncm91bmQ6IHJnYmEoMjU1LDI1NSwyNTUsMC43KTsKICBjb2xvcjogdmFyKC0tbXV0ZWQpOwogIGZvbnQtc2l6ZTogMC44MnJlbTsKICBmb250LXdlaWdodDogNTAwOwogIHRleHQtZGVjb3JhdGlvbjogbm9uZTsKICB0cmFuc2l0aW9uOiBiYWNrZ3JvdW5kIDAuMTJzIGVhc2UsIGNvbG9yIDAuMTJzIGVhc2UsIGJvcmRlci1jb2xvciAwLjEycyBlYXNlOwp9CgoubWVudS1zdGF0dXMtYnRuOmhvdmVyIHsKICBiYWNrZ3JvdW5kOiB2YXIoLS1zb2Z0KTsKICBjb2xvcjogdmFyKC0tYWNjZW50KTsKICBib3JkZXItY29sb3I6ICNjOWQ5ZTY7Cn0KCi8qIERlc2t0b3A6IGltYWdlbiB2ZXJ0aWNhbCBhIGxhIGl6cXVpZXJkYSwgY3JvcCBsZXZlICsgZXNxdWluYXMgcmVkb25kZWFkYXMgKi8KQG1lZGlhIChtaW4td2lkdGg6IDkwMHB4KSB7CiAgLm1lbnUtcGFnZSB7CiAgICBkaXNwbGF5OiBncmlkOwogICAgZ3JpZC10ZW1wbGF0ZS1jb2x1bW5zOiBtaW5tYXgoMjQwcHgsIDM0JSkgMWZyOwogICAgZ2FwOiAzNnB4OwogICAgYWxpZ24taXRlbXM6IGNlbnRlcjsKICAgIHBhZGRpbmc6IDM2cHggMzJweCA1NnB4OwogICAgbWFyZ2luOiAtOHB4IC0xNnB4IDA7CiAgfQogIC5tZW51LWJnIHsKICAgIGRpc3BsYXk6IGJsb2NrOwogICAgcG9zaXRpb246IHJlbGF0aXZlOwogICAgYm9yZGVyLXJhZGl1czogMThweDsKICAgIG92ZXJmbG93OiBoaWRkZW47CiAgICBtaW4taGVpZ2h0OiA1NjBweDsKICAgIG1heC1oZWlnaHQ6IGNhbGMoMTAwdmggLSAxNjBweCk7CiAgICBhc3BlY3QtcmF0aW86IDMgLyA1OwogICAgYm94LXNoYWRvdzogMCAxNHB4IDM2cHggcmdiYSg0MiwgNTIsIDY1LCAwLjEpOwogICAgYmFja2dyb3VuZDogdmFyKC0tc29mdCk7CiAgfQogIC5tZW51LWJnIGltZyB7CiAgICBwb3NpdGlvbjogYWJzb2x1dGU7CiAgICBpbnNldDogMDsKICAgIHdpZHRoOiAxMDAlOwogICAgaGVpZ2h0OiAxMDAlOwogICAgb2JqZWN0LWZpdDogY292ZXI7CiAgICBvYmplY3QtcG9zaXRpb246IGNlbnRlciBjZW50ZXI7CiAgICAvKiBDcm9wIGxldmUgZW4gYW1iYXMgZGltZW5zaW9uZXMgKOKJiCBzcGxhc2ggdmVydGljYWwgKyBtaWzDrW1ldHJvcykgKi8KICAgIHRyYW5zZm9ybTogc2NhbGUoMS4wNik7CiAgICB0cmFuc2Zvcm0tb3JpZ2luOiBjZW50ZXIgY2VudGVyOwogICAgZGlzcGxheTogYmxvY2s7CiAgfQogIC5tZW51LXNoZWxsIHsgcGFkZGluZy10b3A6IDhweDsgbWF4LXdpZHRoOiBub25lOyB9Cn0KCkBtZWRpYSAobWF4LXdpZHRoOiA4OTlweCkgewogIC5tZW51LWdyaWQgeyBncmlkLXRlbXBsYXRlLWNvbHVtbnM6IDFmcjsgbWF4LXdpZHRoOiA0MjBweDsgfQogIC5tZW51LWNhcmQgeyBib3JkZXItcmFkaXVzOiAxMnB4OyB9CiAgLm1lbnUtZW1vamkgeyBmb250LXNpemU6IDIuNHJlbTsgfQp9CnslIGVuZGJsb2NrICV9Cgp7JSBibG9jayBjb250ZW50ICV9CjxkaXYgY2xhc3M9Im1lbnUtcGFnZSI+CiAgPGFzaWRlIGNsYXNzPSJtZW51LWJnIiBhcmlhLWhpZGRlbj0idHJ1ZSI+CiAgICA8aW1nIHNyYz0ieyUgc3RhdGljICdpbWcvc3BsYXNodi5qcGcnICV9IiBhbHQ9IiI+CiAgPC9hc2lkZT4KCiAgPGRpdiBjbGFzcz0ibWVudS1zaGVsbCI+CiAgICA8aDEgY2xhc3M9Im1lbnUtYnJhbmQiPldvcmtpbmcgQ2FwaXRhbCBHcm91cDwvaDE+CiAgICA8cCBjbGFzcz0ibWVudS1sZWFkIj5FbGlqYSB1biBtw7NkdWxvIHBhcmEgY29udGludWFyLjwvcD4KCiAgICA8ZGl2IGNsYXNzPSJtZW51LWdyaWQiPgogICAgICA8YSBjbGFzcz0ibWVudS1jYXJkIiBocmVmPSJ7JSB1cmwgJ3BnYzpkYXNoYm9hcmQnICV9Ij4KICAgICAgICA8c3BhbiBjbGFzcz0ibWVudS1lbW9qaSIgYXJpYS1oaWRkZW49InRydWUiPvCfk4o8L3NwYW4+CiAgICAgICAgPGgyPlBHQzwvaDI+CiAgICAgICAgPHA+UGxhbmVhY2nDs24gY29tZXJjaWFsLCBtZXRhcywgY2xpZW50ZXMgbnVldm9zIHkgdmVudGEgY3J1emFkYS48L3A+CiAgICAgICAgPHNwYW4gY2xhc3M9ImdvIj5FbnRyYXIg4oaSPC9zcGFuPgogICAgICA8L2E+CiAgICAgIDxhIGNsYXNzPSJtZW51LWNhcmQiIGhyZWY9InslIHVybCAncGdvOmRhc2hib2FyZCcgJX0iPgogICAgICAgIDxzcGFuIGNsYXNzPSJtZW51LWVtb2ppIiBhcmlhLWhpZGRlbj0idHJ1ZSI+4pqZ77iPPC9zcGFuPgogICAgICAgIDxoMj5QR088L2gyPgogICAgICAgIDxwPlRpY2tldHMgaGVscGRlc2ssIHRpZW1wb3MgZGUgYXRlbmNpw7NuIHkgY3VtcGxpbWllbnRvIGRlIFNMQS48L3A+CiAgICAgICAgPHNwYW4gY2xhc3M9ImdvIj5FbnRyYXIg4oaSPC9zcGFuPgogICAgICA8L2E+CiAgICAgIDxhIGNsYXNzPSJtZW51LWNhcmQiIGhyZWY9InslIHVybCAnY3JtOmVudGlkYWRfbGlzdCcgJX0iPgogICAgICAgIDxzcGFuIGNsYXNzPSJtZW51LWVtb2ppIiBhcmlhLWhpZGRlbj0idHJ1ZSI+8J+RpTwvc3Bhbj4KICAgICAgICA8aDI+Q1JNPC9oMj4KICAgICAgICA8cD5DbGllbnRlcywgY29udGFjdG9zLCBwcm9kdWN0b3MgeSBzZWd1aW1pZW50byBjb21lcmNpYWwuPC9wPgogICAgICAgIDxzcGFuIGNsYXNzPSJnbyI+RW50cmFyIOKGkjwvc3Bhbj4KICAgICAgPC9hPgogICAgICA8YSBjbGFzcz0ibWVudS1jYXJkIiBocmVmPSJ7JSB1cmwgJ3Jpc2s6Y29tYW5kb19iYWxvbicgJX0iPgogICAgICAgIDxzcGFuIGNsYXNzPSJtZW51LWVtb2ppIiBhcmlhLWhpZGRlbj0idHJ1ZSI+4pq9PC9zcGFuPgogICAgICAgIDxoMj5CYWzDs24gZGUgUmllc2dvPC9oMj4KICAgICAgICA8cD5Nb3JhLCBzYWxkb3MgdmVuY2lkb3MgeSBhbGVydGFzIHBvciBvcGVyYWNpw7NuIGxlYXNpbmcuPC9wPgogICAgICAgIDxzcGFuIGNsYXNzPSJnbyI+RW50cmFyIOKGkjwvc3Bhbj4KICAgICAgPC9hPgogICAgPC9kaXY+CgogICAgPGRpdiBjbGFzcz0ibWVudS1mb290Ij4KICAgICAgPGEgY2xhc3M9Im1lbnUtc3RhdHVzLWJ0biIgaHJlZj0ieyUgdXJsICdwb3J0YWw6ZXN0YWRvJyAlfSI+8J+TiyBFc3RhZG8gZGVsIHNpc3RlbWE8L2E+CiAgICA8L2Rpdj4KICA8L2Rpdj4KPC9kaXY+CnslIGVuZGJsb2NrICV9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/imports/general_hub.html
PATH_JSON="templates/imports/general_hub.html"
FILENAME=general_hub.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=157
SIZE_BYTES_UTF8=6150
CONTENT_SHA256=d851d05d243df4266a77cfd2be677bc810c846231894aa82d1cbdea1fa1cc5b0
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
{% block title %}Importación General — Administración — WCG{% endblock %}
{% block content %}
<div class="page-toolbar">
  <div>
    <p class="text-muted small mb-1 text-uppercase" style="letter-spacing:0.04em;font-weight:600;">Administración · Configuración</p>
    <h1 class="h3 mb-1">Importación General de Datos</h1>
    <p class="text-muted mb-0" style="max-width:40rem;">
      Punto único para cargar clientes nuevos, ventas cruzadas, CRM, PGO y Balón de Riesgo.
      El tipo se detecta por nombre, estructura de columnas y contenido de muestra.
    </p>
  </div>
  <a class="wcg-home-link" href="{% url 'portal:home' %}">← Menú principal</a>
</div>

{% if detection_preview %}
<div class="alert {% if detection_preview.ambiguous or not detection_preview.can_auto_import %}alert-warning{% else %}alert-info{% endif %} mb-4">
  <div class="fw-semibold mb-1">
    Detección: {{ detection_preview.label }}
    · {% widthratio detection_preview.confidence 1 100 %}% confianza
    · capa {{ detection_preview.layer }}
  </div>
  {% if detection_preview.reasons %}
  <ul class="small mb-2 mb-0">
    {% for r in detection_preview.reasons %}
    <li>{{ r }}</li>
    {% endfor %}
  </ul>
  {% endif %}
  {% if detection_preview.ambiguous or not detection_preview.can_auto_import %}
  <p class="small mb-0 mt-2">
    Hay ambigüedad o confianza insuficiente. Elija el tipo en el selector y vuelva a subir el archivo.
  </p>
  {% endif %}
  {% if detection_preview.suggestions %}
  <p class="small mb-0 mt-2">Otras opciones:
    {% for t, lab in detection_preview.suggestions %}{{ lab }}{% if not forloop.last %}; {% endif %}{% endfor %}
  </p>
  {% endif %}
</div>
{% endif %}

<div class="row g-4">
  <div class="col-lg-5">
    <div class="card border-0">
      <div class="card-body">
        <h2 class="h5 mb-3">Subir archivo</h2>
        <form method="post" enctype="multipart/form-data">
          {% csrf_token %}
          <div class="mb-3">
            <label class="form-label" for="id_archivo">{{ form.archivo.label }}</label>
            {{ form.archivo }}
            {% if form.archivo.help_text %}<div class="form-text">{{ form.archivo.help_text }}</div>{% endif %}
          </div>
          <div class="mb-3">
            <label class="form-label" for="id_tipo_forzado">{{ form.tipo_forzado.label }}</label>
            {{ form.tipo_forzado }}
            {% if form.tipo_forzado.help_text %}<div class="form-text">{{ form.tipo_forzado.help_text }}</div>{% endif %}
          </div>
          <div class="d-flex flex-wrap gap-2">
            <button type="submit" name="action" value="import" class="btn btn-primary">Importar y procesar</button>
            <button type="submit" name="action" value="detect" class="btn btn-outline-secondary">Solo detectar</button>
          </div>
        </form>

        {% if result %}
        <div class="alert {% if result.ok %}alert-success{% else %}alert-warning{% endif %} mt-3 mb-0">
          <strong>{{ result.label }}</strong><br>
          {{ result.message }}
          {% if result.detection %}
          <div class="small mt-2 text-muted">
            {{ result.detection.rule_summary }}
            {% if result.forced %} · tipo forzado{% endif %}
          </div>
          {% endif %}
          {% if result.ok and result.redirect_hint %}
          <div class="mt-2"><a href="{% url result.redirect_hint %}">Ver resultados →</a></div>
          {% endif %}
        </div>
        {% endif %}
      </div>
    </div>

    <div class="card border-0 mt-3">
      <div class="card-body">
        <h2 class="h6">Tipos soportados</h2>
        <ul class="small mb-0 text-muted">
          {% for t, lab in importable_types %}
          <li>{{ lab }}</li>
          {% endfor %}
        </ul>
      </div>
    </div>
  </div>

  <div class="col-lg-7">
    <div class="card border-0">
      <div class="card-body">
        <h2 class="h5">Bitácora — lotes recientes (CRM / Risk / PGO)</h2>
        <p class="small text-muted">Cada lote registra tipo detectado, capa/regla e importador usado.</p>
        <div class="table-responsive">
          <table class="table table-sm align-middle mb-0 table-wcg">
            <thead>
              <tr>
                <th>Archivo</th>
                <th>Módulo</th>
                <th>Tipo</th>
                <th>Estado</th>
                <th>C/A/E</th>
              </tr>
            </thead>
            <tbody>
              {% for b in batches %}
              <tr>
                <td class="small">{{ b.archivo_nombre|truncatechars:42 }}</td>
                <td>{{ b.modulo }}</td>
                <td class="small">{{ b.tipo_importacion }}</td>
                <td>
                  <span class="badge text-bg-{% if b.status == 'OK' %}success{% elif b.status == 'PARTIAL' %}warning{% else %}secondary{% endif %}">
                    {{ b.status }}
                  </span>
                </td>
                <td class="small">{{ b.creados }}/{{ b.actualizados }}/{{ b.errores }}</td>
              </tr>
              {% empty %}
              <tr><td colspan="5" class="text-muted">Aún no hay lotes.</td></tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="card border-0 mt-3">
      <div class="card-body">
        <h2 class="h5">Uploads PGC recientes</h2>
        <div class="table-responsive">
          <table class="table table-sm mb-0 table-wcg">
            <thead><tr><th>Archivo</th><th>Tipo</th><th>Estado</th></tr></thead>
            <tbody>
              {% for u in uploads %}
              <tr>
                <td class="small">{{ u.original_filename|truncatechars:48 }}</td>
                <td class="small">{{ u.get_file_type_detected_display }}</td>
                <td class="small">{{ u.get_status_display }}</td>
              </tr>
              {% empty %}
              <tr><td colspan="3" class="text-muted">Sin uploads.</td></tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% extends "base_wcg.html" %}
00002|{% block title %}Importación General — Administración — WCG{% endblock %}
00003|{% block content %}
00004|<div class="page-toolbar">
00005|  <div>
00006|    <p class="text-muted small mb-1 text-uppercase" style="letter-spacing:0.04em;font-weight:600;">Administración · Configuración</p>
00007|    <h1 class="h3 mb-1">Importación General de Datos</h1>
00008|    <p class="text-muted mb-0" style="max-width:40rem;">
00009|      Punto único para cargar clientes nuevos, ventas cruzadas, CRM, PGO y Balón de Riesgo.
00010|      El tipo se detecta por nombre, estructura de columnas y contenido de muestra.
00011|    </p>
00012|  </div>
00013|  <a class="wcg-home-link" href="{% url 'portal:home' %}">← Menú principal</a>
00014|</div>
00015|
00016|{% if detection_preview %}
00017|<div class="alert {% if detection_preview.ambiguous or not detection_preview.can_auto_import %}alert-warning{% else %}alert-info{% endif %} mb-4">
00018|  <div class="fw-semibold mb-1">
00019|    Detección: {{ detection_preview.label }}
00020|    · {% widthratio detection_preview.confidence 1 100 %}% confianza
00021|    · capa {{ detection_preview.layer }}
00022|  </div>
00023|  {% if detection_preview.reasons %}
00024|  <ul class="small mb-2 mb-0">
00025|    {% for r in detection_preview.reasons %}
00026|    <li>{{ r }}</li>
00027|    {% endfor %}
00028|  </ul>
00029|  {% endif %}
00030|  {% if detection_preview.ambiguous or not detection_preview.can_auto_import %}
00031|  <p class="small mb-0 mt-2">
00032|    Hay ambigüedad o confianza insuficiente. Elija el tipo en el selector y vuelva a subir el archivo.
00033|  </p>
00034|  {% endif %}
00035|  {% if detection_preview.suggestions %}
00036|  <p class="small mb-0 mt-2">Otras opciones:
00037|    {% for t, lab in detection_preview.suggestions %}{{ lab }}{% if not forloop.last %}; {% endif %}{% endfor %}
00038|  </p>
00039|  {% endif %}
00040|</div>
00041|{% endif %}
00042|
00043|<div class="row g-4">
00044|  <div class="col-lg-5">
00045|    <div class="card border-0">
00046|      <div class="card-body">
00047|        <h2 class="h5 mb-3">Subir archivo</h2>
00048|        <form method="post" enctype="multipart/form-data">
00049|          {% csrf_token %}
00050|          <div class="mb-3">
00051|            <label class="form-label" for="id_archivo">{{ form.archivo.label }}</label>
00052|            {{ form.archivo }}
00053|            {% if form.archivo.help_text %}<div class="form-text">{{ form.archivo.help_text }}</div>{% endif %}
00054|          </div>
00055|          <div class="mb-3">
00056|            <label class="form-label" for="id_tipo_forzado">{{ form.tipo_forzado.label }}</label>
00057|            {{ form.tipo_forzado }}
00058|            {% if form.tipo_forzado.help_text %}<div class="form-text">{{ form.tipo_forzado.help_text }}</div>{% endif %}
00059|          </div>
00060|          <div class="d-flex flex-wrap gap-2">
00061|            <button type="submit" name="action" value="import" class="btn btn-primary">Importar y procesar</button>
00062|            <button type="submit" name="action" value="detect" class="btn btn-outline-secondary">Solo detectar</button>
00063|          </div>
00064|        </form>
00065|
00066|        {% if result %}
00067|        <div class="alert {% if result.ok %}alert-success{% else %}alert-warning{% endif %} mt-3 mb-0">
00068|          <strong>{{ result.label }}</strong><br>
00069|          {{ result.message }}
00070|          {% if result.detection %}
00071|          <div class="small mt-2 text-muted">
00072|            {{ result.detection.rule_summary }}
00073|            {% if result.forced %} · tipo forzado{% endif %}
00074|          </div>
00075|          {% endif %}
00076|          {% if result.ok and result.redirect_hint %}
00077|          <div class="mt-2"><a href="{% url result.redirect_hint %}">Ver resultados →</a></div>
00078|          {% endif %}
00079|        </div>
00080|        {% endif %}
00081|      </div>
00082|    </div>
00083|
00084|    <div class="card border-0 mt-3">
00085|      <div class="card-body">
00086|        <h2 class="h6">Tipos soportados</h2>
00087|        <ul class="small mb-0 text-muted">
00088|          {% for t, lab in importable_types %}
00089|          <li>{{ lab }}</li>
00090|          {% endfor %}
00091|        </ul>
00092|      </div>
00093|    </div>
00094|  </div>
00095|
00096|  <div class="col-lg-7">
00097|    <div class="card border-0">
00098|      <div class="card-body">
00099|        <h2 class="h5">Bitácora — lotes recientes (CRM / Risk / PGO)</h2>
00100|        <p class="small text-muted">Cada lote registra tipo detectado, capa/regla e importador usado.</p>
00101|        <div class="table-responsive">
00102|          <table class="table table-sm align-middle mb-0 table-wcg">
00103|            <thead>
00104|              <tr>
00105|                <th>Archivo</th>
00106|                <th>Módulo</th>
00107|                <th>Tipo</th>
00108|                <th>Estado</th>
00109|                <th>C/A/E</th>
00110|              </tr>
00111|            </thead>
00112|            <tbody>
00113|              {% for b in batches %}
00114|              <tr>
00115|                <td class="small">{{ b.archivo_nombre|truncatechars:42 }}</td>
00116|                <td>{{ b.modulo }}</td>
00117|                <td class="small">{{ b.tipo_importacion }}</td>
00118|                <td>
00119|                  <span class="badge text-bg-{% if b.status == 'OK' %}success{% elif b.status == 'PARTIAL' %}warning{% else %}secondary{% endif %}">
00120|                    {{ b.status }}
00121|                  </span>
00122|                </td>
00123|                <td class="small">{{ b.creados }}/{{ b.actualizados }}/{{ b.errores }}</td>
00124|              </tr>
00125|              {% empty %}
00126|              <tr><td colspan="5" class="text-muted">Aún no hay lotes.</td></tr>
00127|              {% endfor %}
00128|            </tbody>
00129|          </table>
00130|        </div>
00131|      </div>
00132|    </div>
00133|
00134|    <div class="card border-0 mt-3">
00135|      <div class="card-body">
00136|        <h2 class="h5">Uploads PGC recientes</h2>
00137|        <div class="table-responsive">
00138|          <table class="table table-sm mb-0 table-wcg">
00139|            <thead><tr><th>Archivo</th><th>Tipo</th><th>Estado</th></tr></thead>
00140|            <tbody>
00141|              {% for u in uploads %}
00142|              <tr>
00143|                <td class="small">{{ u.original_filename|truncatechars:48 }}</td>
00144|                <td class="small">{{ u.get_file_type_detected_display }}</td>
00145|                <td class="small">{{ u.get_status_display }}</td>
00146|              </tr>
00147|              {% empty %}
00148|              <tr><td colspan="3" class="text-muted">Sin uploads.</td></tr>
00149|              {% endfor %}
00150|            </tbody>
00151|          </table>
00152|        </div>
00153|      </div>
00154|    </div>
00155|  </div>
00156|</div>
00157|{% endblock %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgZXh0ZW5kcyAiYmFzZV93Y2cuaHRtbCIgJX0KeyUgYmxvY2sgdGl0bGUgJX1JbXBvcnRhY2nDs24gR2VuZXJhbCDigJQgQWRtaW5pc3RyYWNpw7NuIOKAlCBXQ0d7JSBlbmRibG9jayAlfQp7JSBibG9jayBjb250ZW50ICV9CjxkaXYgY2xhc3M9InBhZ2UtdG9vbGJhciI+CiAgPGRpdj4KICAgIDxwIGNsYXNzPSJ0ZXh0LW11dGVkIHNtYWxsIG1iLTEgdGV4dC11cHBlcmNhc2UiIHN0eWxlPSJsZXR0ZXItc3BhY2luZzowLjA0ZW07Zm9udC13ZWlnaHQ6NjAwOyI+QWRtaW5pc3RyYWNpw7NuIMK3IENvbmZpZ3VyYWNpw7NuPC9wPgogICAgPGgxIGNsYXNzPSJoMyBtYi0xIj5JbXBvcnRhY2nDs24gR2VuZXJhbCBkZSBEYXRvczwvaDE+CiAgICA8cCBjbGFzcz0idGV4dC1tdXRlZCBtYi0wIiBzdHlsZT0ibWF4LXdpZHRoOjQwcmVtOyI+CiAgICAgIFB1bnRvIMO6bmljbyBwYXJhIGNhcmdhciBjbGllbnRlcyBudWV2b3MsIHZlbnRhcyBjcnV6YWRhcywgQ1JNLCBQR08geSBCYWzDs24gZGUgUmllc2dvLgogICAgICBFbCB0aXBvIHNlIGRldGVjdGEgcG9yIG5vbWJyZSwgZXN0cnVjdHVyYSBkZSBjb2x1bW5hcyB5IGNvbnRlbmlkbyBkZSBtdWVzdHJhLgogICAgPC9wPgogIDwvZGl2PgogIDxhIGNsYXNzPSJ3Y2ctaG9tZS1saW5rIiBocmVmPSJ7JSB1cmwgJ3BvcnRhbDpob21lJyAlfSI+4oaQIE1lbsO6IHByaW5jaXBhbDwvYT4KPC9kaXY+Cgp7JSBpZiBkZXRlY3Rpb25fcHJldmlldyAlfQo8ZGl2IGNsYXNzPSJhbGVydCB7JSBpZiBkZXRlY3Rpb25fcHJldmlldy5hbWJpZ3VvdXMgb3Igbm90IGRldGVjdGlvbl9wcmV2aWV3LmNhbl9hdXRvX2ltcG9ydCAlfWFsZXJ0LXdhcm5pbmd7JSBlbHNlICV9YWxlcnQtaW5mb3slIGVuZGlmICV9IG1iLTQiPgogIDxkaXYgY2xhc3M9ImZ3LXNlbWlib2xkIG1iLTEiPgogICAgRGV0ZWNjacOzbjoge3sgZGV0ZWN0aW9uX3ByZXZpZXcubGFiZWwgfX0KICAgIMK3IHslIHdpZHRocmF0aW8gZGV0ZWN0aW9uX3ByZXZpZXcuY29uZmlkZW5jZSAxIDEwMCAlfSUgY29uZmlhbnphCiAgICDCtyBjYXBhIHt7IGRldGVjdGlvbl9wcmV2aWV3LmxheWVyIH19CiAgPC9kaXY+CiAgeyUgaWYgZGV0ZWN0aW9uX3ByZXZpZXcucmVhc29ucyAlfQogIDx1bCBjbGFzcz0ic21hbGwgbWItMiBtYi0wIj4KICAgIHslIGZvciByIGluIGRldGVjdGlvbl9wcmV2aWV3LnJlYXNvbnMgJX0KICAgIDxsaT57eyByIH19PC9saT4KICAgIHslIGVuZGZvciAlfQogIDwvdWw+CiAgeyUgZW5kaWYgJX0KICB7JSBpZiBkZXRlY3Rpb25fcHJldmlldy5hbWJpZ3VvdXMgb3Igbm90IGRldGVjdGlvbl9wcmV2aWV3LmNhbl9hdXRvX2ltcG9ydCAlfQogIDxwIGNsYXNzPSJzbWFsbCBtYi0wIG10LTIiPgogICAgSGF5IGFtYmlnw7xlZGFkIG8gY29uZmlhbnphIGluc3VmaWNpZW50ZS4gRWxpamEgZWwgdGlwbyBlbiBlbCBzZWxlY3RvciB5IHZ1ZWx2YSBhIHN1YmlyIGVsIGFyY2hpdm8uCiAgPC9wPgogIHslIGVuZGlmICV9CiAgeyUgaWYgZGV0ZWN0aW9uX3ByZXZpZXcuc3VnZ2VzdGlvbnMgJX0KICA8cCBjbGFzcz0ic21hbGwgbWItMCBtdC0yIj5PdHJhcyBvcGNpb25lczoKICAgIHslIGZvciB0LCBsYWIgaW4gZGV0ZWN0aW9uX3ByZXZpZXcuc3VnZ2VzdGlvbnMgJX17eyBsYWIgfX17JSBpZiBub3QgZm9ybG9vcC5sYXN0ICV9OyB7JSBlbmRpZiAlfXslIGVuZGZvciAlfQogIDwvcD4KICB7JSBlbmRpZiAlfQo8L2Rpdj4KeyUgZW5kaWYgJX0KCjxkaXYgY2xhc3M9InJvdyBnLTQiPgogIDxkaXYgY2xhc3M9ImNvbC1sZy01Ij4KICAgIDxkaXYgY2xhc3M9ImNhcmQgYm9yZGVyLTAiPgogICAgICA8ZGl2IGNsYXNzPSJjYXJkLWJvZHkiPgogICAgICAgIDxoMiBjbGFzcz0iaDUgbWItMyI+U3ViaXIgYXJjaGl2bzwvaDI+CiAgICAgICAgPGZvcm0gbWV0aG9kPSJwb3N0IiBlbmN0eXBlPSJtdWx0aXBhcnQvZm9ybS1kYXRhIj4KICAgICAgICAgIHslIGNzcmZfdG9rZW4gJX0KICAgICAgICAgIDxkaXYgY2xhc3M9Im1iLTMiPgogICAgICAgICAgICA8bGFiZWwgY2xhc3M9ImZvcm0tbGFiZWwiIGZvcj0iaWRfYXJjaGl2byI+e3sgZm9ybS5hcmNoaXZvLmxhYmVsIH19PC9sYWJlbD4KICAgICAgICAgICAge3sgZm9ybS5hcmNoaXZvIH19CiAgICAgICAgICAgIHslIGlmIGZvcm0uYXJjaGl2by5oZWxwX3RleHQgJX08ZGl2IGNsYXNzPSJmb3JtLXRleHQiPnt7IGZvcm0uYXJjaGl2by5oZWxwX3RleHQgfX08L2Rpdj57JSBlbmRpZiAlfQogICAgICAgICAgPC9kaXY+CiAgICAgICAgICA8ZGl2IGNsYXNzPSJtYi0zIj4KICAgICAgICAgICAgPGxhYmVsIGNsYXNzPSJmb3JtLWxhYmVsIiBmb3I9ImlkX3RpcG9fZm9yemFkbyI+e3sgZm9ybS50aXBvX2ZvcnphZG8ubGFiZWwgfX08L2xhYmVsPgogICAgICAgICAgICB7eyBmb3JtLnRpcG9fZm9yemFkbyB9fQogICAgICAgICAgICB7JSBpZiBmb3JtLnRpcG9fZm9yemFkby5oZWxwX3RleHQgJX08ZGl2IGNsYXNzPSJmb3JtLXRleHQiPnt7IGZvcm0udGlwb19mb3J6YWRvLmhlbHBfdGV4dCB9fTwvZGl2PnslIGVuZGlmICV9CiAgICAgICAgICA8L2Rpdj4KICAgICAgICAgIDxkaXYgY2xhc3M9ImQtZmxleCBmbGV4LXdyYXAgZ2FwLTIiPgogICAgICAgICAgICA8YnV0dG9uIHR5cGU9InN1Ym1pdCIgbmFtZT0iYWN0aW9uIiB2YWx1ZT0iaW1wb3J0IiBjbGFzcz0iYnRuIGJ0bi1wcmltYXJ5Ij5JbXBvcnRhciB5IHByb2Nlc2FyPC9idXR0b24+CiAgICAgICAgICAgIDxidXR0b24gdHlwZT0ic3VibWl0IiBuYW1lPSJhY3Rpb24iIHZhbHVlPSJkZXRlY3QiIGNsYXNzPSJidG4gYnRuLW91dGxpbmUtc2Vjb25kYXJ5Ij5Tb2xvIGRldGVjdGFyPC9idXR0b24+CiAgICAgICAgICA8L2Rpdj4KICAgICAgICA8L2Zvcm0+CgogICAgICAgIHslIGlmIHJlc3VsdCAlfQogICAgICAgIDxkaXYgY2xhc3M9ImFsZXJ0IHslIGlmIHJlc3VsdC5vayAlfWFsZXJ0LXN1Y2Nlc3N7JSBlbHNlICV9YWxlcnQtd2FybmluZ3slIGVuZGlmICV9IG10LTMgbWItMCI+CiAgICAgICAgICA8c3Ryb25nPnt7IHJlc3VsdC5sYWJlbCB9fTwvc3Ryb25nPjxicj4KICAgICAgICAgIHt7IHJlc3VsdC5tZXNzYWdlIH19CiAgICAgICAgICB7JSBpZiByZXN1bHQuZGV0ZWN0aW9uICV9CiAgICAgICAgICA8ZGl2IGNsYXNzPSJzbWFsbCBtdC0yIHRleHQtbXV0ZWQiPgogICAgICAgICAgICB7eyByZXN1bHQuZGV0ZWN0aW9uLnJ1bGVfc3VtbWFyeSB9fQogICAgICAgICAgICB7JSBpZiByZXN1bHQuZm9yY2VkICV9IMK3IHRpcG8gZm9yemFkb3slIGVuZGlmICV9CiAgICAgICAgICA8L2Rpdj4KICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgICB7JSBpZiByZXN1bHQub2sgYW5kIHJlc3VsdC5yZWRpcmVjdF9oaW50ICV9CiAgICAgICAgICA8ZGl2IGNsYXNzPSJtdC0yIj48YSBocmVmPSJ7JSB1cmwgcmVzdWx0LnJlZGlyZWN0X2hpbnQgJX0iPlZlciByZXN1bHRhZG9zIOKGkjwvYT48L2Rpdj4KICAgICAgICAgIHslIGVuZGlmICV9CiAgICAgICAgPC9kaXY+CiAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgPC9kaXY+CiAgICA8L2Rpdj4KCiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIG10LTMiPgogICAgICA8ZGl2IGNsYXNzPSJjYXJkLWJvZHkiPgogICAgICAgIDxoMiBjbGFzcz0iaDYiPlRpcG9zIHNvcG9ydGFkb3M8L2gyPgogICAgICAgIDx1bCBjbGFzcz0ic21hbGwgbWItMCB0ZXh0LW11dGVkIj4KICAgICAgICAgIHslIGZvciB0LCBsYWIgaW4gaW1wb3J0YWJsZV90eXBlcyAlfQogICAgICAgICAgPGxpPnt7IGxhYiB9fTwvbGk+CiAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICA8L3VsPgogICAgICA8L2Rpdj4KICAgIDwvZGl2PgogIDwvZGl2PgoKICA8ZGl2IGNsYXNzPSJjb2wtbGctNyI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIj4KICAgICAgPGRpdiBjbGFzcz0iY2FyZC1ib2R5Ij4KICAgICAgICA8aDIgY2xhc3M9Img1Ij5CaXTDoWNvcmEg4oCUIGxvdGVzIHJlY2llbnRlcyAoQ1JNIC8gUmlzayAvIFBHTyk8L2gyPgogICAgICAgIDxwIGNsYXNzPSJzbWFsbCB0ZXh0LW11dGVkIj5DYWRhIGxvdGUgcmVnaXN0cmEgdGlwbyBkZXRlY3RhZG8sIGNhcGEvcmVnbGEgZSBpbXBvcnRhZG9yIHVzYWRvLjwvcD4KICAgICAgICA8ZGl2IGNsYXNzPSJ0YWJsZS1yZXNwb25zaXZlIj4KICAgICAgICAgIDx0YWJsZSBjbGFzcz0idGFibGUgdGFibGUtc20gYWxpZ24tbWlkZGxlIG1iLTAgdGFibGUtd2NnIj4KICAgICAgICAgICAgPHRoZWFkPgogICAgICAgICAgICAgIDx0cj4KICAgICAgICAgICAgICAgIDx0aD5BcmNoaXZvPC90aD4KICAgICAgICAgICAgICAgIDx0aD5Nw7NkdWxvPC90aD4KICAgICAgICAgICAgICAgIDx0aD5UaXBvPC90aD4KICAgICAgICAgICAgICAgIDx0aD5Fc3RhZG88L3RoPgogICAgICAgICAgICAgICAgPHRoPkMvQS9FPC90aD4KICAgICAgICAgICAgICA8L3RyPgogICAgICAgICAgICA8L3RoZWFkPgogICAgICAgICAgICA8dGJvZHk+CiAgICAgICAgICAgICAgeyUgZm9yIGIgaW4gYmF0Y2hlcyAlfQogICAgICAgICAgICAgIDx0cj4KICAgICAgICAgICAgICAgIDx0ZCBjbGFzcz0ic21hbGwiPnt7IGIuYXJjaGl2b19ub21icmV8dHJ1bmNhdGVjaGFyczo0MiB9fTwvdGQ+CiAgICAgICAgICAgICAgICA8dGQ+e3sgYi5tb2R1bG8gfX08L3RkPgogICAgICAgICAgICAgICAgPHRkIGNsYXNzPSJzbWFsbCI+e3sgYi50aXBvX2ltcG9ydGFjaW9uIH19PC90ZD4KICAgICAgICAgICAgICAgIDx0ZD4KICAgICAgICAgICAgICAgICAgPHNwYW4gY2xhc3M9ImJhZGdlIHRleHQtYmcteyUgaWYgYi5zdGF0dXMgPT0gJ09LJyAlfXN1Y2Nlc3N7JSBlbGlmIGIuc3RhdHVzID09ICdQQVJUSUFMJyAlfXdhcm5pbmd7JSBlbHNlICV9c2Vjb25kYXJ5eyUgZW5kaWYgJX0iPgogICAgICAgICAgICAgICAgICAgIHt7IGIuc3RhdHVzIH19CiAgICAgICAgICAgICAgICAgIDwvc3Bhbj4KICAgICAgICAgICAgICAgIDwvdGQ+CiAgICAgICAgICAgICAgICA8dGQgY2xhc3M9InNtYWxsIj57eyBiLmNyZWFkb3MgfX0ve3sgYi5hY3R1YWxpemFkb3MgfX0ve3sgYi5lcnJvcmVzIH19PC90ZD4KICAgICAgICAgICAgICA8L3RyPgogICAgICAgICAgICAgIHslIGVtcHR5ICV9CiAgICAgICAgICAgICAgPHRyPjx0ZCBjb2xzcGFuPSI1IiBjbGFzcz0idGV4dC1tdXRlZCI+QcO6biBubyBoYXkgbG90ZXMuPC90ZD48L3RyPgogICAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgICAgICA8L3Rib2R5PgogICAgICAgICAgPC90YWJsZT4KICAgICAgICA8L2Rpdj4KICAgICAgPC9kaXY+CiAgICA8L2Rpdj4KCiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIG10LTMiPgogICAgICA8ZGl2IGNsYXNzPSJjYXJkLWJvZHkiPgogICAgICAgIDxoMiBjbGFzcz0iaDUiPlVwbG9hZHMgUEdDIHJlY2llbnRlczwvaDI+CiAgICAgICAgPGRpdiBjbGFzcz0idGFibGUtcmVzcG9uc2l2ZSI+CiAgICAgICAgICA8dGFibGUgY2xhc3M9InRhYmxlIHRhYmxlLXNtIG1iLTAgdGFibGUtd2NnIj4KICAgICAgICAgICAgPHRoZWFkPjx0cj48dGg+QXJjaGl2bzwvdGg+PHRoPlRpcG88L3RoPjx0aD5Fc3RhZG88L3RoPjwvdHI+PC90aGVhZD4KICAgICAgICAgICAgPHRib2R5PgogICAgICAgICAgICAgIHslIGZvciB1IGluIHVwbG9hZHMgJX0KICAgICAgICAgICAgICA8dHI+CiAgICAgICAgICAgICAgICA8dGQgY2xhc3M9InNtYWxsIj57eyB1Lm9yaWdpbmFsX2ZpbGVuYW1lfHRydW5jYXRlY2hhcnM6NDggfX08L3RkPgogICAgICAgICAgICAgICAgPHRkIGNsYXNzPSJzbWFsbCI+e3sgdS5nZXRfZmlsZV90eXBlX2RldGVjdGVkX2Rpc3BsYXkgfX08L3RkPgogICAgICAgICAgICAgICAgPHRkIGNsYXNzPSJzbWFsbCI+e3sgdS5nZXRfc3RhdHVzX2Rpc3BsYXkgfX08L3RkPgogICAgICAgICAgICAgIDwvdHI+CiAgICAgICAgICAgICAgeyUgZW1wdHkgJX0KICAgICAgICAgICAgICA8dHI+PHRkIGNvbHNwYW49IjMiIGNsYXNzPSJ0ZXh0LW11dGVkIj5TaW4gdXBsb2Fkcy48L3RkPjwvdHI+CiAgICAgICAgICAgICAgeyUgZW5kZm9yICV9CiAgICAgICAgICAgIDwvdGJvZHk+CiAgICAgICAgICA8L3RhYmxlPgogICAgICAgIDwvZGl2PgogICAgICA8L2Rpdj4KICAgIDwvZGl2PgogIDwvZGl2Pgo8L2Rpdj4KeyUgZW5kYmxvY2sgJX0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/includes/breadcrumbs.html
PATH_JSON="templates/includes/breadcrumbs.html"
FILENAME=breadcrumbs.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=13
SIZE_BYTES_UTF8=471
CONTENT_SHA256=6cd8ca10761f32a6c7bb48c890dc35c4510eb85273980ee5063bf9f2c2f8220b
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
{% if breadcrumbs %}
<nav aria-label="breadcrumb">
  <ol class="breadcrumb">
    {% for item in breadcrumbs %}
      {% if item.url and not forloop.last %}
        <li class="breadcrumb-item"><a href="{{ item.url }}">{{ item.label }}</a></li>
      {% else %}
        <li class="breadcrumb-item{% if forloop.last %} active{% endif %}"{% if forloop.last %} aria-current="page"{% endif %}>{{ item.label }}</li>
      {% endif %}
    {% endfor %}
  </ol>
</nav>
{% endif %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% if breadcrumbs %}
00002|<nav aria-label="breadcrumb">
00003|  <ol class="breadcrumb">
00004|    {% for item in breadcrumbs %}
00005|      {% if item.url and not forloop.last %}
00006|        <li class="breadcrumb-item"><a href="{{ item.url }}">{{ item.label }}</a></li>
00007|      {% else %}
00008|        <li class="breadcrumb-item{% if forloop.last %} active{% endif %}"{% if forloop.last %} aria-current="page"{% endif %}>{{ item.label }}</li>
00009|      {% endif %}
00010|    {% endfor %}
00011|  </ol>
00012|</nav>
00013|{% endif %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgaWYgYnJlYWRjcnVtYnMgJX0KPG5hdiBhcmlhLWxhYmVsPSJicmVhZGNydW1iIj4KICA8b2wgY2xhc3M9ImJyZWFkY3J1bWIiPgogICAgeyUgZm9yIGl0ZW0gaW4gYnJlYWRjcnVtYnMgJX0KICAgICAgeyUgaWYgaXRlbS51cmwgYW5kIG5vdCBmb3Jsb29wLmxhc3QgJX0KICAgICAgICA8bGkgY2xhc3M9ImJyZWFkY3J1bWItaXRlbSI+PGEgaHJlZj0ie3sgaXRlbS51cmwgfX0iPnt7IGl0ZW0ubGFiZWwgfX08L2E+PC9saT4KICAgICAgeyUgZWxzZSAlfQogICAgICAgIDxsaSBjbGFzcz0iYnJlYWRjcnVtYi1pdGVteyUgaWYgZm9ybG9vcC5sYXN0ICV9IGFjdGl2ZXslIGVuZGlmICV9InslIGlmIGZvcmxvb3AubGFzdCAlfSBhcmlhLWN1cnJlbnQ9InBhZ2UieyUgZW5kaWYgJX0+e3sgaXRlbS5sYWJlbCB9fTwvbGk+CiAgICAgIHslIGVuZGlmICV9CiAgICB7JSBlbmRmb3IgJX0KICA8L29sPgo8L25hdj4KeyUgZW5kaWYgJX0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/includes/empty_state.html
PATH_JSON="templates/includes/empty_state.html"
FILENAME=empty_state.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=12
SIZE_BYTES_UTF8=522
CONTENT_SHA256=9a0081641320d883d27dfb2cd37afc5138a23ffdc56bfa7108a74a1ee2834cd4
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
<div class="alert alert-info d-flex align-items-start gap-3 mb-3" role="alert">
  <div class="flex-grow-1">
    <h2 class="h6 alert-heading mb-1">{{ title }}</h2>
    <p class="mb-2 small">{{ message }}</p>
    {% if import_url %}
    <a href="{{ import_url }}" class="btn btn-sm btn-primary">{{ import_label|default:"Importar datos" }}</a>
    {% endif %}
    {% if secondary_url %}
    <a href="{{ secondary_url }}" class="btn btn-sm btn-outline-secondary ms-1">{{ secondary_label }}</a>
    {% endif %}
  </div>
</div>

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|<div class="alert alert-info d-flex align-items-start gap-3 mb-3" role="alert">
00002|  <div class="flex-grow-1">
00003|    <h2 class="h6 alert-heading mb-1">{{ title }}</h2>
00004|    <p class="mb-2 small">{{ message }}</p>
00005|    {% if import_url %}
00006|    <a href="{{ import_url }}" class="btn btn-sm btn-primary">{{ import_label|default:"Importar datos" }}</a>
00007|    {% endif %}
00008|    {% if secondary_url %}
00009|    <a href="{{ secondary_url }}" class="btn btn-sm btn-outline-secondary ms-1">{{ secondary_label }}</a>
00010|    {% endif %}
00011|  </div>
00012|</div>

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
PGRpdiBjbGFzcz0iYWxlcnQgYWxlcnQtaW5mbyBkLWZsZXggYWxpZ24taXRlbXMtc3RhcnQgZ2FwLTMgbWItMyIgcm9sZT0iYWxlcnQiPgogIDxkaXYgY2xhc3M9ImZsZXgtZ3Jvdy0xIj4KICAgIDxoMiBjbGFzcz0iaDYgYWxlcnQtaGVhZGluZyBtYi0xIj57eyB0aXRsZSB9fTwvaDI+CiAgICA8cCBjbGFzcz0ibWItMiBzbWFsbCI+e3sgbWVzc2FnZSB9fTwvcD4KICAgIHslIGlmIGltcG9ydF91cmwgJX0KICAgIDxhIGhyZWY9Int7IGltcG9ydF91cmwgfX0iIGNsYXNzPSJidG4gYnRuLXNtIGJ0bi1wcmltYXJ5Ij57eyBpbXBvcnRfbGFiZWx8ZGVmYXVsdDoiSW1wb3J0YXIgZGF0b3MiIH19PC9hPgogICAgeyUgZW5kaWYgJX0KICAgIHslIGlmIHNlY29uZGFyeV91cmwgJX0KICAgIDxhIGhyZWY9Int7IHNlY29uZGFyeV91cmwgfX0iIGNsYXNzPSJidG4gYnRuLXNtIGJ0bi1vdXRsaW5lLXNlY29uZGFyeSBtcy0xIj57eyBzZWNvbmRhcnlfbGFiZWwgfX08L2E+CiAgICB7JSBlbmRpZiAlfQogIDwvZGl2Pgo8L2Rpdj4K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/includes/kpi_cards.html
PATH_JSON="templates/includes/kpi_cards.html"
FILENAME=kpi_cards.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=12
SIZE_BYTES_UTF8=407
CONTENT_SHA256=d5b3ff729f5850a8a21f2280378a31da816bd5157d424adb1b53496bf9e4f6cf
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
<div class="row g-2 mb-3">
  {% for kpi in kpis %}
  <div class="{{ kpi.col_class|default:'col-md-3 col-6' }}">
    <div class="card border-0 shadow-sm h-100">
      <div class="card-body py-2 px-3 text-center">
        <div class="stat-value" style="font-size:1.4rem;">{{ kpi.value }}</div>
        <div class="text-muted small">{{ kpi.label }}</div>
      </div>
    </div>
  </div>
  {% endfor %}
</div>

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|<div class="row g-2 mb-3">
00002|  {% for kpi in kpis %}
00003|  <div class="{{ kpi.col_class|default:'col-md-3 col-6' }}">
00004|    <div class="card border-0 shadow-sm h-100">
00005|      <div class="card-body py-2 px-3 text-center">
00006|        <div class="stat-value" style="font-size:1.4rem;">{{ kpi.value }}</div>
00007|        <div class="text-muted small">{{ kpi.label }}</div>
00008|      </div>
00009|    </div>
00010|  </div>
00011|  {% endfor %}
00012|</div>

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
PGRpdiBjbGFzcz0icm93IGctMiBtYi0zIj4KICB7JSBmb3Iga3BpIGluIGtwaXMgJX0KICA8ZGl2IGNsYXNzPSJ7eyBrcGkuY29sX2NsYXNzfGRlZmF1bHQ6J2NvbC1tZC0zIGNvbC02JyB9fSI+CiAgICA8ZGl2IGNsYXNzPSJjYXJkIGJvcmRlci0wIHNoYWRvdy1zbSBoLTEwMCI+CiAgICAgIDxkaXYgY2xhc3M9ImNhcmQtYm9keSBweS0yIHB4LTMgdGV4dC1jZW50ZXIiPgogICAgICAgIDxkaXYgY2xhc3M9InN0YXQtdmFsdWUiIHN0eWxlPSJmb250LXNpemU6MS40cmVtOyI+e3sga3BpLnZhbHVlIH19PC9kaXY+CiAgICAgICAgPGRpdiBjbGFzcz0idGV4dC1tdXRlZCBzbWFsbCI+e3sga3BpLmxhYmVsIH19PC9kaXY+CiAgICAgIDwvZGl2PgogICAgPC9kaXY+CiAgPC9kaXY+CiAgeyUgZW5kZm9yICV9CjwvZGl2Pgo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/includes/messages.html
PATH_JSON="templates/includes/messages.html"
FILENAME=messages.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=10
SIZE_BYTES_UTF8=402
CONTENT_SHA256=dcdcd17b56d5b695ccce5752b6ffc8210a9a22e6f4156f188f271d45eb4a3833
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
{% if messages %}
<div class="mb-3">
  {% for message in messages %}
  <div class="alert alert-{% if message.tags == 'error' %}danger{% elif message.tags %}{{ message.tags }}{% else %}info{% endif %} alert-dismissible fade show" role="alert">
    {{ message }}
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button>
  </div>
  {% endfor %}
</div>
{% endif %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{% if messages %}
00002|<div class="mb-3">
00003|  {% for message in messages %}
00004|  <div class="alert alert-{% if message.tags == 'error' %}danger{% elif message.tags %}{{ message.tags }}{% else %}info{% endif %} alert-dismissible fade show" role="alert">
00005|    {{ message }}
00006|    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button>
00007|  </div>
00008|  {% endfor %}
00009|</div>
00010|{% endif %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyUgaWYgbWVzc2FnZXMgJX0KPGRpdiBjbGFzcz0ibWItMyI+CiAgeyUgZm9yIG1lc3NhZ2UgaW4gbWVzc2FnZXMgJX0KICA8ZGl2IGNsYXNzPSJhbGVydCBhbGVydC17JSBpZiBtZXNzYWdlLnRhZ3MgPT0gJ2Vycm9yJyAlfWRhbmdlcnslIGVsaWYgbWVzc2FnZS50YWdzICV9e3sgbWVzc2FnZS50YWdzIH19eyUgZWxzZSAlfWluZm97JSBlbmRpZiAlfSBhbGVydC1kaXNtaXNzaWJsZSBmYWRlIHNob3ciIHJvbGU9ImFsZXJ0Ij4KICAgIHt7IG1lc3NhZ2UgfX0KICAgIDxidXR0b24gdHlwZT0iYnV0dG9uIiBjbGFzcz0iYnRuLWNsb3NlIiBkYXRhLWJzLWRpc21pc3M9ImFsZXJ0IiBhcmlhLWxhYmVsPSJDZXJyYXIiPjwvYnV0dG9uPgogIDwvZGl2PgogIHslIGVuZGZvciAlfQo8L2Rpdj4KeyUgZW5kaWYgJX0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/includes/module_mark.html
PATH_JSON="templates/includes/module_mark.html"
FILENAME=module_mark.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=10
SIZE_BYTES_UTF8=499
CONTENT_SHA256=d417b548eba40d7d096d8f3970e0f7195ccc3016d59fa195ffc675f265df5c3f
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
{# Marcador de módulo: va a la derecha del título dentro de .wcg-report-head #}
{% if module == "pgc" %}
<span class="wcg-title-ico" aria-hidden="true" title="PGC">📊</span>
{% elif module == "pgo" %}
<span class="wcg-title-ico" aria-hidden="true" title="PGO">⚙️</span>
{% elif module == "crm" %}
<span class="wcg-title-ico" aria-hidden="true" title="CRM">👥</span>
{% elif module == "risk" %}
<span class="wcg-title-ico" aria-hidden="true" title="Balón de Riesgo">⚽</span>
{% endif %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{# Marcador de módulo: va a la derecha del título dentro de .wcg-report-head #}
00002|{% if module == "pgc" %}
00003|<span class="wcg-title-ico" aria-hidden="true" title="PGC">📊</span>
00004|{% elif module == "pgo" %}
00005|<span class="wcg-title-ico" aria-hidden="true" title="PGO">⚙️</span>
00006|{% elif module == "crm" %}
00007|<span class="wcg-title-ico" aria-hidden="true" title="CRM">👥</span>
00008|{% elif module == "risk" %}
00009|<span class="wcg-title-ico" aria-hidden="true" title="Balón de Riesgo">⚽</span>
00010|{% endif %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyMgTWFyY2Fkb3IgZGUgbcOzZHVsbzogdmEgYSBsYSBkZXJlY2hhIGRlbCB0w610dWxvIGRlbnRybyBkZSAud2NnLXJlcG9ydC1oZWFkICN9CnslIGlmIG1vZHVsZSA9PSAicGdjIiAlfQo8c3BhbiBjbGFzcz0id2NnLXRpdGxlLWljbyIgYXJpYS1oaWRkZW49InRydWUiIHRpdGxlPSJQR0MiPvCfk4o8L3NwYW4+CnslIGVsaWYgbW9kdWxlID09ICJwZ28iICV9CjxzcGFuIGNsYXNzPSJ3Y2ctdGl0bGUtaWNvIiBhcmlhLWhpZGRlbj0idHJ1ZSIgdGl0bGU9IlBHTyI+4pqZ77iPPC9zcGFuPgp7JSBlbGlmIG1vZHVsZSA9PSAiY3JtIiAlfQo8c3BhbiBjbGFzcz0id2NnLXRpdGxlLWljbyIgYXJpYS1oaWRkZW49InRydWUiIHRpdGxlPSJDUk0iPvCfkaU8L3NwYW4+CnslIGVsaWYgbW9kdWxlID09ICJyaXNrIiAlfQo8c3BhbiBjbGFzcz0id2NnLXRpdGxlLWljbyIgYXJpYS1oaWRkZW49InRydWUiIHRpdGxlPSJCYWzDs24gZGUgUmllc2dvIj7imr08L3NwYW4+CnslIGVuZGlmICV9Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/includes/navbar.html
PATH_JSON="templates/includes/navbar.html"
FILENAME=navbar.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=66
SIZE_BYTES_UTF8=3591
CONTENT_SHA256=125062da527bba47b2128ad6b2227de791f9409c225938886fc6ad30cf05bbea
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
<nav class="navbar navbar-expand-lg">
  <div class="container">
    <a class="navbar-brand wcg-brand mb-0" href="{% url 'portal:home' %}">WCG One</a>
    <a class="wcg-home-link d-none d-md-inline-flex" href="{% url 'portal:home' %}" title="Volver al menú principal">
      ← Menú principal
    </a>
    <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#wcgNav" aria-controls="wcgNav" aria-expanded="false" aria-label="Menú">
      <span class="navbar-toggler-icon" style="filter: invert(0.45);"></span>
    </button>
    <div class="collapse navbar-collapse" id="wcgNav">
      <ul class="navbar-nav wcg-nav-primary me-auto mb-2 mb-lg-0 mt-2 mt-lg-0">
        {% if user.is_authenticated %}
        <li class="nav-item d-md-none">
          <a class="nav-link fw-semibold" href="{% url 'portal:home' %}">← Menú principal</a>
        </li>
        {% endif %}
        <li class="nav-item">
          <a class="nav-link{% if '/tablero/' in request.path or '/pgc/' in request.path %} active{% endif %}" href="{% url 'pgc:dashboard' %}"><span class="wcg-mod-ico" aria-hidden="true">📊</span> PGC</a>
        </li>
        <li class="nav-item">
          <a class="nav-link{% if '/pgo/' in request.path %} active{% endif %}" href="{% url 'wcgone_pgo:dashboard' %}"><span class="wcg-mod-ico" aria-hidden="true">⚙️</span> PGO</a>
        </li>
        <li class="nav-item">
          <a class="nav-link{% if '/crm/' in request.path %} active{% endif %}" href="{% url 'wcgone_crm:entidad_list' %}"><span class="wcg-mod-ico" aria-hidden="true">👥</span> CRM</a>
        </li>
        <li class="nav-item">
          <a class="nav-link{% if '/risk/' in request.path %} active{% endif %}" href="{% url 'wcgone_risk:comando_balon' %}"><span class="wcg-mod-ico" aria-hidden="true">⚽</span> Balón de Riesgo</a>
        </li>
      </ul>
      <ul class="navbar-nav wcg-nav-secondary align-items-lg-center">
        {% if user.is_authenticated %}
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle{% if '/importaciones/' in request.path or '/panel/estado' in request.path %} active{% endif %}" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Administración
          </a>
          <ul class="dropdown-menu dropdown-menu-end">
            <li><h6 class="dropdown-header">Configuración del sistema</h6></li>
            <li>
              <a class="dropdown-item" href="{% url 'imports:import_hub' %}">Importación General</a>
            </li>
            <li><a class="dropdown-item" href="{% url 'portal:estado' %}">Estado del sistema</a></li>
            <li><a class="dropdown-item" href="{% url 'portal:ayuda' %}">Guía de uso</a></li>
            {% if user.is_superuser %}
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="/admin/" target="_blank" rel="noopener">Admin Django</a></li>
            {% endif %}
          </ul>
        </li>
        <li class="nav-item">
          <span class="nav-link disabled" style="opacity:0.7;">{{ user.get_username }}</span>
        </li>
        <li class="nav-item">
          <form method="post" action="{% url 'logout' %}" class="d-inline">
            {% csrf_token %}
            <button type="submit" class="btn btn-link nav-link">Salir</button>
          </form>
        </li>
        {% else %}
        <li class="nav-item">
          <a class="nav-link" href="{% url 'login' %}">Ingresar</a>
        </li>
        {% endif %}
      </ul>
    </div>
  </div>
</nav>

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|<nav class="navbar navbar-expand-lg">
00002|  <div class="container">
00003|    <a class="navbar-brand wcg-brand mb-0" href="{% url 'portal:home' %}">WCG One</a>
00004|    <a class="wcg-home-link d-none d-md-inline-flex" href="{% url 'portal:home' %}" title="Volver al menú principal">
00005|      ← Menú principal
00006|    </a>
00007|    <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#wcgNav" aria-controls="wcgNav" aria-expanded="false" aria-label="Menú">
00008|      <span class="navbar-toggler-icon" style="filter: invert(0.45);"></span>
00009|    </button>
00010|    <div class="collapse navbar-collapse" id="wcgNav">
00011|      <ul class="navbar-nav wcg-nav-primary me-auto mb-2 mb-lg-0 mt-2 mt-lg-0">
00012|        {% if user.is_authenticated %}
00013|        <li class="nav-item d-md-none">
00014|          <a class="nav-link fw-semibold" href="{% url 'portal:home' %}">← Menú principal</a>
00015|        </li>
00016|        {% endif %}
00017|        <li class="nav-item">
00018|          <a class="nav-link{% if '/tablero/' in request.path or '/pgc/' in request.path %} active{% endif %}" href="{% url 'pgc:dashboard' %}"><span class="wcg-mod-ico" aria-hidden="true">📊</span> PGC</a>
00019|        </li>
00020|        <li class="nav-item">
00021|          <a class="nav-link{% if '/pgo/' in request.path %} active{% endif %}" href="{% url 'wcgone_pgo:dashboard' %}"><span class="wcg-mod-ico" aria-hidden="true">⚙️</span> PGO</a>
00022|        </li>
00023|        <li class="nav-item">
00024|          <a class="nav-link{% if '/crm/' in request.path %} active{% endif %}" href="{% url 'wcgone_crm:entidad_list' %}"><span class="wcg-mod-ico" aria-hidden="true">👥</span> CRM</a>
00025|        </li>
00026|        <li class="nav-item">
00027|          <a class="nav-link{% if '/risk/' in request.path %} active{% endif %}" href="{% url 'wcgone_risk:comando_balon' %}"><span class="wcg-mod-ico" aria-hidden="true">⚽</span> Balón de Riesgo</a>
00028|        </li>
00029|      </ul>
00030|      <ul class="navbar-nav wcg-nav-secondary align-items-lg-center">
00031|        {% if user.is_authenticated %}
00032|        <li class="nav-item dropdown">
00033|          <a class="nav-link dropdown-toggle{% if '/importaciones/' in request.path or '/panel/estado' in request.path %} active{% endif %}" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
00034|            Administración
00035|          </a>
00036|          <ul class="dropdown-menu dropdown-menu-end">
00037|            <li><h6 class="dropdown-header">Configuración del sistema</h6></li>
00038|            <li>
00039|              <a class="dropdown-item" href="{% url 'imports:import_hub' %}">Importación General</a>
00040|            </li>
00041|            <li><a class="dropdown-item" href="{% url 'portal:estado' %}">Estado del sistema</a></li>
00042|            <li><a class="dropdown-item" href="{% url 'portal:ayuda' %}">Guía de uso</a></li>
00043|            {% if user.is_superuser %}
00044|            <li><hr class="dropdown-divider"></li>
00045|            <li><a class="dropdown-item" href="/admin/" target="_blank" rel="noopener">Admin Django</a></li>
00046|            {% endif %}
00047|          </ul>
00048|        </li>
00049|        <li class="nav-item">
00050|          <span class="nav-link disabled" style="opacity:0.7;">{{ user.get_username }}</span>
00051|        </li>
00052|        <li class="nav-item">
00053|          <form method="post" action="{% url 'logout' %}" class="d-inline">
00054|            {% csrf_token %}
00055|            <button type="submit" class="btn btn-link nav-link">Salir</button>
00056|          </form>
00057|        </li>
00058|        {% else %}
00059|        <li class="nav-item">
00060|          <a class="nav-link" href="{% url 'login' %}">Ingresar</a>
00061|        </li>
00062|        {% endif %}
00063|      </ul>
00064|    </div>
00065|  </div>
00066|</nav>

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
PG5hdiBjbGFzcz0ibmF2YmFyIG5hdmJhci1leHBhbmQtbGciPgogIDxkaXYgY2xhc3M9ImNvbnRhaW5lciI+CiAgICA8YSBjbGFzcz0ibmF2YmFyLWJyYW5kIHdjZy1icmFuZCBtYi0wIiBocmVmPSJ7JSB1cmwgJ3BvcnRhbDpob21lJyAlfSI+V0NHIE9uZTwvYT4KICAgIDxhIGNsYXNzPSJ3Y2ctaG9tZS1saW5rIGQtbm9uZSBkLW1kLWlubGluZS1mbGV4IiBocmVmPSJ7JSB1cmwgJ3BvcnRhbDpob21lJyAlfSIgdGl0bGU9IlZvbHZlciBhbCBtZW7DuiBwcmluY2lwYWwiPgogICAgICDihpAgTWVuw7ogcHJpbmNpcGFsCiAgICA8L2E+CiAgICA8YnV0dG9uIGNsYXNzPSJuYXZiYXItdG9nZ2xlciBib3JkZXItMCIgdHlwZT0iYnV0dG9uIiBkYXRhLWJzLXRvZ2dsZT0iY29sbGFwc2UiIGRhdGEtYnMtdGFyZ2V0PSIjd2NnTmF2IiBhcmlhLWNvbnRyb2xzPSJ3Y2dOYXYiIGFyaWEtZXhwYW5kZWQ9ImZhbHNlIiBhcmlhLWxhYmVsPSJNZW7DuiI+CiAgICAgIDxzcGFuIGNsYXNzPSJuYXZiYXItdG9nZ2xlci1pY29uIiBzdHlsZT0iZmlsdGVyOiBpbnZlcnQoMC40NSk7Ij48L3NwYW4+CiAgICA8L2J1dHRvbj4KICAgIDxkaXYgY2xhc3M9ImNvbGxhcHNlIG5hdmJhci1jb2xsYXBzZSIgaWQ9IndjZ05hdiI+CiAgICAgIDx1bCBjbGFzcz0ibmF2YmFyLW5hdiB3Y2ctbmF2LXByaW1hcnkgbWUtYXV0byBtYi0yIG1iLWxnLTAgbXQtMiBtdC1sZy0wIj4KICAgICAgICB7JSBpZiB1c2VyLmlzX2F1dGhlbnRpY2F0ZWQgJX0KICAgICAgICA8bGkgY2xhc3M9Im5hdi1pdGVtIGQtbWQtbm9uZSI+CiAgICAgICAgICA8YSBjbGFzcz0ibmF2LWxpbmsgZnctc2VtaWJvbGQiIGhyZWY9InslIHVybCAncG9ydGFsOmhvbWUnICV9Ij7ihpAgTWVuw7ogcHJpbmNpcGFsPC9hPgogICAgICAgIDwvbGk+CiAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICA8bGkgY2xhc3M9Im5hdi1pdGVtIj4KICAgICAgICAgIDxhIGNsYXNzPSJuYXYtbGlua3slIGlmICcvdGFibGVyby8nIGluIHJlcXVlc3QucGF0aCBvciAnL3BnYy8nIGluIHJlcXVlc3QucGF0aCAlfSBhY3RpdmV7JSBlbmRpZiAlfSIgaHJlZj0ieyUgdXJsICdwZ2M6ZGFzaGJvYXJkJyAlfSI+PHNwYW4gY2xhc3M9IndjZy1tb2QtaWNvIiBhcmlhLWhpZGRlbj0idHJ1ZSI+8J+Tijwvc3Bhbj4gUEdDPC9hPgogICAgICAgIDwvbGk+CiAgICAgICAgPGxpIGNsYXNzPSJuYXYtaXRlbSI+CiAgICAgICAgICA8YSBjbGFzcz0ibmF2LWxpbmt7JSBpZiAnL3Bnby8nIGluIHJlcXVlc3QucGF0aCAlfSBhY3RpdmV7JSBlbmRpZiAlfSIgaHJlZj0ieyUgdXJsICd3Y2dvbmVfcGdvOmRhc2hib2FyZCcgJX0iPjxzcGFuIGNsYXNzPSJ3Y2ctbW9kLWljbyIgYXJpYS1oaWRkZW49InRydWUiPuKame+4jzwvc3Bhbj4gUEdPPC9hPgogICAgICAgIDwvbGk+CiAgICAgICAgPGxpIGNsYXNzPSJuYXYtaXRlbSI+CiAgICAgICAgICA8YSBjbGFzcz0ibmF2LWxpbmt7JSBpZiAnL2NybS8nIGluIHJlcXVlc3QucGF0aCAlfSBhY3RpdmV7JSBlbmRpZiAlfSIgaHJlZj0ieyUgdXJsICd3Y2dvbmVfY3JtOmVudGlkYWRfbGlzdCcgJX0iPjxzcGFuIGNsYXNzPSJ3Y2ctbW9kLWljbyIgYXJpYS1oaWRkZW49InRydWUiPvCfkaU8L3NwYW4+IENSTTwvYT4KICAgICAgICA8L2xpPgogICAgICAgIDxsaSBjbGFzcz0ibmF2LWl0ZW0iPgogICAgICAgICAgPGEgY2xhc3M9Im5hdi1saW5reyUgaWYgJy9yaXNrLycgaW4gcmVxdWVzdC5wYXRoICV9IGFjdGl2ZXslIGVuZGlmICV9IiBocmVmPSJ7JSB1cmwgJ3djZ29uZV9yaXNrOmNvbWFuZG9fYmFsb24nICV9Ij48c3BhbiBjbGFzcz0id2NnLW1vZC1pY28iIGFyaWEtaGlkZGVuPSJ0cnVlIj7imr08L3NwYW4+IEJhbMOzbiBkZSBSaWVzZ288L2E+CiAgICAgICAgPC9saT4KICAgICAgPC91bD4KICAgICAgPHVsIGNsYXNzPSJuYXZiYXItbmF2IHdjZy1uYXYtc2Vjb25kYXJ5IGFsaWduLWl0ZW1zLWxnLWNlbnRlciI+CiAgICAgICAgeyUgaWYgdXNlci5pc19hdXRoZW50aWNhdGVkICV9CiAgICAgICAgPGxpIGNsYXNzPSJuYXYtaXRlbSBkcm9wZG93biI+CiAgICAgICAgICA8YSBjbGFzcz0ibmF2LWxpbmsgZHJvcGRvd24tdG9nZ2xleyUgaWYgJy9pbXBvcnRhY2lvbmVzLycgaW4gcmVxdWVzdC5wYXRoIG9yICcvcGFuZWwvZXN0YWRvJyBpbiByZXF1ZXN0LnBhdGggJX0gYWN0aXZleyUgZW5kaWYgJX0iIGhyZWY9IiMiIHJvbGU9ImJ1dHRvbiIgZGF0YS1icy10b2dnbGU9ImRyb3Bkb3duIiBhcmlhLWV4cGFuZGVkPSJmYWxzZSI+CiAgICAgICAgICAgIEFkbWluaXN0cmFjacOzbgogICAgICAgICAgPC9hPgogICAgICAgICAgPHVsIGNsYXNzPSJkcm9wZG93bi1tZW51IGRyb3Bkb3duLW1lbnUtZW5kIj4KICAgICAgICAgICAgPGxpPjxoNiBjbGFzcz0iZHJvcGRvd24taGVhZGVyIj5Db25maWd1cmFjacOzbiBkZWwgc2lzdGVtYTwvaDY+PC9saT4KICAgICAgICAgICAgPGxpPgogICAgICAgICAgICAgIDxhIGNsYXNzPSJkcm9wZG93bi1pdGVtIiBocmVmPSJ7JSB1cmwgJ2ltcG9ydHM6aW1wb3J0X2h1YicgJX0iPkltcG9ydGFjacOzbiBHZW5lcmFsPC9hPgogICAgICAgICAgICA8L2xpPgogICAgICAgICAgICA8bGk+PGEgY2xhc3M9ImRyb3Bkb3duLWl0ZW0iIGhyZWY9InslIHVybCAncG9ydGFsOmVzdGFkbycgJX0iPkVzdGFkbyBkZWwgc2lzdGVtYTwvYT48L2xpPgogICAgICAgICAgICA8bGk+PGEgY2xhc3M9ImRyb3Bkb3duLWl0ZW0iIGhyZWY9InslIHVybCAncG9ydGFsOmF5dWRhJyAlfSI+R3XDrWEgZGUgdXNvPC9hPjwvbGk+CiAgICAgICAgICAgIHslIGlmIHVzZXIuaXNfc3VwZXJ1c2VyICV9CiAgICAgICAgICAgIDxsaT48aHIgY2xhc3M9ImRyb3Bkb3duLWRpdmlkZXIiPjwvbGk+CiAgICAgICAgICAgIDxsaT48YSBjbGFzcz0iZHJvcGRvd24taXRlbSIgaHJlZj0iL2FkbWluLyIgdGFyZ2V0PSJfYmxhbmsiIHJlbD0ibm9vcGVuZXIiPkFkbWluIERqYW5nbzwvYT48L2xpPgogICAgICAgICAgICB7JSBlbmRpZiAlfQogICAgICAgICAgPC91bD4KICAgICAgICA8L2xpPgogICAgICAgIDxsaSBjbGFzcz0ibmF2LWl0ZW0iPgogICAgICAgICAgPHNwYW4gY2xhc3M9Im5hdi1saW5rIGRpc2FibGVkIiBzdHlsZT0ib3BhY2l0eTowLjc7Ij57eyB1c2VyLmdldF91c2VybmFtZSB9fTwvc3Bhbj4KICAgICAgICA8L2xpPgogICAgICAgIDxsaSBjbGFzcz0ibmF2LWl0ZW0iPgogICAgICAgICAgPGZvcm0gbWV0aG9kPSJwb3N0IiBhY3Rpb249InslIHVybCAnbG9nb3V0JyAlfSIgY2xhc3M9ImQtaW5saW5lIj4KICAgICAgICAgICAgeyUgY3NyZl90b2tlbiAlfQogICAgICAgICAgICA8YnV0dG9uIHR5cGU9InN1Ym1pdCIgY2xhc3M9ImJ0biBidG4tbGluayBuYXYtbGluayI+U2FsaXI8L2J1dHRvbj4KICAgICAgICAgIDwvZm9ybT4KICAgICAgICA8L2xpPgogICAgICAgIHslIGVsc2UgJX0KICAgICAgICA8bGkgY2xhc3M9Im5hdi1pdGVtIj4KICAgICAgICAgIDxhIGNsYXNzPSJuYXYtbGluayIgaHJlZj0ieyUgdXJsICdsb2dpbicgJX0iPkluZ3Jlc2FyPC9hPgogICAgICAgIDwvbGk+CiAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgPC91bD4KICAgIDwvZGl2PgogIDwvZGl2Pgo8L25hdj4K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgc/admin/_nav.html
PATH_JSON="templates/pgc/admin/_nav.html"
FILENAME=_nav.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=36
SIZE_BYTES_UTF8=2354
CONTENT_SHA256=9918e9febd049aafcb7f2590bcf3b91be35516b4a7aaa7e0320c1549cf20db3b
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
{# expects year, month, month_from, month_to, adm_nav_active; optional show_django_admin, recalc_status #}
<div class="adm-nav">
    <a href="{% url 'pgc:admin_monthly' %}?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}"
       class="{% if adm_nav_active == 'monthly' %}active{% endif %}">Tablero mensual</a>
    <a href="{% url 'pgc:admin_ingresos_year' %}?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}"
       class="{% if adm_nav_active == 'ingresos_year' %}active{% endif %}">Ingresos (año)</a>
    <a href="{% url 'pgc:admin_manual_edit' %}?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}"
       class="{% if adm_nav_active == 'manual' %}active{% endif %}">Edición manual</a>
    <a href="{% url 'pgc:admin_new_clients_browse' %}?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}"
       class="{% if adm_nav_active == 'clients_browse' %}active{% endif %}">Clientes (browse)</a>
    <a href="{% url 'pgc:admin_new_clients_une' %}?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}"
       class="{% if adm_nav_active == 'clients_une' %}active{% endif %}">Clientes (UNE)</a>
    <a href="{% url 'pgc:admin_monthly_log' %}?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}"
       class="{% if adm_nav_active == 'log' %}active{% endif %}">Bitácora</a>
    <a href="{% url 'pgc:admin_tv_charts' %}?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}"
       class="{% if adm_nav_active == 'tv_charts' %}active{% endif %}">TV charts</a>
    <div class="adm-nav-recalc">
        {% include "pgc/admin/_recalc_button.html" %}
    </div>
    {% if show_django_admin %}
    <a href="/admin/" class="adm-btn-ghost">Soporte técnico</a>
    {% endif %}
</div>
{% if recalc_status and recalc_status.is_pending and recalc_status.pending_periods %}
<details class="adm-recalc-details">
    <summary>Ver {{ recalc_status.pending_count }} período(s) pendiente(s)</summary>
    <ul>
        {% for p in recalc_status.pending_periods %}
        <li>
            <strong>{{ p.label }}</strong>
            — {{ p.reasons|join:"; " }}
        </li>
        {% endfor %}
    </ul>
</details>
{% endif %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{# expects year, month, month_from, month_to, adm_nav_active; optional show_django_admin, recalc_status #}
00002|<div class="adm-nav">
00003|    <a href="{% url 'pgc:admin_monthly' %}?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}"
00004|       class="{% if adm_nav_active == 'monthly' %}active{% endif %}">Tablero mensual</a>
00005|    <a href="{% url 'pgc:admin_ingresos_year' %}?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}"
00006|       class="{% if adm_nav_active == 'ingresos_year' %}active{% endif %}">Ingresos (año)</a>
00007|    <a href="{% url 'pgc:admin_manual_edit' %}?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}"
00008|       class="{% if adm_nav_active == 'manual' %}active{% endif %}">Edición manual</a>
00009|    <a href="{% url 'pgc:admin_new_clients_browse' %}?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}"
00010|       class="{% if adm_nav_active == 'clients_browse' %}active{% endif %}">Clientes (browse)</a>
00011|    <a href="{% url 'pgc:admin_new_clients_une' %}?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}"
00012|       class="{% if adm_nav_active == 'clients_une' %}active{% endif %}">Clientes (UNE)</a>
00013|    <a href="{% url 'pgc:admin_monthly_log' %}?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}"
00014|       class="{% if adm_nav_active == 'log' %}active{% endif %}">Bitácora</a>
00015|    <a href="{% url 'pgc:admin_tv_charts' %}?year={{ year }}&month_from={{ month_from }}&month_to={{ month_to }}&month={{ month }}"
00016|       class="{% if adm_nav_active == 'tv_charts' %}active{% endif %}">TV charts</a>
00017|    <div class="adm-nav-recalc">
00018|        {% include "pgc/admin/_recalc_button.html" %}
00019|    </div>
00020|    {% if show_django_admin %}
00021|    <a href="/admin/" class="adm-btn-ghost">Soporte técnico</a>
00022|    {% endif %}
00023|</div>
00024|{% if recalc_status and recalc_status.is_pending and recalc_status.pending_periods %}
00025|<details class="adm-recalc-details">
00026|    <summary>Ver {{ recalc_status.pending_count }} período(s) pendiente(s)</summary>
00027|    <ul>
00028|        {% for p in recalc_status.pending_periods %}
00029|        <li>
00030|            <strong>{{ p.label }}</strong>
00031|            — {{ p.reasons|join:"; " }}
00032|        </li>
00033|        {% endfor %}
00034|    </ul>
00035|</details>
00036|{% endif %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyMgZXhwZWN0cyB5ZWFyLCBtb250aCwgbW9udGhfZnJvbSwgbW9udGhfdG8sIGFkbV9uYXZfYWN0aXZlOyBvcHRpb25hbCBzaG93X2RqYW5nb19hZG1pbiwgcmVjYWxjX3N0YXR1cyAjfQo8ZGl2IGNsYXNzPSJhZG0tbmF2Ij4KICAgIDxhIGhyZWY9InslIHVybCAncGdjOmFkbWluX21vbnRobHknICV9P3llYXI9e3sgeWVhciB9fSZtb250aF9mcm9tPXt7IG1vbnRoX2Zyb20gfX0mbW9udGhfdG89e3sgbW9udGhfdG8gfX0mbW9udGg9e3sgbW9udGggfX0iCiAgICAgICBjbGFzcz0ieyUgaWYgYWRtX25hdl9hY3RpdmUgPT0gJ21vbnRobHknICV9YWN0aXZleyUgZW5kaWYgJX0iPlRhYmxlcm8gbWVuc3VhbDwvYT4KICAgIDxhIGhyZWY9InslIHVybCAncGdjOmFkbWluX2luZ3Jlc29zX3llYXInICV9P3llYXI9e3sgeWVhciB9fSZtb250aF9mcm9tPXt7IG1vbnRoX2Zyb20gfX0mbW9udGhfdG89e3sgbW9udGhfdG8gfX0mbW9udGg9e3sgbW9udGggfX0iCiAgICAgICBjbGFzcz0ieyUgaWYgYWRtX25hdl9hY3RpdmUgPT0gJ2luZ3Jlc29zX3llYXInICV9YWN0aXZleyUgZW5kaWYgJX0iPkluZ3Jlc29zIChhw7FvKTwvYT4KICAgIDxhIGhyZWY9InslIHVybCAncGdjOmFkbWluX21hbnVhbF9lZGl0JyAlfT95ZWFyPXt7IHllYXIgfX0mbW9udGhfZnJvbT17eyBtb250aF9mcm9tIH19Jm1vbnRoX3RvPXt7IG1vbnRoX3RvIH19Jm1vbnRoPXt7IG1vbnRoIH19IgogICAgICAgY2xhc3M9InslIGlmIGFkbV9uYXZfYWN0aXZlID09ICdtYW51YWwnICV9YWN0aXZleyUgZW5kaWYgJX0iPkVkaWNpw7NuIG1hbnVhbDwvYT4KICAgIDxhIGhyZWY9InslIHVybCAncGdjOmFkbWluX25ld19jbGllbnRzX2Jyb3dzZScgJX0/eWVhcj17eyB5ZWFyIH19Jm1vbnRoX2Zyb209e3sgbW9udGhfZnJvbSB9fSZtb250aF90bz17eyBtb250aF90byB9fSZtb250aD17eyBtb250aCB9fSIKICAgICAgIGNsYXNzPSJ7JSBpZiBhZG1fbmF2X2FjdGl2ZSA9PSAnY2xpZW50c19icm93c2UnICV9YWN0aXZleyUgZW5kaWYgJX0iPkNsaWVudGVzIChicm93c2UpPC9hPgogICAgPGEgaHJlZj0ieyUgdXJsICdwZ2M6YWRtaW5fbmV3X2NsaWVudHNfdW5lJyAlfT95ZWFyPXt7IHllYXIgfX0mbW9udGhfZnJvbT17eyBtb250aF9mcm9tIH19Jm1vbnRoX3RvPXt7IG1vbnRoX3RvIH19Jm1vbnRoPXt7IG1vbnRoIH19IgogICAgICAgY2xhc3M9InslIGlmIGFkbV9uYXZfYWN0aXZlID09ICdjbGllbnRzX3VuZScgJX1hY3RpdmV7JSBlbmRpZiAlfSI+Q2xpZW50ZXMgKFVORSk8L2E+CiAgICA8YSBocmVmPSJ7JSB1cmwgJ3BnYzphZG1pbl9tb250aGx5X2xvZycgJX0/eWVhcj17eyB5ZWFyIH19Jm1vbnRoX2Zyb209e3sgbW9udGhfZnJvbSB9fSZtb250aF90bz17eyBtb250aF90byB9fSZtb250aD17eyBtb250aCB9fSIKICAgICAgIGNsYXNzPSJ7JSBpZiBhZG1fbmF2X2FjdGl2ZSA9PSAnbG9nJyAlfWFjdGl2ZXslIGVuZGlmICV9Ij5CaXTDoWNvcmE8L2E+CiAgICA8YSBocmVmPSJ7JSB1cmwgJ3BnYzphZG1pbl90dl9jaGFydHMnICV9P3llYXI9e3sgeWVhciB9fSZtb250aF9mcm9tPXt7IG1vbnRoX2Zyb20gfX0mbW9udGhfdG89e3sgbW9udGhfdG8gfX0mbW9udGg9e3sgbW9udGggfX0iCiAgICAgICBjbGFzcz0ieyUgaWYgYWRtX25hdl9hY3RpdmUgPT0gJ3R2X2NoYXJ0cycgJX1hY3RpdmV7JSBlbmRpZiAlfSI+VFYgY2hhcnRzPC9hPgogICAgPGRpdiBjbGFzcz0iYWRtLW5hdi1yZWNhbGMiPgogICAgICAgIHslIGluY2x1ZGUgInBnYy9hZG1pbi9fcmVjYWxjX2J1dHRvbi5odG1sIiAlfQogICAgPC9kaXY+CiAgICB7JSBpZiBzaG93X2RqYW5nb19hZG1pbiAlfQogICAgPGEgaHJlZj0iL2FkbWluLyIgY2xhc3M9ImFkbS1idG4tZ2hvc3QiPlNvcG9ydGUgdMOpY25pY288L2E+CiAgICB7JSBlbmRpZiAlfQo8L2Rpdj4KeyUgaWYgcmVjYWxjX3N0YXR1cyBhbmQgcmVjYWxjX3N0YXR1cy5pc19wZW5kaW5nIGFuZCByZWNhbGNfc3RhdHVzLnBlbmRpbmdfcGVyaW9kcyAlfQo8ZGV0YWlscyBjbGFzcz0iYWRtLXJlY2FsYy1kZXRhaWxzIj4KICAgIDxzdW1tYXJ5PlZlciB7eyByZWNhbGNfc3RhdHVzLnBlbmRpbmdfY291bnQgfX0gcGVyw61vZG8ocykgcGVuZGllbnRlKHMpPC9zdW1tYXJ5PgogICAgPHVsPgogICAgICAgIHslIGZvciBwIGluIHJlY2FsY19zdGF0dXMucGVuZGluZ19wZXJpb2RzICV9CiAgICAgICAgPGxpPgogICAgICAgICAgICA8c3Ryb25nPnt7IHAubGFiZWwgfX08L3N0cm9uZz4KICAgICAgICAgICAg4oCUIHt7IHAucmVhc29uc3xqb2luOiI7ICIgfX0KICAgICAgICA8L2xpPgogICAgICAgIHslIGVuZGZvciAlfQogICAgPC91bD4KPC9kZXRhaWxzPgp7JSBlbmRpZiAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgc/admin/_period_select.html
PATH_JSON="templates/pgc/admin/_period_select.html"
FILENAME=_period_select.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=34
SIZE_BYTES_UTF8=1703
CONTENT_SHA256=c3db748b34d970606e7025da7dc0f71d6af4e9d05eafafa17d8b0e3890186126
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
{# expects year, month_from, month_to, month_choices, year_choices; optional: tab, selected_block #}
<form method="get" class="adm-period-select" id="adm-period-form">
    <div>
        <label for="year">Año</label><br>
        <select id="year" name="year" onchange="this.form.requestSubmit()">
            {% for y in year_choices %}
            <option value="{{ y }}" {% if y == year %}selected{% endif %}>{{ y }}</option>
            {% endfor %}
        </select>
    </div>
    <div>
        <label for="month_from">Desde</label><br>
        <select id="month_from" name="month_from" onchange="this.form.requestSubmit()">
            {% for m in month_choices %}
            <option value="{{ m }}" {% if m == month_from %}selected{% endif %}>{{ m|stringformat:"02d" }}</option>
            {% endfor %}
        </select>
    </div>
    <div>
        <label for="month_to">Hasta</label><br>
        <select id="month_to" name="month_to" onchange="this.form.requestSubmit()">
            {% for m in month_choices %}
            <option value="{{ m }}" {% if m == month_to %}selected{% endif %}>{{ m|stringformat:"02d" }}</option>
            {% endfor %}
        </select>
    </div>
    {% if tab %}<input type="hidden" name="tab" value="{{ tab }}">{% endif %}
    {% if selected_block %}<input type="hidden" name="block" value="{{ selected_block }}">{% endif %}
</form>
{% if period_is_range and single_month_ops %}
<p class="muted adm-period-hint">Esta pantalla opera solo el fin del rango: <strong>{{ period_focus_label }}</strong>.</p>
{% elif period_is_range and supports_month_range %}
<p class="muted adm-period-hint">Mostrando rango <strong>{{ period_label }}</strong>.</p>
{% endif %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{# expects year, month_from, month_to, month_choices, year_choices; optional: tab, selected_block #}
00002|<form method="get" class="adm-period-select" id="adm-period-form">
00003|    <div>
00004|        <label for="year">Año</label><br>
00005|        <select id="year" name="year" onchange="this.form.requestSubmit()">
00006|            {% for y in year_choices %}
00007|            <option value="{{ y }}" {% if y == year %}selected{% endif %}>{{ y }}</option>
00008|            {% endfor %}
00009|        </select>
00010|    </div>
00011|    <div>
00012|        <label for="month_from">Desde</label><br>
00013|        <select id="month_from" name="month_from" onchange="this.form.requestSubmit()">
00014|            {% for m in month_choices %}
00015|            <option value="{{ m }}" {% if m == month_from %}selected{% endif %}>{{ m|stringformat:"02d" }}</option>
00016|            {% endfor %}
00017|        </select>
00018|    </div>
00019|    <div>
00020|        <label for="month_to">Hasta</label><br>
00021|        <select id="month_to" name="month_to" onchange="this.form.requestSubmit()">
00022|            {% for m in month_choices %}
00023|            <option value="{{ m }}" {% if m == month_to %}selected{% endif %}>{{ m|stringformat:"02d" }}</option>
00024|            {% endfor %}
00025|        </select>
00026|    </div>
00027|    {% if tab %}<input type="hidden" name="tab" value="{{ tab }}">{% endif %}
00028|    {% if selected_block %}<input type="hidden" name="block" value="{{ selected_block }}">{% endif %}
00029|</form>
00030|{% if period_is_range and single_month_ops %}
00031|<p class="muted adm-period-hint">Esta pantalla opera solo el fin del rango: <strong>{{ period_focus_label }}</strong>.</p>
00032|{% elif period_is_range and supports_month_range %}
00033|<p class="muted adm-period-hint">Mostrando rango <strong>{{ period_label }}</strong>.</p>
00034|{% endif %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyMgZXhwZWN0cyB5ZWFyLCBtb250aF9mcm9tLCBtb250aF90bywgbW9udGhfY2hvaWNlcywgeWVhcl9jaG9pY2VzOyBvcHRpb25hbDogdGFiLCBzZWxlY3RlZF9ibG9jayAjfQo8Zm9ybSBtZXRob2Q9ImdldCIgY2xhc3M9ImFkbS1wZXJpb2Qtc2VsZWN0IiBpZD0iYWRtLXBlcmlvZC1mb3JtIj4KICAgIDxkaXY+CiAgICAgICAgPGxhYmVsIGZvcj0ieWVhciI+QcOxbzwvbGFiZWw+PGJyPgogICAgICAgIDxzZWxlY3QgaWQ9InllYXIiIG5hbWU9InllYXIiIG9uY2hhbmdlPSJ0aGlzLmZvcm0ucmVxdWVzdFN1Ym1pdCgpIj4KICAgICAgICAgICAgeyUgZm9yIHkgaW4geWVhcl9jaG9pY2VzICV9CiAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9Int7IHkgfX0iIHslIGlmIHkgPT0geWVhciAlfXNlbGVjdGVkeyUgZW5kaWYgJX0+e3sgeSB9fTwvb3B0aW9uPgogICAgICAgICAgICB7JSBlbmRmb3IgJX0KICAgICAgICA8L3NlbGVjdD4KICAgIDwvZGl2PgogICAgPGRpdj4KICAgICAgICA8bGFiZWwgZm9yPSJtb250aF9mcm9tIj5EZXNkZTwvbGFiZWw+PGJyPgogICAgICAgIDxzZWxlY3QgaWQ9Im1vbnRoX2Zyb20iIG5hbWU9Im1vbnRoX2Zyb20iIG9uY2hhbmdlPSJ0aGlzLmZvcm0ucmVxdWVzdFN1Ym1pdCgpIj4KICAgICAgICAgICAgeyUgZm9yIG0gaW4gbW9udGhfY2hvaWNlcyAlfQogICAgICAgICAgICA8b3B0aW9uIHZhbHVlPSJ7eyBtIH19IiB7JSBpZiBtID09IG1vbnRoX2Zyb20gJX1zZWxlY3RlZHslIGVuZGlmICV9Pnt7IG18c3RyaW5nZm9ybWF0OiIwMmQiIH19PC9vcHRpb24+CiAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgIDwvc2VsZWN0PgogICAgPC9kaXY+CiAgICA8ZGl2PgogICAgICAgIDxsYWJlbCBmb3I9Im1vbnRoX3RvIj5IYXN0YTwvbGFiZWw+PGJyPgogICAgICAgIDxzZWxlY3QgaWQ9Im1vbnRoX3RvIiBuYW1lPSJtb250aF90byIgb25jaGFuZ2U9InRoaXMuZm9ybS5yZXF1ZXN0U3VibWl0KCkiPgogICAgICAgICAgICB7JSBmb3IgbSBpbiBtb250aF9jaG9pY2VzICV9CiAgICAgICAgICAgIDxvcHRpb24gdmFsdWU9Int7IG0gfX0iIHslIGlmIG0gPT0gbW9udGhfdG8gJX1zZWxlY3RlZHslIGVuZGlmICV9Pnt7IG18c3RyaW5nZm9ybWF0OiIwMmQiIH19PC9vcHRpb24+CiAgICAgICAgICAgIHslIGVuZGZvciAlfQogICAgICAgIDwvc2VsZWN0PgogICAgPC9kaXY+CiAgICB7JSBpZiB0YWIgJX08aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJ0YWIiIHZhbHVlPSJ7eyB0YWIgfX0iPnslIGVuZGlmICV9CiAgICB7JSBpZiBzZWxlY3RlZF9ibG9jayAlfTxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9ImJsb2NrIiB2YWx1ZT0ie3sgc2VsZWN0ZWRfYmxvY2sgfX0iPnslIGVuZGlmICV9CjwvZm9ybT4KeyUgaWYgcGVyaW9kX2lzX3JhbmdlIGFuZCBzaW5nbGVfbW9udGhfb3BzICV9CjxwIGNsYXNzPSJtdXRlZCBhZG0tcGVyaW9kLWhpbnQiPkVzdGEgcGFudGFsbGEgb3BlcmEgc29sbyBlbCBmaW4gZGVsIHJhbmdvOiA8c3Ryb25nPnt7IHBlcmlvZF9mb2N1c19sYWJlbCB9fTwvc3Ryb25nPi48L3A+CnslIGVsaWYgcGVyaW9kX2lzX3JhbmdlIGFuZCBzdXBwb3J0c19tb250aF9yYW5nZSAlfQo8cCBjbGFzcz0ibXV0ZWQgYWRtLXBlcmlvZC1oaW50Ij5Nb3N0cmFuZG8gcmFuZ28gPHN0cm9uZz57eyBwZXJpb2RfbGFiZWwgfX08L3N0cm9uZz4uPC9wPgp7JSBlbmRpZiAlfQo=
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgc/admin/_recalc_button.html
PATH_JSON="templates/pgc/admin/_recalc_button.html"
FILENAME=_recalc_button.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=45
SIZE_BYTES_UTF8=1938
CONTENT_SHA256=21cfb93d69942340e02fd6787463d0998261b208a11b20a7e4d8077448406cbd
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
{# Botón universal de recálculo inteligente. Espera recalc_status + year/month* en contexto. #}
{% if recalc_status %}
<form method="post"
      action="{% url 'pgc:admin_smart_recalc' %}"
      class="adm-recalc-form"
      title="{{ recalc_status.button_hint }}">
    {% csrf_token %}
    <input type="hidden" name="year" value="{{ year }}">
    <input type="hidden" name="month" value="{{ month }}">
    <input type="hidden" name="month_from" value="{{ month_from }}">
    <input type="hidden" name="month_to" value="{{ month_to }}">
    <input type="hidden" name="next" value="{{ request.get_full_path }}">
    <button type="submit"
            class="adm-recalc-btn {% if recalc_status.is_pending %}is-pending{% else %}is-ready{% endif %}">
        <span class="adm-recalc-symbol" aria-hidden="true">{% if recalc_status.is_pending %}△{% else %}✓{% endif %}</span>
        <span class="adm-recalc-text">
            {% if recalc_status.is_pending %}
            Recalcular pendientes
            <span class="adm-recalc-count">({{ recalc_status.pending_count }})</span>
            {% else %}
            Recálculo al día
            {% endif %}
        </span>
        <span class="adm-recalc-spinner" aria-hidden="true"></span>
    </button>
</form>
<script>
(function () {
  var form = document.currentScript && document.currentScript.previousElementSibling;
  if (!form || !form.classList || !form.classList.contains("adm-recalc-form")) {
    form = document.querySelector(".adm-recalc-form");
  }
  if (!form || form.dataset.recalcBound) return;
  form.dataset.recalcBound = "1";
  form.addEventListener("submit", function () {
    var btn = form.querySelector(".adm-recalc-btn");
    if (!btn || btn.disabled) return;
    btn.disabled = true;
    btn.classList.add("is-working");
    var text = btn.querySelector(".adm-recalc-text");
    if (text) text.textContent = "Recalculando…";
  });
})();
</script>
{% endif %}

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|{# Botón universal de recálculo inteligente. Espera recalc_status + year/month* en contexto. #}
00002|{% if recalc_status %}
00003|<form method="post"
00004|      action="{% url 'pgc:admin_smart_recalc' %}"
00005|      class="adm-recalc-form"
00006|      title="{{ recalc_status.button_hint }}">
00007|    {% csrf_token %}
00008|    <input type="hidden" name="year" value="{{ year }}">
00009|    <input type="hidden" name="month" value="{{ month }}">
00010|    <input type="hidden" name="month_from" value="{{ month_from }}">
00011|    <input type="hidden" name="month_to" value="{{ month_to }}">
00012|    <input type="hidden" name="next" value="{{ request.get_full_path }}">
00013|    <button type="submit"
00014|            class="adm-recalc-btn {% if recalc_status.is_pending %}is-pending{% else %}is-ready{% endif %}">
00015|        <span class="adm-recalc-symbol" aria-hidden="true">{% if recalc_status.is_pending %}△{% else %}✓{% endif %}</span>
00016|        <span class="adm-recalc-text">
00017|            {% if recalc_status.is_pending %}
00018|            Recalcular pendientes
00019|            <span class="adm-recalc-count">({{ recalc_status.pending_count }})</span>
00020|            {% else %}
00021|            Recálculo al día
00022|            {% endif %}
00023|        </span>
00024|        <span class="adm-recalc-spinner" aria-hidden="true"></span>
00025|    </button>
00026|</form>
00027|<script>
00028|(function () {
00029|  var form = document.currentScript && document.currentScript.previousElementSibling;
00030|  if (!form || !form.classList || !form.classList.contains("adm-recalc-form")) {
00031|    form = document.querySelector(".adm-recalc-form");
00032|  }
00033|  if (!form || form.dataset.recalcBound) return;
00034|  form.dataset.recalcBound = "1";
00035|  form.addEventListener("submit", function () {
00036|    var btn = form.querySelector(".adm-recalc-btn");
00037|    if (!btn || btn.disabled) return;
00038|    btn.disabled = true;
00039|    btn.classList.add("is-working");
00040|    var text = btn.querySelector(".adm-recalc-text");
00041|    if (text) text.textContent = "Recalculando…";
00042|  });
00043|})();
00044|</script>
00045|{% endif %}

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
eyMgQm90w7NuIHVuaXZlcnNhbCBkZSByZWPDoWxjdWxvIGludGVsaWdlbnRlLiBFc3BlcmEgcmVjYWxjX3N0YXR1cyArIHllYXIvbW9udGgqIGVuIGNvbnRleHRvLiAjfQp7JSBpZiByZWNhbGNfc3RhdHVzICV9Cjxmb3JtIG1ldGhvZD0icG9zdCIKICAgICAgYWN0aW9uPSJ7JSB1cmwgJ3BnYzphZG1pbl9zbWFydF9yZWNhbGMnICV9IgogICAgICBjbGFzcz0iYWRtLXJlY2FsYy1mb3JtIgogICAgICB0aXRsZT0ie3sgcmVjYWxjX3N0YXR1cy5idXR0b25faGludCB9fSI+CiAgICB7JSBjc3JmX3Rva2VuICV9CiAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJ5ZWFyIiB2YWx1ZT0ie3sgeWVhciB9fSI+CiAgICA8aW5wdXQgdHlwZT0iaGlkZGVuIiBuYW1lPSJtb250aCIgdmFsdWU9Int7IG1vbnRoIH19Ij4KICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9Im1vbnRoX2Zyb20iIHZhbHVlPSJ7eyBtb250aF9mcm9tIH19Ij4KICAgIDxpbnB1dCB0eXBlPSJoaWRkZW4iIG5hbWU9Im1vbnRoX3RvIiB2YWx1ZT0ie3sgbW9udGhfdG8gfX0iPgogICAgPGlucHV0IHR5cGU9ImhpZGRlbiIgbmFtZT0ibmV4dCIgdmFsdWU9Int7IHJlcXVlc3QuZ2V0X2Z1bGxfcGF0aCB9fSI+CiAgICA8YnV0dG9uIHR5cGU9InN1Ym1pdCIKICAgICAgICAgICAgY2xhc3M9ImFkbS1yZWNhbGMtYnRuIHslIGlmIHJlY2FsY19zdGF0dXMuaXNfcGVuZGluZyAlfWlzLXBlbmRpbmd7JSBlbHNlICV9aXMtcmVhZHl7JSBlbmRpZiAlfSI+CiAgICAgICAgPHNwYW4gY2xhc3M9ImFkbS1yZWNhbGMtc3ltYm9sIiBhcmlhLWhpZGRlbj0idHJ1ZSI+eyUgaWYgcmVjYWxjX3N0YXR1cy5pc19wZW5kaW5nICV94pazeyUgZWxzZSAlfeKck3slIGVuZGlmICV9PC9zcGFuPgogICAgICAgIDxzcGFuIGNsYXNzPSJhZG0tcmVjYWxjLXRleHQiPgogICAgICAgICAgICB7JSBpZiByZWNhbGNfc3RhdHVzLmlzX3BlbmRpbmcgJX0KICAgICAgICAgICAgUmVjYWxjdWxhciBwZW5kaWVudGVzCiAgICAgICAgICAgIDxzcGFuIGNsYXNzPSJhZG0tcmVjYWxjLWNvdW50Ij4oe3sgcmVjYWxjX3N0YXR1cy5wZW5kaW5nX2NvdW50IH19KTwvc3Bhbj4KICAgICAgICAgICAgeyUgZWxzZSAlfQogICAgICAgICAgICBSZWPDoWxjdWxvIGFsIGTDrWEKICAgICAgICAgICAgeyUgZW5kaWYgJX0KICAgICAgICA8L3NwYW4+CiAgICAgICAgPHNwYW4gY2xhc3M9ImFkbS1yZWNhbGMtc3Bpbm5lciIgYXJpYS1oaWRkZW49InRydWUiPjwvc3Bhbj4KICAgIDwvYnV0dG9uPgo8L2Zvcm0+CjxzY3JpcHQ+CihmdW5jdGlvbiAoKSB7CiAgdmFyIGZvcm0gPSBkb2N1bWVudC5jdXJyZW50U2NyaXB0ICYmIGRvY3VtZW50LmN1cnJlbnRTY3JpcHQucHJldmlvdXNFbGVtZW50U2libGluZzsKICBpZiAoIWZvcm0gfHwgIWZvcm0uY2xhc3NMaXN0IHx8ICFmb3JtLmNsYXNzTGlzdC5jb250YWlucygiYWRtLXJlY2FsYy1mb3JtIikpIHsKICAgIGZvcm0gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKCIuYWRtLXJlY2FsYy1mb3JtIik7CiAgfQogIGlmICghZm9ybSB8fCBmb3JtLmRhdGFzZXQucmVjYWxjQm91bmQpIHJldHVybjsKICBmb3JtLmRhdGFzZXQucmVjYWxjQm91bmQgPSAiMSI7CiAgZm9ybS5hZGRFdmVudExpc3RlbmVyKCJzdWJtaXQiLCBmdW5jdGlvbiAoKSB7CiAgICB2YXIgYnRuID0gZm9ybS5xdWVyeVNlbGVjdG9yKCIuYWRtLXJlY2FsYy1idG4iKTsKICAgIGlmICghYnRuIHx8IGJ0bi5kaXNhYmxlZCkgcmV0dXJuOwogICAgYnRuLmRpc2FibGVkID0gdHJ1ZTsKICAgIGJ0bi5jbGFzc0xpc3QuYWRkKCJpcy13b3JraW5nIik7CiAgICB2YXIgdGV4dCA9IGJ0bi5xdWVyeVNlbGVjdG9yKCIuYWRtLXJlY2FsYy10ZXh0Iik7CiAgICBpZiAodGV4dCkgdGV4dC50ZXh0Q29udGVudCA9ICJSZWNhbGN1bGFuZG/igKYiOwogIH0pOwp9KSgpOwo8L3NjcmlwdD4KeyUgZW5kaWYgJX0K
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
BEGIN_LITERAL_FILE_RECORD
PATH_LITERAL=templates/pgc/admin/_save_footer.html
PATH_JSON="templates/pgc/admin/_save_footer.html"
FILENAME=_save_footer.html
EXTENSION=.html
LANGUAGE_HINT=html
LINE_COUNT=13
SIZE_BYTES_UTF8=640
CONTENT_SHA256=00a1e626aba662c0081ae3b5c8a5c30cf995127378e7498ea476f6d6cd6a7438
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
<div class="adm-form-footer">
    <div>
        <label for="reason">Motivo{% if reason_required %} (obligatorio){% else %} (opcional){% endif %}</label><br>
        <input type="text" name="reason" id="reason" {% if reason_required %}required{% endif %}
               placeholder="Ej. corrección tras revisión de archivo">
    </div>
    <label style="display:flex; align-items:center; gap:6px; font-size:0.88rem;">
        <input type="checkbox" name="recalc_after" value="1">
        Recalcular período después de guardar
    </label>
    <button type="submit" class="adm-btn adm-btn-primary">Guardar cambios</button>
</div>
</form>

~~~~~
CONTENT_END

CONTENT_NUMBERED_BEGIN
00001|<div class="adm-form-footer">
00002|    <div>
00003|        <label for="reason">Motivo{% if reason_required %} (obligatorio){% else %} (opcional){% endif %}</label><br>
00004|        <input type="text" name="reason" id="reason" {% if reason_required %}required{% endif %}
00005|               placeholder="Ej. corrección tras revisión de archivo">
00006|    </div>
00007|    <label style="display:flex; align-items:center; gap:6px; font-size:0.88rem;">
00008|        <input type="checkbox" name="recalc_after" value="1">
00009|        Recalcular período después de guardar
00010|    </label>
00011|    <button type="submit" class="adm-btn adm-btn-primary">Guardar cambios</button>
00012|</div>
00013|</form>

CONTENT_NUMBERED_END

CONTENT_BASE64_BEGIN
PGRpdiBjbGFzcz0iYWRtLWZvcm0tZm9vdGVyIj4KICAgIDxkaXY+CiAgICAgICAgPGxhYmVsIGZvcj0icmVhc29uIj5Nb3Rpdm97JSBpZiByZWFzb25fcmVxdWlyZWQgJX0gKG9ibGlnYXRvcmlvKXslIGVsc2UgJX0gKG9wY2lvbmFsKXslIGVuZGlmICV9PC9sYWJlbD48YnI+CiAgICAgICAgPGlucHV0IHR5cGU9InRleHQiIG5hbWU9InJlYXNvbiIgaWQ9InJlYXNvbiIgeyUgaWYgcmVhc29uX3JlcXVpcmVkICV9cmVxdWlyZWR7JSBlbmRpZiAlfQogICAgICAgICAgICAgICBwbGFjZWhvbGRlcj0iRWouIGNvcnJlY2Npw7NuIHRyYXMgcmV2aXNpw7NuIGRlIGFyY2hpdm8iPgogICAgPC9kaXY+CiAgICA8bGFiZWwgc3R5bGU9ImRpc3BsYXk6ZmxleDsgYWxpZ24taXRlbXM6Y2VudGVyOyBnYXA6NnB4OyBmb250LXNpemU6MC44OHJlbTsiPgogICAgICAgIDxpbnB1dCB0eXBlPSJjaGVja2JveCIgbmFtZT0icmVjYWxjX2FmdGVyIiB2YWx1ZT0iMSI+CiAgICAgICAgUmVjYWxjdWxhciBwZXLDrW9kbyBkZXNwdcOpcyBkZSBndWFyZGFyCiAgICA8L2xhYmVsPgogICAgPGJ1dHRvbiB0eXBlPSJzdWJtaXQiIGNsYXNzPSJhZG0tYnRuIGFkbS1idG4tcHJpbWFyeSI+R3VhcmRhciBjYW1iaW9zPC9idXR0b24+CjwvZGl2Pgo8L2Zvcm0+Cg==
CONTENT_BASE64_END

END_LITERAL_FILE_RECORD

========== RECORD_BOUNDARY ==========
