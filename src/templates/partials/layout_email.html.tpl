{% include "partials/doctype.html.tpl" %}
<head>
    {% block head %}
        {% include "partials/content_type.html.tpl" %}
    {% endblock %}
</head>
<body>
    {% block content %}{% endblock %}
</body>
{% include "partials/end_doctype.html.tpl" %}
