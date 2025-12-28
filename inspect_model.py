import pickle,os
with open('reg_model.pkl','rb') as f:
    m=pickle.load(f)
print('model type:', type(m))
print('has n_features_in_:', hasattr(m,'n_features_in_'))
if hasattr(m,'n_features_in_'):
    print('n_features_in_:', m.n_features_in_)
if hasattr(m,'coef_'):
    try:
        print('coef_ length:', len(m.coef_))
    except Exception as e:
        print('coef_ err', e)
if os.path.exists('scaling.pkl'):
    with open('scaling.pkl','rb') as f:
        s=pickle.load(f)
    print('scaler type:', type(s))
    print('scaler has n_features_in_:', hasattr(s,'n_features_in_'))
    if hasattr(s,'n_features_in_'):
        print('scaler n_features_in_:', s.n_features_in_)
else:
    print('scaling.pkl not found')
