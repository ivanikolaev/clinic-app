from django import template

register = template.Library()

@register.simple_tag
def doctor_icon(specialization):
    """
    Returns the appropriate Font Awesome icon class for a doctor's specialization.
    
    Usage: {% doctor_icon doctor.specialization %}
    """
    icons = {
        'Терапевт': 'fa-stethoscope',
        'Кардиолог': 'fa-heartbeat',
        'Невролог': 'fa-brain',
        'Хирург': 'fa-procedures',
        'Педиатр': 'fa-baby',
        'Психотерапевт': 'fa-comments',
        'Инфекционист': 'fa-virus',
        'Стоматолог': 'fa-tooth',
    }
    
    return icons.get(specialization, 'fa-user-md')

@register.simple_tag
def doctor_icon_with_size(specialization, size='4x'):
    """
    Returns a complete Font Awesome icon HTML for a doctor's specialization with specified size.
    
    Usage: {% doctor_icon_with_size doctor.specialization '5x' %}
    """
    icon = doctor_icon(specialization)
    return f'fas {icon} fa-{size} text-primary mb-3'