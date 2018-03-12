# -*- coding: utf-8 -*-
from brasil.gov.tiles import _ as _
from brasil.gov.tiles.tiles.list import IListTile
from brasil.gov.tiles.tiles.list import ListTile
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from plone import api
from plone.autoform import directives as form
from plone.memoize import view
from plone.namedfile.field import NamedBlobImage as NamedImage
from plone.tiles.interfaces import ITileDataManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.interface import implementer


class ISlideSwiperTile(IListTile):
    """
    Interface for Slide Swiper
    """

    form.omitted('header')
    form.no_omit(IDefaultConfigureForm, 'header')
    header = schema.TextLine(
        title=_(u'Header'),
        required=False,
        readonly=True,
    )

    form.omitted('title')
    form.no_omit(IDefaultConfigureForm, 'title')
    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
        readonly=True,
    )

    form.omitted('description')
    form.no_omit(IDefaultConfigureForm, 'description')
    description = schema.Text(
        title=_(u'Description'),
        required=False,
        readonly=True,
    )

    form.omitted('date')
    form.no_omit(IDefaultConfigureForm, 'date')
    date = schema.Datetime(
        title=_(u'Date'),
        required=False,
        readonly=True,
    )

    form.omitted('image')
    form.no_omit(IDefaultConfigureForm, 'image')
    image = NamedImage(
        title=_(u'Image'),
        required=False,
        readonly=True,
    )

    form.omitted('uuids')
    form.no_omit(IDefaultConfigureForm, 'uuids')
    uuids = schema.List(
        title=_(u'Elements'),
        value_type=schema.TextLine(),
        required=False,
        readonly=True,
    )


@implementer(ISlideSwiperTile)
class SlideSwiperTile(ListTile):

    index = ViewPageTemplateFile('templates/slide_swiper.pt')
    is_configurable = False
    is_editable = True

    def populate_with_object(self, obj):
        super(BannerRotativoTile, self).populate_with_object(
            obj)  # check permission
        if not self._has_image_field(obj):
            return
        self.set_limit()
        uuid = api.content.get_uuid(obj)
        title = obj.Title()
        description = obj.Description()
        rights = obj.Rights()
        data_mgr = ITileDataManager(self)
        old_data = data_mgr.get()
        if data_mgr.get()['uuids']:
            uuids = data_mgr.get()['uuids']
            if type(uuids) != list:
                uuids = [uuid]
            elif uuid not in uuids:
                uuids.append(uuid)

            old_data['uuids'] = uuids[:self.limit]
        else:
            old_data['uuids'] = [uuid]
        old_data['title'] = title
        old_data['description'] = description
        old_data['rights'] = rights
        data_mgr.set(old_data)

    # FIXME: Usado para que o método em collective.cover 1.1b1 chame o
    # corretamente o método enquanto não herdamos diretamente do List do cover.
    # Utilizado principalmente quando muda a ordem de um item no banner rotativo.
    def replace_with_uuids(self, uuids):
        """Usado enquanto não herda do List do collective.cover."""
        super(BannerRotativoTile, self).replace_with_uuids(uuids)

    def thumbnail(self, item):
        """Return a thumbnail of an image if the item has an image field and
        the field is visible in the tile.

        :param item: [required]
        :type item: content object
        """
        if self._has_image_field(item):
            scales = item.restrictedTraverse('@@images')
            return scales.scale('image', width=750, height=423)

    @view.memoize
    def accepted_ct(self):
        results = ListTile.accepted_ct(self)
        results.append(u'ExternalContent')
        return results
