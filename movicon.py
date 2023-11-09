"""
This module acts a an opcua connection to Movicon

Classes:
- IOServer: An object that represents Movicon's IOServer, you can get/set tags and alarms
"""
import opcua
from opcua.ua import NodeClass
class IOServer:
    """
    IOServer object to access tags and alarms
        Args:
            hostname (str): the hostname or IP of the Movicon server's machine
            (optional) port (int): the port of Movicon's OPC UA server, the default is 62841
        Attributes:
            hostname (str): the hostname or IP of the Movicon server's machine
            port: the port used OPC UA client to connect to Movicon's IOServer
            tags (dict): dictionary of movicon tag objects
            alarms (dict): dictionary of movicon alarm objects
    """
    def __init__(self,hostname,port=62841):
        self.hostname = hostname
        self.port = port
        self._url = f'opc.tcp://{hostname}:{port}'
        self._opcua_client = opcua.Client(self._url)
        self._root_node = None
        self._opcua_nodes = {}
        self.tags = {}
        self.alarms = {}

    def connect(self) -> bool:
        """
        Attempt to connect to the IOServer via OPC UA.
            Returns:
                bool: whether the connection attempt was succesfull
        """
        try:
            self._opcua_client.connect()
            self._root_node = self._opcua_client.get_root_node()
            self._opcua_nodes = IOServer._get_nodes(self._root_node)
        except Exception as e:
            print(f"""The OPC UA connection to you Movicon IOServer failed
             with the error: {e}\n\nPlease ensure the server is running,
             the OPC UA transport is enabled, and the port you've provided
             to IOServer() is correct""")
            return False
        return True

    def get_tags(self) -> dict:
        """
            Returns:
                dict: Tag Dictionaries
        """
        return self._opcua_nodes['Objects']
    @staticmethod
    def set_tag(tag:opcua.common.node.Node, value):
        """
            Static method to set the value of a tag. Value passed must be of same data type as tag.
                Args:
                    tag (opcua.common.node.Node): the tag in which the value is to be set 
                                                  (i.e. tags_dict['tag']['self'])
                    value (tag's datatype): the value to set the tag to
        """
        variant_type = tag.get_data_type_as_variant_type()
        try:
            tag.set_value(value,variant_type)
        except Exception as e:
            print(f"Error setting tag value: {e}\n")

    @staticmethod
    def _get_nodes(node:opcua.common.node.Node) -> dict:
        """
            Static method to retrieve all child nodes of the passed node
                Returns:
                    dict: All of the nodes as a dictionary. Folder nodes dictionaries of children.
                          Access node attributes using dict['node']['self']
        """
        nodes = {}
        for child in node.get_children():
            dname = child.get_display_name().Text
            if isinstance(child, opcua.common.node.Node):
                if child.get_node_class() == NodeClass.Variable:
                    nodes[child.get_display_name().Text] = child
                else:
                    nodes[dname] = IOServer._get_nodes(child)
            else:
                nodes[child.get_display_name().Text] = child
        return nodes
