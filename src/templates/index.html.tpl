{% extends "partials/layout.html.tpl" %}
{% block title %}Home{% endblock %}
{% block name %}Test App{% endblock %}
{% block content %}
    {% if success %}
        <div class="quote success">
            {{ success }}
        </div>
    {% endif %}
{% endblock %}
