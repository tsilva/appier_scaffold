<div id="footer">
    {% block footer %}
        &copy; Copyright 2014 by <a href="http://www.test.com">Test App</a>.<br />
        <div class="button footer-logo" data-link="{{ url_for('base.index') }}"></div>
    {% endblock %}
</div>
