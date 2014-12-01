{% extends "partials/layout.html.tpl" %}
{% block title %}Sign In{% endblock %}
{% block name %}Sign In{% endblock %}
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
    <form action="{{ url_for('base.login_post') }}" method="post" class="form">
        <input type="hidden" name="next" value="{{ next|default('', True) }}" />
        <div class="input">
            <input class="small" name="email" value="{{ email }}" placeholder="email" />
        </div>
        <div class="input">
            <input class="small" name="password" placeholder="password" type="password" />
        </div>
        <span class="button" data-submit="true">Sign in</span>
        <p>
            <a href="{{ url_for('base.recover_get') }}">Forgot Password?</a>
           </p>
    </form>
{% endblock %}
