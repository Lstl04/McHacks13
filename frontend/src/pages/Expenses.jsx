import { useState, useRef, useEffect } from 'react';
import './Expenses.css';
import { useAuth0 } from '@auth0/auth0-react';
import { 
  Upload, Trash2, Plus, Receipt, Calendar, Store, 
  AlertCircle, Loader2, FileSearch, LayoutList 
} from 'lucide-react';

const GUMLOOP_API_KEY = import.meta.env.VITE_GUMLOOP_API_KEY || 'c74b5f4d4b8a4f0086a0ceccd7a2bc6b';
const GUMLOOP_USER_ID = import.meta.env.VITE_GUMLOOP_USER_ID || 'XURX5znR9YQQrJJRyzSRo5ExDJG3';
const GUMLOOP_SAVED_ITEM_ID = import.meta.env.VITE_GUMLOOP_SAVED_ITEM_ID || '5ktCd2DhH8WtW8UMdqZ2dY';
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

function Expenses() {
  const { isAuthenticated, getAccessTokenSilently } = useAuth0();
  const fileInputRef = useRef(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingStatus, setProcessingStatus] = useState('');
  const [previewUrl, setPreviewUrl] = useState(null);
  const [expenseData, setExpenseData] = useState(null);
  const [error, setError] = useState(null);
  const [isSaving, setIsSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [mongoUserId, setMongoUserId] = useState(null);
  const [existingExpenses, setExistingExpenses] = useState([]);
  const [isLoadingExpenses, setIsLoadingExpenses] = useState(true);
  const [activeView, setActiveView] = useState('scan');

  useEffect(() => {
    const fetchUserId = async () => {
      if (isAuthenticated) {
        try {
          const token = await getAccessTokenSilently();
          const response = await fetch(`${API_URL}/users/profile`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          if (response.ok) {
            const userData = await response.json();
            setMongoUserId(userData._id);
          }
        } catch (err) { console.error('Auth Error:', err); }
      }
    };
    fetchUserId();
  }, [isAuthenticated, getAccessTokenSilently]);

  const fetchExpenses = async () => {
    if (!mongoUserId) return;
    setIsLoadingExpenses(true);
    try {
      const response = await fetch(`${API_URL}/expenses/?user_id=${mongoUserId}`);
      if (response.ok) {
        const expenses = await response.json();
        setExistingExpenses(expenses);
      }
    } catch (err) { console.error('Fetch Error:', err); }
    finally { setIsLoadingExpenses(false); }
  };

  useEffect(() => { fetchExpenses(); }, [mongoUserId]);

  const pollForResult = async (runId) => {
    let attempts = 0;
    while (attempts < 60) {
      const pollUrl = `https://api.gumloop.com/api/v1/get_pl_run?run_id=${runId}&user_id=${GUMLOOP_USER_ID}`;
      const response = await fetch(pollUrl, {
        headers: { 'Authorization': `Bearer ${GUMLOOP_API_KEY}` }
      });
      const result = await response.json();
      if (result.state === 'DONE') return result.outputs;
      if (result.state === 'FAILED') throw new Error('AI_PIPELINE_FAILURE');
      setProcessingStatus(`PROCESSING_MANIFEST... ${Math.round((attempts / 60) * 100)}%`);
      await new Promise(r => setTimeout(r, 2000));
      attempts++;
    }
    throw new Error('TIMEOUT_EXCEEDED');
  };

  const handleFileSelect = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setError(null);
    setPreviewUrl(URL.createObjectURL(file));
    setIsProcessing(true);
    
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = async () => {
      try {
        const startResponse = await fetch(`https://api.gumloop.com/api/v1/start_pipeline?user_id=${GUMLOOP_USER_ID}&saved_item_id=${GUMLOOP_SAVED_ITEM_ID}`, {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${GUMLOOP_API_KEY}`, 'Content-Type': 'application/json' },
          body: JSON.stringify({ pipeline_inputs: [{ input_name: 'receipt_image', value: reader.result }] })
        });
        const startResult = await startResponse.json();
        const outputs = await pollForResult(startResult.run_id);
        const data = outputs?.expense_data || Object.values(outputs)[0];
        const parsed = typeof data === 'string' ? JSON.parse(data) : data;

        // Ensure line items have all required fields
        const lineItems = (parsed.line_items || []).map(item => ({
          description: item.description || '',
          quantity: item.quantity || 1,
          unitPrice: item.unitPrice || (item.total || 0) / (item.quantity || 1),
          total: item.total || 0
        }));

        setExpenseData({
          vendor_name: parsed.vendor_name || '',
          date: parsed.date ? parsed.date.split('T')[0] : '',
          total_amount: parsed.total_amount || 0,
          tax_amount: parsed.tax_amount || 0,
          currency: parsed.currency || 'USD',
          line_items: lineItems || []
        });
      } catch (err) { 
        setError('DATA_EXTRACTION_FAILED'); 
        setExpenseData({ vendor_name: '', date: '', total_amount: 0, tax_amount: 0, currency: 'USD', line_items: [] });
      } finally { setIsProcessing(false); }
    };
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSaving(true);
    setError(null);
    setSaveSuccess(false);
    try {
      const token = await getAccessTokenSilently();
      // Transform line items to match backend structure
      const lineItems = (expenseData.line_items || []).map(item => ({
        description: item.description || '',
        quantity: parseFloat(item.quantity) || 1,
        unitPrice: parseFloat(item.unitPrice) || 0,
        total: parseFloat(item.total) || 0
      }));

      const payload = {
        userId: mongoUserId,
        vendorName: expenseData.vendor_name,
        date: expenseData.date ? new Date(expenseData.date).toISOString() : null,
        totalAmount: parseFloat(expenseData.total_amount),
        taxAmount: parseFloat(expenseData.tax_amount),
        currency: expenseData.currency,
        lineItems: lineItems,
        receiptImageUrl: previewUrl
      };
      const response = await fetch(`${API_URL}/expenses/`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });
      
      if (response.ok) {
        const result = await response.json();
        setSaveSuccess(true);
        fetchExpenses();
        setTimeout(() => { setActiveView('list'); setExpenseData(null); setPreviewUrl(null); setSaveSuccess(false); }, 1500);
      } else {
        const errorData = await response.json().catch(() => ({ detail: 'Failed to create expense' }));
        setError(`SAVE_ERROR: ${errorData.detail || response.statusText}`);
      }
    } catch (err) { 
      console.error('Expense creation error:', err);
      setError('SAVE_SYNC_ERROR'); 
    }
    finally { setIsSaving(false); }
  }

  const formatCurrency = (amount, curr) => new Intl.NumberFormat('en-US', { style: 'currency', currency: curr || 'USD' }).format(amount || 0);

  return (
    <div className="expenses-container">
      <h1>EXPENSES</h1>
      <p className="expenses-subtitle">INDUSTRIAL_DATA_ACQUISITION // V1.0</p>

      <div className="expenses-tabs">
        <button className={`tab-btn ${activeView === 'scan' ? 'active' : ''}`} onClick={() => setActiveView('scan')}>
          <FileSearch size={18} /> SCAN RECEIPT
        </button>
        <button className={`tab-btn ${activeView === 'list' ? 'active' : ''}`} onClick={() => setActiveView('list')}>
          <LayoutList size={18} /> PAST EXPENSES <span className="tab-count">{existingExpenses.length}</span>
        </button>
      </div>

      {activeView === 'scan' ? (
        <div className="expenses-content">
          <div className="upload-section">
            <input type="file" ref={fileInputRef} onChange={handleFileSelect} accept="image/*" hidden />
            {!previewUrl ? (
              <div className="upload-zone" onClick={() => fileInputRef.current?.click()}>
                <Upload className="upload-icon" size={40} />
                <p>UPLOADING_PORT_OPEN</p>
                <span>SELECT_IMAGE_FILE</span>
              </div>
            ) : (
              <div className="preview-section">
                <img src={previewUrl} className="receipt-preview" alt="Preview" />
                <button className="change-image-btn" onClick={() => fileInputRef.current?.click()}>RESCAN_MODULE</button>
              </div>
            )}
            {isProcessing && (
              <div className="processing-overlay">
                <Loader2 className="spinner" size={40} />
                <p>{processingStatus}</p>
              </div>
            )}
            {error && <div className="error-message"><AlertCircle size={16} /> {error}</div>}
          </div>

          {expenseData && (
            <form className="expense-form" onSubmit={handleSubmit}>
              <h2>VERIFICATION_PORT</h2>
              <div className="form-row">
                <div className="form-group">
                  <label>VENDOR_ID</label>
                  <input type="text" value={expenseData.vendor_name} onChange={(e) => setExpenseData({...expenseData, vendor_name: e.target.value})} />
                </div>
                <div className="form-group">
                  <label>TIMESTAMP</label>
                  <input type="date" value={expenseData.date} onChange={(e) => setExpenseData({...expenseData, date: e.target.value})} />
                </div>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>TOTAL_VAL</label>
                  <input type="number" value={expenseData.total_amount} onChange={(e) => setExpenseData({...expenseData, total_amount: e.target.value})} step="0.01" />
                </div>
                <div className="form-group">
                  <label>TAX_AMT</label>
                  <input type="number" value={expenseData.tax_amount} onChange={(e) => setExpenseData({...expenseData, tax_amount: e.target.value})} step="0.01" />
                </div>
              </div>

              <div className="line-items-section">
                <div className="line-items-header">
                  <h3>MANIFEST_ITEMS</h3>
                  <button type="button" className="add-item-btn" onClick={() => setExpenseData({...expenseData, line_items: [...expenseData.line_items, { description: '', quantity: 1, unitPrice: 0, total: 0 }]})}>+ ADD_ROW</button>
                </div>
                {expenseData.line_items.map((item, idx) => (
                  <div key={idx} className="line-item">
                    <input type="text" placeholder="DESC" value={item.description || ''} onChange={(e) => {
                      const items = [...expenseData.line_items];
                      items[idx].description = e.target.value;
                      setExpenseData({...expenseData, line_items: items});
                    }} />
                    <input type="number" placeholder="QTY" value={item.quantity || 1} onChange={(e) => {
                      const items = [...expenseData.line_items];
                      items[idx].quantity = parseFloat(e.target.value) || 1;
                      items[idx].total = (items[idx].quantity || 1) * (items[idx].unitPrice || 0);
                      setExpenseData({...expenseData, line_items: items});
                    }} step="0.01" />
                    <input type="number" placeholder="UNIT PRICE" value={item.unitPrice || 0} onChange={(e) => {
                      const items = [...expenseData.line_items];
                      items[idx].unitPrice = parseFloat(e.target.value) || 0;
                      items[idx].total = (items[idx].quantity || 1) * (items[idx].unitPrice || 0);
                      setExpenseData({...expenseData, line_items: items});
                    }} step="0.01" />
                    <input type="number" placeholder="TOTAL" value={item.total || 0} onChange={(e) => {
                      const items = [...expenseData.line_items];
                      items[idx].total = parseFloat(e.target.value) || 0;
                      setExpenseData({...expenseData, line_items: items});
                    }} step="0.01" />
                    <button type="button" className="remove-item-btn" onClick={() => setExpenseData({...expenseData, line_items: expenseData.line_items.filter((_, i) => i !== idx)})}>×</button>
                  </div>
                ))}
              </div>

              <button type="submit" className="submit-btn" disabled={isSaving}>
                {isSaving ? 'SYNCING...' : saveSuccess ? 'SYNC COMPLETE' : 'COMMIT EXPENSE'}
              </button>
            </form>
          )}
        </div>
      ) : (
        <div className="expenses-list-container">
          {isLoadingExpenses ? (
            <div className="processing-overlay"><Loader2 className="spinner" size={40} /></div>
          ) : (
            <>
              <div className="expenses-grid">
                {existingExpenses.map((exp) => (
                  <div key={exp._id} className="expense-card">
                    <div className="expense-card-header">
                      <div className="expense-vendor">
                        <Store size={18} />
                        <h3>{exp.vendorName}</h3>
                      </div>
                      <div className="expense-amount">{formatCurrency(exp.totalAmount, exp.currency)}</div>
                    </div>
                    <div className="expense-card-body">
                      <div className="expense-date"><Calendar size={14} /> {new Date(exp.date).toLocaleDateString()}</div>
                      <div className="expense-tax"><span className="tax-label">TAX:</span> {formatCurrency(exp.taxAmount, exp.currency)}</div>
                    </div>
                    <div className="expense-card-footer">
                      <button className="expense-action-btn delete" onClick={async () => {
                        if (confirm('DELETE_ENTRY?')) {
                          await fetch(`${API_URL}/expenses/${exp._id}`, { method: 'DELETE' });
                          fetchExpenses();
                        }
                      }}><Trash2 size={16} /></button>
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="expenses-summary">
                <h2>SUMMARY_REPORT</h2>
                <div className="summary-stats">
                  <div className="summary-stat">
                    <span className="stat-label">AGGREGATE_VAL</span>
                    <span className="stat-value">{formatCurrency(existingExpenses.reduce((s, e) => s + e.totalAmount, 0))}</span>
                  </div>
                  <div className="summary-stat">
                    <span className="stat-label">TAX_TOTAL</span>
                    <span className="stat-value">{formatCurrency(existingExpenses.reduce((s, e) => s + e.taxAmount, 0))}</span>
                  </div>
                  <div className="summary-stat">
                    <span className="stat-label">ENTRY_COUNT</span>
                    <span className="stat-value">{existingExpenses.length}</span>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default Expenses;
