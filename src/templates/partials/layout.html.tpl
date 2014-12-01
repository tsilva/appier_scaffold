{% include "partials/doctype.html.tpl" %}
<head>
    {% block head %}
        {% include "partials/content_type.html.tpl" %}
        {% include "partials/includes.html.tpl" %}
        {% include "partials/analytics.html.tpl" %}
        <title>Test App / {% block title %}{% endblock %}</title>
    {% endblock %}
</head>
<body class="ux romantic wait-load">
    <div id="overlay" class="overlay"></div>
    <div id="header">
        {% block header %}
            <h1>{% block name %}{% endblock %}</h1>
            <div class="links">
                {% if link == "home" %}
                    <a href="{{ url_for('base.index') }}" class="active">home</a>
                {% else %}
                    <a href="{{ url_for('base.index') }}">home</a>
                {% endif %}
                //
                {% if account_s and account_s.is_owner %}
                    {% if link == "accounts" %}
                        <a href="{{ url_for('account.list') }}" class="active">accounts</a>
                    {% else %}
                        <a href="{{ url_for('account.list') }}">accounts</a>
                    {% endif %}
                    //
                 {% endif %}
                {% if link == "about" %}
                    <a href="{{ url_for('base.about') }}" class="active">about</a>
                {% else %}
                    <a href="{{ url_for('base.about') }}">about</a>
                {% endif %}
                ||
                {% if account_s %}
                    <a href="{{ url_for('base.logout') }}">logout</a>
                {% else %}
                    {% if link == "signin" %}
                        <a href="{{ url_for('base.login') }}" class="active">signin</a>
                    {% else %}
                        <a href="{{ url_for('base.login') }}">signin</a>
                    {% endif %}
                    //
                    {% if link == "signup" %}
                        <a href="{{ url_for('base.signup_get') }}" class="active">signup</a>
                    {% else %}
                        <a href="{{ url_for('base.signup_get') }}">signup</a>
                    {% endif %}
                {% endif %}
            </div>
        {% endblock %}
    </div>
    <div id="content" class="shortcuts">
        {% block content %}{% endblock %}
    </div>
    {% include "partials/footer.html.tpl" %}
</body>
{% include "partials/end_doctype.html.tpl" %}
