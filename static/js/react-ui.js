(function () {
  const currency = (value) => {
    const numberValue = typeof value === 'number' ? value : parseFloat(value || 0);
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
    }).format(numberValue || 0);
  };

  const parseJSONScript = (id) => {
    const el = document.getElementById(id);
    if (!el) return null;
    try {
      return JSON.parse(el.textContent);
    } catch (err) {
      console.error('Unable to parse JSON script', id, err);
      return null;
    }
  };

  const Pill = ({ label, tone }) =>
    React.createElement('span', { className: `react-pill react-pill-${tone}` }, label);

  const SectionHeader = ({ title, subtitle, actionLabel, actionHref }) => {
    const action = actionHref
      ? React.createElement(
          'a',
          { className: 'react-primary-btn', href: actionHref },
          actionLabel || 'Create'
        )
      : null;

    return React.createElement(
      'div',
      { className: 'react-header' },
      [
        React.createElement(
          'div',
          { className: 'react-titles', key: 'titles' },
          [
            React.createElement('p', { className: 'react-kicker', key: 'kicker' }, subtitle || 'Dashboard'),
            React.createElement('h1', { key: 'title' }, title),
          ]
        ),
        action && React.createElement(React.Fragment, { key: 'action' }, action),
      ].filter(Boolean)
    );
  };

  const WalletCard = ({ wallet }) => {
    const remaining = wallet.remainingBalance;
    const statusPill =
      remaining === null || remaining === undefined
        ? null
        : Pill({
            label: `${remaining >= 0 ? 'Remaining' : 'Overspent'}: ${currency(Math.abs(remaining))}`,
            tone: remaining >= 0 ? 'success' : 'danger',
          });

    return React.createElement(
      'a',
      { className: 'wallet-card react-card', href: wallet.detailUrl },
      [
        React.createElement('div', { className: 'wallet-icon', key: 'icon' }),
        React.createElement(
          'div',
          { className: 'react-card-body', key: 'body' },
          [
            React.createElement('h3', { className: 'wallet-label', key: 'title' }, wallet.name),
            React.createElement(
              'p',
              { className: 'wallet-total', key: 'total' },
              `Spent so far: ${currency(wallet.totalSpent)}`
            ),
            statusPill && React.createElement('div', { key: 'pill' }, statusPill),
          ].filter(Boolean)
        ),
      ]
    );
  };

  const EmptyState = ({ createUrl }) =>
    React.createElement(
      'div',
      { className: 'react-empty' },
      [
        React.createElement('h3', { key: 'title' }, 'No wallets yet'),
        React.createElement(
          'p',
          { key: 'copy' },
          'Create your first wallet to start tracking your spending.'
        ),
        React.createElement(
          'a',
          { className: 'react-primary-btn', href: createUrl, key: 'cta' },
          'Create wallet'
        ),
      ]
    );

  const WalletGrid = ({ wallets, createUrl }) =>
    React.createElement(
      'section',
      { className: 'react-panel' },
      [
        SectionHeader({ title: 'Your wallets', subtitle: 'Finance Manager', actionLabel: 'New wallet', actionHref: createUrl }),
        wallets.length
          ? React.createElement(
              'div',
              { className: 'wallet-grid react-grid', key: 'grid' },
              wallets.map((wallet) => React.createElement(WalletCard, { key: wallet.id, wallet }))
            )
          : React.createElement(EmptyState, { createUrl, key: 'empty' }),
      ]
    );

  const ActionBar = ({ actions }) =>
    React.createElement(
      'div',
      { className: 'react-actions' },
      [
        React.createElement(
          'a',
          { key: 'add', className: 'react-primary-btn', href: actions.addTransaction },
          '+ Add transaction'
        ),
        React.createElement(
          'a',
          { key: 'print', className: 'react-ghost-btn', href: actions.printStatement },
          '🖨️ Print statement'
        ),
        React.createElement(
          'a',
          { key: 'topup', className: 'react-ghost-btn', href: actions.topUp },
          '➕ Add funds'
        ),
        React.createElement(
          'a',
          { key: 'delete', className: 'react-danger-btn', href: actions.deleteWallet },
          '🗑️ Delete wallet'
        ),
      ]
    );

  const TransactionList = ({ transactions }) =>
    React.createElement(
      'div',
      { className: 'react-transaction-card react-card' },
      [
        React.createElement('h3', { key: 'title' }, 'History'),
        transactions.length === 0
          ? React.createElement('p', { key: 'empty', className: 'react-muted' }, 'No transactions yet.')
          : React.createElement(
              'ul',
              { key: 'list', className: 'react-history-list' },
              transactions.map((tx) =>
                React.createElement(
                  'li',
                  { key: tx.id },
                  [
                    React.createElement('span', { className: 'tx-date', key: 'date' }, tx.date),
                    React.createElement('span', { className: 'tx-reason', key: 'reason' }, tx.reason),
                    React.createElement('span', { className: 'tx-amount', key: 'amount' }, currency(tx.amount)),
                  ]
                )
              )
            ),
      ]
    );

  const WalletDetail = ({ wallet, actions }) => {
    const remaining = wallet.remainingBalance;
    const balancePill =
      remaining === null || remaining === undefined
        ? null
        : Pill({
            label: `${remaining >= 0 ? 'Remaining' : 'Overspent'}: ${currency(Math.abs(remaining))}`,
            tone: remaining >= 0 ? 'success' : 'danger',
          });

    return React.createElement(
      'section',
      { className: 'react-panel react-detail' },
      [
        SectionHeader({ title: wallet.name, subtitle: 'Wallet overview' }),
        React.createElement(
          'div',
          { className: 'react-summary react-card', key: 'summary' },
          [
            React.createElement('div', { className: 'react-metric', key: 'spent' }, [
              React.createElement('p', { className: 'react-label', key: 'label' }, 'Total spent'),
              React.createElement('div', { className: 'react-value', key: 'value' }, currency(wallet.totalSpent)),
            ]),
            balancePill && React.createElement('div', { className: 'react-pill-row', key: 'pill' }, balancePill),
          ].filter(Boolean)
        ),
        ActionBar({ actions }),
        TransactionList({ transactions: wallet.transactions || [] }),
      ]
    );
  };

  const mountWalletList = () => {
    const container = document.getElementById('react-wallet-list');
    if (!container) return;
    const data = parseJSONScript('wallet-list-data');
    const wallets = Array.isArray(data) ? data : [];
    const root = ReactDOM.createRoot(container);
    root.render(React.createElement(WalletGrid, { wallets, createUrl: container.dataset.createUrl }));
  };

  const mountWalletDetail = () => {
    const container = document.getElementById('react-wallet-detail');
    if (!container) return;
    const data = parseJSONScript('wallet-detail-data');
    if (!data) return;
    const root = ReactDOM.createRoot(container);
    root.render(
      React.createElement(WalletDetail, {
        wallet: data,
        actions: data.actions || {
          addTransaction: container.dataset.addUrl,
          printStatement: container.dataset.statementUrl,
          deleteWallet: container.dataset.deleteUrl,
          topUp: container.dataset.topupUrl,
        },
      })
    );
  };

  document.addEventListener('DOMContentLoaded', () => {
    mountWalletList();
    mountWalletDetail();
  });
})();
