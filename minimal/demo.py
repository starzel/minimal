from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five import BrowserView
from string import ascii_lowercase
from zope.interface import alsoProvides

import json
import logging
import random
import requests

logger = logging.getLogger(__name__)


class Demo(BrowserView):

    def __call__(self, amount=3, remote=False):
        self.amount = amount
        if not remote:
            self.create_jokes()
        else:
            self.create_remote_jokes()
        return self.request.response.redirect(self.context.absolute_url())

    def create_jokes(self):
        """Create some jokes locally"""
        alsoProvides(self.request, IDisableCSRFProtection)
        plone_view = api.content.get_view('plone', self.context, self.request)
        jokes = self.random_jokes()
        for data in jokes:
            joke = data['joke']
            random_id = ''.join(random.choice(ascii_lowercase) for i in range(6))
            joke = api.content.create(
                container=self.context,
                type='Document',
                title=plone_view.cropText(joke, length=40),
                id=random_id,
                description=joke,
            )
            logger.debug(f'Created joke {joke.absolute_url()}')
        api.portal.show_message(f'Created {self.amountcZ} jokes!', self.request)

    def create_remote_jokes(self, url=None):
        """Create some jokes on demo.plone.org"""
        url = url or 'https://demo.plone.org/en/demo'
        plone_view = api.content.get_view('plone', self.context, self.request)
        jokes = self.random_jokes()
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        auth = ('editor', 'editor')
        for data in jokes:
            joke = data['joke']
            payload = {
                '@type': 'Document',
                'title': plone_view.cropText(joke, length=40),
                'description': joke,
                'id': ''.join(random.choice(ascii_lowercase) for i in range(6)),
            }
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                auth=auth,
            )
            response.raise_for_status()
            logger.info(f'Created joke {response.json()["@id"]}')
        api.portal.show_message(f'Created {self.amount} jokes!', self.request)

    def random_jokes(self):
        jokes = requests.get(f'http://api.icndb.com/jokes/random/{self.amount}?escape=javascript')
        return json.loads(jokes.text)['value']
