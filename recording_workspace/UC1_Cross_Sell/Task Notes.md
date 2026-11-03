# Task: Cross-sell targeting model + back-test

## In plain words
- **Who should we offer a new product to?** The bank has 20,000 existing customers, but the campaign budget only covers contacting **4,000** of them.
- Picked at random, only about **1 in 9** buys. Every contact costs money, so a badly chosen list wastes most of the budget.
- **My job:** learn from past results which kinds of customers tend to buy, give every customer a score (their chance of buying), and contact the 4,000 with the highest scores, only customers who agreed to marketing and nobody with repeated complaints.
- **Proof:** check it on a past campaign where we already know who bought. How many more sales, and how much more profit, than picking at random?

**Request (Head of CRM & Cross-Sell):** Marketing contacts 4,000 customers per campaign and converts ~1 in 9 at random. Before the Q4 budget is signed off, prove a model does better: which 4,000 customers would it have picked on 30 June, and how many actually converted vs random?

## Starting point
- **1_Input**: customers.csv (20,000 customers, 30 Jun 2026 snapshot, Jul–Sep outcome) · data dictionary · campaign brief (PDF) · deck template
- **2_Code**: my cross-sell pipeline (config + 4 notebooks), built for this request, first full run today

## Plan
1. Brief + dictionary: constraints and leakage suspects
2. LibreOffice Calc pivots on the raw extract: conversion drivers, data quality, leakage, missing data
3. Walk through and run the pipeline end to end, fixing what the run exposes: preprocessing → training → testing → back-test
4. Validate the back-test ROI in Calc
5. Complete the summary deck in Impress

## Done when
- Hold-out ROC-AUC ≥ 0.78 · beats the baseline on PR-AUC · top-20% lift ≥ 2.5×
- No leaky or gender fields
- 4,000 compliant customers converting ≥ 2× the eligible average
