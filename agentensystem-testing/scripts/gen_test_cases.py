#!/usr/bin/env python3
"""Generate comprehensive test cases for JOVI project."""
import json
from datetime import datetime

# Test case templates for different requirement types
test_cases = []
tc_counter = 1

def add_tc(title, desc, category, priority, precond, steps, expected, test_data, req_ids, endpoint="", error_code=""):
    global tc_counter
    tc = {
        "TC_ID": f"TC-JOVI-{tc_counter:03d}",
        "Test_Scenario": title,
        "Priority": priority,
        "Test_Case_Description": desc,
        "Preconditions": precond,
        "Test_Data": test_data,
        "Test_Steps": steps,
        "Expected_Result": expected,
        "REQ_ID": ", ".join(req_ids) if isinstance(req_ids, list) else req_ids,
        "API_Endpoint": endpoint,
        "Error_Code": error_code,
        "Category": category
    }
    test_cases.append(tc)
    tc_counter += 1

# REQ-JOVI-001: XSD Validation
add_tc("Valid pacs.008 XSD Validation", "Verify valid pacs.008 passes XSD validation",
       "FUNC", "CRITICAL",
       "JOVI system active; Valid ISO 20022 XSD schema loaded",
       "1. Given a valid pacs.008 XML message conforming to ISO 20022 schema\n2. When the message is submitted to validation endpoint\n3. Then the system performs XSD validation",
       "XSD validation passes; Message accepted for processing; No admi.011 NACK generated",
       "Valid pacs.008 with MsgId=MSG20260701001, TxId=TXN20260701001, Amount=1500.00 EUR, Debtor BIC=BBRUBEBBXXX, Creditor BIC=INGBNL2AXXX",
       ["REQ-JOVI-001"], "/jovi/payments/ip/incoming/validation")

add_tc("Invalid pacs.008 XSD - Missing Mandatory Element", "Verify invalid pacs.008 with missing element is rejected",
       "NEG", "CRITICAL",
       "JOVI system active",
       "1. Given a pacs.008 XML message missing mandatory CdtTrfTxInf element\n2. When the message is submitted to validation endpoint\n3. Then the system performs XSD validation",
       "XSD validation fails; admi.011 NACK returned with syntax error; Message rejected",
       "pacs.008 with missing <CdtTrfTxInf> element",
       ["REQ-JOVI-001"], "/jovi/payments/ip/incoming/validation", "NARR")

add_tc("Invalid pacs.008 XSD - Malformed XML", "Verify malformed XML is rejected with syntax error",
       "NEG", "CRITICAL",
       "JOVI system active",
       "1. Given a malformed XML structure (unclosed tags)\n2. When the message is submitted\n3. Then XML parsing fails",
       "Syntax error returned; admi.011 NACK generated; Message not processed",
       "Malformed XML with unclosed <Document> tag",
       ["REQ-JOVI-001"], "/jovi/payments/ip/incoming/validation", "FF01")

# REQ-JOVI-002: Dual Operating Mode
add_tc("Passthrough Mode - Forward to OVI", "Verify passthrough mode forwards to OVI mainframe",
       "FUNC", "CRITICAL",
       "JOVI activation switch = OFF; OVI mainframe available",
       "1. Given JOVI activation switch is OFF\n2. When valid pacs.008 is received\n3. Then request is forwarded to OVI mainframe via TEC Connector",
       "Request forwarded to OVI; No local processing; TEC Connector invoked; Response from OVI returned",
       "Valid pacs.008, JOVI_ACTIVATION_FLAG=0",
       ["REQ-JOVI-002"])

add_tc("Active Mode - Independent Processing", "Verify active mode processes independently",
       "FUNC", "CRITICAL",
       "JOVI activation switch = ON; All dependencies available",
       "1. Given JOVI activation switch is ON\n2. When valid pacs.008 is received\n3. Then request is processed independently by JOVI",
       "Request processed by JOVI; Validation, persistence, and downstream sync performed; No OVI forwarding",
       "Valid pacs.008, JOVI_ACTIVATION_FLAG=1",
       ["REQ-JOVI-002"])

# REQ-JOVI-003: Incoming Validation Endpoint
add_tc("Incoming Validation Endpoint - Valid Request", "Verify incoming validation endpoint processes valid request",
       "INT", "CRITICAL",
       "JOVI API available; Valid authentication",
       "1. Given valid JoviIncomingIPValidationReq with payment integrity\n2. When POST request sent to /jovi/payments/ip/incoming/validation\n3. Then pacs.008 is processed and response returned",
       "HTTP 200; JoviIncomingIPValidationRes with transactionId; pacs.008 validated",
       "transactionId=TXN-001, paymentIntegrity with valid signature and timestamp",
       ["REQ-JOVI-003"], "/jovi/payments/ip/incoming/validation")

# REQ-JOVI-004: Incoming Execution Endpoint
add_tc("Incoming Execution - Process Delivery Report", "Verify pacs.002 DR processing",
       "INT", "HIGH",
       "Valid incoming payment exists in system",
       "1. Given valid JoviIncomingIPExecutionReq with pacs.002 DR\n2. When POST to /jovi/payments/ip/incoming/execution\n3. Then delivery report is processed",
       "HTTP 200; JoviIncomingIPExecutionRes returned; Status updated for original payment",
       "pacs.002 DR with OriginalMsgId referencing existing payment",
       ["REQ-JOVI-004"], "/jovi/payments/ip/incoming/execution")

# REQ-JOVI-005: Outgoing Payment Initiation
add_tc("Outgoing Initiation - Successful Payment", "Verify FI payment initiation returns ACCP",
       "INT", "CRITICAL",
       "FI authenticated; CABI available; Clearing reachable",
       "1. Given valid pacs.008 from Financial Institution\n2. When POST to /jovi/payments/ip/outgoing/initiation\n3. Then payment is processed and pacs.002 returned",
       "HTTP 200; pacs.002 with status ACCP; Payment sent to clearing",
       "pacs.008 from FI with Amount=1500.00, valid Debtor/Creditor",
       ["REQ-JOVI-005"], "/jovi/payments/ip/outgoing/initiation", "ACCP")

add_tc("Outgoing Initiation - Rejected Payment", "Verify FI payment rejection returns RJCT",
       "NEG", "HIGH",
       "FI authenticated; Validation failure condition",
       "1. Given pacs.008 with invalid BIC\n2. When POST to /jovi/payments/ip/outgoing/initiation\n3. Then validation fails and RJCT returned",
       "HTTP 200; pacs.002 with status RJCT; Rejection reason code included",
       "pacs.008 with invalid Creditor BIC=INVALID123",
       ["REQ-JOVI-005"], "/jovi/payments/ip/outgoing/initiation", "AB08")

# REQ-JOVI-006: BIC Reachability - Creditor
add_tc("Creditor BIC Reachability - Valid BIC", "Verify reachable Creditor BIC passes validation",
       "FUNC", "HIGH",
       "FOVIREA table populated with valid BICs",
       "1. Given Creditor BIC exists in FOVIREA with valid date range\n2. When BIC reachability is checked\n3. Then validation passes",
       "BIC lookup returns valid record; DAGRTAR <= system date < DAGREND; Processing continues",
       "Creditor BIC=INGBNL2AXXX in FOVIREA with DAGRTAR=2024-01-01, DAGREND=2099-12-31",
       ["REQ-JOVI-006"])

add_tc("Creditor BIC Reachability - Unknown BIC", "Verify unreachable BIC rejected with AB08",
       "NEG", "HIGH",
       "FOVIREA table accessible",
       "1. Given Creditor BIC not in FOVIREA\n2. When BIC reachability is checked\n3. Then payment is rejected with AB08",
       "BIC lookup returns no record; Payment rejected; Error code AB08 returned",
       "Creditor BIC=UNKNOWNBIC not in FOVIREA",
       ["REQ-JOVI-006"], "", "AB08")

# REQ-JOVI-007: BIC Reachability - Debtor
add_tc("Debtor BIC Reachability - Valid BIC", "Verify reachable Debtor BIC passes validation",
       "FUNC", "HIGH",
       "FANALYSE populated; FOVIREA accessible",
       "1. Given Debtor BIC from FANALYSE is not NULL\n2. When BIC reachability checked in FOVIREA\n3. Then validation passes and TACCFILORO fetched",
       "BIC valid and reachable; FI Loro account retrieved; Processing continues",
       "Debtor BIC=BBRUBEBBXXX from FANALYSE, exists in FOVIREA",
       ["REQ-JOVI-007"])

add_tc("Debtor BIC Reachability - NULL BIC", "Verify NULL Debtor BIC rejected with AB08",
       "NEG", "HIGH",
       "FANALYSE returns NULL for Debtor BIC",
       "1. Given Debtor BIC from FANALYSE is NULL\n2. When BIC reachability checked\n3. Then payment is rejected with AB08",
       "Debtor BIC is NULL; Payment rejected immediately; Error code AB08",
       "Account without Debtor BIC in FANALYSE",
       ["REQ-JOVI-007"], "", "AB08")

# REQ-JOVI-008: Leading IBAN BIC Verification
add_tc("Leading IBAN - BIC Match", "Verify matching BIC from LeadingIBAN passes",
       "FUNC", "HIGH",
       "LeadingIBAN API available",
       "1. Given debtor IBAN BE68539007547034\n2. When LeadingIBAN API called\n3. Then derived BIC matches first 8 chars of Debtor BIC",
       "LeadingIBAN returns BBRUBEBB; First 8 chars of Debtor BIC match; Validation passes",
       "Debtor IBAN=BE68539007547034, Debtor BIC=BBRUBEBBXXX",
       ["REQ-JOVI-008"])

add_tc("Leading IBAN - BIC Mismatch", "Verify BIC mismatch rejected with MS03",
       "NEG", "HIGH",
       "LeadingIBAN API available",
       "1. Given debtor IBAN with derived BIC different from provided BIC\n2. When LeadingIBAN API called\n3. Then BIC mismatch detected",
       "LeadingIBAN returns ABNANL2A; Debtor BIC=INGBNL2A mismatch; Rejection with MS03",
       "Debtor IBAN=NL91ABNA0417164300, Debtor BIC=INGBNL2AXXX (mismatch)",
       ["REQ-JOVI-008"], "", "MS03")

# REQ-JOVI-009: Duplicate Detection - Incoming
add_tc("Incoming Duplicate Detection - New Transaction", "Verify new transaction proceeds",
       "FUNC", "HIGH",
       "FOVIIPI table accessible",
       "1. Given TTxId + Debtor BIC combination not in FOVIIPI\n2. When duplicate check performed\n3. Then transaction proceeds",
       "No duplicate found; Transaction marked as new; Processing continues",
       "TTxId=TXN20260701NEW, Debtor BIC=BBRUBEBBXXX",
       ["REQ-JOVI-009"])

add_tc("Incoming Duplicate Detection - Duplicate Found", "Verify duplicate transaction rejected",
       "NEG", "HIGH",
       "Existing transaction in FOVIIPI",
       "1. Given TTxId + Debtor BIC exists in FOVIIPI\n2. When duplicate check performed\n3. Then transaction rejected",
       "Duplicate detected; NOK response to gateway; LAPS log entry created",
       "TTxId=TXN20260701EXISTING (exists in FOVIIPI), Debtor BIC=BBRUBEBBXXX",
       ["REQ-JOVI-009"], "", "DUPL")

# REQ-JOVI-010: Duplicate Detection - Outgoing
add_tc("Outgoing Duplicate - Return Positive pacs.002", "Verify duplicate with CSTA=02 returns ACCP",
       "FUNC", "HIGH",
       "Existing FOVIIPO record with CSTA=02",
       "1. Given TTxId + Debtor BIC exists with CSTA=02 (To be Booked)\n2. When duplicate check performed\n3. Then return positive pacs.002 with ACCP",
       "Duplicate found with booked status; pacs.002 ACCP returned; No re-processing",
       "TTxId=TXN20260701DUP, CSTA=02",
       ["REQ-JOVI-010"])

add_tc("Outgoing Duplicate - Return Negative pacs.002", "Verify duplicate with CSTA>=90 returns RJCT",
       "NEG", "HIGH",
       "Existing FOVIIPO record with CSTA=90",
       "1. Given TTxId + Debtor BIC exists with CSTA=90 (Rejected)\n2. When duplicate check performed\n3. Then return negative pacs.002 with RJCT",
       "Duplicate found with rejected status; pacs.002 RJCT returned",
       "TTxId=TXN20260701DUP, CSTA=90",
       ["REQ-JOVI-010"], "", "RJCT")

# REQ-JOVI-011: Transaction ID Format
add_tc("Transaction ID Format - Valid IDs", "Verify valid IDs without leading spaces pass",
       "DATA", "HIGH",
       "System ready",
       "1. Given pacs.008 with valid IDs without leading spaces\n2. When format validation performed\n3. Then processing continues",
       "All IDs valid; No format errors; Processing proceeds",
       "TxId=TXN20260701001, MsgId=MSG20260701001, InstrId=INSTR001",
       ["REQ-JOVI-011"])

add_tc("Transaction ID Format - Leading Spaces", "Verify IDs with leading spaces rejected with FF01",
       "NEG", "HIGH",
       "System ready",
       "1. Given pacs.008 with leading space in TxId\n2. When format validation performed\n3. Then rejection with FF01",
       "Leading space detected; Payment rejected; FF01 error code",
       "TxId= TXN20260701001 (leading space)",
       ["REQ-JOVI-011"], "", "FF01")

# REQ-JOVI-012: Settlement Method
add_tc("Settlement Method - Valid CLRG", "Verify CLRG settlement method accepted",
       "FUNC", "HIGH",
       "System ready",
       "1. Given pacs.008 with SttlMtd=CLRG\n2. When settlement validation performed\n3. Then processing continues",
       "CLRG accepted; Validation passes; Processing continues",
       "SttlMtd=CLRG",
       ["REQ-JOVI-012"])

add_tc("Settlement Method - Invalid Non-CLRG", "Verify non-CLRG rejected with FF01",
       "NEG", "HIGH",
       "System ready",
       "1. Given pacs.008 with SttlMtd=INDA\n2. When settlement validation performed\n3. Then group-level rejection with FF01",
       "Non-CLRG rejected; Group-level rejection; ZOVI-FDB-cStsOrig=RJCT",
       "SttlMtd=INDA",
       ["REQ-JOVI-012"], "", "FF01")

# REQ-JOVI-013: Charge Bearer
add_tc("Charge Bearer - Valid SLEV", "Verify SLEV charge bearer accepted",
       "FUNC", "HIGH",
       "System ready",
       "1. Given pacs.008 with ChrgBr=SLEV\n2. When charge bearer validation performed\n3. Then processing continues",
       "SLEV accepted; Validation passes",
       "ChrgBr=SLEV",
       ["REQ-JOVI-013"])

add_tc("Charge Bearer - Invalid Non-SLEV", "Verify non-SLEV rejected with FF01",
       "NEG", "HIGH",
       "System ready",
       "1. Given pacs.008 with ChrgBr=DEBT\n2. When charge bearer validation performed\n3. Then group-level rejection with FF01",
       "Non-SLEV rejected; FF01 at group level",
       "ChrgBr=DEBT",
       ["REQ-JOVI-013"], "", "FF01")

# REQ-JOVI-015: Global Screening Flag
add_tc("Global Screening Flag - ON", "Verify screening applied when flag is ON",
       "FUNC", "HIGH",
       "screeningGlobalFlag=1",
       "1. Given screeningGlobalFlag=1 (ON)\n2. When payment processed\n3. Then screening logic is applied",
       "Screening API called; Status updated to 05 (Sent to Screening)",
       "screeningGlobalFlag=1",
       ["REQ-JOVI-015"])

add_tc("Global Screening Flag - OFF", "Verify screening bypassed when flag is OFF",
       "FUNC", "HIGH",
       "screeningGlobalFlag=0",
       "1. Given screeningGlobalFlag=0 (OFF)\n2. When payment processed\n3. Then screening is bypassed",
       "Screening API not called; Processing continues without screening",
       "screeningGlobalFlag=0",
       ["REQ-JOVI-015"])

# REQ-JOVI-016: Cross-Border Screening
add_tc("Cross-Border Payment - Screening Required", "Verify cross-border sends to screening",
       "COMPLIANCE", "HIGH",
       "screeningGlobalFlag=1; Fircosoft available",
       "1. Given Creditor country (NL) differs from Debtor country (BE)\n2. When payment processed\n3. Then transaction sent to Fircosoft screening",
       "Cross-border detected; Screening request sent; CSTAWTG=05",
       "Debtor country=BE, Creditor country=NL",
       ["REQ-JOVI-016"])

# REQ-JOVI-018: Screening HIT Response
add_tc("Screening HIT - Payment Rejected", "Verify HIT response rejects with RR04",
       "COMPLIANCE", "HIGH",
       "Screening returns HIT",
       "1. Given payment sent to screening\n2. When Fircosoft returns HIT/HOLD response\n3. Then payment rejected with RR04",
       "HIT detected; Status=08; Payment rejected; RR04 error code",
       "Screening response=HIT",
       ["REQ-JOVI-018"], "", "RR04")

# REQ-JOVI-019: Screening NO-HIT Response
add_tc("Screening NO-HIT - Payment Continues", "Verify NO-HIT allows payment to proceed",
       "COMPLIANCE", "HIGH",
       "Screening returns NO-HIT",
       "1. Given payment sent to screening\n2. When Fircosoft returns NO-HIT response\n3. Then payment continues to FI Gateway",
       "NO-HIT received; Status=09; Processing continues to FI",
       "Screening response=NO-HIT",
       ["REQ-JOVI-019"])

# REQ-JOVI-022: FI Response Timeout
add_tc("FI Response Timeout - 7 Second SLA", "Verify timeout after 7 seconds triggers recovery",
       "NFR", "CRITICAL",
       "FI Gateway configured with 7s timeout",
       "1. Given payment sent to FI for validation\n2. When no response received within 7 seconds\n3. Then timeout handling triggered",
       "Timeout after 7s; Status updated; OVI146 recovery scheduled",
       "FI response delay > 7000ms",
       ["REQ-JOVI-022"])

# REQ-JOVI-023: FI Acceptance
add_tc("FI Acceptance - Positive pacs.002", "Verify FI acceptance generates ACCP response",
       "FUNC", "CRITICAL",
       "FI returns positive response",
       "1. Given payment validated by FI\n2. When FI returns acceptance\n3. Then status=17 and pacs.002 ACCP sent to clearing",
       "Status updated to 17; Positive pacs.002 generated; Sent to clearing",
       "FI response=ACCEPTANCE",
       ["REQ-JOVI-023"], "", "ACCP")

# REQ-JOVI-024: FI Rejection
add_tc("FI Rejection - Negative pacs.002", "Verify FI rejection generates RJCT response",
       "FUNC", "HIGH",
       "FI returns rejection",
       "1. Given payment sent to FI\n2. When FI returns rejection with error code\n3. Then status=96 and negative pacs.002 with FI error",
       "Status updated to 96; Negative pacs.002 generated; FI error code propagated",
       "FI response=REJECTION with AC04",
       ["REQ-JOVI-024"], "", "AC04")

# REQ-JOVI-025: Clearing Timeout - Outgoing
add_tc("Clearing Timeout - Pending Status", "Verify clearing timeout returns PDNG",
       "NFR", "HIGH",
       "Clearing response delayed > 7s",
       "1. Given payment sent to clearing\n2. When no response within 7 seconds\n3. Then status=10 and PDNG response with pacs.028 recovery",
       "Status=10 (Awaiting Inquiry); pacs.002 PDNG returned; pacs.028 status request sent",
       "Clearing response delay > 7000ms",
       ["REQ-JOVI-025"], "", "PDNG")

# REQ-JOVI-027: Payment Integrity Verification
add_tc("Payment Integrity - Valid Signature", "Verify valid RTPE signature passes",
       "FUNC", "HIGH",
       "RTPE library available",
       "1. Given pacs.008 with valid payment integrity signature\n2. When RTPE library validates signature\n3. Then validation passes within 3000ms",
       "Signature valid; Timestamp within 60s drift; Processing continues",
       "Valid RTPE signature, timestamp < 60s old",
       ["REQ-JOVI-027"])

add_tc("Payment Integrity - Invalid Signature", "Verify invalid signature rejected with AM05",
       "NEG", "HIGH",
       "RTPE library available",
       "1. Given pacs.008 with invalid payment integrity signature\n2. When RTPE library validates\n3. Then validation fails with AM05",
       "Signature invalid; Payment rejected; AM05 error code",
       "Invalid/tampered RTPE signature",
       ["REQ-JOVI-027"], "", "AM05")

# REQ-JOVI-028: CABI Debit Reservation
add_tc("CABI Reservation - Successful", "Verify successful debit reservation",
       "INT", "CRITICAL",
       "CABI AIP037 API available; Sufficient funds",
       "1. Given outgoing payment with valid debtor account\n2. When CABI AIP037 reservation called\n3. Then funds reserved successfully",
       "Reservation confirmed; CABI reference returned; Processing continues",
       "Debtor account with balance > payment amount",
       ["REQ-JOVI-028"])

add_tc("CABI Reservation - Insufficient Funds", "Verify insufficient funds rejected with AM23",
       "NEG", "HIGH",
       "CABI available; Insufficient funds",
       "1. Given outgoing payment with insufficient funds\n2. When CABI AIP037 reservation called\n3. Then reservation fails with AM23",
       "Reservation failed; Payment rejected; AM23 error code",
       "Debtor account with balance < payment amount",
       ["REQ-JOVI-028"], "", "AM23")

# REQ-JOVI-055: Incoming Health Check
add_tc("Incoming API Health Check - Healthy", "Verify health check returns 200 when healthy",
       "NFR", "MEDIUM",
       "All dependencies available",
       "1. Given all JOVI incoming dependencies healthy\n2. When GET /jovi/ip/incoming/health-check\n3. Then HTTP 200 with healthy status",
       "HTTP 200; JSON response with status=UP, timestamp, dependencies all healthy",
       "All dependencies UP",
       ["REQ-JOVI-055"], "/jovi/ip/incoming/health-check")

add_tc("Incoming API Health Check - Unhealthy", "Verify health check returns 503 when unhealthy",
       "NEG", "MEDIUM",
       "One or more dependencies down",
       "1. Given Cassandra dependency down\n2. When GET /jovi/ip/incoming/health-check\n3. Then HTTP 503 with unhealthy status",
       "HTTP 503; JSON response with status=DOWN, failed dependency listed",
       "Cassandra dependency DOWN",
       ["REQ-JOVI-055"], "/jovi/ip/incoming/health-check")

# REQ-JOVI-058: 24/7 Availability
add_tc("High Availability - 99.9% SLA", "Verify system meets availability SLA",
       "NFR", "CRITICAL",
       "Monitoring configured",
       "1. Given JOVI system operating 24/7\n2. When availability measured over 30 days\n3. Then availability >= 99.9%",
       "Availability >= 99.9%; Max downtime <= 8.76 hours/year; MTTR < 15 minutes",
       "30-day monitoring period",
       ["REQ-JOVI-058"])

# E2E Tests
add_tc("E2E Incoming Payment - Happy Path", "Full incoming payment flow",
       "E2E", "CRITICAL",
       "All systems active; screeningGlobalFlag=0",
       "1. Given valid pacs.008 from clearing\n2. When submitted to validation endpoint\n3. Then validated, sent to FI, accepted, booked, pacs.002 ACCP returned",
       "Complete flow: Validation -> FI -> Booking -> pacs.002 ACCP; Status transitions: 00->01->05->09->16->17->21",
       "Full valid pacs.008 with all required fields",
       ["REQ-JOVI-001", "REQ-JOVI-003", "REQ-JOVI-006", "REQ-JOVI-009", "REQ-JOVI-023"])

add_tc("E2E Outgoing Payment - Happy Path", "Full outgoing payment flow",
       "E2E", "CRITICAL",
       "All systems active; CABI available; Clearing reachable",
       "1. Given valid pacs.008 from FI\n2. When submitted to initiation endpoint\n3. Then validated, reserved, screened, sent to clearing, ACCP returned",
       "Complete flow: Validation -> CABI -> Screening -> Clearing -> pacs.002 ACCP",
       "Full valid pacs.008 from FI with sufficient funds",
       ["REQ-JOVI-005", "REQ-JOVI-007", "REQ-JOVI-008", "REQ-JOVI-010", "REQ-JOVI-028"])

add_tc("E2E Incoming Payment - Screening HIT", "Incoming payment blocked by screening",
       "E2E", "HIGH",
       "screeningGlobalFlag=1; Fircosoft configured to return HIT",
       "1. Given pacs.008 matching screening watchlist\n2. When processed through screening\n3. Then payment rejected with RR04",
       "Flow stops at screening; pacs.002 RJCT with RR04; Compliance alert raised",
       "pacs.008 with entity on watchlist",
       ["REQ-JOVI-016", "REQ-JOVI-018"])

add_tc("E2E Outgoing Payment - CABI Failure", "Outgoing payment fails due to insufficient funds",
       "E2E", "HIGH",
       "CABI available; Account has insufficient funds",
       "1. Given pacs.008 with amount exceeding account balance\n2. When CABI reservation attempted\n3. Then payment rejected with AM23",
       "CABI returns failure; pacs.002 RJCT with AM23; No funds reserved",
       "pacs.008 with Amount=100000.00, Account balance=50000.00",
       ["REQ-JOVI-005", "REQ-JOVI-028"])

# Boundary Tests
add_tc("Amount Boundary - Maximum SEPA Amount", "Verify maximum SEPA instant amount accepted",
       "BOUNDARY", "HIGH",
       "System configured with max amount",
       "1. Given pacs.008 with Amount=100000.00 EUR (max)\n2. When validation performed\n3. Then amount accepted",
       "Maximum amount accepted; Validation passes",
       "Amount=100000.00 EUR",
       ["REQ-JOVI-028"])

add_tc("Amount Boundary - Over Maximum", "Verify amount over maximum rejected",
       "BOUNDARY", "HIGH",
       "System configured with max amount",
       "1. Given pacs.008 with Amount=100000.01 EUR (over max)\n2. When validation performed\n3. Then rejected with AM23",
       "Amount exceeds limit; Payment rejected; AM23",
       "Amount=100000.01 EUR",
       ["REQ-JOVI-028"], "", "AM23")

add_tc("Amount Boundary - Minimum Amount", "Verify minimum amount accepted",
       "BOUNDARY", "MEDIUM",
       "System ready",
       "1. Given pacs.008 with Amount=0.01 EUR (minimum)\n2. When validation performed\n3. Then amount accepted",
       "Minimum amount accepted; Validation passes",
       "Amount=0.01 EUR",
       ["REQ-JOVI-028"])

# Additional coverage for remaining requirements
add_tc("MOD97 Communication Reference - Valid", "Verify MOD97 check passes for valid reference",
       "FUNC", "MEDIUM",
       "System ready",
       "1. Given cComTrf=00001 with valid MOD97 TcomTrf\n2. When MOD97 check performed\n3. Then CCOMTRF=3",
       "MOD97 passes; CCOMTRF=3; TCOMSTC and TCOM set",
       "cComTrf=00001, TcomTrf=+++123/1234/12345+++",
       ["REQ-JOVI-014"])

add_tc("MOD97 Communication Reference - Invalid", "Verify MOD97 check failure sets CCOMTRF=2",
       "NEG", "MEDIUM",
       "System ready",
       "1. Given cComTrf=00001 with invalid MOD97 TcomTrf\n2. When MOD97 check performed\n3. Then CCOMTRF=2",
       "MOD97 fails; CCOMTRF=2; TCOM set; Processing continues",
       "cComTrf=00001, TcomTrf=INVALID (fails MOD97)",
       ["REQ-JOVI-014"])

add_tc("Domestic Screening Flag - ON", "Verify domestic screening when flag enabled",
       "COMPLIANCE", "HIGH",
       "screeningGlobalFlag=1; TEVTTYP=1 in FOVIREA",
       "1. Given domestic payment (same country)\n2. When TEVTTYP flag checked in FOVIREA\n3. Then screening performed",
       "TEVTTYP=1; Payment sent to screening",
       "Domestic payment, TEVTTYP=1",
       ["REQ-JOVI-017"])

add_tc("Domestic Screening Flag - OFF", "Verify domestic screening bypassed when flag disabled",
       "COMPLIANCE", "HIGH",
       "screeningGlobalFlag=1; TEVTTYP=0 in FOVIREA",
       "1. Given domestic payment (same country)\n2. When TEVTTYP flag checked in FOVIREA\n3. Then screening bypassed",
       "TEVTTYP=0; Screening skipped; Processing continues",
       "Domestic payment, TEVTTYP=0",
       ["REQ-JOVI-017"])

add_tc("Screening Technical Error - Retry", "Verify technical error triggers retry then rejection",
       "RESILIENCE", "HIGH",
       "Screening API returns error",
       "1. Given payment sent to screening\n2. When API returns technical error\n3. Then retry once, if still fails reject with RR04",
       "Retry performed; After failure status=07; RR04 if persists",
       "Screening API error response",
       ["REQ-JOVI-020"])

add_tc("Screening Timeout - Retry", "Verify screening timeout triggers retry",
       "RESILIENCE", "HIGH",
       "Screening API slow response",
       "1. Given payment sent to screening\n2. When response timeout occurs\n3. Then retry once with status=06",
       "Timeout detected; Status=06; One retry attempted",
       "Screening response > timeout threshold",
       ["REQ-JOVI-021"])

add_tc("ADMI.011 NACK Processing", "Verify ADMI.011 NACK updates original payment",
       "FUNC", "HIGH",
       "Original payment exists in system",
       "1. Given admi.011 NACK received with empty MsgIdOrig\n2. When processed as NACK\n3. Then original payment status updated",
       "NACK identified; Original payment found and updated; Appropriate status set",
       "admi.011 with empty MsgIdOrig referencing existing pacs.008",
       ["REQ-JOVI-026"])

add_tc("Skip Reservation Flag - Enabled", "Verify reservation skipped when flag enabled",
       "FUNC", "MEDIUM",
       "skipReservationFlag configured",
       "1. Given skipReservationFlag=1 via EASY SCREENS\n2. When outgoing payment processed\n3. Then CABI reservation skipped",
       "Flag checked; CABI not called; SKIP_RES marker set; Processing continues",
       "skipReservationFlag=1",
       ["REQ-JOVI-033"])

add_tc("Skip Booking Flag - Enabled", "Verify booking skipped when flag enabled",
       "FUNC", "MEDIUM",
       "bookingSkipFlag configured; OVI146 scanner ready",
       "1. Given bookingSkipFlag=1\n2. When payment reaches booking step\n3. Then CABI booking skipped, OVI146 handles reconciliation",
       "Booking skipped; OVI146 scanner picks up for reconciliation within 30s cycle",
       "bookingSkipFlag=1",
       ["REQ-JOVI-034"])

add_tc("FOVIIPI Scanner - Status Check", "Verify scanner polls Cassandra for status updates",
       "INT", "MEDIUM",
       "Cassandra accessible; Scanner active",
       "1. Given FOVIIPI scanner running\n2. When 30 second interval elapses\n3. Then scanner polls CASSDB.FOVIIPI for pending records",
       "Scanner executes; Records retrieved with DCR/WPR parameters; Max 3 retries on failure",
       "Scanner interval=30s",
       ["REQ-JOVI-038"])

add_tc("Outgoing API Health Check", "Verify outgoing health check includes CABI/SIPG",
       "NFR", "MEDIUM",
       "Dependencies configured",
       "1. Given outgoing API running\n2. When GET /jovi/payments/ip/outgoing/health-check\n3. Then response includes CABI and SIPG status",
       "HTTP 200/503; JSON with status, dependencies including CABI and SIPG",
       "All dependencies configured",
       ["REQ-JOVI-056"], "/jovi/payments/ip/outgoing/health-check")

add_tc("Network Security - Allowed Ports", "Verify only allowed ports accessible",
       "NFR", "HIGH",
       "Firewall configured",
       "1. Given firewall rules applied\n2. When connection attempted on port 8443\n3. Then connection allowed",
       "Port 8443 accessible; Ports 9443, 443, 9093 also allowed; Others blocked and logged to Splunk",
       "Connection to port 8443",
       ["REQ-JOVI-061"])

add_tc("Audit Logging - JSON Format", "Verify audit logs in JSON format with required fields",
       "NFR", "HIGH",
       "Kibana logging configured",
       "1. Given transaction processed\n2. When audit log entry created\n3. Then log is JSON with required fields",
       "JSON format; Contains transactionId, messageId, timestamp, status; 90-day retention",
       "Any transaction",
       ["REQ-JOVI-062"])

# Write output
output = {
    "project": "JOVI",
    "domain": "Core Banking/Payments",
    "generated_date": datetime.now().strftime("%Y-%m-%d"),
    "llm_model": "Claude Opus 4",
    "total_test_cases": len(test_cases),
    "test_cases": test_cases
}

with open("output/test_cases/_llm_test_cases.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Generated {len(test_cases)} test cases")

# Category breakdown
categories = {}
for tc in test_cases:
    cat = tc.get("Category", "UNKNOWN")
    categories[cat] = categories.get(cat, 0) + 1

print("\nCategory breakdown:")
for cat, count in sorted(categories.items()):
    print(f"  {cat}: {count}")

# Priority breakdown
priorities = {}
for tc in test_cases:
    pri = tc.get("Priority", "UNKNOWN")
    priorities[pri] = priorities.get(pri, 0) + 1

print("\nPriority breakdown:")
for pri, count in sorted(priorities.items()):
    print(f"  {pri}: {count}")
