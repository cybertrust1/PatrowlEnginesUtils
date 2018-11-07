#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This file manage tests on PatrowlEngine."""

import json
import requests
import time
import random


class PatrowlEngineTest:
    """Class definition of PatrowlEngineTest."""

    def __init__(self, engine_name, base_url):
        """Initialise a new PatrowlEngineTest."""
        self.engine_name = engine_name
        self.base_url = base_url

    def test_connectivity(self):
        """Test engine connectivity."""
        print("test-{}-connectivity".format(self.engine_name))
        try:
            r = requests.get(url="{}/".format(self.base_url))
            assert r.status_code == 200
            assert r.json()["page"] == "index"
        except AssertionError:
            print(r.json())
            assert False
        finally:
            return r.json()

    def test_status(self):
        """Test engine status."""
        print("test-{}-status".format(self.engine_name))
        r = requests.get(url="{}/status".format(self.base_url))
        try:
            assert r.status_code == 200
            assert r.json()["page"] == "status"
            assert r.json()["status"] == "READY"
        except AssertionError:
            print(r.json())
            assert False
        finally:
            return r.json()

    def test_info(self):
        """Test engine info page."""
        print("test-{}-info".format(self.engine_name))
        r = requests.get(url="{}/info".format(self.base_url))
        try:
            assert r.status_code == 200
            assert r.json()["page"] == "info"
            assert r.json()["engine_config"]["status"] == "READY"
        except AssertionError:
            print(r.json())
            assert False
        finally:
            return r.json()

    def test_reloadconfig(self):
        """Test configuration reload."""
        print("test-{}-reloadconfig".format(self.engine_name))
        r = requests.get(url="{}/reloadconfig".format(self.base_url))
        try:
            assert r.status_code == 200
            assert r.json()["config"]["status"] == "READY"
        except AssertionError:
            print(r.json())
            assert False
        finally:
            return r.json()

    def test_stopscans(self):
        """Test to stop all the scans."""
        print("test-{}-stopscans".format(self.engine_name))
        r = requests.get(url="{}/stopscans".format(self.base_url))
        try:
            assert r.status_code == 200
            assert r.json()["page"] == "stopscans"
            assert r.json()["status"] == "SUCCESS"
        except AssertionError:
            print(r.json())
            assert False
        finally:
            return r.json()

    def test_cleanscans(self):
        """Test to clean all the scans."""
        print("test-{}-cleanscans".format(self.engine_name))
        r = requests.get(url="{}/clean".format(self.base_url))
        try:
            assert r.status_code == 200
            assert r.json()["page"] == "clean"
            assert r.json()["status"] == "SUCCESS"
        except AssertionError:
            print(r.json())
            assert False
        finally:
            return r.json()

    def custom_test(self, test_name, assets, scan_policy={}, is_valid=True,
                    max_timeout=1200):
        """Start a custom test."""
        print("test-{}-custom: {}".format(self.engine_name, test_name))
        TEST_SCAN_ID = random.randint(1000000, 1999999)
        post_data = {
            "assets":  assets,
            "options": scan_policy,
            "scan_id": str(TEST_SCAN_ID)
        }

        r = requests.post(
            url="{}/startscan".format(self.base_url),
            data=json.dumps(post_data),
            headers={
                'Content-type': 'application/json',
                'Accept': 'application/json'
                })
        try:
            assert r.status_code == 200
            assert r.json()['status'] == "accepted"
        except AssertionError:
            print(r.json())
            assert False
        finally:
            return r.json()

        # Wait until scan is finished
        timeout_start = time.time()
        has_error = False
        while time.time() < timeout_start + max_timeout:
            r = requests.get(
                url="{}/status/{}".format(self.base_url, TEST_SCAN_ID))
            if r.json()["status"] == "SCANNING":
                time.sleep(3)
            else:
                if r.json()["status"] == "FINISHED":
                    assert True
                else:
                    has_error = True
                    assert False
                break

        # Get findings
        if not has_error:
            findings = {}
            r = requests.get(
                url="{}/getfindings/{}".format(self.base_url, TEST_SCAN_ID))
            try:
                assert r.json()['status'] == "success"
                findings = r.json()
            except AssertionError:
                print(r.json())
                assert False

            # Get report
            r = requests.get(
                url="{}/getreport/{}".format(self.base_url, TEST_SCAN_ID))
            try:
                # check the file name & siza !!
                assert True
                # assert r.json()['scan']['status'] == "FINISHED"
            except AssertionError:
                print(r.json())
                assert False
            finally:
                return findings
        else:
            assert False

    def do_generic_tests(self):
        """Start the generic tests."""
        self.test_connectivity()
        self.test_status()
        self.test_info()
        self.test_reloadconfig()
        self.test_stopscans()
        self.test_cleanscans()
