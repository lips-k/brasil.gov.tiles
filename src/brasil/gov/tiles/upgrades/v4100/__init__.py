# -*- coding: utf-8 -*-
from brasil.gov.tiles.logger import logger
from brasil.gov.tiles.upgrades import add_tile
from brasil.gov.tiles.upgrades import get_valid_objects
from brasil.gov.tiles.upgrades import replace_attribute
from brasil.gov.tiles.upgrades import replace_tile
from plone import api

import json


RESOURCES_TO_UPDATE = {
    '++resource++brasil.gov.tiles/tiles.css': '++resource++brasil.gov.tiles/brasilgovtiles.css',
    '++resource++brasil.gov.tiles/swiper.min.css': '++resource++brasil.gov.tiles/vendor/swiper.min.css',
    '++resource++brasil.gov.tiles/tiles.js': '++resource++brasil.gov.tiles/brasilgovtiles.js',
    '++resource++brasil.gov.tiles/jquery.cycle2.carousel.js': '++resource++brasil.gov.tiles/vendor/jquery.cycle2.carousel.js',
    '++resource++brasil.gov.tiles/jquery.cycle2.js': '++resource++brasil.gov.tiles/vendor/jquery.cycle2.js',
    '++resource++brasil.gov.tiles/jquery.jplayer.min.js': '++resource++brasil.gov.tiles/vendor/jquery.jplayer.min.js',
    '++resource++brasil.gov.tiles/swiper.min.js': '++resource++brasil.gov.tiles/vendor/swiper.min.js',
}


def _rename_resources(tool, from_to):
    for id_ in tool.getResourceIds():
        if id_ in from_to:
            tool.renameResource(id_, from_to[id_])


def update_static_resources(setup_tool):
    """Fix resource references after static files reorganization."""
    css_tool = api.portal.get_tool('portal_css')
    _rename_resources(css_tool, RESOURCES_TO_UPDATE)
    logger.info('CSS resources were updated')

    js_tool = api.portal.get_tool('portal_javascripts')
    _rename_resources(js_tool, RESOURCES_TO_UPDATE)
    logger.info('JavaScript resources were updated')


DEPRECATED_TILES = [u'nitf']


def remove_deprecated_tiles(setup_tool):
    """Remove deprecated tiles."""
    from brasil.gov.tiles.utils import disable_tile
    for tile in DEPRECATED_TILES:
        disable_tile(tile)


def add_quote_tile(setup_tool):
    """Add Quote tile."""
    add_tile(u'brasil.gov.tiles.quote')


def add_potd_tile(setup_tool):
    """Add Photo of the Day tile."""
    add_tile(u'brasil.gov.tiles.potd')


def add_photogallery_tile(setup_tool):
    """Add Photo Gallery tile."""
    add_tile(u'brasil.gov.tiles.photogallery')


def add_navigation_tile(setup_tool):
    """Add Navigation tile."""
    add_tile(u'brasil.gov.tiles.navigation')


def replace_nitf_tile(setup_tool):
    """Replace NITF tile."""
    tile = u'collective.nitf'
    add_tile(tile)

    logger.info('Replacing NITF tile on collective.cover objects')
    for obj in get_valid_objects(portal_type='collective.cover.content'):
        try:
            layout = json.loads(obj.cover_layout)
        except TypeError:
            continue  # empty layout?

        layout = replace_tile(layout, 'nitf', tile)
        obj.cover_layout = json.dumps(layout)

        replace_attribute(obj, tile, 'image_description', 'alt_text')

    logger.info('Done')


def update_banner_tile(setup_tool):
    """Update Banner tile."""
    tile = u'collective.cover.banner'

    logger.info('Updating NITF tile on collective.cover objects')
    for obj in get_valid_objects(portal_type='collective.cover.content'):
        replace_attribute(obj, tile, 'image_description', 'alt_text')

    logger.info('Done')