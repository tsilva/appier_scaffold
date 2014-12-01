{% extends "partials/layout.html.tpl" %}
{% block title %}Sign Up{% endblock %}
{% block name %}Sign Up{% endblock %}
{% block content %}
    {% if success %}
        <div class="quote success">
            {{ success }}
        </div>
    {% endif %}
    {% if error %}
        <div class="quote error">
            {{ error }}
        </div>
    {% endif %}
    <form action="{{ url_for('base.signup_post') }}" method="post" class="form">
        <div class="input">
            <input class="text-field small" name="name" value="{{ account.name }}" placeholder="name" data-error="{{ errors.name|default('', True) }}" />
        </div>
        <div class="input">
            <input class="text-field small" name="email" value="{{ account.email }}" placeholder="email" data-error="{{ errors.email|default('', True) }}" />
        </div>
        <div class="input">
            <input class="text-field small" name="_password" placeholder="password" type="password" data-error="{{ errors._password|default('', True) }}" />
        </div>
        <div class="input">
            <input class="text-field small" name="_password_confirm" placeholder="confirm password" type="password" data-error="{{ errors._password_confirm|default('', True) }}" />
        </div>
        <span class="button" data-submit="true">Sign Up</span>
    </form>
{% endblock %}
