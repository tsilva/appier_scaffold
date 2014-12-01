{% extends "partials/layout.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        {% if sub_link == "show" %}
            <a href="{{ url_for('account.show_account', id = account.id) }}" class="active">show</a>
        {% else %}
            <a href="{{ url_for('account.show_account', id = account.id) }}">show</a>
        {% endif %}
        {% if account_s and account_s.is_owner %}
            //
            {% if sub_link == "edit" %}
                <a href="{{ url_for('account.edit_account', id = account.id) }}" class="active">edit</a>
            {% else %}
                <a href="{{ url_for('account.edit_account', id = account.id) }}">edit</a>
            {% endif %}
            //
            {% if account.enabled %}
                <a class="link link-red link-confirm warning" href="{{ url_for('disable_account', id = account.id) }}"
                   data-message="Do you really want to disable [{{ account.nickname }}] ?">disable</a>
            {% else %}
                <a class="link link-red link-confirm warning" href="{{ url_for('enable_account', id = account.id) }}"
                   data-message="Do you really want to enable [{{ account.nickname }}] ?">enable</a>
            {% endif %}
        {% endif %}
    </div>
{% endblock %}
