from django.db import models
import uuid
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from django.corevalidators import MinValueValidator 


class SusuGroup(models.Model):
    group_id = models.UUIDField (primary_key=True, default=uuid.uuid4,
                                  editable=False)
    name =models.CharFiield(max_length=255)
    contribution_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
current_week = models.PositiveIntergerField(default=1)
def __str__(self):
    return f"{self.name} (week{self.current_week})"
def close_week(self):
    members = self.members.all().order_index()
    if not members.exists():
        raise ValidationError("Cannot close a week with zero members.")
    
    arrears= {}
    for member in members:
        owed = member.get_remaining_owed_for_current_week()
        if owed > 0:
            arrears [member.name] = float(owed)
        if arrears: 
            return {
                'success':False,
                "message": f"cannot close week{self.current_week}.Arrear pendind",
                "arrears": arrears
            }
        #calculate exact target pot size 
        pot_size = self.contribution_amount*members.count()
        #calculate recipient order using modular arithmetic rotation
        recipient_idx = (self.current_week -1) % members.count()
        recipient = members[recipient_idx]
        # Execute payout recording 
        WeekPayout.objects.create(
            group=self,
            week_number=self.current_week,
            recipient_member=recipient,
            amount_paid=pot_size

        )
        #Advance the week counter
        old_week = self.current_week
        self.current_week +=1
        self.save()

        return {
            "success":True,
            "message":f"week{old_week} succesfully closed.",
            "payout": {
                "week":old_week,
                "recipient":recipient.name,
                "amount":float(pot_size
                               )
            }

        }
class GroupMemberQuerySet (models.QuerySet):
    def order_index(self):
        return self.order_by('join_order')
class GroupMember(models.Model):
    # no duplicate names within the same group
    unique_together = ('group','name')

def save(self, *args, **kwargs):
    if not self.join_order:
        max_order = GroupMember.objects.filter(group=self.group).aggregate(models.Max('join_order'))['join_order__max']
        self.join_order= (max_order or 0)+ 1
    super().save(*args, *kwargs)
def get_total_paid_for_current_week(self):
    total = self.contributions.filter(week_numberself.group.current_week).aggregate(models.Sum('amount_paid'))['amount_paid__sum']
    return total or Decimal('0.00')

def get_remaining_owed_for_current_week(self):
    return self.group.contribution_amount - self.get_total_paid_for_current_week()
def record_contribution(self, amount):
            
            """Enforces payment validation logic and records transactions."""
            payment = Decimal(str(amount))
            if payment <= 0:
                 raise ValidationError("Payment amount must be greater than zero")
            remaining_owed = self.get_remaining_owed_for_current_week()
                    # Rule 1: Reject payments above what a member owes for that week
            if payment > remaining_owed:
                 raise ValidationError (
                      f"Overpayment reject. {self.name} owes {remaining_owed} GHS"
                      f"for week {self.gruop.current_week}, but tried to pay {payment} GHS"

                 )
            return MemberContribution.objects.create(
                 group=self.group,
                 member=self,
                 week_number=self.group.current_week,
                 amount_paid=payment
            )

            def __str__(self):
                 return f"{self.name} (Position{self.join_order})"
class MemberContribution(models.Model):
     contribution_id = models.UUIDField (primary_key=True, default=uuid.uuid)
     group=models.ForeignKey(SusuGroup, on_delete=models.CASCADE)
     member=models.ForeignKey(GroupMember, on_delete=models.CASCADE,related_name="contributions")
     week_number = models.PositiveIntergerField()
     amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
     created_at= models.DateTimeField (auto_now_add=True)


class weekPayout(models.model):
     payout_id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
     group = models.ForeignKey(SusuGroup, on_delete=models.CASCADE, related_name='payouts')
     week_number = models.PositiveIntegerField()
     recipient_member = models.ForeignKey(GroupMember, on_delete=models.CASCADE)
     amount_paid = models.DecimalField(max_digits=12, decimal_places=2)

     class Meta:
          unique_together=('group', 'week_number')






