# Installation Lockdown pour accès sécurisé
# ~ cd ~/www/salsalive_site/
# ~ source env/bin/activate
# ~ pip install django-lockdown
# python manage.py migrate

from django.shortcuts import render
from django.http import HttpResponse

from django.utils.dateformat import format
from django.utils.translation import gettext as _

import re

from lockdown.decorators import lockdown

from salsalive_viz.models import Events

# ------------
# Home page
# ------------
@lockdown()
def index(request):
    return render(
        request,
        'compta_index.html',
        {
            'page': {
                'title': 'Comptabilité Salsa Live!',
                'description': None,
                'active': None,
                'header': None,
            },
        }
    )
    

# -----------------
# Compta All page
# ----------------
@lockdown()
def all(request):
    rows = Events.objects.raw(f"""
        SELECT 
            comptas.id, comptas.date, moyen, label, labelbanque, amount, tiers, isBanqueOk,
            members.forname AS member_forname, members.name AS member_name,
            categories.id AS category_id, categories.name AS category_name,
            actions.id AS action_id, actions.name AS action_name
        FROM beautifuldata_salsa.comptas
        LEFT OUTER JOIN members ON
            comptas.member_id = members.id
        LEFT OUTER JOIN categories ON
            comptas.categorie_id = categories.id
        LEFT OUTER JOIN actions ON
            comptas.action_id = actions.id
        ORDER BY comptas.date ASC, member_id ASC, label ASC
        """)

    total_credit = 0
    total_debit = 0
    total_balance = 0
    lines = []
    current_month=''
    real_done = False
    
    for row in rows:
        month = row.date.strftime("%B %Y")

        if row.isBanqueOk == 0 and  not real_done :
            lines.append({
              'type': 'real',
              'total_debit': f"{total_debit:.2f}€",
              'total_credit': f"{total_credit:.2f}€",
              'total_balance' : f"{total_balance:.2f}€",
            })
            real_done = True
        
        # credit, debit, balance
        if row.amount>0:
            total_credit += row.amount
        else:
            total_debit += row.amount
        total_balance += row.amount
        
        if month != current_month:
            lines.append({
              'type': 'separator',
              'month': month,
            })
            current_month = month
       
        lines.append({
            'type': 'line',
            'date': row.date.strftime("%d/%m/%Y"),
            'labelbank': row.labelbanque,
            'member': {
                'forname': row.member_forname,
                'name': row.member_name,
            },
            'label': row.label,
            'category': row.category_name,
            'action': row.action_name,
            'credit': f"{row.amount:.2f}€" if row.amount>=0 else '',
            'debit': f"{row.amount:.2f}€" if row.amount<0 else '',
        })
    
    return render(
        request,
        'compta_all.html',
        {
            'page': {
                'title': 'Comptabilité complète Salsa Live!',
                'description': None,
                'active': None,
                'header': None,
            },
            'lines': lines,
            'total_debit': f"{total_debit:.2f}€",
            'total_credit': f"{total_credit:.2f}€",
            'total_balance' : f"{total_balance:.2f}€",
        }
    )

