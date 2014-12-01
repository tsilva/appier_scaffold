<div id="footer">
    {% block footer %}
        &copy; Copyright 2014 by <a href="http://www.testapp.com">Test</a>.<br />
        <div class="button footer-logo" data-link="{{ url_for('base.index') }}"></div>
    {% endblock %}
</div>
