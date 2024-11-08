import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import random
import logging
import uuid
from streamlit_extras.let_it_rain import rain
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("HAZO_DEMO")

# Add logging function
def log_event(message, level="info"):
    """
    Log events with consistent formatting
    Args:
        message: The message to log
        level: The log level (info, warning, error, success)
    """
    # Generate a random UUID for this event
    event_uuid = str(uuid.uuid4())
    
    if level == "info":
        logger.info(message)
    elif level == "warning":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    elif level == "success":
        logger.info(f"SUCCESS: {message}")
    elif level == "transaction":
        logger.info(f"TRANSACTION: {message}")
    
    # Print to console with UUID
    print(f"\n{'='*50}")
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"UUID: {event_uuid}")
    print(f"Level: {level.upper()}")
    print(f"{message}")
    print(f"{'='*50}\n")

# Must be first Streamlit command
st.set_page_config(
    page_title="Delco Collective Ecosystem",
    layout="wide"
)

# Initialize session state
if 'transactions' not in st.session_state:
    st.session_state.transactions = []
if 'hazo_balance' not in st.session_state:
    st.session_state.hazo_balance = 1000
if 'rav_balance' not in st.session_state:
    st.session_state.rav_balance = 500
if 'connected_wallet' not in st.session_state:
    st.session_state.connected_wallet = None
if 'sol_balance' not in st.session_state:
    st.session_state.sol_balance = 25.5
if 'kyc_status' not in st.session_state:
    st.session_state.kyc_status = None
if 'verification_step' not in st.session_state:
    st.session_state.verification_step = 1
if 'twofa_enabled' not in st.session_state:
    st.session_state.twofa_enabled = False
if 'kyc_documents' not in st.session_state:
    st.session_state.kyc_documents = {}

# Wallet connection simulation
def get_wallet_display():
    try:
        if 'connected_wallet' in st.session_state and st.session_state.connected_wallet:
            wallet = st.session_state.connected_wallet
            if isinstance(wallet, dict) and 'address' in wallet:
                address = wallet['address']
                return f"{address[:6]}...{address[-4:]}"
    except:
        pass
    return 'Unknown'

def connect_wallet(wallet_type):
    wallet_addresses = {
        'Phantom': '7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU',
        'Metamask': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e',
        'Coinbase': '0x89205A3A3b2A69De6Dbf7f01ED13B2108B2c43e7',
        'Trust Wallet': '0x7A16fF8270133F063aAb6C9977183D9e72835428',
        'Ledger': '0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD'
    }
    st.session_state.connected_wallet = {
        'type': wallet_type,
        'address': wallet_addresses[wallet_type]
    }
    return wallet_addresses[wallet_type]

# Enhanced wallet connection with KYC workflow
def show_kyc_workflow():
    st.markdown("### 🔐 Account Verification")
    
    # Progress bar for verification steps
    steps = ["Basic Info", "Identity Verification", "2FA Setup", "Wallet Connection"]
    progress = (st.session_state.verification_step - 1) / len(steps)
    st.progress(progress)
    st.markdown(f"**Step {st.session_state.verification_step} of {len(steps)}:** {steps[st.session_state.verification_step-1]}")
    
    if st.session_state.verification_step == 1:
        st.markdown("#### Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            dob = st.date_input("Date of Birth")
        with col2:
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number")
            country = st.selectbox("Country of Residence", 
                ["United States", "Canada", "Other"])
        
        if st.button("Continue to Identity Verification"):
            if all([first_name, last_name, email, phone]):
                st.session_state.verification_step = 2
                st.rerun()
            else:
                st.error("Please fill in all required fields")

    elif st.session_state.verification_step == 2:
        st.markdown("#### Identity Verification")
        doc_type = st.selectbox("Select ID Type", 
            ["Driver's License", "Passport", "Government ID"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("Upload Front of ID")
            id_front = st.file_uploader("Front", type=["jpg", "png", "pdf"])
        with col2:
            st.markdown("Upload Back of ID")
            id_back = st.file_uploader("Back", type=["jpg", "png", "pdf"])
            
        st.markdown("#### Proof of Address")
        address_doc = st.file_uploader("Upload Proof of Address", 
            type=["jpg", "png", "pdf"])
            
        if st.button("Submit Documents"):
            if id_front and id_back and address_doc:
                st.session_state.kyc_documents = {
                    "id_type": doc_type,
                    "id_front": True,
                    "id_back": True,
                    "address": True
                }
                st.session_state.verification_step = 3
                st.success("Documents submitted successfully!")
                st.rerun()
            else:
                st.error("Please upload all required documents")

    elif st.session_state.verification_step == 3:
        st.markdown("#### Two-Factor Authentication Setup")
        
        if not st.session_state.twofa_enabled:
            st.markdown("##### Scan QR Code")
            # Simulate QR code display
            st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=HAZO2FADEMO", 
                caption="Scan with Google Authenticator or similar app")
            
            verification_code = st.text_input("Enter Verification Code")
            
            if st.button("Verify 2FA"):
                if verification_code:  # In real app, verify the code
                    st.session_state.twofa_enabled = True
                    st.session_state.verification_step = 4
                    st.success("2FA enabled successfully!")
                    st.rerun()
                else:
                    st.error("Please enter verification code")
        
    elif st.session_state.verification_step == 4:
        st.markdown("#### Connect Your Wallet")
        wallet_col1, wallet_col2 = st.columns([3, 1])
        with wallet_col1:
            wallet_type = st.selectbox(
                "Select Wallet",
                ['Phantom', 'Metamask', 'Coinbase', 'Trust Wallet', 'Ledger']
            )
        with wallet_col2:
            if st.button("Connect Wallet"):
                address = connect_wallet(wallet_type)
                st.session_state.kyc_status = "VERIFIED"
                st.success(f"Wallet connected and verification complete!")
                st.rerun()

# Header with wallet connection
st.title("🌿 Delco Collective Ecosystem")

# Description
st.markdown("""
    <div style='background-color: #1E1E1E; padding: 15px; border-radius: 5px; margin-bottom: 20px;'>
    <h4 style='color: #4CAF50;'>Blockchain Technology for the Cannabis Industry</h4>
    <p style='color: #FFFFFF;'>Demonstrating our dual-token system and industry-specific features on Solana</p>
    </div>
""", unsafe_allow_html=True)

# Create tabs - now with 7 tabs including Historical Transactions
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "💰 Wallet", 
    "🔗 Supply Chain", 
    "📊 Tokenomics", 
    "🏦 Staking", 
    "⚡ Solana Features",
    "🔐 Account & KYC",
    "📜 Historical Transactions",
    "📈 ROI Analysis"
])

with tab1:
    # Enhanced Wallet Section
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("HAZO Balance", f"{st.session_state.hazo_balance:,.2f} HAZO", "↑ 2.5%")
    with col2:
        st.metric("RAV Balance", f"{st.session_state.rav_balance:,.2f} RAV", "↑ 1.2%")
    with col3:
        st.metric("SOL Balance", f"{st.session_state.sol_balance:,.2f} SOL", "↑ 3.8%")
    
    # Transaction Section
    st.subheader("New Transaction")
    tx_type = st.selectbox(
        "Transaction Type",
        ["Seed-to-Sale", "Supply Chain Verification", "Payment Processing", "Staking"]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        batch_id = st.text_input("Batch ID", "BATCH-001")
        product = st.selectbox(
            "Product",
            ["Cannabis Flower", "Edibles", "Concentrates", "Seeds", "Clones"]
        )
    with col2:
        quantity = st.number_input("Quantity", 1, 1000, 100)
        price = st.number_input("Price per unit (RAV)", 0.1, 1000.0, 1.0)
    
    if st.button("Process Transaction"):
        gas_fee = random.uniform(0.1, 1.0)
        tx_hash = f"0x{''.join(random.choices('0123456789abcdef', k=64))}"
        
        # Create transaction record
        transaction = {
            'Timestamp': datetime.now(),
            'Type': tx_type,
            'Product': product,
            'Quantity': quantity,
            'Price (RAV)': price,
            'Total Value': quantity * price,
            'Gas Fee (RAV)': gas_fee,
            'Transaction Hash': tx_hash[:10] + "..." + tx_hash[-6:],
            'Status': 'Confirmed'
        }
        
        # Add to session state
        if 'transaction_history' not in st.session_state:
            st.session_state.transaction_history = []
        st.session_state.transaction_history.insert(0, transaction)  # Add new transaction at the beginning
        
        st.session_state.rav_balance -= gas_fee
        
        # Show success message
        st.success(f"Transaction processed! Gas fee: {gas_fee:.2f} RAV")
        
        # Log the event
        log_event(f"""
        TRANSACTION PROCESSED
        Type: {tx_type}
        Product: {product}
        Quantity: {quantity:,}
        Price: {price:,.2f} RAV
        Gas Fee: {gas_fee:.2f} RAV
        Total Value: {quantity * price:,.2f} RAV
        Hash: {tx_hash}
        """)

    # Display Transaction History
    if 'transaction_history' in st.session_state and st.session_state.transaction_history:
        st.subheader("Transaction History")
        df = pd.DataFrame(st.session_state.transaction_history)
        
        # Style the dataframe
        st.dataframe(
            df.style.format({
                'Timestamp': lambda x: x.strftime('%Y-%m-%d %H:%M:%S'),
                'Price (RAV)': '{:.2f}',
                'Total Value': '{:,.2f}',
                'Gas Fee (RAV)': '{:.4f}'
            }).apply(lambda x: ['background-color: #1a1a1a' if i % 2 else 'background-color: #2d2d2d' 
                              for i in range(len(x))]),
            use_container_width=True,
            height=400
        )

with tab2:
    st.subheader("Supply Chain Tracking")
    
    # Supply Chain Stage Selector
    stages = ['Cultivation', 'Testing', 'Processing', 'Distribution', 'Retail']
    current_stage = st.selectbox("Select Supply Chain Stage", stages)
    stage_index = stages.index(current_stage)
    
    # Progress Bar
    progress = st.progress(0)
    for i in range(stage_index + 1):
        progress.progress((i + 1) * (100 // len(stages)))
    
    # Stage Details
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Current Stage:** {current_stage}")
        st.markdown("**Status:** ✅ Verified on Blockchain")
        st.markdown("**Last Updated:** Just now")
    with col2:
        st.markdown("**Smart Contract:** Active")
        st.markdown("**Compliance Status:** Compliant")
        st.markdown("**Quality Control:** Passed")

with tab3:
    st.subheader("Tokenomics")
    
    # Create multiple tabs for different tokenomics charts
    token_tab1, token_tab2, token_tab3, token_tab4 = st.tabs([
        "Distribution", "Price History", "Trading Volume", "Staking Analytics"
    ])
    
    with token_tab1:
        col1, col2 = st.columns(2)
        with col1:
            # Token Distribution Pie Chart
            labels = ['Exchange LP', 'Presale', 'Marketing', 'Partnerships', 'Team']
            values = [210210210, 50000000, 34210210, 63000000, 63000000]
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=.3,
                marker_colors=['#4CAF50', '#81C784', '#A5D6A7', '#C8E6C9', '#E8F5E9'],
                textinfo='label+percent',
                hovertemplate="<b>%{label}</b><br>" +
                            "Amount: %{value:,.0f} HAZO<br>" +
                            "<extra></extra>"
            )])
            fig.update_layout(
                title="HAZO Token Distribution",
                showlegend=True,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            ### Token Details
            - **Total Supply:** 420,420,420 HAZO
            - **Circulating Supply:** 210,210,210 HAZO
            - **Current Price:** $0.15 USD
            - **Market Cap:** $63,063,063 USD
            - **24h Volume:** $1,234,567 USD
            """)
    
    with token_tab2:
        # Price History Area Chart
        dates = pd.date_range(start='2024-01-01', end='2024-03-14', freq='D')
        price_data = pd.DataFrame({
            'Date': dates,
            'Price': [0.10 + random.uniform(-0.02, 0.05) + (i * 0.001) for i in range(len(dates))]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=price_data['Date'],
            y=price_data['Price'],
            fill='tozeroy',
            fillcolor='rgba(76, 175, 80, 0.2)',
            line=dict(color='#4CAF50'),
            name='HAZO Price'
        ))
        
        fig.update_layout(
            title="HAZO Price History",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with token_tab3:
        # Trading Volume Bar Chart
        volume_data = pd.DataFrame({
            'Date': dates,
            'Volume': [random.uniform(500000, 2000000) for _ in range(len(dates))]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=volume_data['Date'],
            y=volume_data['Volume'],
            marker_color='#4CAF50',
            name='Trading Volume'
        ))
        
        fig.update_layout(
            title="Daily Trading Volume",
            xaxis_title="Date",
            yaxis_title="Volume (USD)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with token_tab4:
        # Staking Analytics
        col1, col2 = st.columns(2)
        with col1:
            # Staking Distribution Donut
            staking_labels = ['30 Days', '90 Days', '180 Days', '365 Days']
            staking_values = [15000000, 25000000, 35000000, 45000000]
            
            fig = go.Figure(data=[go.Pie(
                labels=staking_labels,
                values=staking_values,
                hole=.6,
                marker_colors=['#81C784', '#66BB6A', '#4CAF50', '#43A047'],
                textinfo='label+percent'
            )])
            fig.update_layout(
                title="Staking Duration Distribution",
                annotations=[dict(text='120M HAZO<br>Total Staked', x=0.5, y=0.5, font_size=12, showarrow=False)],
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # APY vs Lock Period Line Chart
            lock_periods = [30, 90, 180, 365]
            apy_rates = [12, 15, 18, 22]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=lock_periods,
                y=apy_rates,
                mode='lines+markers',
                line=dict(color='#4CAF50', width=3),
                marker=dict(size=10),
                name='APY Rate'
            ))
            
            fig.update_layout(
                title="APY vs Lock Period",
                xaxis_title="Lock Period (Days)",
                yaxis_title="APY (%)",
                height=400,
                xaxis=dict(tickmode='array', tickvals=lock_periods),
                yaxis=dict(ticksuffix='%')
            )
            st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Staking Platform")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Stake HAZO")
        stake_amount = st.number_input(
            "Amount to Stake", 
            min_value=0.0,
            max_value=float(st.session_state.hazo_balance),
            value=min(100.0, float(st.session_state.hazo_balance)),
            step=1.0,
            key="stake_amount_input"
        )
        stake_period = st.selectbox(
            "Staking Period", 
            ["30 Days", "90 Days", "180 Days", "365 Days"],
            key="stake_period_select"
        )
        if st.button("Stake HAZO", key="stake_hazo_button"):
            if stake_amount <= st.session_state.hazo_balance:
                st.session_state.hazo_balance -= stake_amount
                log_event(f"""
                STAKING COMPLETED
                Amount: {stake_amount:,.2f} HAZO
                Period: {stake_period}
                APY: {{"30 Days": "12%", "90 Days": "15%", "180 Days": "18%", "365 Days": "22%"}}[{stake_period}]
                Timestamp: {datetime.now()}
                """)
                st.success(f"Successfully staked {stake_amount:,.2f} HAZO")
            else:
                log_event("Insufficient HAZO balance for staking", "error")
    
    with col2:
        st.markdown("### Staking Rewards")
        st.markdown("""
        - 30 Days: 12% APY
        - 90 Days: 15% APY
        - 180 Days: 18% APY
        - 365 Days: 22% APY
        """)

with tab5:
    st.subheader("Solana Integration")
    
    col1, col2 = st.columns(2)
    with col1:
        # Add Token Swap section
        st.markdown("### Token Swap")
        swap_from = st.selectbox("From Token", ["HAZO", "RAV", "SOL"], key="swap_from")
        swap_to = st.selectbox("To Token", ["SOL", "HAZO", "RAV"], key="swap_to")
        
        # Add amount input with balance display
        max_amount = {
            "HAZO": st.session_state.hazo_balance,
            "RAV": st.session_state.rav_balance,
            "SOL": st.session_state.sol_balance
        }[swap_from]
        
        swap_amount = st.number_input(
            "Amount", 
            min_value=0.0,
            max_value=float(max_amount),
            value=1.0,
            key="swap_amount"
        )
        
        # Show estimated output with loading animation
        if swap_amount > 0:
            with st.spinner("Calculating best route..."):
                time.sleep(1)  # Simulate price calculation
                est_output = swap_amount * 1.5  # Simplified price calculation
                
            st.markdown(f"""
            **Estimated Output:** {est_output:.4f} {swap_to}
            - Price Impact: 0.05%
            - Minimum Received: {est_output * 0.995:.4f} {swap_to}
            - Network Fee: ~0.00001 SOL
            """)
        
        # Add swap button with loading animation
        if st.button("Swap Tokens"):
            with st.spinner("Processing swap..."):
                time.sleep(2)  # Simulate blockchain delay
                
                # Log the swap transaction
                log_event(f"""
                TOKEN SWAP EXECUTED
                From: {swap_amount:.4f} {swap_from}
                To: {est_output:.4f} {swap_to}
                Price Impact: 0.05%
                Network Fee: 0.00001 SOL
                """, "transaction")
                
                # Update balances
                if swap_from == "HAZO":
                    st.session_state.hazo_balance -= swap_amount
                elif swap_from == "RAV":
                    st.session_state.rav_balance -= swap_amount
                else:
                    st.session_state.sol_balance -= swap_amount
                
                if swap_to == "HAZO":
                    st.session_state.hazo_balance += est_output
                elif swap_to == "RAV":
                    st.session_state.rav_balance += est_output
                else:
                    st.session_state.sol_balance += est_output
                
                # Show success message
                st.success("✅ Swap Completed Successfully!")
                
                # Display transaction details in expandable section
                with st.expander("Transaction Details", expanded=True):
                    st.markdown(f"""
                    ### Swap Details
                    - **Amount In:** {swap_amount:.4f} {swap_from}
                    - **Amount Out:** {est_output:.4f} {swap_to}
                    - **Price Impact:** 0.05%
                    - **Route:** {swap_from} → {swap_to}
                    - **Network:** Solana
                    - **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    - **Status:** Confirmed
                    """)

    with col2:
        st.markdown("### Solana Network Stats")
        st.markdown("""
        - **Network Status:** ✅ Operational
        - **TPS:** 2,435
        - **Recent Block:** 189,274,893
        - **Epoch:** 347
        - **Slot:** 189,274,893
        """)
        
    st.markdown("### SPL Token Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Token Creation")
        token_name = st.text_input("Token Name", "Custom SPL Token", key="token_name")
        token_symbol = st.text_input("Token Symbol", "CSPL", key="token_symbol")
        token_decimals = st.number_input("Decimals", min_value=0, max_value=18, value=9)
        
        if st.button("Create SPL Token"):
            # Simulate loading
            with st.spinner("Creating token..."):
                time.sleep(1)  # Simulate blockchain delay
                
            log_message = f"""
            SPL TOKEN CREATED
            Name: {token_name}
            Symbol: {token_symbol}
            Decimals: {token_decimals}
            Initial Supply: 1,000,000
            Network: Solana Devnet
            Creator: {st.session_state.connected_wallet['address'] if st.session_state.connected_wallet else 'Unknown'}
            Timestamp: {datetime.now().isoformat()}
            """
            log_event(log_message, "success")
            
            # Show MEGA explosive diamond celebration
            # Single massive initial burst
            rain(
                emoji="💎",
                font_size=150,  # Massive diamonds
                falling_speed=500,  # Much faster
                animation_length=0.1  # Much shorter
            )
            
            # Quick follow-up bursts
            for _ in range(2):
                rain(
                    emoji="💎",
                    font_size=100,
                    falling_speed=400,  # Much faster
                    animation_length=0.05  # Much shorter
                )
            
            # Final sustained shower #add payment processing in route
            rain(
                emoji="💎",
                font_size=80,
                falling_speed=300,  # Much faster
                animation_length=0.05  # Much shorter
            )
            
            st.success("""
            ✅ Token Created Successfully
            """)
            
            with st.expander("Token Details", expanded=True):
                st.markdown(f"""
                ### Token Information
                - **Name:** {token_name}
                - **Symbol:** {token_symbol}
                - **Decimals:** {token_decimals}
                - **Initial Supply:** 1,000,000
                - **Network:** Solana Devnet
                - **Standard:** SPL Token
                - **Creator:** `{get_wallet_display()}`
                - **Creation Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                
                ### Token Features
                - ✓ Mintable
                - ✓ Burnable
                - ✓ Pausable
                - ✓ Metadata Support
                
                ### Contract Verification
                ```
                Successfully verified contract on Solana Explorer
                View on Explorer: https://explorer.solana.com/tx/...
                ```
                """)
            
    with col2:
        st.markdown("#### Token Minting")
        mint_amount = st.number_input("Mint Amount", min_value=0)
        destination = st.selectbox(
            "Destination",
            ["Treasury Wallet", "Liquidity Pool", "Marketing Wallet", "Custom Address"]
        )
        
        if destination == "Custom Address":
            custom_address = st.text_input("Enter Destination Address")
            
        if st.button("Mint Tokens"):
            with st.spinner("Minting tokens..."):
                # Simulate minting process
                time.sleep(2)  # Simulated delay
                
                # Log the minting transaction
                log_event("Minting 1,000 HAZO tokens", level="transaction")
                
                # Update balance
                st.session_state.hazo_balance += 1000
                
                # Show success message
                st.success("✅ Tokens Minted Successfully")
                
                # Display transaction details
                st.markdown(f"""
                ### Minting Details
                - **Amount:** 1,000 HAZO
                - **Recipient:** `{get_wallet_display()}`
                - **Network:** Solana Devnet
                - **Transaction Hash:** `{str(uuid.uuid4())}`
                - **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """)
            
    with col3:
        st.markdown("#### Token Burning")
        burn_amount = st.number_input("Burn Amount", min_value=0)
        if st.button("Burn Tokens"):
            with st.spinner("Burning tokens..."):
                time.sleep(2)  # Simulate burning process

                # Log the burning transaction
                log_event("Burning 1,000 HAZO tokens", level="transaction")

                # Update balance
                st.session_state.hazo_balance -= 1000

                # Show success message
                st.success("✅ Tokens Burned Successfully")

                # Display transaction details
                st.markdown(f"""
                ### Burning Details
                - **Amount:** 1,000 HAZO
                - **Burned From:** `{get_wallet_display()}`
                - **Network:** Solana Devnet
                - **Transaction Hash:** `{str(uuid.uuid4())}`
                - **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                """)

                # Add the same diamond celebration animation
                rain(
                    emoji="💎",
                    font_size=150,
                    falling_speed=500,
                    animation_length=0.1
                )

                # Quick follow-up bursts
                for _ in range(2):
                    rain(
                        emoji="💎",
                        font_size=100,
                        falling_speed=400,
                        animation_length=0.05
                    )

                # Final sustained shower
                rain(
                    emoji="💎",
                    font_size=80,
                    falling_speed=300,
                    animation_length=0.05
                )

    st.markdown("### Solana Program Deployment")
    col1, col2 = st.columns(2)
    with col1:
        st.code("""
// Sample Solana Program
pub fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    // Program logic here
    Ok(())
}
        """, language="rust")
    with col2:
        st.markdown("#### Deploy Program")
        if st.button("Deploy to Devnet"):
            st.success("Program deployed successfully to Devnet!")
            st.code("Program ID: BPFLoader2111111111111111111111111111111111")

with tab6:
    st.subheader("Account Setup & KYC")
    
    if not st.session_state.kyc_status:
        steps = ["Basic Info", "Identity Verification", "2FA Setup", "Wallet Connection"]
        progress = (st.session_state.verification_step - 1) / len(steps)
        st.progress(progress)
        st.markdown(f"**Step {st.session_state.verification_step} of {len(steps)}:** {steps[st.session_state.verification_step-1]}")
        
        if st.session_state.verification_step == 1:
            st.markdown("#### Basic Information")
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name", key="kyc_first_name")
                last_name = st.text_input("Last Name", key="kyc_last_name")
                dob = st.date_input("Date of Birth", key="kyc_dob")
            with col2:
                email = st.text_input("Email Address", key="kyc_email")
                phone = st.text_input("Phone Number", key="kyc_phone")
                country = st.selectbox("Country of Residence", 
                    ["United States", "Canada", "Other"],
                    key="kyc_country")
            
            if st.button("Continue to Identity Verification", key="kyc_continue_1"):
                if all([first_name, last_name, email, phone]):
                    st.session_state.verification_step = 2
                    log_event(f"""
                    📋 Basic Information Verified
                    Name: {first_name} {last_name}
                    Country: {country}
                    Status: Proceeding to Identity Verification
                    """, "info")
                    st.rerun()
                else:
                    log_event("Please fill in all required fields", "error")

        elif st.session_state.verification_step == 2:
            st.markdown("#### Identity Verification")
            doc_type = st.selectbox("Select ID Type", 
                ["Driver's License", "Passport", "Government ID"],
                key="kyc_doc_type")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("Upload Front of ID")
                id_front = st.file_uploader("Front", type=["jpg", "png", "pdf"], key="kyc_id_front")
            with col2:
                st.markdown("Upload Back of ID")
                id_back = st.file_uploader("Back", type=["jpg", "png", "pdf"], key="kyc_id_back")
                
            st.markdown("#### Proof of Address")
            address_doc = st.file_uploader("Upload Proof of Address", 
                type=["jpg", "png", "pdf"],
                key="kyc_address_doc")
                
            if st.button("Submit Documents", key="kyc_submit_docs"):
                if id_front and id_back and address_doc:
                    st.session_state.kyc_documents = {
                        "id_type": doc_type,
                        "id_front": True,
                        "id_back": True,
                        "address": True
                    }
                    st.session_state.verification_step = 3
                    st.success("Documents submitted successfully!")
                    st.rerun()
                else:
                    st.error("Please upload all required documents")

        elif st.session_state.verification_step == 3:
            st.markdown("#### Two-Factor Authentication Setup")
            
            if not st.session_state.twofa_enabled:
                st.markdown("##### Scan QR Code")
                st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=HAZO2FADEMO", 
                    caption="Scan with Google Authenticator or similar app")
                
                verification_code = st.text_input("Enter Verification Code", key="kyc_2fa_code")
                
                if st.button("Verify 2FA", key="kyc_verify_2fa"):
                    if verification_code:
                        st.session_state.twofa_enabled = True
                        log_event(f"""
                        🔐 Two-Factor Authentication Enabled
                        Method: Google Authenticator
                        Status: Active
                        Security Level: Enhanced
                        """, "success")
                        st.session_state.verification_step = 4
                        st.rerun()
                    else:
                        log_event("Please enter verification code", "error")
            
        elif st.session_state.verification_step == 4:
            st.markdown("#### Connect Your Wallet")
            wallet_col1, wallet_col2 = st.columns([3, 1])
            with wallet_col1:
                wallet_type = st.selectbox(
                    "Select Wallet",
                    ['Phantom', 'Metamask', 'Coinbase', 'Trust Wallet', 'Ledger'],
                    key="kyc_wallet_select"
                )
            with wallet_col2:
                if st.button("Connect Wallet", key="kyc_connect_wallet"):
                    address = connect_wallet(wallet_type)
                    log_event(f"""
                    WALLET CONNECTED
                    Type: {wallet_type}
                    Address: {address}
                    Status: Verified
                    Timestamp: {datetime.now()}
                    """)
                    st.session_state.kyc_status = "VERIFIED"
                    st.success(f"Wallet connected and verification complete!")
                    st.rerun()

    else:
        st.success("✅ KYC Verification Complete")
        st.markdown("### Account Status")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - **KYC Status:** Verified
            - **2FA Status:** Enabled
            - **Account Level:** Full Access
            """)
        with col2:
            st.markdown("""
            - **Verification Date:** {current_date}
            - **Last Login:** Just Now
            - **Security Status:** Strong
            """.format(current_date=datetime.now().strftime("%Y-%m-%d")))

with tab7:
    st.markdown("### 📜 Historical Transactions")
    
    # Create tabs for different transaction types
    tx_tab1, tx_tab2, tx_tab3 = st.tabs(["All Transactions", "Token Transfers", "Smart Contract Interactions"])

    with tx_tab1:
        # Sample historical transaction data
        all_transactions = pd.DataFrame({
            'Timestamp': [datetime.now() - pd.Timedelta(minutes=x) for x in range(10)],
            'Type': ['Transfer', 'Mint', 'Burn', 'Stake', 'Swap', 'Transfer', 'Mint', 'Burn', 'Stake', 'Swap'],
            'Amount': [random.randint(100, 10000) for _ in range(10)],
            'Token': ['HAZO', 'RAV', 'HAZO', 'RAV', 'HAZO', 'RAV', 'HAZO', 'RAV', 'HAZO', 'RAV'],
            'From': ['0x' + ''.join(random.choices('0123456789abcdef', k=8)) + '...' for _ in range(10)],
            'To': ['0x' + ''.join(random.choices('0123456789abcdef', k=8)) + '...' for _ in range(10)],
            'Status': ['Confirmed'] * 8 + ['Pending'] * 2,
            'Gas Fee (SOL)': [round(random.uniform(0.001, 0.01), 6) for _ in range(10)]
        })
        
        # Style the dataframe
        st.dataframe(
            all_transactions.style.apply(lambda x: ['background-color: #1a1a1a' if i % 2 else 'background-color: #2d2d2d' 
                                                  for i in range(len(x))]),
            use_container_width=True,
            height=300
        )

    with tx_tab2:
        # Token transfers only
        token_transfers = pd.DataFrame({
            'Timestamp': [datetime.now() - pd.Timedelta(minutes=x) for x in range(5)],
            'Token': ['HAZO', 'RAV', 'HAZO', 'RAV', 'HAZO'],
            'Amount': [random.randint(100, 10000) for _ in range(5)],
            'Sender': ['0x' + ''.join(random.choices('0123456789abcdef', k=8)) + '...' for _ in range(5)],
            'Recipient': ['0x' + ''.join(random.choices('0123456789abcdef', k=8)) + '...' for _ in range(5)],
            'Value (USD)': [round(random.uniform(100, 10000), 2) for _ in range(5)],
            'Status': ['Confirmed'] * 4 + ['Pending']
        })
        
        st.dataframe(
            token_transfers.style.apply(lambda x: ['background-color: #1a1a1a' if i % 2 else 'background-color: #2d2d2d' 
                                                 for i in range(len(x))]),
            use_container_width=True,
            height=300
        )

    with tx_tab3:
        # Smart contract interactions
        contract_interactions = pd.DataFrame({
            'Timestamp': [datetime.now() - pd.Timedelta(minutes=x) for x in range(5)],
            'Contract': ['Staking', 'Liquidity Pool', 'Governance', 'NFT Marketplace', 'Token Bridge'],
            'Function': ['stake()', 'addLiquidity()', 'vote()', 'listNFT()', 'bridge()'],
            'Caller': ['0x' + ''.join(random.choices('0123456789abcdef', k=8)) + '...' for _ in range(5)],
            'Gas Used': [random.randint(50000, 200000) for _ in range(5)],
            'Success': [''] * 4 + ['⏳'],
            'Block': [random.randint(1000000, 9999999) for _ in range(5)]
        })
        
        st.dataframe(
            contract_interactions.style.apply(lambda x: ['background-color: #1a1a1a' if i % 2 else 'background-color: #2d2d2d' 
                                                       for i in range(len(x))]),
            use_container_width=True,
            height=300
        )

    # Add filters and search
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("🔍 Search Transactions", placeholder="Search by hash, address, or token", key="hist_search")
    with col2:
        st.selectbox("Filter by Type", ["All Types", "Transfers", "Mints", "Burns", "Stakes", "Swaps"], key="hist_type")
    with col3:
        st.selectbox("Filter by Status", ["All Statuses", "Confirmed", "Pending", "Failed"], key="hist_status")

with tab8:
    st.subheader("🎯 Investment ROI Analysis")
    
    # Create two columns for different ROI metrics
    roi_col1, roi_col2 = st.columns(2)
    
    with roi_col1:
        st.markdown("### Token Investment Metrics")
        
        # Investment simulation inputs
        initial_investment = st.number_input(
            "Initial Investment (USD)", 
            min_value=100.0,
            value=10000.0,
            step=100.0,
            key="roi_investment_input"
        )
        
        investment_period = st.slider(
            "Investment Period (Months)",
            min_value=1,
            max_value=48,
            value=12,
            key="roi_period_slider"
        )
        
        # Calculate projected returns based on tokenomics
        projected_hazo_price = 0.15  # Initial HAZO price
        projected_growth = 1.2  # 20% projected growth rate
        rav_generation_rate = 0.05  # 5% RAV generation rate
        
        # Calculate projected values
        hazo_tokens = initial_investment / projected_hazo_price
        projected_hazo_value = hazo_tokens * (projected_hazo_price * (1 + projected_growth) ** (investment_period/12))
        projected_rav_generation = hazo_tokens * rav_generation_rate * investment_period
        
        total_projected_value = projected_hazo_value + projected_rav_generation
        roi_percentage = ((total_projected_value - initial_investment) / initial_investment) * 100
        
        # Display metrics
        st.metric(
            "Projected ROI",
            f"{roi_percentage:.2f}%",
            f"${total_projected_value - initial_investment:,.2f}"
        )
        
        # Create ROI breakdown chart
        roi_breakdown = {
            'HAZO Value': projected_hazo_value,
            'RAV Generation': projected_rav_generation
        }
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(roi_breakdown.keys()),
                y=list(roi_breakdown.values()),
                marker_color=['#4CAF50', '#81C784']
            )
        ])
        
        fig.update_layout(
            title="Projected Return Breakdown",
            yaxis_title="Value (USD)",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with roi_col2:
        st.markdown("### Staking & Yield Analysis")
        
        # Staking simulation
        staking_amount = st.number_input(
            "Staking Amount (HAZO)",
            min_value=100.0,
            value=5000.0,
            step=100.0,
            key="roi_staking_amount"
        )
        
        staking_period = st.selectbox(
            "Staking Period",
            ["30 Days", "90 Days", "180 Days", "365 Days"],
            key="roi_staking_period"
        )
        
        # APY rates based on staking period
        apy_rates = {
            "30 Days": 12,
            "90 Days": 15,
            "180 Days": 18,
            "365 Days": 22
        }
        
        selected_apy = apy_rates[staking_period]
        days = int(staking_period.split()[0])
        
        # Calculate staking returns
        staking_return = staking_amount * (1 + selected_apy/100 * days/365)
        staking_profit = staking_return - staking_amount
        
        # Display staking metrics
        st.metric(
            "Staking APY",
            f"{selected_apy}%",
            f"+{staking_profit:.2f} HAZO"
        )
        
        # Create staking projection chart
        periods = list(range(days + 1))
        values = [staking_amount * (1 + selected_apy/100 * d/365) for d in periods]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=periods,
            y=values,
            fill='tozeroy',
            fillcolor='rgba(76, 175, 80, 0.2)',
            line=dict(color='#4CAF50'),
            name='Staking Value'
        ))
        
        fig.update_layout(
            title=f"Projected Staking Growth ({staking_period})",
            xaxis_title="Days",
            yaxis_title="HAZO Tokens",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)