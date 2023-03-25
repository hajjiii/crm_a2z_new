from django import forms
from .models import *

class LeadAddForm(forms.ModelForm):
    class Meta:
        model = Leads
        fields = "__all__"
        exclude = ['added_by','added_on','added_by_admin']

        widgets ={
            'lead_title':forms.TextInput(attrs={'class':'form-control'}),
            'lead_description':forms.Textarea(attrs={'class':'form-control','rows':'3'}),
            'contact_person_name':forms.TextInput(attrs={'class':'form-control'}),
            'contact_person_phone':forms.TextInput(attrs={'class':'form-control'}),
            'contact_person_designation':forms.TextInput(attrs={'class':'form-control'}),
            'business_name':forms.TextInput(attrs={'class':'form-control'}),
            'business_address':forms.Textarea(attrs={'class':'form-control','rows':'3'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'district':forms.Select(attrs={'class':'form-control'}),
            'city':forms.Select(attrs={'class':'form-control'}),
            # 'city':forms.TextInput(attrs={'class':'form-control'}),
            'interest_rate':forms.Select(attrs={'class':'form-control'}),
            'lead_generated_date':forms.DateInput(attrs={'class':'form-control','type': 'date'}),
            'next_follow_up_date':forms.DateInput(attrs={'class':'form-control','type': 'date'}),
            'min_price':forms.NumberInput(attrs={'class':'form-control'}),
            'max_price':forms.NumberInput(attrs={'class':'form-control'}),
            'lead_category':forms.Select(attrs={'class':'form-control'}),
            'status':forms.Select(attrs={'class':'form-control'}),
            'notes_about_client':forms.Textarea(attrs={'class':'form-control','rows':'3'})

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].queryset = District.objects.none()
        self.fields['city'].queryset = City.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['district'].queryset = District.objects.filter(state=state_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.state.district_set.all()

        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['city'].queryset = City.objects.filter(district=district_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.district:
            self.fields['city'].queryset = self.instance.district.city_set.all()
    

class LeadViewForm(forms.ModelForm):
    notes_about_client = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows':3}), required=True)
    class Meta:
        model = Leads
        fields = ['notes_about_client']
       