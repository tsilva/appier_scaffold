{% extends "partials/layout.html.tpl" %}
{% block title %}Change Password{% endblock %}
{% block name %}Change Password{% endblock %}
{% block content %}
    <form class="form form-medium" action="{{ url_for('base.reset_post') }}" method="post">
        <input type="hidden" name="reset_code" value="{{ reset_code }}" />
        <p>Please type your new password and click change password.</p>
        <br />
        {% if success %}
            <p>
                <span class="success">{{ success }}</span>
            </p>
        {% endif %}
        {% if error %}
            <p>
                <span class="error">{{ error }}</span>
            </p>
        {% endif %}
        <br />
        <div class="input">
            <input type="password" class="text-field small"
                   name="_password" placeholder="password"
                   data-error="{{ errors.password }}" />
        </div>
        <div class="input">
            <input type="password" class="text-field small"
                   name="_password_confirm" placeholder="confirm password"
                   data-error="{{ errors.confirm_password }}" />
        </div>
        <span class="button" data-submit="true">Change Password</span>
    </form>
{% endblock %}
