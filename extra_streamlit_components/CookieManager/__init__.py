import datetime
import os
from typing import Literal, Optional, Union

import streamlit.components.v1 as components
from extra_streamlit_components import IS_RELEASE

if IS_RELEASE:
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    # build_path = os.path.join(absolute_path, "frontend/build")
    # _component_func = components.declare_component("tab_bar", path=build_path)
    # for lupe streamlit purpose
    build_path = os.path.join(absolute_path, "../../lupe/css_dir")
    # build_path = os.path.join(os.getcwd(), 'build')
    # _component_func = components.declare_component("tab_bar", path=build_path)
else:
    _component_func = components.declare_component("cookie_manager", url="http://localhost:3000")


class CookieManager:
    def __init__(self, key="init"):
        self.cookie_manager = _component_func
        self.cookies = self.cookie_manager(method="getAll", key=key, default={})

    def get(self, cookie: str):
        return self.cookies.get(cookie)

    def set(
        self,
        cookie: str,
        val: Union[str, int, float, bool],
        key: str = "set",
        path: str = "/",
        expires_at: Optional[datetime.datetime] = None,
        max_age: Optional[float] = None,
        domain: Optional[str] = None,
        secure: Optional[bool] = None,
        same_site: Union[bool, None, Literal["lax", "strict"]] = "strict",
    ):
        """Sets a cookie with the given name and value.

        Args:
            cookie: The name of the cookie to set.
            val: The value of the cookie.
            key: The key to use for the component.
            path: Cookie path. Use '/' as the path if you want your cookie to be accessible on all pages.
            expires_at: Absolute expiration date for the cookie. Defaults to 1 day from now.
            max_age: Relative max age of the cookie from when the client receives it in seconds.
            domain: Domain for the cookie (sub.domain.com or .allsubdomains.com)
            secure: Is only accessible through HTTPS?
            same_site: Strict or Lax enforcement.
        """
        if cookie is None or cookie == "":
            return

        if expires_at is None:
            expires_at = datetime.datetime.now() + datetime.timedelta(days=1)

        expires = expires_at.isoformat()
        options = {
            "path": path,
            "expires": expires,
            "maxAge": max_age,
            "domain": domain,
            "secure": secure,
            "sameSite": same_site,
        }
        # Remove None's
        options = {k: v for k, v in options.items() if v is not None}
        did_add = self.cookie_manager(method="set", cookie=cookie, value=val, options=options, key=key, default=False)
        if did_add:
            self.cookies[cookie] = val

    def delete(self, cookie, key="delete"):
        if cookie is None or cookie == "":
            return
        did_add = self.cookie_manager(method="delete", cookie=cookie, key=key, default=False)
        if did_add:
            del self.cookies[cookie]

    def get_all(self, key="get_all"):
        self.cookies = self.cookie_manager(method="getAll", key=key, default={})
        return self.cookies
