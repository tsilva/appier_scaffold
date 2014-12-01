{% extends "partials/layout.html.tpl" %}
{% block title %}Recover Password{% endblock %}
{% block name %}Recover Password{% endblock %}
{% block content %}
    <form class="form form-medium" action="{{ url_for('base.recover_post') }}" method="post">
        <p>Please type your email, click send email, then check your inbox for further instructions.</p>
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
            <input class="small" name="email" value="{{ email }}" placeholder="email" />
        </div>
        <span class="button" data-submit="true">Send Email</span>
    </form>
{% endblock %}
