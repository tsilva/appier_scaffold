{% extends "partials/layout.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        {% if sub_link == "list" %}
            <a href="{{ url_for('account.list_accounts') }}" class="active">list</a>
        {% else %}
            <a href="{{ url_for('account.list_accounts') }}">list</a>
        {% endif %}
        {% if account_s and account_s.is_owner %}
            //
            {% if sub_link == "create" %}
                <a href="{{ url_for('account.new_account') }}" class="active">create</a>
            {% else %}
                <a href="{{ url_for('account.new_account') }}">create</a>
            {% endif %}
        {% endif %}
    </div>
{% endblock %}
