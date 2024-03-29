package pylumi

import (
    "fmt"
    "sync"

    "github.com/blang/semver"

    "github.com/pulumi/pulumi/sdk/v3/go/common/diag"
    "github.com/pulumi/pulumi/sdk/v3/go/common/resource/plugin"
    "github.com/pulumi/pulumi/sdk/v3/go/common/tokens"
)

var (
    contexts map[string]*Context = make(map[string]*Context)
    contextCreationLock sync.Mutex
)

func SetupContext(name string, path string, sink, statusSink diag.Sink) error {
    _, ok := contexts[name]
    if !ok {
        contextCreationLock.Lock()
        // Check again after acquiring lock to see that it wasn't already
        // created in the mean time.
        _, ok := contexts[name]
        if ok {
            return nil
        }
        defer contextCreationLock.Unlock()

        if err := ForceSetupContext(name, path, sink, statusSink); err != nil {
            return fmt.Errorf("context creation failed: %v", err)
        }
    }
    return nil
}

func ForceSetupContext(name string, path string, sink, statusSink diag.Sink) error {
    ctx, err := NewContextFromPath(path, sink, statusSink)
    if err == nil {
        contexts[name] = ctx
    }
    return err
}

func GetContext(name string) (*Context, error) {
    ctx, ok := contexts[name]
    if !ok {
        return nil, fmt.Errorf("context has not been initialized.")
    }
    return ctx, nil
}

func Provider(ctxName string, name tokens.Package, version *semver.Version) (*plugin.Provider, error) {
    ctx, err := GetContext(ctxName)
    if err != nil {
        return nil, err
    }
    return ctx.Provider(name, version)
}

func CloseContext(name string) error {
    ctx, err := GetContext(name)
    if err != nil {
        return fmt.Errorf("error getting context: %v", err)
    }
    if err := ctx.CloseProviders(); err != nil {
        return fmt.Errorf("error closing providers: %v", err)
    }
    ctx.Close()
    delete(contexts, name)
    return nil
}
