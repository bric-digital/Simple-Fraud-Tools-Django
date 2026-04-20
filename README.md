# Simple Fraud Tools for Django

This is a Django app for generating and catching fraud signals in the context of research studies.

It currently implements an endpoint that allows MaxMind DB files to be used to annotate IP addresses with attributes such as location and endpoint type (eyeball, VPN, data center), but is intended to be the starting point for a number of techniques that have been discussed over the years, but not packaged into a decent utility package.

*Use at your own risk (for now)!*
