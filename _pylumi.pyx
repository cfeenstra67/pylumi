import json

from cpython.string cimport PyString_AsString
from libc.stdlib cimport malloc, free
from libc.string cimport strcpy


cdef extern from "libpylumigo.h":

    ctypedef signed char GoInt8
    ctypedef unsigned char GoUint8
    ctypedef short GoInt16
    ctypedef unsigned short GoUint16
    ctypedef int GoInt32
    ctypedef unsigned int GoUint32
    ctypedef long long GoInt64
    ctypedef unsigned long long GoUint64
    ctypedef GoInt64 GoInt
    ctypedef GoUint64 GoUint
    ctypedef float GoFloat32
    ctypedef double GoFloat64

    struct ContextSetup_return:
        GoInt r0
        char* r1

    ContextSetup_return ContextSetup(char* name, char* cwd) nogil

    struct ContextTeardown_return:
        GoInt r0
        char* r1

    ContextTeardown_return ContextTeardown(char* name) nogil

    struct ContextListPlugins_return:
        GoInt r0
        char** r1
        GoInt r2
        char* r3

    ContextListPlugins_return ContextListPlugins(char* name) nogil

    struct ProviderTeardown_return:
        GoInt r0
        char* r1

    ProviderTeardown_return ProviderTeardown(char* ctx, char* provider) nogil

    struct ProviderGetSchema_return:
        GoInt r0
        char* r1
        char* r2

    ProviderGetSchema_return ProviderGetSchema(char* ctxName, char* name, GoInt version) nogil

    struct ProviderCheckConfig_return:
        GoInt r0
        char* r1
        char* r2
        char* r3

    ProviderCheckConfig_return ProviderCheckConfig(char* ctx, char* provider, char* urn, char* olds, char* news, GoUint8 allowUnknowns) nogil

    struct ProviderDiffConfig_return:
        GoInt r0
        char* r1
        char* r2

    ProviderDiffConfig_return ProviderDiffConfig(char* ctx, char* provider, char* urn, char* olds, char* news, GoUint8 allowUnknowns, char** ignoreChanges, GoInt nIgnoreChanges) nogil

    struct ProviderConfigure_return:
        GoInt r0
        char* r1

    ProviderConfigure_return ProviderConfigure(char* ctx, char* provider, char* inputs) nogil

    struct ProviderCheck_return:
        GoInt r0
        char* r1
        char* r2
        char* r3

    ProviderCheck_return ProviderCheck(char* ctx, char* provider, char* urn, char* olds, char* news, GoUint8 allowUnknowns) nogil

    struct ProviderDiff_return:
        GoInt r0
        char* r1
        char* r2

    ProviderDiff_return ProviderDiff(char* ctx, char* provider, char* urn, char* id, char* olds, char* news, GoUint8 allowUnknowns, char** ignoreChanges, GoInt nIgnoreChanges) nogil

    struct ProviderCreate_return:
        GoInt r0
        char* r1
        char* r2

    ProviderCreate_return ProviderCreate(char* ctx, char* provider, char* urn, char* news, GoFloat64 timeout, GoUint8 preview) nogil

    struct ProviderRead_return:
        GoInt r0
        char* r1
        char* r2

    ProviderRead_return ProviderRead(char* ctx, char* provider, char* urn, char* id, char* inputs, char* state) nogil

    struct ProviderUpdate_return:
        GoInt r0
        char* r1
        char* r2

    ProviderUpdate_return ProviderUpdate(char* ctx, char* provider, char* urn, char* id, char* olds, char* news, GoFloat64 timeout, char** ignoreChanges, GoInt nIgnoreChanges, GoUint8 preview) nogil

    struct ProviderDelete_return:
        GoInt r0
        GoInt r1
        char* r2

    ProviderDelete_return ProviderDelete(char* ctx, char* provider, char* urn, char* id, char* news, GoFloat64 timeout) nogil

    ctypedef struct Unknowns:
        char* Key
        char* BoolValue
        char* NumberValue
        char* StringValue
        char* ArrayValue
        char* AssetValue
        char* ArchiveValue
        char* ObjectValue

    Unknowns GetUnknowns() nogil

    ctypedef struct DiffKinds:
        int DiffAdd
        int DiffAddReplace
        int DiffDelete
        int DiffDeleteReplace
        int DiffUpdate
        int DiffUpdateReplace

    DiffKinds GetDiffKinds() nogil


# Helper functions
cdef bytes _bytes(s):
    """
    Coerce text input to bytes
    """
    if type(s) is bytes:
        return s
    if isinstance(s, str):
        return s.encode()
    raise TypeError(f'Invalid bytes value: {s}.')


cdef str _str(s):
    """
    Coerce text input to bytes
    """
    if isinstance(s, str):
        return s
    if isinstance(s, bytes):
        return s.decode()
    raise TypeError(f'Invalid str value: {s}.')


cdef char* _cstr(s):
    """
    Coerce text or bytes to a c string. This must be freed by the caller.
    """
    cdef char* c_string = <char*> malloc((len(s) + 1) * sizeof(char))
    if not c_string:
        raise MemoryError()
    strcpy(c_string, _bytes(s))
    return c_string


cdef char ** to_cstring_array(list_str):
    cdef char **ret = <char **>malloc(len(list_str) * sizeof(char *))
    for i in xrange(len(list_str)):
        as_bytes = list_str[i].encode()
        ret[i] = as_bytes
    return ret

# Globals

cdef Unknowns UNKNOWNS_C = GetUnknowns()

UNKNOWN_KEY = _str(UNKNOWNS_C.Key)

UNKNOWN_BOOL_VALUE = _str(UNKNOWNS_C.BoolValue)

UNKNOWN_NUMBER_VALUE = _str(UNKNOWNS_C.NumberValue)

UNKNOWN_STRING_VALUE = _str(UNKNOWNS_C.StringValue)

UNKNOWN_ARRAY_VALUE = _str(UNKNOWNS_C.ArrayValue)

UNKNOWN_ASSET_VALUE = _str(UNKNOWNS_C.AssetValue)

UNKNOWN_ARCHIVE_VALUE = _str(UNKNOWNS_C.ArchiveValue)

UNKNOWN_OBJECT_VALUE = _str(UNKNOWNS_C.ObjectValue)

cdef DiffKinds DIFF_KINDS_C = GetDiffKinds()

DIFF_ADD = DIFF_KINDS_C.DiffAdd

DIFF_ADD_REPLACE = DIFF_KINDS_C.DiffAddReplace

DIFF_DELETE = DIFF_KINDS_C.DiffDelete

DIFF_DELETE_REPLACE = DIFF_KINDS_C.DiffDeleteReplace

DIFF_UPDATE = DIFF_KINDS_C.DiffUpdate

DIFF_UPDATE_REPLACE = DIFF_KINDS_C.DiffUpdateReplace

# Context methods

def context_setup(str ctxName, str cwd):
    cdef char* ctx_name_c = _cstr(ctxName)
    cdef char* cwd_c = _cstr(cwd)
    with nogil:
        res = ContextSetup(ctx_name_c, cwd_c)
    free(ctx_name_c)
    free(cwd_c)
    if res.r0 == 0:
        return None
    raise ContextError(res.r0, _str(res.r1))


def context_teardown(str ctxName):
    cdef char* ctx_name_c = _cstr(ctxName)
    with nogil:
        res = ContextTeardown(ctx_name_c)
    free(ctx_name_c)
    if res.r0 == 0:
        return None
    raise ContextError(res.r0, _str(res.r1))


def context_list_plugins(str ctxName):
    cdef char* ctx_name_c = _cstr(ctxName)
    with nogil:
        res = ContextListPlugins(ctx_name_c)
    free(ctx_name_c)
    if res.r0 == 0:
        return [x.decode() for x in res.r1[:res.r2]]
    raise ContextError(res.r0, _str(res.r3))


# Provider methods

def provider_teardown(str ctx, str provider):
    cdef char* ctx_c = _cstr(ctx)
    cdef char* provider_c = _cstr(provider)
    with nogil:
        res = ProviderTeardown(ctx_c, provider_c)
    free(ctx_c)
    free(provider_c)
    if res.r0 == 0:
        return None
    raise ProviderError(res.r0, _str(res.r1))


def provider_get_schema(str ctxName, str name, int version=0):
    cdef char* ctx_c = _cstr(ctxName)
    cdef char* provider_c = _cstr(name)
    with nogil:
        res = ProviderGetSchema(ctx_c, provider_c, version)
    free(ctx_c)
    free(provider_c)
    if res.r0 == 0:
        return res.r1
    raise ProviderError(res.r0, _str(res.r2))


def provider_check_config(str ctx, str provider, str urn, olds, news, bint allow_unknowns=False):
    cdef char* olds_encoded = _cstr(json.dumps(olds).encode())
    cdef char* news_encoded = _cstr(json.dumps(news).encode())
    cdef char* ctx_c = _cstr(ctx)
    cdef char* provider_c = _cstr(provider)
    cdef char* urn_c = _cstr(urn)
    with nogil:
        res = ProviderCheckConfig(
            ctx_c, provider_c,  urn_c,
            olds_encoded, news_encoded, allow_unknowns
        )
    free(ctx_c)
    free(provider_c)
    free(olds_encoded)
    free(news_encoded)
    free(urn_c)
    if res.r0 == 0:
        props_decoded = json.loads(_bytes(res.r1))
        failures_decoded = json.loads(_bytes(res.r2))
        return props_decoded, failures_decoded
    raise ProviderError(res.r0, _str(res.r3))


def provider_diff_config(str ctx, str provider, str urn, olds, news, bint allow_unknowns=False, ignore_changes=()):
    cdef char* olds_encoded = _cstr(json.dumps(olds).encode())
    cdef char* news_encoded = _cstr(json.dumps(news).encode())
    cdef char* ctx_c = _cstr(ctx)
    cdef char* provider_c = _cstr(provider)
    cdef char* urn_c = _cstr(urn)
    cdef char** ignore_changes_c = to_cstring_array(ignore_changes)
    cdef int ignore_changes_len_c = len(ignore_changes)
    with nogil:
        res = ProviderDiffConfig(
            ctx_c, provider_c, urn_c,
            olds_encoded, news_encoded,
            allow_unknowns, ignore_changes_c, ignore_changes_len_c
        )
    free(ctx_c)
    free(provider_c)
    free(olds_encoded)
    free(news_encoded)
    free(urn_c)
    free(ignore_changes_c)
    if res.r0 == 0:
        out_decoded = json.loads(_bytes(res.r1))
        return out_decoded
    raise ProviderError(res.r0, _str(res.r2))


def provider_configure(str ctx, str provider, inputs):
    cdef char* ctx_c = _cstr(ctx)
    cdef char* provider_c = _cstr(provider)
    cdef char* inputs_encoded = _cstr(json.dumps(inputs).encode())
    with nogil:
        res = ProviderConfigure(ctx_c, provider_c, inputs_encoded)
    free(ctx_c)
    free(provider_c)
    free(inputs_encoded)
    if res.r0 == 0:
        return None
    raise ProviderError(res.r0, _str(res.r1))


def provider_check(str ctx, str provider, str urn, olds, news, bint allow_unknowns=False):
    cdef char* olds_encoded = _cstr(json.dumps(olds).encode())
    cdef char* news_encoded = _cstr(json.dumps(news).encode())
    cdef char* ctx_c = _cstr(ctx)
    cdef char* provider_c = _cstr(provider)
    cdef char* urn_c = _cstr(urn)
    with nogil:
        res = ProviderCheck(
            ctx_c, provider_c, urn_c,
            olds_encoded, news_encoded, allow_unknowns
        )

    free(ctx_c)
    free(provider_c)
    free(olds_encoded)
    free(news_encoded)
    free(urn_c)

    if res.r0 == 0:
        props = json.loads(_bytes(res.r1))
        failures = json.loads(_bytes(res.r2))
        return props, failures
    raise ProviderError(res.r0, _str(res.r3))


def provider_diff(str ctx, str provider, str urn, str id, olds, news, bint allow_unknowns=False, ignore_changes=()):
    cdef char* olds_encoded = _cstr(json.dumps(olds).encode())
    cdef char* news_encoded = _cstr(json.dumps(news).encode())
    cdef char* ctx_c = _cstr(ctx)
    cdef char* provider_c = _cstr(provider)
    cdef char* urn_c = _cstr(urn)
    cdef char* id_c = _cstr(id)
    cdef char** ignore_changes_c = to_cstring_array(ignore_changes)
    cdef int ignore_changes_len_c = len(ignore_changes)
    with nogil:
        res = ProviderDiff(
            ctx_c, provider_c, urn_c, id_c,
            olds_encoded, news_encoded,
            allow_unknowns, ignore_changes_c, ignore_changes_len_c
        )

    free(ctx_c)
    free(provider_c)
    free(olds_encoded)
    free(news_encoded)
    free(urn_c)
    free(id_c)
    free(ignore_changes_c)

    if res.r0 == 0:
        out_decoded = json.loads(_bytes(res.r1))
        return out_decoded
    raise ProviderError(res.r0, _str(res.r2))


def provider_create(str ctx, str provider, str urn, news, int timeout=60, bint preview=False):
    cdef char* news_encoded = _cstr(json.dumps(news).encode())
    cdef char* ctx_c = _cstr(ctx)
    cdef char* provider_c = _cstr(provider)
    cdef char* urn_c = _cstr(urn)
    with nogil:
        res = ProviderCreate(
            ctx_c, provider_c, urn_c,
            news_encoded, timeout, preview
        )

    free(news_encoded)
    free(ctx_c)
    free(provider_c)
    free(urn_c)

    if res.r0 == 0:
        out_decoded = json.loads(_bytes(res.r1))
        return out_decoded
    raise ProviderError(res.r0, _str(res.r2))


def provider_read(str ctx, str provider, str urn, str id, inputs, state):
    cdef char* input_encoded = _cstr(json.dumps(inputs).encode())
    cdef char* state_encoded = _cstr(json.dumps(state).encode())
    cdef char* ctx_c = _cstr(ctx)
    cdef char* provider_c = _cstr(provider)
    cdef char* urn_c = _cstr(urn)
    cdef char* id_c = _cstr(id)

    with nogil:
        res = ProviderRead(
            ctx_c, provider_c, urn_c, id_c,
            input_encoded, state_encoded
        )

    free(input_encoded)
    free(state_encoded)
    free(ctx_c)
    free(provider_c)
    free(urn_c)
    free(id_c)

    if res.r0 == 0:
        out_decoded = json.loads(_bytes(res.r1))
        return out_decoded
    raise ProviderError(res.r0, _str(res.r2))


def provider_update(str ctx, str provider, str urn, str id, olds, news, int timeout=60, ignore_changes=(), bint preview=False):
    cdef char* olds_encoded = _cstr(json.dumps(olds).encode())
    cdef char* news_encoded = _cstr(json.dumps(news).encode())
    cdef char* ctx_c = _cstr(ctx)
    cdef char* provider_c = _cstr(provider)
    cdef char* urn_c = _cstr(urn)
    cdef char* id_c = _cstr(id)
    cdef char** ignore_changes_c = to_cstring_array(ignore_changes)
    cdef int ignore_changes_len_c = len(ignore_changes)

    with nogil:
        res = ProviderUpdate(
            ctx_c, provider_c, urn_c, id_c,
            olds_encoded, news_encoded,
            timeout, ignore_changes_c, ignore_changes_len_c, preview
        )

    free(ctx_c)
    free(provider_c)
    free(olds_encoded)
    free(news_encoded)
    free(urn_c)
    free(id_c)
    free(ignore_changes_c)

    if res.r0 == 0:
        out_decoded = json.loads(_bytes(res.r1))
        return out_decoded
    raise ProviderError(res.r0, _str(res.r2))


def provider_delete(str ctx, str provider, str urn, str id, news, int timeout=60):
    cdef char* news_encoded = _cstr(json.dumps(news).encode())
    cdef char* ctx_c = _cstr(ctx)
    cdef char* provider_c = _cstr(provider)
    cdef char* urn_c = _cstr(urn)
    cdef char* id_c = _cstr(id)

    with nogil:
        res = ProviderDelete(
            ctx_c, provider_c, urn_c, id_c,
            news_encoded, timeout
        )

    free(ctx_c)
    free(provider_c)
    free(news_encoded)
    free(urn_c)
    free(id_c)

    if res.r0 == 0:
        return res.r1
    raise ProviderError(res.r0, _str(res.r2))


class PylumiGoError(Exception):
    """
    Errors originating from go within Pylumi
    """


class ContextError(PylumiGoError):
    """
    Errors from context_ methods
    """
    def __init__(self, int status_code, str message):
        self.status_code = status_code
        self.message = message
        super().__init__(
            'Error from pulumi context: %s (status code: %d)'
            % (message, status_code)
        )


class ProviderError(PylumiGoError):
    """
    Errors from provider_ methods
    """
    def __init__(self, int status_code, str message):
        self.status_code = status_code
        self.message = message
        super().__init__(
            'Error from pulumi provider: %s (status code: %d)'
            % (message, status_code)
        )
