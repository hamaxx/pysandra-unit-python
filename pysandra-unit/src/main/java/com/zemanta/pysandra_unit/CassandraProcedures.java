package com.zemanta.pysandra_unit;
import java.io.File;
import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.List;

import org.cassandraunit.DataLoader;
import org.cassandraunit.dataset.yaml.FileYamlDataSet;
import org.cassandraunit.utils.EmbeddedCassandraServerHelper;
import org.json.simple.JSONObject;


public class CassandraProcedures {
	public static final String CASSANDRA_HOST = "localhost:9171";
	
	public static List<String> validProcedures = Arrays.asList(new String[] {"start", "stop", "clean", "load"});
	
	private static boolean hasMethod(String methodName) {
		return validProcedures.contains(methodName);
	}
	
	public static Object run(String methodName, JSONObject arg) throws CassandraProceduresException {
		if (!hasMethod(methodName)) {
			throw new CassandraProceduresException("Method doesn't exist: " + methodName);
		}
		
		try {			
			Method method = CassandraProcedures.class.getMethod(methodName, JSONObject.class);
			return (JsonRpcResponse) method.invoke(CassandraProcedures.class, arg);
		} catch (SecurityException e) {
		} catch (NoSuchMethodException e) {
		} catch (Exception e) {
			return new CassandraProceduresException("Runtime error: " + e);
		}
		
		throw new CassandraProceduresException("Method doesn't exist: " + methodName);
	}
	
	public static JsonRpcResponse start(JSONObject val) {
		String tmpDir = (String)val.get("tmpdir");
		if (tmpDir == null) {
			return new JsonRpcErrorResponse("cassandra_start_error: Missing tmpdir");
		}
		
		String yamlConf = (String)val.get("yamlconf");
		if (yamlConf == null) {
			return new JsonRpcErrorResponse("cassandra_start_error: Missing yamlconf");	
		}
		
		try {
			File file = new File(yamlConf);
			EmbeddedCassandraServerHelper.startEmbeddedCassandra(file, tmpDir);
			return new JsonRpcOkResponse(CASSANDRA_HOST);
		} catch (Exception ex) {
			return new JsonRpcErrorResponse("cassandra_start_error " + ex);
		}
	}
	
	public static JsonRpcResponse stop(JSONObject val) {
		return new JsonRpcOkStopResponse();
	}
	
	public static JsonRpcResponse load(JSONObject val) {
		String fileName = (String)val.get("filename");
		try {
			DataLoader dataLoader = new DataLoader("TestCluster", CASSANDRA_HOST);
			dataLoader.load(new FileYamlDataSet(fileName));
			return new JsonRpcOkResponse();
		} catch (Exception ex) {
			return new JsonRpcErrorResponse("load_data_error " + ex + " " + fileName);
		}
	}
	
	public static JsonRpcResponse clean(JSONObject val) {
		try {
			EmbeddedCassandraServerHelper.cleanEmbeddedCassandra();
			return new JsonRpcOkResponse();
		} catch (Exception ex) {
			return new JsonRpcErrorResponse("clean_data_error " + ex);
		}
	}
}

class CassandraProceduresException extends Exception {

	public CassandraProceduresException(String string) {
		super(string);
	}

	private static final long serialVersionUID = 1L;
	
}
