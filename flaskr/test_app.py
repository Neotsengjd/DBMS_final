import requests

class TestCase:
    def __init__(self):
        self.base_url = 'http://localhost:5000'

    def test_get_all_wallets(self):
        suffix = '/wallet/get_all_wallets?user_id=1'
        response = requests.get(self.base_url + suffix)
        print(response.status_code)
        print(response.json())  # 打印回應的JSON內容

    def test_get_ledgers(self):
        suffix = '/ledger/get_ledgers?wallet_id=1'
        response = requests.get(self.base_url + suffix)
        print(response.status_code)
        print(response.json())

    def test_get_all_ledgers(self):
        suffix = '/ledger/get_all_ledgers?user_id=1'
        response = requests.get(self.base_url + suffix)
        print(response.status_code)
        print(response.json())

    def test_get_all_goals(self):
        suffix = '/goal/get_all_goals?user_id=1'
        response = requests.get(self.base_url + suffix)
        print(response.status_code)
        print(response.json())

    def test_get_my_partner_goal(self):
        suffix = '/goal/get_my_partner_goal?data_id=1'
        response = requests.get(self.base_url + suffix)
        print(response.status_code)
        print(response.json())

    def test_get_my_partner_ledger(self):
        suffix = '/ledger/get_my_partner_ledger?data_id=1'
        response = requests.get(self.base_url + suffix)
        print(response.status_code)
        print(response.json())

    def test_insert_wallet(self):
        suffix = '/wallet/insert_wallet?user_id=1&wallet_name=wallet1'
        response = requests.post(self.base_url + suffix)
        print(response.status_code)
        print(response.json())

    def test_delete_wallet(self):
        suffix = '/wallet/delete_wallet?wallet_id=1'
        response = requests.delete(self.base_url + suffix)
        print(response.status_code)
        print(response.json())

    def test_update_wallet(self):
        suffix = '/wallet/update_wallet?wallet_id=2&new_wallet_name=fuckyou'
        response = requests.put(self.base_url + suffix)
        print(response.status_code)
        print(response.json())

    def test_get_wallet_all_ledger(self):
        suffix = '/ledger/get_wallet_all_ledger?wallet_id=1'
        response = requests.get(self.base_url + suffix)
        print(response.status_code)
        print(response.json())

def main():
    test = TestCase()
    test.test_get_all_wallets()
    test.test_get_all_ledgers()
    test.test_get_ledgers()
    test.test_get_all_goals()
    test.test_get_my_partner_goal()
    test.test_get_my_partner_ledger()
    test.test_insert_wallet()
    test.test_delete_wallet()
    test.test_update_wallet()
    test.test_get_wallet_all_ledger()


if __name__ == "__main__":
    main()

