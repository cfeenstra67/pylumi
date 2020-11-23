import json
from cpython.string cimport PyString_AsString
from libc.stdlib cimport malloc, free


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

    ContextSetup_return ContextSetup(char* name, char* cwd)

    struct ContextTeardown_return:
        GoInt r0
        char* r1

    ContextTeardown_return ContextTeardown(char* name)

    struct ContextListPlugins_return:
        GoInt r0
        char** r1
        GoInt r2
        char* r3

    ContextListPlugins_return ContextListPlugins(char* name)

    struct ProviderTeardown_return:
        GoInt r0
        char* r1

    ProviderTeardown_return ProviderTeardown(char* ctx, char* provider)

    struct ProviderGetSchema_return:
        GoInt r0
        char* r1
        char* r2

    ProviderGetSchema_return ProviderGetSchema(char* ctxName, char* name, GoInt version)

    struct ProviderCheckConfig_return:
        GoInt r0
        char* r1
        char* r2
        char* r3

    ProviderCheckConfig_return ProviderCheckConfig(char* ctx, char* provider, char* urn, char* olds, char* news, GoUint8 allowUnknowns)

    struct ProviderDiffConfig_return:
        GoInt r0
        char* r1
        char* r2

    ProviderDiffConfig_return ProviderDiffConfig(char* ctx, char* provider, char* urn, char* olds, char* news, GoUint8 allowUnknowns, char** ignoreChanges, GoInt nIgnoreChanges)

    struct ProviderConfigure_return:
        GoInt r0
        char* r1

    ProviderConfigure_return ProviderConfigure(char* ctx, char* provider, char* inputs)

    struct ProviderCheck_return:
        GoInt r0
        char* r1
        char* r2
        char* r3

    ProviderCheck_return ProviderCheck(char* ctx, char* provider, char* urn, char* olds, char* news, GoUint8 allowUnknowns)

    struct ProviderDiff_return:
        GoInt r0
        char* r1
        char* r2

    ProviderDiff_return ProviderDiff(char* ctx, char* provider, char* urn, char* id, char* olds, char* news, GoUint8 allowUnknowns, char** ignoreChanges, GoInt nIgnoreChanges)

    struct ProviderCreate_return:
        GoInt r0
        char* r1
        char* r2

    ProviderCreate_return ProviderCreate(char* ctx, char* provider, char* urn, char* news, GoFloat64 timeout, GoUint8 preview)

    struct ProviderRead_return:
        GoInt r0
        char* r1
        char* r2

    ProviderRead_return ProviderRead(char* ctx, char* provider, char* urn, char* id, char* inputs, char* state)

    struct ProviderUpdate_return:
        GoInt r0
        char* r1
        char* r2

    ProviderUpdate_return ProviderUpdate(char* ctx, char* provider, char* urn, char* id, char* olds, char* news, GoFloat64 timeout, char** ignoreChanges, GoInt nIgnoreChanges, GoUint8 preview)

    struct ProviderDelete_return:
        GoInt r0
        GoInt r1
        char* r2

    ProviderDelete_return ProviderDelete(char* ctx, char* provider, char* urn, char* id, char* news, GoFloat64 timeout)

    ctypedef struct Unknowns:
        char* Key
        char* BoolValue
        char* NumberValue
        char* StringValue
        char* ArrayValue
        char* AssetValue
        char* ArchiveValue
        char* ObjectValue

    Unknowns GetUnknowns()

    ctypedef struct DiffKinds:
        int DiffAdd
        int DiffAddReplace
        int DiffDelete
        int DiffDeleteReplace
        int DiffUpdate
        int DiffUpdateReplace

    DiffKinds GetDiffKinds()


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
    res = ContextSetup(_bytes(ctxName), _bytes(cwd))
    if res.r0 == 0:
        return None
    raise ContextError(res.r0, _str(res.r1))


def context_teardown(str ctxName):
    res = ContextTeardown(_bytes(ctxName))
    if res.r0 == 0:
        return None
    raise ContextError(res.r0, _str(res.r1))


def context_list_plugins(str ctxName):
    res = ContextListPlugins(_bytes(ctxName))
    if res.r0 == 0:
        return [x.decode() for x in res.r1[:res.r2]]
    raise ContextError(res.r0, _str(res.r3))


# Provider methods

def provider_teardown(str ctx, str provider):
    res = ProviderTeardown(_bytes(ctx), _bytes(provider))
    if res.r0 == 0:
        return None
    raise ProviderError(res.r0, _str(res.r1))


def provider_get_schema(str ctxName, str name, int version=0):
    res = ProviderGetSchema(_bytes(ctxName), _bytes(name), version)
    if res.r0 == 0:
        return res.r1
    raise ProviderError(res.r0, _str(res.r2))


def provider_check_config(str ctx, str provider, str urn, olds, news, allow_unknowns=False):
    olds_encoded = json.dumps(olds).encode()
    news_encoded = json.dumps(news).encode()
    res = ProviderCheckConfig(
        _bytes(ctx), _bytes(provider), _bytes(urn),
        olds_encoded, news_encoded, allow_unknowns
    )
    if res.r0 == 0:
        props_decoded = json.loads(_bytes(res.r1))
        failures_decoded = json.loads(_bytes(res.r2))
        return props_decoded, failures_decoded
    raise ProviderError(res.r0, _str(res.r3))


def provider_diff_config(str ctx, str provider, str urn, olds, news, allow_unknowns=False, ignore_changes=()):
    olds_encoded = json.dumps(olds).encode()
    news_encoded = json.dumps(news).encode()
    res = ProviderDiffConfig(
        _bytes(ctx), _bytes(provider), _bytes(urn),
        olds_encoded, news_encoded,
        allow_unknowns, to_cstring_array(ignore_changes), len(ignore_changes)
    )
    if res.r0 == 0:
        out_decoded = json.loads(_bytes(res.r1))
        return out_decoded
    raise ProviderError(res.r0, _str(res.r2))


def provider_configure(str ctx, str provider, inputs):
    inputs_encoded = json.dumps(inputs).encode()
    res = ProviderConfigure(_bytes(ctx), _bytes(provider), inputs_encoded)
    if res.r0 == 0:
        return None
    raise ProviderError(res.r0, _str(res.r1))


def provider_check(str ctx, str provider, str urn, olds, news, allow_unknowns=False):
    olds_encoded = json.dumps(olds).encode()
    news_encoded = json.dumps(news).encode()
    res = ProviderCheck(
        _bytes(ctx), _bytes(provider), _bytes(urn),
        olds_encoded, news_encoded, allow_unknowns
    )
    if res.r0 == 0:
        props = json.loads(_bytes(res.r1))
        failures = json.loads(_bytes(res.r2))
        return props, failures
    raise ProviderError(res.r0, _str(res.r3))


def provider_diff(str ctx, str provider, str urn, str id, olds, news, allow_unknowns=False, ignore_changes=()):
    olds_encoded = json.dumps(olds).encode()
    news_encoded = json.dumps(news).encode()
    res = ProviderDiff(
        _bytes(ctx), _bytes(provider), _bytes(urn), _bytes(id),
        olds_encoded, news_encoded,
        allow_unknowns, to_cstring_array(ignore_changes), len(ignore_changes)
    )
    if res.r0 == 0:
        out_decoded = json.loads(_bytes(res.r1))
        return out_decoded
    raise ProviderError(res.r0, _str(res.r2))


def provider_create(str ctx, str provider, str urn, news, int timeout=60, preview=False):
    news_encoded = json.dumps(news).encode()
    res = ProviderCreate(
        _bytes(ctx), _bytes(provider), _bytes(urn),
        news_encoded, timeout, preview
    )
    if res.r0 == 0:
        out_decoded = json.loads(_bytes(res.r1))
        return out_decoded
    raise ProviderError(res.r0, _str(res.r2))


def provider_read(str ctx, str provider, str urn, str id, inputs, state):
    input_encoded = json.dumps(inputs).encode()
    state_encoded = json.dumps(state).encode()
    res = ProviderRead(
        _bytes(ctx), _bytes(provider), _bytes(urn), _bytes(id),
        input_encoded, state_encoded
    )
    if res.r0 == 0:
        out_decoded = json.loads(_bytes(res.r1))
        return out_decoded
    raise ProviderError(res.r0, _str(res.r2))


def provider_update(str ctx, str provider, str urn, str id, olds, news, int timeout=60, ignore_changes=(), preview=False):
    olds_encoded = json.dumps(olds).encode()
    news_encoded = json.dumps(news).encode()
    res = ProviderUpdate(
        _bytes(ctx), _bytes(provider), _bytes(urn), _bytes(id),
        olds_encoded, news_encoded,
        timeout, to_cstring_array(ignore_changes), len(ignore_changes), preview
    )
    if res.r0 == 0:
        out_decoded = json.loads(_bytes(res.r1))
        return out_decoded
    raise ProviderError(res.r0, _str(res.r2))


def provider_delete(str ctx, str provider, str urn, str id, news, int timeout=60):
    news_encoded = json.dumps(news).encode()
    res = ProviderDelete(
        _bytes(ctx), _bytes(provider), _bytes(urn), _bytes(id),
        news_encoded, timeout
    )
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
