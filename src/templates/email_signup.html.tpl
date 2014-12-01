{% extends "partials/layout_email.html.tpl" %}
{% block content %}
    <p>
        Hello {{ account.name }},<br />
        <br />
        Welcome to Test App! Please click the following link to confirm your account:<br />
        <br />
        <a href="{{ account.get_confirm_url() }}">Confirm account</a><br />
        <br />
        Yours sincerely,<br />
        {{ sender_name|default('Administrator', True) }}
    </p>
{% endblock %}
