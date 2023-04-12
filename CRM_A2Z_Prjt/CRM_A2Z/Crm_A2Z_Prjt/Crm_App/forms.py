from django import forms
from Crm_App.models import *







class BranchAddForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'

        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'addrs' : forms.Textarea(attrs={'class':'form-control'}),
            'phn' : forms.NumberInput(attrs={'class':'form-control'}),
        }




class BranchUpdateForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'
        
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'addrs' : forms.Textarea(attrs={'class':'form-control'}),
            'phn' : forms.NumberInput(attrs={'class':'form-control'}),
        }




class LeadAddForm(forms.ModelForm):
    class Meta:
        model = Leads
        fields = "__all__"
        exclude = ['added_by','added_on','added_by_admin']

        widgets ={
            'lead_title':forms.TextInput(attrs={'class':'form-control'}),
            'lead_description':forms.Textarea(attrs={'class':'form-control','rows':'3'}),
            'contact_person_name':forms.TextInput(attrs={'class':'form-control'}),
            'contact_person_phone':forms.NumberInput(attrs={'class':'form-control'}),
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
            'lead_delivery_date': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'notes_about_client':forms.Textarea(attrs={'class':'form-control','rows':'3'}),
            'note_about_field_executive':forms.Textarea(attrs={'class':'form-control','rows':'3'})

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
       



class ProjectEditForm(forms.ModelForm):
    class Meta:
        model = Leads
        fields = "__all__"
        exclude = ['added_by','added_on','added_by_admin']

        widgets ={
            'lead_title':forms.TextInput(attrs={'class':'form-control'}),
            'lead_description':forms.Textarea(attrs={'class':'form-control','rows':'3'}),
            'contact_person_name':forms.TextInput(attrs={'class':'form-control'}),
            'contact_person_phone':forms.NumberInput(attrs={'class':'form-control'}),
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
            'lead_delivery_date': forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'notes_about_client':forms.Textarea(attrs={'class':'form-control','rows':'3'}),
            'note_about_field_executive':forms.Textarea(attrs={'class':'form-control','rows':'3'})

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




class ProjectModuleForm(forms.ModelForm):
    class Meta:
        model = ProjectModule
        fields = "__all__"
        exclude = ['key','project','lead','added_by','added_on','status']
        widgets ={
            'module_title':forms.TextInput(attrs={'class':'form-control'}),
            'module_description':forms.Textarea(attrs={'class':'form-control','rows':'3'}),
        }




class ProjectAsignmentForm(forms.ModelForm):
    module_assigned = forms.ModelMultipleChoiceField(
        queryset=ProjectModule.objects.none(),
        widget=forms.CheckboxSelectMultiple
    )
    project_assignment = forms.ModelMultipleChoiceField(
        queryset=ExtendedUserModel.objects.none(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

   

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        project = kwargs.pop('project')
        if not request.user.is_superuser:
            branch = kwargs.pop('branch')
            name = kwargs.pop('name')

        super().__init__(*args, **kwargs)
        self.fields['module_assigned'].queryset = ProjectModule.objects.filter(project=project)
        if not request.user.is_superuser:
            self.fields['project_assignment'].queryset = ExtendedUserModel.objects.filter(branch=branch).exclude(user__username=name)
        else:
            self.fields['project_assignment'].queryset = ExtendedUserModel.objects.all()


    class Meta:
        model = ProjectAssignment
        fields = ['project_assignment', 'module_assigned']
        exclude = ['key', 'project', 'lead', 'project_module', 'added_by', 'added_on']
       

        
    