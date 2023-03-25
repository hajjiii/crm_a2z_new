from .models import Leads
import django_filters

class LeadFilter(django_filters.FilterSet):
    fromdate = django_filters.DateFilter(field_name="lead_generated_date", lookup_expr='gte')
    todate = django_filters.DateFilter(field_name="lead_generated_date", lookup_expr='lte')
    class Meta:
        model = Leads
        fields = ['lead_title', 'contact_person_name', 'contact_person_phone','interest_rate','lead_generated_date','min_price','max_price','status','lead_category' ]