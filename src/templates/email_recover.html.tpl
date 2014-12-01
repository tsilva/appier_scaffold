{% extends "partials/layout_email.html.tpl" %}
{% block content %}
    <p>
        Dear {{ account.name }},<br />
        <br />
        Someone requested a new password for your account. In case this was you, just click the following link:<br />
        <br />
        <a href="{{ account.get_reset_url() }}">Change password</a><br />
        <br />
        If you didn't ask us for help with your password, please <a href="mailto:{{ sender }}">let us know</a> right away.<br />
        <br />
        Yours sincerely,<br />
        {{ sender_name|default('Administrator', True) }}
    </p>
{% endblock %}
