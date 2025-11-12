import React, { useState, useMemo, useCallback } from 'react';
import { MenuItem, OrderItem } from './types';
import { MENU, TAX_RATE } from './constants';
import { PlusIcon, MinusIcon, TrashIcon, ReceiptIcon } from './components/icons';

// --- Helper Components (Defined outside App to prevent re-creation on render) ---

interface MenuItemCardProps {
  item: MenuItem;
  onAddItem: (item: MenuItem) => void;
}
const MenuItemCard: React.FC<MenuItemCardProps> = ({ item, onAddItem }) => (
  <div className="bg-white rounded-lg shadow-md p-4 flex justify-between items-center transition-transform hover:scale-105 gap-4">
    <div className="flex-grow">
      <h3 className="text-lg font-semibold text-gray-800">{item.name}</h3>
      <p className="text-gray-600">${item.price.toFixed(2)}</p>
    </div>
    <button
      onClick={() => onAddItem(item)}
      className="bg-emerald-500 text-white rounded-full p-2 hover:bg-emerald-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 transition-colors flex-shrink-0"
      aria-label={`Add ${item.name} to order`}
    >
      <PlusIcon className="h-6 w-6" />
    </button>
  </div>
);

interface OrderItemRowProps {
  item: OrderItem;
  onUpdateQuantity: (name: string, newQuantity: number) => void;
  onRemoveItem: (name: string) => void;
}
const OrderItemRow: React.FC<OrderItemRowProps> = ({ item, onUpdateQuantity, onRemoveItem }) => (
  <div className="flex items-center justify-between py-3 border-b border-gray-200">
    <div className="flex-grow">
      <p className="font-medium text-gray-800">{item.name}</p>
      <p className="text-sm text-gray-500">${item.price.toFixed(2)} each</p>
    </div>
    <div className="flex items-center gap-2 mx-4">
      <button onClick={() => onUpdateQuantity(item.name, item.quantity - 1)} className="p-1 rounded-full text-gray-500 hover:bg-gray-200"><MinusIcon className="h-5 w-5"/></button>
      <span className="w-8 text-center font-semibold">{item.quantity}</span>
      <button onClick={() => onUpdateQuantity(item.name, item.quantity + 1)} className="p-1 rounded-full text-gray-500 hover:bg-gray-200"><PlusIcon className="h-5 w-5"/></button>
    </div>
    <p className="w-20 text-right font-semibold text-gray-900">${item.subtotal.toFixed(2)}</p>
    <button onClick={() => onRemoveItem(item.name)} className="ml-4 text-red-500 hover:text-red-700">
      <TrashIcon className="h-5 w-5" />
    </button>
  </div>
);

interface ReceiptViewProps {
    orderItems: OrderItem[];
    subtotal: number;
    taxAmount: number;
    grandTotal: number;
    onNewOrder: () => void;
}
const ReceiptView: React.FC<ReceiptViewProps> = ({ orderItems, subtotal, taxAmount, grandTotal, onNewOrder }) => (
    <div className="max-w-md mx-auto bg-white rounded-xl shadow-lg overflow-hidden md:max-w-2xl my-10 animate-fade-in">
        <div className="p-8">
            <div className="text-center mb-6 border-b-2 border-dashed pb-4">
                <h1 className="text-2xl font-bold text-gray-800">M2DIZIKE CAFE RECEIPT</h1>
                <p className="text-sm text-gray-500">{new Date().toLocaleString()}</p>
            </div>
            <div className="space-y-3 mb-6">
                {orderItems.map(item => (
                    <div key={item.name} className="flex justify-between text-gray-700">
                        <span>{item.name} x{item.quantity}</span>
                        <span>${item.subtotal.toFixed(2)}</span>
                    </div>
                ))}
            </div>
            <div className="border-t border-dashed pt-4 space-y-2">
                <div className="flex justify-between font-medium text-gray-800">
                    <span>Subtotal</span>
                    <span>${subtotal.toFixed(2)}</span>
                </div>
                <div className="flex justify-between text-gray-600">
                    <span>Tax ({(TAX_RATE * 100).toFixed(0)}%)</span>
                    <span>${taxAmount.toFixed(2)}</span>
                </div>
                <div className="border-t border-black my-2"></div>
                <div className="flex justify-between text-xl font-bold text-gray-900">
                    <span>GRAND TOTAL</span>
                    <span>${grandTotal.toFixed(2)}</span>
                </div>
            </div>
            <div className="text-center mt-8">
                <p className="text-gray-500">Thank you for your visit!</p>
                <button
                    onClick={onNewOrder}
                    className="mt-4 w-full bg-blue-500 text-white font-bold py-3 px-4 rounded-lg hover:bg-blue-600 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                    Start New Order
                </button>
            </div>
        </div>
    </div>
);


// --- Main App Component ---

export default function App() {
  const [orderItems, setOrderItems] = useState<OrderItem[]>([]);
  const [view, setView] = useState<'ordering' | 'receipt'>('ordering');

  const handleAddItem = useCallback((itemToAdd: MenuItem) => {
    setOrderItems(prevItems => {
      const existingItem = prevItems.find(item => item.name === itemToAdd.name);
      if (existingItem) {
        return prevItems.map(item =>
          item.name === itemToAdd.name
            ? { ...item, quantity: item.quantity + 1, subtotal: (item.quantity + 1) * item.price }
            : item
        );
      } else {
        return [...prevItems, { ...itemToAdd, quantity: 1, subtotal: itemToAdd.price }];
      }
    });
  }, []);

  const handleUpdateQuantity = useCallback((name: string, newQuantity: number) => {
    if (newQuantity <= 0) {
      setOrderItems(prevItems => prevItems.filter(item => item.name !== name));
    } else {
      setOrderItems(prevItems =>
        prevItems.map(item =>
          item.name === name
            ? { ...item, quantity: newQuantity, subtotal: newQuantity * item.price }
            : item
        )
      );
    }
  }, []);

  const handleRemoveItem = useCallback((name: string) => {
    setOrderItems(prevItems => prevItems.filter(item => item.name !== name));
  }, []);
  
  const handleGenerateReceipt = useCallback(() => {
    if (orderItems.length > 0) {
        setView('receipt');
    }
  }, [orderItems]);

  const handleNewOrder = useCallback(() => {
    setOrderItems([]);
    setView('ordering');
  }, []);

  const subtotal = useMemo(() => orderItems.reduce((acc, item) => acc + item.subtotal, 0), [orderItems]);
  const taxAmount = useMemo(() => subtotal * TAX_RATE, [subtotal]);
  const grandTotal = useMemo(() => subtotal + taxAmount, [subtotal, taxAmount]);

  return (
    <div className="bg-slate-50 min-h-screen font-sans text-gray-800">
      <header className="bg-white shadow-md">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-4 text-center">
          <h1 className="text-3xl font-bold text-gray-900 tracking-tight">M2DIZIKE CAFE</h1>
        </div>
      </header>

      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {view === 'ordering' ? (
          <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
            {/* Menu Section */}
            <div className="lg:col-span-3">
              <h2 className="text-2xl font-semibold mb-4">Menu</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {MENU.map(item => (
                  <MenuItemCard key={item.name} item={item} onAddItem={handleAddItem} />
                ))}
              </div>
            </div>

            {/* Order Section */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-lg shadow-lg sticky top-8">
                <div className="p-6">
                  <h2 className="text-2xl font-semibold mb-4 border-b pb-3">Current Order</h2>
                  {orderItems.length === 0 ? (
                    <p className="text-gray-500 py-10 text-center">Your order is empty.</p>
                  ) : (
                    <div className="max-h-[40vh] overflow-y-auto pr-2">
                      {orderItems.map(item => (
                        <OrderItemRow key={item.name} item={item} onUpdateQuantity={handleUpdateQuantity} onRemoveItem={handleRemoveItem} />
                      ))}
                    </div>
                  )}
                </div>
                {orderItems.length > 0 && (
                    <div className="bg-gray-50 p-6 rounded-b-lg border-t">
                        <div className="space-y-2 mb-4">
                            <div className="flex justify-between text-lg">
                                <span className="font-medium text-gray-600">Subtotal:</span>
                                <span className="font-semibold text-gray-900">${subtotal.toFixed(2)}</span>
                            </div>
                             <div className="flex justify-between text-sm">
                                <span className="text-gray-500">Tax ({(TAX_RATE * 100).toFixed(0)}%):</span>
                                <span className="text-gray-600">${taxAmount.toFixed(2)}</span>
                            </div>
                        </div>
                        <div className="border-t-2 border-dashed my-3"></div>
                        <div className="flex justify-between text-xl font-bold">
                            <span>Total:</span>
                            <span>${grandTotal.toFixed(2)}</span>
                        </div>
                        <button
                          onClick={handleGenerateReceipt}
                          disabled={orderItems.length === 0}
                          className="mt-6 w-full flex items-center justify-center gap-2 bg-green-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-green-700 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                        >
                          <ReceiptIcon className="h-5 w-5"/>
                          Generate Receipt
                        </button>
                    </div>
                )}
              </div>
            </div>
          </div>
        ) : (
          <ReceiptView 
            orderItems={orderItems}
            subtotal={subtotal}
            taxAmount={taxAmount}
            grandTotal={grandTotal}
            onNewOrder={handleNewOrder}
          />
        )}
      </main>
    </div>
  );
}
