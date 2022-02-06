"""Data models for the reporting framework."""
from dataclasses import field
from enum import Enum
import os
import re
import typing
import unicodedata
from uuid import uuid4

from marshmallow import post_load
from marshmallow_dataclass import dataclass

from ..jobs.models import Job


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)

    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD',
                                      value).encode('ascii',
                                                    'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())

    return re.sub(r'[-\s]+', '-', value).strip('-_')


class OutputFormat(Enum):
    """Formats for output reports."""
    PDF = 'pdf'
    IMAGE = 'image'

    def __str__(self):
        # For marshmallow to serialize the value
        return self.value


@dataclass
class ReportOutputOptions:
    """
    Settings for generating output reports.
    In the templates.json file, for:
        - PDF output: specify "output_format":"PDF"
        - Image output: specify "output_format":"IMAGE" and
            "format_params":{
                "image_type":"jpg" or "jpeg" or "png" or "bmp"
         }
    Please note that the output_format should be in uppercase.
    """
    output_format: OutputFormat = field(default=OutputFormat.PDF)
    include_qpt: bool = field(default=True)
    format_params: dict = field(default_factory=dict)

    def file_extension(self) -> str:
        """
        If output format is IMAGE and its type is not defined, it will
        default to PNG.
        """
        if self.output_format == OutputFormat.PDF:
            return 'pdf'
        else:
            img_type = self.format_params.get('image_type', 'PNG')
            return img_type.lower()


class LayoutItemType(Enum):
    """Types of layout items."""
    MAP = 'map'
    LABEL = 'label'
    PICTURE = 'picture'

    def __str__(self):
        # For marshmallow to serialize the value
        return self.value


@dataclass
class ItemScopeMapping:
    """Provides a simple mechanism for grouping layout items based on a
    scope, which in most cases refers to an algorithm. This is especially
    useful when a layout contains items linked to different algorithms where
    it becomes important to define how values for each item will be fetched
    from which scope/algorithm.
    """
    # Corresponds to algorithm name
    name: str
    type_id_mapping: typing.Dict[str, list] = field(default_factory=dict)

    def __init__(self, name: str, **kwargs) -> None:
        self.name = name
        self.type_id_mapping = kwargs.pop('type_id_mapping', dict())

    def add_item_mapping(
            self,
            item_type: str,
            item_id: str
    ) -> None:
        """Group item ids in a list based on their type."""
        str_item_type = str(item_type)
        if not str_item_type in self.type_id_mapping:
            self.type_id_mapping[str_item_type] = []

        items = self.type_id_mapping[str_item_type]
        items.append(item_id)

    def add_map(self, item_id: str) -> None:
        # Add map_id to the collection
        self.add_item_mapping(LayoutItemType.MAP, item_id)

    def add_label(self, item_id: str) -> None:
        # Add label to the collection
        self.add_item_mapping(LayoutItemType.LABEL, item_id)

    def add_picture(self, item_id: str) -> None:
        # Add picture item id to the collection
        self.add_item_mapping(LayoutItemType.PICTURE, item_id)

    def item_ids_by_type(self, item_type: str) -> list:
        """Get collection of item_ids based on the layout type."""
        str_item_type = str(item_type)
        if str_item_type in self.type_id_mapping:
            return self.type_id_mapping[str_item_type]

        return []

    def map_ids(self) -> list:
        """Map ids defined for the current scope."""
        return self.item_ids_by_type(LayoutItemType.MAP)

    def label_ids(self) -> list:
        """Label ids defined for the current scope."""
        return self.item_ids_by_type(LayoutItemType.LABEL)

    def picture_ids(self) -> list:
        """Picture ids defined for the current scope."""
        return self.item_ids_by_type(LayoutItemType.PICTURE)


@dataclass
class ReportTemplateInfo:
    """Contains information about the QGIS layout associated with one or more
    algorithm scopes.
    """
    id: typing.Optional[str]
    name: typing.Optional[str]
    description: typing.Optional[str]
    portrait_path: typing.Optional[str]
    landscape_path: typing.Optional[str]
    item_scopes: typing.List[ItemScopeMapping] = field(default_factory=list)

    def __init__(self, **kwargs) -> None:
        self.id = kwargs.pop('id', str(uuid4()))
        self.name = kwargs.pop('name', '')
        self.description = kwargs.pop('description', '')
        self.portrait_path = kwargs.pop('portrait_path', '')
        self.landscape_path = kwargs.pop('landscape_path', '')
        self.item_scopes = kwargs.pop('item_scopes', list())
        self._abs_portrait_path = ''
        self._abs_landscape_path = ''

    def add_scope_mapping(self, item_scope: ItemScopeMapping) -> None:
        self.item_scopes.append(item_scope)

    def scope_mappings_by_name(
            self,
            name: str
    ) -> typing.List[ItemScopeMapping]:
        return [sm for sm in self.item_scopes if sm.name == name]

    def update_paths(self, templates_dir) -> None:
        # set absolute paths for portrait and landscape templates
        concat_path = lambda file_name: os.path.normpath(
            f'{templates_dir}{os.sep}{file_name}'
        )
        self._abs_portrait_path = concat_path(self.portrait_path)
        self._abs_landscape_path = concat_path(self.landscape_path)

    @property
    def absolute_template_paths(self) -> typing.Tuple[str, str]:
        """Absolute paths for portrait and landscape templates."""
        return self._abs_portrait_path, self._abs_landscape_path

    @property
    def is_multi_scope(self) -> bool:
        """True if the template is for compound reports."""
        return True if len(self.item_scopes) > 1 else False

    def contains_scope(self, name: str) -> bool:
        """
        True if the template contains a scope mapping with the given name.
        """
        return True if len(self.scope_mappings_by_name(name)) > 0 else False


@dataclass
class ReportConfiguration:
    """Contains template and output settings for a report.
    """
    template_info: typing.Optional[ReportTemplateInfo]
    output_options: typing.Optional[ReportOutputOptions]

    class Meta:
        ordered = True

    def __init__(
            self,
            template_info: ReportTemplateInfo,
            output_options: ReportOutputOptions
    ) -> None:
        self.template_info = template_info
        self.output_options = output_options

    def update_paths(self, template_dir):
        # Convenience function for updating absolute paths for template files.
        self.template_info.update_paths(template_dir)


@dataclass
class ReportTaskContext:
    """
    Provides context information for generating reports.
    """
    report_configuration: ReportConfiguration
    output_paths: typing.Tuple[str, str]
    jobs: typing.List[Job] = field(default_factory=list)

    def __init__(
            self,
            report_configuration: ReportConfiguration,
            output_paths: typing.Tuple[str, str],
            jobs: typing.List[Job]
    ):
        self.report_configuration = report_configuration
        # (report_path, template_path)
        self.output_paths = output_paths
        self.jobs = jobs




