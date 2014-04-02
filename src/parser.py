#!/usr/bin/python

"""Author: Enfeng Huang @ NYU Polytechnic School of Engineering, 2014-02
Html file parser"""

from sgmllib import SGMLParser
import urlparse
import re
import debug


class Parser(SGMLParser):
	def reset(self):
		SGMLParser.reset(self)
		self.base_url = ""
		self.urls = []
		self.redirect = ""
		self.redirect_reg = re.compile(r'.*[uU][rR][lL]\s*=\s*(.+)')

	def start_base(self, attrs):
		"""Deal with 'base' tag"""
		for k, v in attrs:
			if k == 'href':
				#print "Find <base>: %s" % v
				self.base_url = v
				return

	def start_a(self, attrs):
		"""Deal with 'a' tag"""
		href = [v for k, v in attrs if k == 'href']
		if href:
			self.urls.extend(href)

	def start_frame(self, attrs):
		"""Deal with 'frame' tag"""
		src = [v for (k, v) in attrs if k == 'src']
		if src:
			self.urls.extend(src)

	def start_meta(self, attrs):
		"""Deal with 'meta' tag"""
		for (k, v) in attrs:
			if k == 'content':
				s = self.redirect_reg.search(v)
				if (s is not None) and (self.redirect is ""):
					self.redirect = s.group(1)
					#print "Redirection on META tag is found: %s" % self.redirect

	def start_area(self, attrs):
		"""Deal with 'area' tag"""
		href = [v for k, v in attrs if k == 'href']
		if href:
			self.urls.extend(href)


	def summary(self, data, search_terms):
		term_cnt = {}
		for t in search_terms:
			idx = [i.start() for i in re.finditer(t, data)]
			if len(idx) > 0:
				if t not in term_cnt:
					term_cnt[t] = 0
				term_cnt[t] += len(idx)		

		score = 0.0
		terms = []
		for (k, v) in term_cnt.iteritems():
			terms.append(k)
			score += v
		score *= len(terms)
		if len(self.urls) > 0:
			score /= len(self.urls)
		return {"score": score, "terms": terms, "urls": self.urls}


def parse(url, page, search_terms):
	"""Get all the URLs in a page"""
	urls = []
	redirect = ""
	ret = None

	try:
		parser = Parser()
		parser.feed(page)
		parser.close()
		ret = parser.summary(page, search_terms)
	except Exception as e:
		print url
		debug.print_info()
		print e
		return None
	else:
		base = url
		if parser.base_url != "":
			base = parser.base_url

		redirect = urlparse.urljoin(base, parser.redirect)
		urls.append(redirect)
		for u in parser.urls:
			urls.append(urlparse.urljoin(base, u))
		ret["urls"] = urls
		return ret





