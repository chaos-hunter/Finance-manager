from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import WalletForm, TransactionForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import io
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4              # ← import A4 here
from .models import Wallet, Transaction
from .forms import TopUpForm
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Wallet

@login_required
def wallet_delete(request, pk):
    wallet = get_object_or_404(Wallet, pk=pk, user=request.user)
    if request.method == 'POST':
        wallet_name = wallet.name
        wallet.delete()
        #messages.success(request, f'Wallet "{wallet_name}" deleted.')
        return redirect('wallet_list')
    return render(request, 'wallets/wallet_confirm_delete.html', {
        'wallet': wallet
    })

@login_required
def wallet_list(request):
    wallets = Wallet.objects.filter(user=request.user)
    return render(request, 'wallets/wallet_list.html', {'wallets': wallets})

@login_required
def wallet_detail(request, pk):
    wallet = get_object_or_404(Wallet, pk=pk, user=request.user)
    tx_form = TransactionForm(request.POST or None)
    if tx_form.is_valid():
        tx = tx_form.save(commit=False)
        tx.wallet = wallet
        tx.save()
        return redirect('wallet_detail', pk=pk)

    return render(request, 'wallets/wallet_detail.html', {
        'wallet': wallet,
        'tx_form': tx_form,
        'transactions': wallet.transactions.all(),
        'total': wallet.total_spent,
    })

@login_required
def wallet_create(request):
    if request.method == "POST":
        form = WalletForm(request.POST)
        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.user = request.user
            wallet.save()
            return redirect("wallet_detail", pk=wallet.pk)
    else:
        form = WalletForm()
    return render(request, "wallets/wallet_form.html", {"form": form})


@login_required
@csrf_exempt
def wallet_add_json(request, pk):
    # ensure it’s a POST
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

    wallet = get_object_or_404(Wallet, pk=pk, user=request.user)
    form   = TransactionForm(request.POST)
    if form.is_valid():
        tx = form.save(commit=False)
        tx.wallet = wallet
        tx.save()
        return JsonResponse({
            'success': True,
            'date':   tx.date.isoformat(),
            'reason': tx.reason,
            'amount': f"{tx.amount:.2f}",
            'total':  f"{wallet.total_spent:.2f}",
        })
    else:
        return JsonResponse({'success': False, 'error': 'Invalid data'}, status=400)

@login_required
def transaction_create(request, pk):
    wallet = get_object_or_404(Wallet, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            tx = form.save(commit=False)
            tx.wallet = wallet
            tx.save()
            return redirect('wallet_detail', pk=pk)
    else:
        form = TransactionForm()
    return render(request, 'wallets/transaction_form.html', {'form': form, 'wallet': wallet})
def wallet_statement(request, pk):
    # Make sure we only load wallets belonging to the logged‑in user:
    wallet = get_object_or_404(Wallet, pk=pk, user=request.user)

    # Pull in all the transactions (if you set related_name='transactions')
    txs = wallet.transactions.order_by('date')

    # Kick off a PDF in memory
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header
    p.setFont('Helvetica-Bold', 16)
    p.drawCentredString(width/2, height - 50, f"Statement for {wallet.name}")

    # Columns
    p.setFont('Helvetica-Bold', 12)
    y = height - 80
    p.drawString(40, y, "Date")
    p.drawString(140, y, "Reason")
    p.drawRightString(width - 40, y, "Amount")

    # Transactions
    p.setFont('Helvetica', 10)
    y -= 20
    for tx in txs:
        if y < 50:
            p.showPage()
            y = height - 50
        p.drawString(40, y, tx.date.strftime("%Y-%m-%d"))
        p.drawString(140, y, tx.reason[:40])
        p.drawRightString(width - 40, y, f"${tx.amount:,.2f}")
        y -= 15

    # Total
    if y < 70:
        p.showPage()
        y = height - 50
    p.setFont('Helvetica-Bold', 12)
    p.drawRightString(width - 40, y - 20, f"Total: ${wallet.total_spent:,.2f}")

    # Finish up
    p.save()
    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename=f"statement_{wallet.name}.pdf"
    )
def wallet_topup(request, pk):
    wallet = get_object_or_404(Wallet, pk=pk, user=request.user)
    if request.method == "POST":
        form = TopUpForm(request.POST)
        if form.is_valid():
            wallet.starting_balance = (wallet.starting_balance or Decimal("0")) + form.cleaned_data["amount"]
            wallet.save()
            return redirect("wallet_detail", pk=pk)
    else:
        form = TopUpForm()
    return render(request, "wallets/wallet_topup.html", {
        "wallet": wallet, "form": form
    })