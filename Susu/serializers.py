from rest_framwork import serializers
from .models import SusuGroup, GroupMember, MemberContribution, WeekPayout

class SusuGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SusuGroup
        fields = ['group_id', 'name', 'contribution_amount','current_week']
        read_only_fields = ['group_id', 'current_week']

class GroupMemberSerializer(serializers.ModelSerializer):
    class meta:
        model = GroupMember
        fields= ['member_id','group','name','join_order']
        read_only_field=['member_id','join_order']
class ContributionInputSerializer(serializers.serializer):
    """parses and validates payment values."""
    amount = serializers.Decimal(max_digits=12, decimal_places=2 min_value=0.01)
class PayoutSerializer(serializers.modelSerializer):
    recipient_name = serializers.CharField(source="recipint_menber.name",ready_only=True)
    class Meta: 
        model = WeekPayout
        fields = ['payout_id','week','recipient_name','amount_paid']
