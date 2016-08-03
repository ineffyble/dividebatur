#!/usr/bin/python3

# We don't have a copy of the "all-candidates" CSV file for the 2014
# WA Senate election, so synthesise the parts we care about from the
# GVT data file.

import csv

all_candidates_columns = ["txn_nm","nom_ty","state_ab","div_nm","ticket","ballot_position","surname","ballot_given_nm","party_ballot_nm","occupation","address_1","address_2","postcode","suburb","address_state_ab","contact_work_ph","contact_home_ph","postal_address_1","postal_address_2","postal_suburb","postal_postcode","contact_fax","postal_state_ab","contact_mobile_no","contact_email"]

with open('all-candidates-synthesised.csv', 'wt') as fp:
    writer = csv.DictWriter(fp, all_candidates_columns)
    writer.writeheader()

    with open('SenateGroupVotingTicketsDownload-17875.csv', 'rt') as fp:
        reader = csv.reader(fp)
        next(reader)
        gvt_column_id = {col: i for (i, col) in enumerate(next(reader))}
        current_ticket = None
        for t in reader:
            # We can stop once we've read one entire ticket
            ticket = (t[gvt_column_id["OwnerGroupNm"]],
                      t[gvt_column_id["OwnerTicket"]])
            if current_ticket is not None and current_ticket != ticket:
                break
            current_ticket = ticket

            writer.writerow(dict(
                nom_ty="S",
                state_ab="WA",
                ticket=t[gvt_column_id["CandidateTicket"]],
                surname=t[gvt_column_id["Surname"]],
                ballot_given_nm=t[gvt_column_id["GivenNm"]],
                party_ballot_nm=t[gvt_column_id["PartyNm"]],
                ballot_position=t[gvt_column_id["BallotPosition"]],
            ))
