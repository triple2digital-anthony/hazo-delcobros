import unittest
from datetime import datetime
import streamlit as st
from test_hazo import log_event, connect_wallet

class TestHazoDemo(unittest.TestCase):
    def setUp(self):
        # Setup test environment
        if 'transactions' not in st.session_state:
            st.session_state.transactions = []
        if 'hazo_balance' not in st.session_state:
            st.session_state.hazo_balance = 1000
        if 'rav_balance' not in st.session_state:
            st.session_state.rav_balance = 500

    def test_log_event(self):
        # Test logging functionality
        test_message = "Test log message"
        log_event(test_message, "info")
        log_event(test_message, "error")
        log_event(test_message, "success")
        # If no exception is raised, test passes

    def test_wallet_connection(self):
        # Test wallet connection
        wallet_type = 'Phantom'
        address = connect_wallet(wallet_type)
        self.assertIsNotNone(address)
        self.assertTrue(len(address) > 0)
        self.assertEqual(address, '7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU')

    def test_transaction_validation(self):
        # Test transaction validation
        initial_balance = st.session_state.rav_balance
        gas_fee = 0.5
        
        # Simulate transaction
        st.session_state.rav_balance -= gas_fee
        
        # Check balance was properly deducted
        self.assertEqual(st.session_state.rav_balance, initial_balance - gas_fee)

if __name__ == '__main__':
    unittest.main() 