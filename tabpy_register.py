from tabpy_client import Client

# Connect to a running TabPy server. Default TabPy listens on http://localhost:9004
client = Client('http://localhost:9004/')

# Example Python function to deploy: multiply numbers by two
def multiply_by_two(arg):
    # TabPy passes lists/columns from Tableau as lists/iterables
    return [float(x) * 2 for x in arg]

if __name__ == '__main__':
    # Deploy (or override) the function on the TabPy server under the name 'multiply_by_two'
    client.deploy('multiply_by_two', multiply_by_two, 'Multiply numeric values by two', override=True)
    print("Deployed 'multiply_by_two' to TabPy at http://localhost:9004/")
    print("In Tableau use: SCRIPT_REAL(\"return tabpy.query('multiply_by_two', _arg1)['response']\", SUM([YourNumericField]))")
