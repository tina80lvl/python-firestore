# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple

from google.api_core import grpc_helpers_async  # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.firestore_admin_v1.types import field
from google.cloud.firestore_admin_v1.types import firestore_admin
from google.cloud.firestore_admin_v1.types import index
from google.longrunning import operations_pb2 as operations  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore

from .base import FirestoreAdminTransport
from .grpc import FirestoreAdminGrpcTransport


class FirestoreAdminGrpcAsyncIOTransport(FirestoreAdminTransport):
    """gRPC AsyncIO backend transport for FirestoreAdmin.

    Operations are created by service ``FirestoreAdmin``, but are
    accessed via service ``google.longrunning.Operations``.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "firestore.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        **kwargs
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            address (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """
        scopes = scopes or cls.AUTH_SCOPES
        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            **kwargs
        )

    def __init__(
        self,
        *,
        host: str = "firestore.googleapis.com",
        credentials: credentials.Credentials = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: aio.Channel = None,
        api_mtls_endpoint: str = None,
        client_cert_source: Callable[[], Tuple[bytes, bytes]] = None
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): The mutual TLS endpoint. If
                provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]): A
                callback to provide client SSL certificate bytes and private key
                bytes, both in PEM format. It is ignored if ``api_mtls_endpoint``
                is None.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
        elif api_mtls_endpoint:
            host = (
                api_mtls_endpoint
                if ":" in api_mtls_endpoint
                else api_mtls_endpoint + ":443"
            )

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = type(self).create_channel(
                host,
                credentials=credentials,
                credentials_file=credentials_file,
                ssl_credentials=ssl_credentials,
                scopes=scopes or self.AUTH_SCOPES,
            )

        # Run the base constructor.
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes or self.AUTH_SCOPES,
        )

        self._stubs = {}

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, "_grpc_channel"):
            self._grpc_channel = self.create_channel(
                self._host, credentials=self._credentials,
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsAsyncClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Sanity check: Only create a new client if we do not already have one.
        if "operations_client" not in self.__dict__:
            self.__dict__["operations_client"] = operations_v1.OperationsAsyncClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self.__dict__["operations_client"]

    @property
    def create_index(
        self,
    ) -> Callable[
        [firestore_admin.CreateIndexRequest], Awaitable[operations.Operation]
    ]:
        r"""Return a callable for the create index method over gRPC.

        Creates a composite index. This returns a
        [google.longrunning.Operation][google.longrunning.Operation]
        which may be used to track the status of the creation. The
        metadata for the operation will be the type
        [IndexOperationMetadata][google.firestore.admin.v1.IndexOperationMetadata].

        Returns:
            Callable[[~.CreateIndexRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_index" not in self._stubs:
            self._stubs["create_index"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/CreateIndex",
                request_serializer=firestore_admin.CreateIndexRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["create_index"]

    @property
    def list_indexes(
        self,
    ) -> Callable[
        [firestore_admin.ListIndexesRequest],
        Awaitable[firestore_admin.ListIndexesResponse],
    ]:
        r"""Return a callable for the list indexes method over gRPC.

        Lists composite indexes.

        Returns:
            Callable[[~.ListIndexesRequest],
                    Awaitable[~.ListIndexesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_indexes" not in self._stubs:
            self._stubs["list_indexes"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/ListIndexes",
                request_serializer=firestore_admin.ListIndexesRequest.serialize,
                response_deserializer=firestore_admin.ListIndexesResponse.deserialize,
            )
        return self._stubs["list_indexes"]

    @property
    def get_index(
        self,
    ) -> Callable[[firestore_admin.GetIndexRequest], Awaitable[index.Index]]:
        r"""Return a callable for the get index method over gRPC.

        Gets a composite index.

        Returns:
            Callable[[~.GetIndexRequest],
                    Awaitable[~.Index]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_index" not in self._stubs:
            self._stubs["get_index"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/GetIndex",
                request_serializer=firestore_admin.GetIndexRequest.serialize,
                response_deserializer=index.Index.deserialize,
            )
        return self._stubs["get_index"]

    @property
    def delete_index(
        self,
    ) -> Callable[[firestore_admin.DeleteIndexRequest], Awaitable[empty.Empty]]:
        r"""Return a callable for the delete index method over gRPC.

        Deletes a composite index.

        Returns:
            Callable[[~.DeleteIndexRequest],
                    Awaitable[~.Empty]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_index" not in self._stubs:
            self._stubs["delete_index"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/DeleteIndex",
                request_serializer=firestore_admin.DeleteIndexRequest.serialize,
                response_deserializer=empty.Empty.FromString,
            )
        return self._stubs["delete_index"]

    @property
    def get_field(
        self,
    ) -> Callable[[firestore_admin.GetFieldRequest], Awaitable[field.Field]]:
        r"""Return a callable for the get field method over gRPC.

        Gets the metadata and configuration for a Field.

        Returns:
            Callable[[~.GetFieldRequest],
                    Awaitable[~.Field]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_field" not in self._stubs:
            self._stubs["get_field"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/GetField",
                request_serializer=firestore_admin.GetFieldRequest.serialize,
                response_deserializer=field.Field.deserialize,
            )
        return self._stubs["get_field"]

    @property
    def update_field(
        self,
    ) -> Callable[
        [firestore_admin.UpdateFieldRequest], Awaitable[operations.Operation]
    ]:
        r"""Return a callable for the update field method over gRPC.

        Updates a field configuration. Currently, field updates apply
        only to single field index configuration. However, calls to
        [FirestoreAdmin.UpdateField][google.firestore.admin.v1.FirestoreAdmin.UpdateField]
        should provide a field mask to avoid changing any configuration
        that the caller isn't aware of. The field mask should be
        specified as: ``{ paths: "index_config" }``.

        This call returns a
        [google.longrunning.Operation][google.longrunning.Operation]
        which may be used to track the status of the field update. The
        metadata for the operation will be the type
        [FieldOperationMetadata][google.firestore.admin.v1.FieldOperationMetadata].

        To configure the default field settings for the database, use
        the special ``Field`` with resource name:
        ``projects/{project_id}/databases/{database_id}/collectionGroups/__default__/fields/*``.

        Returns:
            Callable[[~.UpdateFieldRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "update_field" not in self._stubs:
            self._stubs["update_field"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/UpdateField",
                request_serializer=firestore_admin.UpdateFieldRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["update_field"]

    @property
    def list_fields(
        self,
    ) -> Callable[
        [firestore_admin.ListFieldsRequest],
        Awaitable[firestore_admin.ListFieldsResponse],
    ]:
        r"""Return a callable for the list fields method over gRPC.

        Lists the field configuration and metadata for this database.

        Currently,
        [FirestoreAdmin.ListFields][google.firestore.admin.v1.FirestoreAdmin.ListFields]
        only supports listing fields that have been explicitly
        overridden. To issue this query, call
        [FirestoreAdmin.ListFields][google.firestore.admin.v1.FirestoreAdmin.ListFields]
        with the filter set to ``indexConfig.usesAncestorConfig:false``.

        Returns:
            Callable[[~.ListFieldsRequest],
                    Awaitable[~.ListFieldsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_fields" not in self._stubs:
            self._stubs["list_fields"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/ListFields",
                request_serializer=firestore_admin.ListFieldsRequest.serialize,
                response_deserializer=firestore_admin.ListFieldsResponse.deserialize,
            )
        return self._stubs["list_fields"]

    @property
    def export_documents(
        self,
    ) -> Callable[
        [firestore_admin.ExportDocumentsRequest], Awaitable[operations.Operation]
    ]:
        r"""Return a callable for the export documents method over gRPC.

        Exports a copy of all or a subset of documents from
        Google Cloud Firestore to another storage system, such
        as Google Cloud Storage. Recent updates to documents may
        not be reflected in the export. The export occurs in the
        background and its progress can be monitored and managed
        via the Operation resource that is created. The output
        of an export may only be used once the associated
        operation is done. If an export operation is cancelled
        before completion it may leave partial data behind in
        Google Cloud Storage.

        Returns:
            Callable[[~.ExportDocumentsRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "export_documents" not in self._stubs:
            self._stubs["export_documents"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/ExportDocuments",
                request_serializer=firestore_admin.ExportDocumentsRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["export_documents"]

    @property
    def import_documents(
        self,
    ) -> Callable[
        [firestore_admin.ImportDocumentsRequest], Awaitable[operations.Operation]
    ]:
        r"""Return a callable for the import documents method over gRPC.

        Imports documents into Google Cloud Firestore.
        Existing documents with the same name are overwritten.
        The import occurs in the background and its progress can
        be monitored and managed via the Operation resource that
        is created. If an ImportDocuments operation is
        cancelled, it is possible that a subset of the data has
        already been imported to Cloud Firestore.

        Returns:
            Callable[[~.ImportDocumentsRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "import_documents" not in self._stubs:
            self._stubs["import_documents"] = self.grpc_channel.unary_unary(
                "/google.firestore.admin.v1.FirestoreAdmin/ImportDocuments",
                request_serializer=firestore_admin.ImportDocumentsRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs["import_documents"]


__all__ = ("FirestoreAdminGrpcAsyncIOTransport",)
