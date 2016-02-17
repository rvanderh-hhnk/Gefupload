{% extends "base.html" %}
{% load crispy_forms_tags %}

{% block form1 %}
<div class='row'>
<div class='col-sm-6 col-sm-offset-3'>
<form method='POST' action''>{% crsf_token %}
{{ form|crispy }}

<input class='btn btn-default' type='submit' value='Submin' />

</form>
</div>
</div>

# dit nog een keer doen...
