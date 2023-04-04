from django import forms
from .models import *

class LeadAddForm(forms.ModelForm):
    class Meta:
        model = Leads
        fields = "__all__"
        exclude = ['added_by','added_on','added_by_admin','exit_lead_desc']

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
       


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields =['description']
        widgets ={
            'description':forms.Textarea(attrs={'class':'form-control','rows':'3'}),
        }
        

class LeadsManpowerAssignmentForm(forms.ModelForm):
    added_by = forms.ModelMultipleChoiceField(queryset=ExtendedUserModel.objects.filter(usertype='Field Executive'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    
    class Meta:
        model = Leads
        fields = ['added_by']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get the branch of the exit lead requested person
        self.branch = self.instance.added_by.first().branch

        # Update the queryset of the added_by field to filter by usertype='Admin' and branch=self.branch
        self.fields['added_by'].queryset = ExtendedUserModel.objects.filter(usertype='Field Executive', branch=self.branch)
    
    
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.instance.pk:
    #         # Get the already assigned field executives
    #         assigned_field_executives = self.instance.added_by.values_list('pk', flat=True)
    #         # Exclude them from the queryset
    #         self.fields['added_by'].queryset = ExtendedUserModel.objects.filter(
    #             usertype='Field Executive'
    #         ).exclude(id__in=assigned_field_executives)
    #     else:
    #         self.fields['added_by'].queryset = ExtendedUserModel.objects.filter(
    #             usertype='Field Executive'
    #         )
    

    
class ExitLeadAssignmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get the branch of the exit lead requested person
        self.branch = self.instance.added_by.first().branch

        # Update the queryset of the added_by field to filter by usertype='Admin' and branch=self.branch
        self.fields['added_by'].queryset = ExtendedUserModel.objects.filter(usertype='Admin', branch=self.branch).exclude(
            id=self.instance.added_by.first().id
        )

    added_by = forms.ModelMultipleChoiceField(queryset=ExtendedUserModel.objects.filter(usertype='Admin'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    
    class Meta:
        model = Leads
        fields = ['added_by']

        
    